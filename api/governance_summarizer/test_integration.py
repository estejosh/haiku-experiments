"""Integration tests for the governance summarizer API."""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✓ Health check passed")

def test_single_proposal():
    """Test summarizing a single proposal."""
    future_time = int((datetime.now() + timedelta(days=3)).timestamp())

    payload = {
        "proposals": [
            {
                "proposal_id": "aave-123",
                "dao_name": "Aave",
                "proposal_text": """AIP-456: Enable XYZ Market on Polygon
This proposal enables support for the XYZ token on the Aave Polygon deployment.
Key changes:
- Add XYZ as a borrowable asset
- Set LTV to 75% (risk-adjusted for market conditions)
- Enable flash loan support
- Expected to generate $50K monthly revenue in interest fees""",
                "voting_state": {
                    "for_votes": "1200000000000000000000",  # 1200 tokens with 18 decimals
                    "against_votes": "450000000000000000000",  # 450 tokens
                    "abstain_votes": "150000000000000000000"   # 150 tokens
                },
                "proposal_url": "https://governance.aave.com/proposals/456"
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1

    result = data["results"][0]
    assert result["proposal_id"] == "aave-123"
    assert "summary" in result
    assert "voting" in result
    assert "impact" in result
    assert result["voting"]["for_percentage"] > 50  # Should be winning

    print("✓ Single proposal summarization passed")
    print(f"  - Cost: ${result['cost_tokens']['input']} input tokens, ${result['cost_tokens']['output']} output tokens")
    print(f"  - Risk level: {result['impact']['risk_level']}")

def test_batch_proposals():
    """Test summarizing multiple proposals."""
    future_time = int((datetime.now() + timedelta(days=2)).timestamp())

    payload = {
        "proposals": [
            {
                "proposal_id": "compound-234",
                "dao_name": "Compound",
                "proposal_text": """Proposal 234: Update Reserve Factor for cDAI
Increase reserve factor from 10% to 12% to increase reserves for future needs.
This is a routine operational proposal with low risk.""",
                "voting_state": {
                    "for_votes": "800000000000000000000",
                    "against_votes": "200000000000000000000",
                    "abstain_votes": "50000000000000000000"
                }
            },
            {
                "proposal_id": "curve-189",
                "dao_name": "Curve",
                "proposal_text": """Proposal 189: Gauge Weight Update for ETH/BTC Pool
Rebalance gauge weights to incentivize liquidity in high-volume trading pairs.
Expected impact: 15% increase in ETH/BTC swap volume.""",
                "voting_state": {
                    "for_votes": "600000000000000000000",
                    "against_votes": "300000000000000000000",
                    "abstain_votes": "100000000000000000000"
                }
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["results"]) == 2

    total_cost_usd = data["total_cost"]["estimated_usd"]
    print(f"✓ Batch proposal summarization passed (2 proposals)")
    print(f"  - Total cost: ${total_cost_usd} USD")
    print(f"  - Cost per proposal: ${round(total_cost_usd / 2, 6)}")

def test_error_handling():
    """Test error handling."""
    # Test empty proposals
    payload = {"proposals": []}
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    assert response.status_code == 400
    print("✓ Empty proposal validation passed")

    # Test oversized batch
    large_batch = {
        "proposals": [
            {
                "proposal_id": f"prop-{i}",
                "dao_name": "TestDAO",
                "proposal_text": f"Test proposal {i}",
                "voting_state": {
                    "for_votes": "1000000000000000000000",
                    "against_votes": "100000000000000000000",
                    "abstain_votes": "50000000000000000000"
                }
            }
            for i in range(51)
        ]
    }
    response = requests.post(f"{BASE_URL}/summarize", json=large_batch)
    assert response.status_code == 400
    print("✓ Oversized batch validation passed")

def test_cost_model():
    """Test that cost model is reasonable."""
    future_time = int((datetime.now() + timedelta(hours=24)).timestamp())

    payload = {
        "proposals": [
            {
                "proposal_id": "test-cost",
                "dao_name": "TestDAO",
                "proposal_text": "A simple test proposal to validate cost tracking.",
                "voting_state": {
                    "for_votes": "1000000000000000000000",
                    "against_votes": "100000000000000000000",
                    "abstain_votes": "50000000000000000000"
                }
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    assert response.status_code == 200

    data = response.json()
    total_cost = data["total_cost"]["estimated_usd"]

    # Cost should be reasonable (< $1 for single proposal)
    assert total_cost < 1.0

    # Cost per proposal should be < $0.01
    per_proposal_cost = total_cost
    assert per_proposal_cost < 0.01

    print(f"✓ Cost model validation passed")
    print(f"  - Per proposal: ${round(per_proposal_cost, 6)}")

if __name__ == "__main__":
    print("Starting governance summarizer integration tests...\n")

    try:
        test_health()
        print()

        test_single_proposal()
        print()

        test_batch_proposals()
        print()

        test_error_handling()
        print()

        test_cost_model()
        print()

        print("✓ All integration tests passed!")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise