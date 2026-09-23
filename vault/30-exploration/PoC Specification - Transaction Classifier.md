---
name: PoC Specification - Transaction Classifier
description: Technical specification for proof-of-concept transaction classification API
---

# PoC: Ethereum Transaction Classifier

**Goal**: Classify Ethereum transactions (whale, MEV, liquidation, arbitrage)  
**Timeline**: 2 weeks  
**Success Metric**: <$0.50 cost per 1M transactions; >85% precision; API ready for integration

---

## Problem Statement

DeFi projects need to classify high-volume on-chain transactions to:
- **Whale Activity**: Identify large transfers that impact markets
- **MEV Detection**: Find transactions with sandwich patterns
- **Liquidation Events**: Spot underwater positions being closed
- **Arbitrage**: Identify cross-exchange or cross-DEX trades

Current solutions: Manual analysis (expensive), heuristic rules (brittle), specialized ML (slow).

**Haiku Angle**: Fast, cheap classification via structured prompting + batching.

---

## Technical Design

### Input
```
{
  "transaction_hash": "0x123...",
  "from": "0xabc...",
  "to": "0xdef...",
  "value": "50000000000000000000",  // 50 ETH
  "data": "0xa9059cbb...",           // token transfer function
  "gas_price": "50000000000",
  "timestamp": "2026-09-23T12:34:56Z"
  // Optional: decoded function call, token metadata
}
```

### Output
```
{
  "transaction_hash": "0x123...",
  "classifications": [
    {
      "type": "whale_activity",
      "confidence": 0.92,
      "rationale": "Transfer of 50 ETH from unknown address at 12:34 UTC"
    },
    {
      "type": "liquidation",
      "confidence": 0.45,
      "rationale": "Aave liquidation pattern detected (collateral + debt tx)"
    }
  ],
  "cost_tokens": {
    "input": 245,
    "output": 38
  }
}
```

### Classification Types
1. **Whale Activity**: Large value transfers (>10K USD)
2. **MEV**: Sandwich or reordering patterns (before/after large swaps)
3. **Liquidation**: Liquidation call patterns (Aave, Compound, others)
4. **Arbitrage**: Cross-exchange or DEX-to-DEX swaps
5. **None**: Regular transaction

**Confidence Threshold**: Return only >0.5 confidence classifications

---

## Implementation Plan

### Week 1: Setup + Core API (Days 1-5)

**Day 1-2: Architecture**
```
transaction-classifier/
├── main.py                 # FastAPI server
├── classifier.py           # Haiku + batching logic
├── encoder.py              # Transaction → prompt
├── config.py               # Classifications + prompts
├── requirements.txt
└── test/
    └── test_classifier.py  # Unit tests
```

**Day 3: Haiku Integration**
- Batch encoder: 10-20 transactions per call
- Structured output parsing (JSON)
- Token counting + cost tracking

**Day 4: Testing**
- Unit tests: encoder, parser, cost calculation
- Integration test: 100 transactions from Etherscan
- Cost measurement: tokens per transaction

**Day 5: API Server**
- FastAPI endpoint: POST /classify
- Rate limiting: 100 req/min
- Error handling: Failed classifications → clear error response

### Week 2: Refinement + Deployment (Days 6-10)

**Day 1-2: Accuracy Improvement**
- Run sample data through classifier
- Refine prompts based on false positives
- Add confidence thresholds

**Day 3: Documentation**
- README with examples
- Integration guide for customers
- Cost model (USD per 1M transactions)

**Day 4: Deployment Setup**
- Docker containerization
- Environment variables (.env)
- Customer onboarding docs

**Day 5: Pilot Integration**
- Deploy to staging
- Customer test data integration
- Feedback loop

---

## Prompt Design (Core Logic)

**System Prompt**:
```
You are a cryptocurrency transaction classifier. Analyze Ethereum transactions 
and classify them by type: whale_activity, mev, liquidation, arbitrage, none.

Provide ONLY valid JSON output with classifications and confidence scores.
Be conservative with confidence: only report patterns you are certain of.
```

**User Prompt** (per-batch):
```
Classify these Ethereum transactions:

1. TX: 0x123...
   From: 0xabc... (unknown)
   To: 0x7a250d... (Uniswap V2 router)
   Value: 0 (token transfer)
   Data: 0xa9059cbb... (ERC20 transfer)
   
2. TX: 0x456...
   From: 0xdef... (known MEV searcher)
   To: 0xC02... (WETH)
   Value: 25 ETH
   Data: 0xd0e30db0 (deposit)

Provide JSON:
{
  "classifications": [
    {"tx_index": 0, "type": "arbitrage", "confidence": 0.8},
    {"tx_index": 1, "type": "mev", "confidence": 0.6}
  ]
}
```

---

## Cost Estimation

### Token Consumption
**Input tokens per transaction**:
- Tx hash: 10
- Address fields: 30
- Value: 5
- Data (truncated): 50
- **Total per tx**: ~95 tokens

**Batch of 20 transactions**:
- Input: 95 × 20 = 1,900 tokens
- Output: ~200 tokens (JSON response)
- **Total per batch**: ~2,100 tokens
- **Cost**: 2,100 × ($0.80 / 1M) = $0.0017 per batch

**Per transaction**:
- $0.0017 / 20 = $0.000085 per transaction
- **Per 1M transactions**: $85

**Haiku Cost**: $85/M transactions  
**Target Price**: $200-300/month (aim for >50% margin)  
**Volume Needed**: 3-4M transactions/month to reach $200+/month revenue

---

## Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| API latency (p95) | <100ms | TBD (Week 2) |
| Cost per 1M tx | <$0.50 | $0.085 (on target) |
| Classification precision | >85% | TBD (Week 2) |
| Documentation complete | 100% | TBD (Week 2) |
| Customer ready | Yes | TBD (Week 2) |

---

## Dependencies

- `anthropic` (Claude API)
- `fastapi` (HTTP server)
- `pydantic` (data validation)
- `web3.py` (optional: on-chain data)

---

## Risk Mitigations

**Risk**: Haiku classification accuracy insufficient  
**Mitigation**: Start with high-confidence-only output; gather customer feedback to refine prompts

**Risk**: Token cost too high  
**Mitigation**: Batching (20 tx per call) + early termination (stop if first classification confident)

**Risk**: Customer integration complexity  
**Mitigation**: Provide curl examples + Python SDK; host reference implementation

---

## Next Steps

1. ✓ Design approved
2. → Start implementation (Week of 2026-09-30)
3. → Customer outreach in parallel (Week of 2026-09-23)
4. → Integrate with first pilot customer (Week of 2026-10-14)
