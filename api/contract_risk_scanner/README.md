# Smart Contract Risk Scanner

**Revenue Stream 3**: Analyze Solidity contracts for vulnerabilities and security risks using Claude Haiku.

## Overview

The Smart Contract Risk Scanner analyzes Solidity source code to detect vulnerabilities, assess risk scores, and provide actionable security recommendations. Designed for security teams, custody providers, and bridge operators.

### Target Customers
- **Custody Providers** (Coinbase, Ledger, etc.) - Pre-integration contract analysis
- **Bridge Operators** (Stargate, Across) - Liquidity contract monitoring
- **Insurance Protocols** (Nexus Mutual) - Risk assessment for policy pricing

### Economics
- **Cost per contract**: $0.001-0.005 (2 contracts per batch to manage token efficiency)
- **Target price**: $0.01-0.025 per contract analysis
- **Margin**: 85%+ (high-value security analysis)
- **Breakeven**: 25-50 contracts/month (~$250-500/month)

## API Endpoint

**POST /analyze**

Analyze Solidity contracts for vulnerabilities, security patterns, and risk scores.

### Request

```json
{
  "contracts": [
    {
      "contract_id": "unique-contract-id",
      "contract_name": "ContractName",
      "chain": "ethereum",
      "contract_source": "pragma solidity ^0.8.0; ...",
      "tvl_usd": 1000000
    }
  ]
}
```

**Parameters:**
- `contract_id`: Unique identifier for the contract
- `contract_name`: Human-readable contract name
- `chain`: Blockchain network (ethereum, polygon, arbitrum)
- `contract_source`: Solidity source code (max 15,000 chars)
- `tvl_usd` (optional): Total value locked for risk weighting

### Response

```json
{
  "results": [
    {
      "contract_id": "unique-contract-id",
      "contract_name": "ContractName",
      "risk_level": "high",
      "risk_score": 72,
      "findings": [
        {
          "issue": "Reentrancy vulnerability in withdrawTokens",
          "severity": "critical",
          "location": "Line 45",
          "recommendation": "Use checks-effects-interactions pattern or reentrancy guard"
        }
      ],
      "security_patterns": [
        {
          "pattern": "Missing access control",
          "severity": "high",
          "occurrences": 2
        }
      ],
      "audit_history": "Not found in public audit databases",
      "code_quality": "Low - missing input validation and error handling",
      "recommendations": [
        "Add OpenZeppelin ReentrancyGuard to prevent reentrancy",
        "Implement access control (onlyOwner, role-based)"
      ]
    }
  ],
  "total_cost": {
    "input_tokens": 2048,
    "output_tokens": 512,
    "estimated_usd": 0.0024
  }
}
```

**Response Fields:**
- `risk_level`: LOW, MEDIUM, HIGH, or CRITICAL
- `risk_score`: 0-100 (higher = more risk)
- `findings`: Array of specific vulnerabilities with severity levels
- `security_patterns`: Common vulnerability patterns detected
- `recommendations`: Actionable security improvements

## Quick Start

### Prerequisites
- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# 3. Run the API
python main.py

# 4. In another terminal, run tests
python test_integration.py
```

### Analyzing a Contract

```bash
curl -X POST http://localhost:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contracts": [
      {
        "contract_id": "test-1",
        "contract_name": "TestContract",
        "chain": "ethereum",
        "contract_source": "pragma solidity ^0.8.0; contract Test {}"
      }
    ]
  }'
```

## Deployment

### Docker

```bash
# Build image
docker build -t contract-risk-scanner .

# Run container
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 8002:8002 contract-risk-scanner
```

### Environment Configuration

Create `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...
HAIKU_MODEL=claude-3-5-haiku-20241022
BATCH_SIZE=2
MAX_SOURCE_LENGTH=15000
HOST=0.0.0.0
PORT=8002
```

## Cost Model

### Per-Contract Cost Breakdown

| Item | Cost |
|------|------|
| Input tokens (avg 2000) | $0.0016 |
| Output tokens (avg 500) | $0.0020 |
| **Total cost per contract** | **$0.0036** |
| **Target price** | **$0.015** |
| **Margin** | **77%** |

### Batch Processing

- **Batch size**: 2 contracts per API call
- **Efficiency**: Combining 2 contracts saves ~10% on token overhead
- **Total batch cost**: $0.0072
- **Total batch revenue**: $0.030
- **Batch margin**: 76%

## Known Limitations

1. **Knowledge cutoff**: Analysis uses Haiku's training data cutoff (Jan 2025)
2. **New vulnerabilities**: May miss very recent CVE patterns
3. **Code context**: Large contracts (>15k chars) will be truncated
4. **False positives**: Conservative analysis may flag non-issues

## Architecture

```
request → validate → batch contracts → 
call Claude Haiku → parse JSON → 
track costs → respond with analysis
```

**Key design patterns:**
- Batch processing: 2 contracts per API call for cost efficiency
- Confidence filtering: Only high-confidence findings (>0.5)
- Cost tracking: Every response includes token usage and USD estimation
- Error handling: Clear HTTP exceptions for invalid inputs
- Defensive validation: Input size limits, JSON validation

## Testing

```bash
# Run integration tests
python test_integration.py

# Tests cover:
# - Health check
# - Safe contract analysis
# - Complex contract with vulnerabilities
# - Error handling (empty contracts, oversized batches)
# - Cost tracking
```

## Production Readiness

✓ **Code**: Production-ready with error handling  
✓ **Tests**: Integration test suite included  
✓ **Documentation**: Complete API docs and cost model  
✓ **Deployment**: Docker containerization ready  
✓ **Monitoring**: Cost tracking built-in  

**Not yet ready:**
- Multi-contract accuracy validation (need real contracts)
- Customer onboarding flow
- SLA/uptime guarantees
- Rate limiting (customer tiers)

## Next Steps

1. **Accuracy validation**: Test against known vulnerable contracts
2. **Customer pilots**: Deploy to security team staging environments
3. **Integration documentation**: API client libraries and SDKs
4. **Monitoring & alerting**: Set up production health checks

---

**Status**: Production-ready, awaiting customer pilots  
**Margin**: 77-85% on cost model  
**Target customers**: Security teams, custody providers, insurance protocols