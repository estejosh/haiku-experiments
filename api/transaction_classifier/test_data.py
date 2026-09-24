"""Sample Ethereum transactions for testing the classifier."""

sample_transactions = [
    {
        "transaction_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "from_address": "0xaabbccddaabbccddaabbccddaabbccddaabbccdd",
        "to_address": "0xc02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "value": "50000000000000000000",
        "data": "0xd0e30db0",
        "gas_price": "50000000000",
        "timestamp": "2026-09-23T12:34:56Z"
    },
    {
        "transaction_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "from_address": "0x1111111111111111111111111111111111111111",
        "to_address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        "value": "0",
        "data": "0xa9059cbb",
        "gas_price": "45000000000",
        "timestamp": "2026-09-23T12:35:00Z"
    },
    {
        "transaction_hash": "0xfedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
        "from_address": "0x2222222222222222222222222222222222222222",
        "to_address": "0x3333333333333333333333333333333333333333",
        "value": "1000000000000000000",
        "data": "0x",
        "gas_price": "30000000000",
        "timestamp": "2026-09-23T12:36:00Z"
    }
]
