"""
DAO Governance Proposal Summarizer - Haiku-powered API
Extracts and analyzes governance proposals: voting state, impact, recommendations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
from anthropic import Anthropic
from datetime import datetime

app = FastAPI(title="Governance Summarizer", version="0.1.0")
client = Anthropic()

# Configuration
HAIKU_MODEL = "claude-3-5-haiku-20241022"
BATCH_SIZE = 5  # proposals per API call
CONFIDENCE_THRESHOLD = 0.6

class VotingState(BaseModel):
    for_votes: str  # in wei/raw vote count
    against_votes: str
    abstain_votes: str
    voting_end_timestamp: str

class Proposal(BaseModel):
    proposal_id: str
    dao_name: str
    proposal_text: str
    voting_state: VotingState
    proposal_url: Optional[str] = None
class ProposalSummary(BaseModel):
    title: str
    author: Optional[str] = None
    description: str
    key_changes: List[str]

class VotingSummary(BaseModel):
    for_percentage: float
    against_percentage: float
    abstain_percentage: float
    winning_option: str
    voting_end_date: str
    time_remaining_hours: int

class ImpactAssessment(BaseModel):
    financial_impact: str
    risk_level: str  # low, medium, high
    risk_factors: List[str]

class ProposalResult(BaseModel):
    proposal_id: str
    summary: ProposalSummary
    voting: VotingSummary
    impact: ImpactAssessment
    recommendation: str
    cost_tokens: Dict[str, int]

class BatchRequest(BaseModel):
    proposals: List[Proposal]

class BatchResponse(BaseModel):
    results: List[ProposalResult]
    total_cost: Dict[str, Any]

def calculate_voting_percentages(for_votes: str, against_votes: str, abstain_votes: str):
    """Calculate voting percentages from raw vote counts."""
    try:
        for_val = int(for_votes)
        against_val = int(against_votes)
        abstain_val = int(abstain_votes)

        total = for_val + against_val + abstain_val
        if total == 0:
            return 0, 0, 0

        for_pct = (for_val / total) * 100
        against_pct = (against_val / total) * 100
        abstain_pct = (abstain_val / total) * 100

        return round(for_pct, 1), round(against_pct, 1), round(abstain_pct, 1)
    except (ValueError, TypeError):
        return 0, 0, 0
def calculate_time_remaining(voting_end_timestamp: str) -> int:
    """Calculate hours remaining until voting ends."""
    try:
        end_time = int(voting_end_timestamp)
        current_time = int(datetime.now().timestamp())
        hours_remaining = (end_time - current_time) / 3600
        return max(0, int(hours_remaining))
    except (ValueError, TypeError):
        return 0

def build_batch_prompt(proposals: List[Proposal]) -> str:
    """Build the user prompt for a batch of proposals."""
    prompt = "Analyze these DAO governance proposals:\n\n"

    for i, prop in enumerate(proposals, 1):
        for_pct, against_pct, abstain_pct = calculate_voting_percentages(
            prop.voting_state.for_votes,
            prop.voting_state.against_votes,
            prop.voting_state.abstain_votes
        )
        time_remaining = calculate_time_remaining(prop.voting_state.voting_end_timestamp)

        prompt += f"{i}. Proposal ID: {prop.proposal_id}\n"
        prompt += f"   DAO: {prop.dao_name}\n"
        prompt += f"   Text: {prop.proposal_text[:300]}...\n"
        prompt += f"   Voting: For: {for_pct}%, Against: {against_pct}%, Abstain: {abstain_pct}%\n"
        prompt += f"   Time Remaining: {time_remaining} hours\n"
        if prop.proposal_url:
            prompt += f"   URL: {prop.proposal_url}\n"
        prompt += "\n"

    prompt += """For each proposal, provide ONLY valid JSON:
{
  "summaries": [
    {
      "proposal_id": "123",
      "title": "...",
      "description": "...",
      "key_changes": ["...", "..."],
      "author": "0x...",
      "voting_analysis": {
        "winning_option": "for|against|abstain|tie",
        "confidence": 0.95,
        "reasoning": "..."
      },
      "financial_impact": "Estimated impact...",
      "risk_level": "low|medium|high",
      "risk_factors": ["...", "..."],
      "recommendation": "Brief recommendation on passing likelihood..."
    },
    ...
  ]
}"""

    return prompt
@app.post("/summarize", response_model=BatchResponse)
async def summarize_proposals(request: BatchRequest):
    """Summarize a batch of governance proposals."""

    if not request.proposals:
        raise HTTPException(status_code=400, detail="No proposals provided")

    if len(request.proposals) > 50:
        raise HTTPException(status_code=400, detail="Max 50 proposals per request")

    # Split into batches
    batches = [
        request.proposals[i:i+BATCH_SIZE]
        for i in range(0, len(request.proposals), BATCH_SIZE)
    ]

    all_results = []
    total_input_tokens = 0
    total_output_tokens = 0

    # System prompt
    system_prompt = """You are a DeFi governance expert with deep knowledge of major DAOs.
Analyze governance proposals and provide:
1. Clear summary of what's being proposed
2. Detailed voting breakdown and likelihood of passage
3. Financial impact assessment (in USD if possible)
4. Risk assessment with specific risk factors
5. Recommendation on probability of passing

Be conservative in impact estimates. Flag uncertain assumptions.
Return ONLY valid JSON."""

    for batch in batches:
        prompt = build_batch_prompt(batch)

        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            response_text = response.content[0].text
            try:
                parsed = json.loads(response_text)
                summaries_data = parsed.get("summaries", [])
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Failed to parse governance summarizer response")

            # Map results back to original proposals
            for item in summaries_data:
                proposal_id = item.get("proposal_id")

                # Find matching proposal in batch
                matching_proposal = None
                for prop in batch:
                    if prop.proposal_id == proposal_id:
                        matching_proposal = prop
                        break

                if not matching_proposal:
                    continue

                # Calculate voting percentages
                for_pct, against_pct, abstain_pct = calculate_voting_percentages(
                    matching_proposal.voting_state.for_votes,
                    matching_proposal.voting_state.against_votes,
                    matching_proposal.voting_state.abstain_votes
                )

                # Determine winning option
                voting_analysis = item.get("voting_analysis", {})
                winning_option = voting_analysis.get("winning_option", "for")

                # Convert voting end timestamp to date
                try:
                    end_time = int(matching_proposal.voting_state.voting_end_timestamp)
                    voting_end_date = datetime.fromtimestamp(end_time).isoformat() + "Z"
                except (ValueError, TypeError):
                    voting_end_date = "Unknown"

                time_remaining = calculate_time_remaining(
                    matching_proposal.voting_state.voting_end_timestamp
                )

                result = ProposalResult(
                    proposal_id=proposal_id,
                    summary=ProposalSummary(
                        title=item.get("title", ""),
                        author=item.get("author"),
                        description=item.get("description", ""),
                        key_changes=item.get("key_changes", [])
                    ),
                    voting=VotingSummary(
                        for_percentage=for_pct,
                        against_percentage=against_pct,
                        abstain_percentage=abstain_pct,
                        winning_option=winning_option,
                        voting_end_date=voting_end_date,
                        time_remaining_hours=time_remaining
                    ),
                    impact=ImpactAssessment(
                        financial_impact=item.get("financial_impact", "Unknown"),
                        risk_level=item.get("risk_level", "medium"),
                        risk_factors=item.get("risk_factors", [])
                    ),
                    recommendation=item.get("recommendation", ""),
                    cost_tokens={
                        "input": response.usage.input_tokens,
                        "output": response.usage.output_tokens
                    }
                )
                all_results.append(result)

            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")

    return BatchResponse(
        results=all_results,
        total_cost={
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "estimated_usd": round((total_input_tokens * 0.80 + total_output_tokens * 4.0) / 1_000_000, 4)
        }
    )

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok", "model": HAIKU_MODEL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)