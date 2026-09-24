"""
Ethereum Transaction Classifier - Haiku-powered API
Classifies transactions: whale_activity, mev, liquidation, arbitrage, none
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from anthropic import Anthropic

app = FastAPI(title="Transaction Classifier", version="0.1.0")
client = Anthropic()

# Configuration
HAIKU_MODEL = "claude-3-5-haiku-20241022"
BATCH_SIZE = 10  # transactions per API call
CONFIDENCE_THRESHOLD = 0.5

class Transaction(BaseModel):
    transaction_hash: str
    from_address: str
    to_address: str
    value: str  # in wei
    data: Optional[str] = None
    gas_price: Optional[str] = None
    timestamp: Optional[str] = None

class Classification(BaseModel):
    type: str  # whale_activity, mev, liquidation, arbitrage, none
    confidence: float
    rationale: str

class TransactionResult(BaseModel):
    transaction_hash: str
    classifications: List[Classification]
    cost_tokens: dict

class BatchRequest(BaseModel):
    transactions: List[Transaction]

class BatchResponse(BaseModel):
    results: List[TransactionResult]
    total_cost: dict

def build_batch_prompt(transactions: List[Transaction]) -> str:
    """Build the user prompt for a batch of transactions."""
    prompt = "Classify these Ethereum transactions:\n\n"
    
    for i, tx in enumerate(transactions, 1):
        prompt += f"{i}. TX: {tx.transaction_hash[:16]}...\n"
        prompt += f"   From: {tx.from_address[:16]}... \n"
        prompt += f"   To: {tx.to_address[:16]}...\n"
        prompt += f"   Value: {int(tx.value) / 1e18:.2f} ETH\n"
        if tx.data:
            prompt += f"   Data: {tx.data[:20]}... (function)\n"
        prompt += "\n"
    
    prompt += """Classify each transaction. Return ONLY valid JSON:
{
  "classifications": [
    {"tx_index": 0, "type": "whale_activity|mev|liquidation|arbitrage|none", "confidence": 0.85, "rationale": "..."},
    ...
  ]
}"""
    
    return prompt

@app.post("/classify", response_model=BatchResponse)
async def classify_transactions(request: BatchRequest):
    """Classify a batch of transactions."""
    
    if not request.transactions:
        raise HTTPException(status_code=400, detail="No transactions provided")
    
    if len(request.transactions) > 100:
        raise HTTPException(status_code=400, detail="Max 100 transactions per request")
    
    # Split into batches
    batches = [
        request.transactions[i:i+BATCH_SIZE] 
        for i in range(0, len(request.transactions), BATCH_SIZE)
    ]
    
    all_results = []
    total_input_tokens = 0
    total_output_tokens = 0
    
    # System prompt
    system_prompt = """You are a cryptocurrency transaction classifier. Analyze Ethereum transactions 
and classify them by type: whale_activity, mev, liquidation, arbitrage, none.

Definitions:
- whale_activity: Large transfers (>10K USD) that could impact markets
- mev: Sandwich attacks or MEV extraction patterns
- liquidation: Liquidation calls from lending protocols
- arbitrage: Cross-exchange or DEX-to-DEX swaps
- none: Regular transaction

Be conservative with confidence. Only report patterns you're certain of."""
    
    for batch in batches:
        prompt = build_batch_prompt(batch)
        
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            response_text = response.content[0].text
            try:
                parsed = json.loads(response_text)
                classifications_data = parsed.get("classifications", [])
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Failed to parse classifier response")
            
            # Map results back to original transactions
            for item in classifications_data:
                tx_index = item.get("tx_index", 0)
                if tx_index < len(batch):
                    tx = batch[tx_index]
                    
                    # Only include high-confidence classifications
                    classifications = [
                        Classification(
                            type=item.get("type", "none"),
                            confidence=item.get("confidence", 0),
                            rationale=item.get("rationale", "")
                        )
                    ] if item.get("confidence", 0) >= CONFIDENCE_THRESHOLD else []
                    
                    result = TransactionResult(
                        transaction_hash=tx.transaction_hash,
                        classifications=classifications,
                        cost_tokens={
                            "input": response.usage.input_tokens,
                            "output": response.usage.output_tokens
                        }
                    )
                    all_results.append(result)
            
            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
    
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
