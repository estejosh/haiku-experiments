"""
Smart Contract Risk Scanner - Haiku-powered API
Analyzes Solidity contracts for security risks, vulnerabilities, and code quality
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
from anthropic import Anthropic

app = FastAPI(title="Contract Risk Scanner", version="0.1.0")
client = Anthropic()

# Configuration
HAIKU_MODEL = "claude-3-5-haiku-20241022"
BATCH_SIZE = 2  # contracts per API call (high token count per contract)
MAX_SOURCE_LENGTH = 15000  # truncate very large contracts

class SecurityPattern(BaseModel):
    has_access_controls: bool
    has_pause_mechanism: bool
    has_upgrade_mechanism: bool
    uses_external_calls: bool
    external_call_count: int
    self_destruct_present: bool

class Finding(BaseModel):
    severity: str  # critical, high, medium, low, info
    category: str
    description: str
    recommendation: str
    line_number: Optional[int] = None

class ContractAnalysis(BaseModel):
    contract_id: str
    risk_level: str  # critical, high, medium, low
    risk_score: int  # 0-100
    summary: str
    findings: List[Finding]
    security_patterns: SecurityPattern
    cve_matches: List[str]
    audit_history: Optional[str] = None
    recommendations: List[str]
    cost_tokens: Dict[str, int]

class AnalysisRequest(BaseModel):
    contract_id: str
    contract_name: Optional[str] = None
    contract_source: str  # Full Solidity source or bytecode hex
    chain: Optional[str] = None
    address: Optional[str] = None
    deployment_date: Optional[str] = None
    tvl_usd: Optional[float] = None

class BatchRequest(BaseModel):
    contracts: List[AnalysisRequest]

class BatchResponse(BaseModel):
    results: List[ContractAnalysis]
    total_cost: Dict[str, Any]

def truncate_code(source: str, max_length: int = MAX_SOURCE_LENGTH) -> str:
    """Truncate very large contracts to manageable size."""
    if len(source) > max_length:
        return source[:max_length] + f"\n// ... ({len(source) - max_length} characters truncated)"
    return source

def build_batch_prompt(contracts: List[AnalysisRequest]) -> str:
    """Build the user prompt for a batch of contracts."""
    prompt = "Analyze these Solidity smart contracts for security risks:\n\n"

    for i, contract in enumerate(contracts, 1):
        source = truncate_code(contract.contract_source)
        prompt += f"{i}. Contract ID: {contract.contract_id}\n"
        if contract.contract_name:
            prompt += f"   Name: {contract.contract_name}\n"
        if contract.chain:
            prompt += f"   Chain: {contract.chain}\n"
        if contract.tvl_usd:
            prompt += f"   TVL: ${contract.tvl_usd:,.0f}\n"

        prompt += f"   Source (first {min(len(source), MAX_SOURCE_LENGTH)} chars):\n"
        prompt += "   ```solidity\n"
        for line in source.split('\n')[:100]:  # Show first 100 lines
            prompt += f"   {line}\n"
        if len(source.split('\n')) > 100:
            more_lines = len(source.split('\n')) - 100
            prompt += f"   ... ({more_lines} more lines)\n"
        prompt += "   ```\n\n"

    prompt += """For each contract, provide ONLY valid JSON:
{
  "analyses": [
    {
      "contract_id": "uniswap-v3-router",
      "risk_level": "low|medium|high|critical",
      "risk_score": 25,
      "summary": "Brief assessment...",
      "findings": [
        {
          "severity": "critical|high|medium|low|info",
          "category": "reentrancy|access_control|overflow|external_call|etc",
          "description": "Detailed finding...",
          "recommendation": "How to fix...",
          "line_number": 245
        }
      ],
      "security_patterns": {
        "has_access_controls": true,
        "has_pause_mechanism": true,
        "has_upgrade_mechanism": false,
        "uses_external_calls": true,
        "external_call_count": 8,
        "self_destruct_present": false
      },
      "cve_matches": [],
      "audit_history": "Audit info if known...",
      "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
      ]
    }
  ]
}"""

    return prompt
@app.post("/analyze", response_model=BatchResponse)
async def analyze_contracts(request: BatchRequest):
    """Analyze a batch of smart contracts for security risks."""

    if not request.contracts:
        raise HTTPException(status_code=400, detail="No contracts provided")

    if len(request.contracts) > 20:
        raise HTTPException(status_code=400, detail="Max 20 contracts per request")

    # Split into batches
    batches = [
        request.contracts[i:i+BATCH_SIZE]
        for i in range(0, len(request.contracts), BATCH_SIZE)
    ]

    all_results = []
    total_input_tokens = 0
    total_output_tokens = 0

    # System prompt
    system_prompt = """You are an expert Solidity security auditor with 10+ years of experience.
Analyze smart contracts for security risks, vulnerabilities, and code quality issues.

Focus on:
1. Access control and authorization patterns
2. Reentrancy and state management issues
3. Integer overflow/underflow (Solidity <0.8)
4. External call safety and ordering
5. Known CVE patterns
6. Code quality and maintainability

Known safe patterns (don't flag as vulnerabilities):
- OpenZeppelin libraries (AccessControl, SafeMath, ReentrancyGuard)
- Standard Uniswap router patterns
- Common factory patterns
- Proven bridge/bridge patterns

Be precise but avoid false positives. Standard implementations should not trigger warnings.
Return ONLY valid JSON."""

    for batch in batches:
        prompt = build_batch_prompt(batch)

        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            response_text = response.content[0].text
            try:
                parsed = json.loads(response_text)
                analyses_data = parsed.get("analyses", [])
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Failed to parse contract analysis response")

            # Map results back to original contracts
            for item in analyses_data:
                contract_id = item.get("contract_id")

                # Find matching contract in batch
                matching_contract = None
                for contract in batch:
                    if contract.contract_id == contract_id:
                        matching_contract = contract
                        break

                if not matching_contract:
                    continue

                # Parse findings
                findings = []
                for finding_data in item.get("findings", []):
                    findings.append(Finding(
                        severity=finding_data.get("severity", "info"),
                        category=finding_data.get("category", "unknown"),
                        description=finding_data.get("description", ""),
                        recommendation=finding_data.get("recommendation", ""),
                        line_number=finding_data.get("line_number")
                    ))

                # Parse security patterns
                patterns_data = item.get("security_patterns", {})
                security_patterns = SecurityPattern(
                    has_access_controls=patterns_data.get("has_access_controls", False),
                    has_pause_mechanism=patterns_data.get("has_pause_mechanism", False),
                    has_upgrade_mechanism=patterns_data.get("has_upgrade_mechanism", False),
                    uses_external_calls=patterns_data.get("uses_external_calls", False),
                    external_call_count=patterns_data.get("external_call_count", 0),
                    self_destruct_present=patterns_data.get("self_destruct_present", False)
                )

                result = ContractAnalysis(
                    contract_id=contract_id,
                    risk_level=item.get("risk_level", "medium"),
                    risk_score=item.get("risk_score", 50),
                    summary=item.get("summary", ""),
                    findings=findings,
                    security_patterns=security_patterns,
                    cve_matches=item.get("cve_matches", []),
                    audit_history=item.get("audit_history"),
                    recommendations=item.get("recommendations", []),
                    cost_tokens={
                        "input": response.usage.input_tokens,
                        "output": response.usage.output_tokens
                    }
                )
                all_results.append(result)

            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Contract analysis error: {str(e)}")

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
    uvicorn.run(app, host="0.0.0.0", port=8001)