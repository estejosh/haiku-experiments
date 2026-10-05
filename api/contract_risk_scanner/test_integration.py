"""Integration tests for the contract risk scanner API."""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✓ Health check passed")

def test_simple_contract():
    """Test analyzing a simple safe contract."""
    # A simple ERC20-like contract
    simple_contract = """
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SafeToken is ERC20, Ownable {
    constructor(string memory name, string memory symbol, uint256 initialSupply)
        ERC20(name, symbol) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
"""

    payload = {
        "contracts": [
            {
                "contract_id": "safe-token",
                "contract_name": "SafeToken",
                "chain": "ethereum",
                "contract_source": simple_contract,
                "tvl_usd": 1000000
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1

    result = data["results"][0]
    assert result["contract_id"] == "safe-token"
    assert "findings" in result
    assert "security_patterns" in result
    assert result["risk_score"] >= 0 and result["risk_score"] <= 100

    print("✓ Simple contract analysis passed")
    print(f"  - Risk level: {result['risk_level']}")
    print(f"  - Risk score: {result['risk_score']}")
    print(f"  - Findings: {len(result['findings'])}")

def test_complex_contract():
    """Test analyzing a more complex contract."""
    complex_contract = """
pragma solidity ^0.7.0;

interface ISwapRouter {
    function swap(address token0, address token1, uint256 amount) external;
}

contract SimpleDEX {
    ISwapRouter public router;

    constructor(address _router) {
        router = ISwapRouter(_router);
    }

    // Missing access control - anyone can call
    function executeSwap(address token0, address token1, uint256 amount) public {
        router.swap(token0, token1, amount);
    }

    // Potential reentrancy if token has custom transfer
    function withdrawTokens(address token, uint256 amount) public {
        (bool success,) = token.call(abi.encodeWithSignature("transfer(address,uint256)", msg.sender, amount));
        require(success);

        // Update state after external call (wrong order)
        userBalance[msg.sender] -= amount;
    }

    mapping(address => uint256) public userBalance;
}
"""

    payload = {
        "contracts": [
            {
                "contract_id": "dex-contract",
                "contract_name": "SimpleDEX",
                "chain": "ethereum",
                "contract_source": complex_contract,
                "tvl_usd": 5000000
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    result = data["results"][0]

    # Should have identified some issues
    assert len(result["findings"]) > 0
    assert result["risk_score"] > 30  # More risky than safe contract

    print("✓ Complex contract analysis passed")
    print(f"  - Risk level: {result['risk_level']}")
    print(f"  - Critical findings: {sum(1 for f in result['findings'] if f['severity'] == 'critical')}")
    print(f"  - High findings: {sum(1 for f in result['findings'] if f['severity'] == 'high')}")

def test_error_handling():
    """Test error handling."""
    # Empty contracts
    payload = {"contracts": []}
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert response.status_code == 400
    print("✓ Empty contract validation passed")

    # Too many contracts
    large_batch = {
        "contracts": [
            {
                "contract_id": f"contract-{i}",
                "contract_source": "pragma solidity ^0.8.0;"
            }
            for i in range(21)
        ]
    }
    response = requests.post(f"{BASE_URL}/analyze", json=large_batch)
    assert response.status_code == 400
    print("✓ Oversized batch validation passed")

def test_cost_tracking():
    """Test cost tracking functionality."""
    test_contract = "pragma solidity ^0.8.0; contract Test {}"

    payload = {
        "contracts": [
            {
                "contract_id": "minimal-contract",
                "contract_source": test_contract
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    total_cost = data["total_cost"]["estimated_usd"]

    # Cost should be tracked
    assert total_cost >= 0
    # Should be reasonable for single minimal contract
    assert total_cost < 0.1

    print(f"✓ Cost tracking passed")
    print(f"  - Per contract cost: ${total_cost:.6f}")

if __name__ == "__main__":
    print("Starting contract risk scanner integration tests...\n")

    try:
        test_health()
        print()

        test_simple_contract()
        print()

        test_complex_contract()
        print()

        test_error_handling()
        print()

        test_cost_tracking()
        print()

        print("✓ All contract analysis tests passed!")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise