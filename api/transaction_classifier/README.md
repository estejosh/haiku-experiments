# Transaction Classifier API

Haiku-powered Ethereum transaction classification API. Classifies on-chain transactions for whale activity, MEV patterns, liquidations, arbitrage, and regular transactions.

**Cost**: ~$85 per 1M transactions processed  
**Speed**: <100ms per transaction (batched)  
**Accuracy Target**: >85% precision on whale detection

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the API

```bash
python main.py
```

Server runs on `http://localhost:8000`

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok", "model": "claude-3-5-haiku-20241022"}
```

## API Usage

### POST /classify

Classify a batch of Ethereum transactions.

**Request**:
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d @request.json
```

**Request Body** (request.json):
```json
{
  "transactions": [
    {
      "transaction_hash": "0x123abc...",
      "from_address": "0xabc123...",
      "to_address": "0xdef456...",
      "value": "50000000000000000000",
      "data": "0xa9059cbb...",
      "gas_price": "50000000000",
      "timestamp": "2026-09-23T12:34:56Z"
    }
  ]
}
```

**Response**:
```json
{
  "results": [
    {
      "transaction_hash": "0x123abc...",
      "classifications": [
        {
          "type": "whale_activity",
          "confidence": 0.92,
          "rationale": "Transfer of 50 ETH from unknown address"
        }
      ],
      "cost_tokens": {
        "input": 245,
        "output": 38
      }
    }
  ],
  "total_cost": {
    "input_tokens": 245,
    "output_tokens": 38,
    "estimated_usd": 0.0002
  }
}
```

## Classification Types

| Type | Definition | Example |
|------|-----------|---------|
| `whale_activity` | Large transfers (>10K USD) impacting markets | 50 ETH transfer from unknown address |
| `mev` | Sandwich attacks or MEV extraction patterns | Frontrunning detected on Uniswap swap |
| `liquidation` | Liquidation calls from lending protocols | Aave liquidation pattern detected |
| `arbitrage` | Cross-exchange or DEX-to-DEX swaps | Token swap across multiple DEX venues |
| `none` | Regular transaction | Standard ERC20 transfer |

## Request Limits

- **Max transactions per request**: 100
- **Batch size**: 10 transactions per API call
- **Confidence threshold**: 0.5 (only report classifications above this)

## Cost Model

```
Input tokens per transaction: ~95
Output tokens per transaction: ~10
Total per transaction: ~105 tokens

Batch of 10 transactions:
- Input: ~950 tokens
- Output: ~100 tokens  
- Total: ~1050 tokens
- Cost: 1050 * ($0.80/1M input + $4.0/1M output) / 1000 = $0.00085

Per 1M transactions: $85
```

## Deployment

### Docker

```bash
docker build -t transaction-classifier .
docker run -p 8000:8000 --env-file .env transaction-classifier
```

### Environment Variables

- `ANTHROPIC_API_KEY` (required): Your Anthropic API key
- `HAIKU_MODEL`: Model to use (default: claude-3-5-haiku-20241022)
- `BATCH_SIZE`: Transactions per API call (default: 10)
- `CONFIDENCE_THRESHOLD`: Minimum confidence to report (default: 0.5)

## Testing

Run integration tests with sample transactions:

```bash
# Load sample data and test classification
python test_integration.py
```

## Go-Live Checklist

- [ ] API key configured in production environment
- [ ] Rate limiting configured (if needed)
- [ ] Error handling tested with malformed transactions
- [ ] Cost tracking validated against actual API usage
- [ ] Documentation reviewed and customer-ready
- [ ] Customer test data integrated
- [ ] Feedback loop established

## Next Steps

- Refine prompts based on classification accuracy
- Add customer-specific transaction metadata
- Implement continuous monitoring for prompt degradation
- Build batch processing job for high-volume data

---

**Status**: MVP (Week 1 of PoC development)  
**Owner**: Claude Agent  
**Timeline**: 2-week sprint to production readiness
