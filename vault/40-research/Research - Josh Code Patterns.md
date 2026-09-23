---
name: Josh Code Patterns
description: Architectural and design patterns from Josh's production code repositories
---

# Josh's Production Code Patterns

## Defensive Error Handling
**Pattern**: Raise hard errors rather than silent failures
- In redaktly's detector.py, missing spaCy models trigger ModelUnavailableError instead of falling back silently
- LEGALREDACT_OFFLINE env var forces failures instead of unexpected network calls
- Rationale: "found nothing" and "could not look" must never be the same answer
- **Haiku application**: Classification/extraction APIs must fail loudly with clear error types, not return partial/incorrect results silently

## Modular Architecture
**Pattern**: Clear separation of concerns with explicit module boundaries
- redaktly: detector (NER + regex), extractor (pattern matching), redactor (output generation), config (settings), passes (pipeline stages)
- ferryman: separate work repo and channel repo; coordination never touches work
- Rationale: Prevents cascading failures and allows independent testing/upgrades
- **Haiku application**: Build extraction/classification APIs as composable pipelines (detection → validation → enrichment)

## Environment-Based Configuration
**Pattern**: All runtime settings via env vars, with clear precedence and defaults
- redaktly: LEGALREDACT_* variables override config.yaml which overrides hardcoded defaults
- Precedence: defaults < config.yaml < environment < CLI flags
- Zero secrets in repo; all credentials injected at runtime
- **Haiku application**: Configuration should be completely decoupled from code for easy customer deployment

## Batch Processing with Cost Tracking
**Pattern**: Support both single and bulk operations with observable resource usage
- redaktly: supports both `scan` (single) and `batch` (directory) workflows
- ferryman: explicit `cost plan` (estimation) and `cost project` (actual usage)
- Cost model: token heuristic with editable rates, not live meters
- **Haiku application**: Expose cost estimation before commits; support bulk operations for DeFi monitoring tasks

## Audit Trail Logging
**Pattern**: JSON-structured logs for compliance and debugging
- redaktly: JSON audit logs of all redactions (what was found, where, confidence)
- ferryman: hash-chained audit trail with cryptographic proof
- Rationale: Regulatory compliance + debugging without exposing sensitive data
- **Haiku application**: Log all classifications/extractions with confidence scores and data lineage for compliance

## Local-First, Privacy-Preserving Design
**Pattern**: All processing local by default; no external calls unless explicitly configured
- redaktly: all processing on user's machine; no data to external servers
- ursos: Ollama (local LLM) instead of cloud API by default
- ferryman: no central server; files synced via Syncthing only
- Rationale: User control, privacy, offline capability, cost predictability
- **Haiku application**: Offer self-hosted option for DeFi projects; process documents locally before extraction

## Pluggable LLM Integration
**Pattern**: Support multiple inference backends with consistent interface
- ursos: Ollama interface that could swap for other providers
- redaktly: dual detection (regex + spaCy NER) with --method flag to choose
- Rationale: Flexibility without rewriting logic
- **Haiku application**: Support both Haiku API and local model backends for customer flexibility

## Cost-Conscious Token Usage
**Pattern**: Minimize token consumption through routing, batching, and early termination
- Haiku sweet spot: classification, extraction, summarization, routing, structured data generation
- Haiku weak spot: complex reasoning, creative writing, novel code generation
- **Opportunity**: Use Haiku's strengths to build high-volume APIs (100M+ tokens/month = $200-300/month revenue)

## Configuration via YAML + Environment
**Pattern**: Human-editable configs that respect environment overrides
- redaktly: config.yaml for regex patterns, detection methods, entity types; env vars override selectively
- Rationale: Operators can customize without code changes; automation can override for specific runs
- **Haiku application**: Allow DeFi projects to configure classification rules (smart contract types, bridge names, token lists) without code

## Monitoring and Health Checks
**Pattern**: Clear health visibility; restart-safe behavior
- ursos: explicit monitoring hooks and restart-safe state management
- ferryman: cost metrics and task tracking in dashboard
- Rationale: Operational visibility + predictable behavior under failure
- **Haiku application**: Expose API health, latency, and cost metrics to customers

## Go-Live Readiness
**Pattern**: Explicit verification before production deployment
- redaktly: GOLIVE_ANALYSIS.md, VERIFICATION.md, FINAL_IMPLEMENTATION_STATUS.md
- ferryman: docs/OPERATOR_BRIEF.md with safety procedure
- Rationale: No silent assumptions; every operator can validate before deploy
- **Haiku application**: Create runbooks for each DeFi use case with validation steps

---

## Applicable Patterns for DeFi Revenue Streams

### Transaction Classification (High Volume)
- Use batch processing pattern + cost tracking
- Classify on-chain transactions (whale activity, MEV, arbitrage, liquidations) with Haiku + structured output
- Cost: ~400M tokens/month @ Haiku rates = ~$1600/month output cost; target $600-800/month revenue (50% margin)

### Smart Contract Documentation
- Extract patterns from bytecode/ABI with Haiku classification
- Generate readable specs with structured output format
- Apply redaktly's extraction + batching patterns

### DAO Governance Summarization
- Batch proposals through Haiku summarization (Haiku sweet spot)
- Extract voting points and rationale with structured output
- Track cost per proposal for billing

### Bridge/Cross-Chain Monitoring
- Route transactions to Haiku classifier for bridge detection
- Low-token-cost extraction (bridge name, asset, amounts)
- High-volume use case fits Haiku costs perfectly

### Compliance Scanning
- Regex patterns (local, free) for contract addresses + known scams
- Haiku for semantic detection (unusual activity patterns)
- Hybrid approach minimizes token spend

---

## Next Steps
1. Validate patterns against actual DeFi project needs (reach out to 2-3 crypto projects)
2. Build proof-of-concept API wrapper for one pattern (e.g., transaction classification)
3. Measure token consumption vs. revenue targets
4. Document go-live runbook per use case
