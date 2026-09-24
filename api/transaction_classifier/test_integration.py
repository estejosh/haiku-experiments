#!/usr/bin/env python3
"""
Integration test for transaction classifier.
Tests the classifier API with sample Ethereum transactions.
"""

import json
import requests
import time
from test_data import sample_transactions

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print(f"✓ Health check passed: {data}")

def test_classify_single():
    """Test classifying a single transaction."""
    print("\nTesting single transaction classification...")

    request_data = {
        "transactions": [sample_transactions[0]]
    }

    response = requests.post(f"{API_URL}/classify", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "results" in data
    assert "total_cost" in data

    result = data["results"][0]
    print(f"✓ Transaction: {result['transaction_hash'][:16]}...")
    print(f"  Classifications: {len(result['classifications'])}")
    for clf in result['classifications']:
        print(f"    - {clf['type']}: {clf['confidence']:.2f} confidence")

    cost = data["total_cost"]
    print(f"  Cost: ${cost['estimated_usd']:.4f} ({cost['input_tokens']} input, {cost['output_tokens']} output tokens)")

def test_classify_batch():
    """Test classifying multiple transactions."""
    print("\nTesting batch transaction classification...")

    request_data = {
        "transactions": sample_transactions
    }

    response = requests.post(f"{API_URL}/classify", json=request_data)
    assert response.status_code == 200

    data = response.json()
    print(f"✓ Classified {len(data['results'])} transactions")

    total_cost = data["total_cost"]
    print(f"  Total cost: ${total_cost['estimated_usd']:.4f}")
    print(f"  Total tokens: {total_cost['input_tokens']} input, {total_cost['output_tokens']} output")

    # Verify cost model
    expected_usd = (total_cost['input_tokens'] * 0.80 + total_cost['output_tokens'] * 4.0) / 1_000_000
    assert abs(total_cost['estimated_usd'] - expected_usd) < 0.00001
    print(f"  ✓ Cost model validated")

def test_error_handling():
    """Test error cases."""
    print("\nTesting error handling...")

    # Test empty request
    response = requests.post(f"{API_URL}/classify", json={"transactions": []})
    assert response.status_code == 400
    print("✓ Empty request rejected (400)")

    # Test too many transactions
    too_many = {"transactions": sample_transactions * 50}  # 150 transactions
    response = requests.post(f"{API_URL}/classify", json=too_many)
    assert response.status_code == 400
    print("✓ Oversized request rejected (400)")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Transaction Classifier - Integration Tests")
    print("=" * 60)

    try:
        test_health()
        test_classify_single()
        test_classify_batch()
        test_error_handling()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API at " + API_URL)
        print("Make sure the server is running: python main.py")
        exit(1)
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()
