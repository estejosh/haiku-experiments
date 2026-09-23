# Haiku Crazy - Project Home

**Goal**: Can Claude Haiku, constrained to the cheapest model, generate enough revenue to sustain its own API costs independently?

**Target**: $200-400/month revenue to cover ~$200/month Haiku API costs + margin

**Status**: Phase 2 - Repo Analysis & Pattern Documentation  
**Last Updated**: 2026-09-23

---

## Navigation
- [[Exploration MOC]] - Active hypotheses, experiments, questions
- [[Research MOC]] - Validated findings and documentation
- [[Ideas MOC]] - Future directions and brainstorms

---

## Key Findings (Phase 2)

### Repo Exploration Complete
Analyzed three major production codebases:
- **redaktly**: Document extraction, regex + NER detection, batch processing, audit logging
- **ferryman**: Agent coordination, cost tracking, local-first architecture, signed messages
- **ursos**: Telegram bot, LLM integration, cloud archival, monitoring patterns

### Pattern Extraction
Documented 10+ architectural patterns applicable to Haiku revenue:
- Defensive error handling (fail loudly, not silently)
- Modular pipelines (detection → validation → enrichment)
- Batch processing + cost tracking
- Environment-based configuration
- JSON audit trails for compliance
- Local-first, privacy-preserving design

**Link**: [Josh Code Patterns](vault/40-research/Research%20-%20Josh%20Code%20Patterns.md)

### DeFi Opportunity Validation
Identified 5 specific DeFi use cases + corresponding patterns:
1. **Transaction Classification** (high volume) - Haiku batch + structured output
2. **Smart Contract Documentation** - Extraction + batching patterns
3. **DAO Governance Summarization** - Haiku sweet spot (summarization)
4. **Bridge/Cross-Chain Monitoring** - Low-token-cost routing
5. **Compliance Scanning** - Hybrid regex + semantic approach

Economics: ~400M tokens/month @ Haiku = $1600 output cost; target $600-800/month revenue (50% margin)

---

## Current Phase Objectives
- [ ] Validate DeFi problems against actual crypto projects (customer discovery)
- [ ] Build proof-of-concept API for one use case (transaction classification)
- [ ] Measure actual token consumption vs. revenue targets
- [ ] Design cold-start customer acquisition strategy
- [ ] Document go-live runbook per use case

---

## Project Structure
```
haiku_crazy/
├── vault/
│   ├── 20-mocs/          # Maps of Content (navigation)
│   ├── 30-exploration/   # Active hypotheses and experiments
│   ├── 40-research/      # Validated findings
│   └── HOME.md           # This file
├── .env                  # GitHub tokens (READONLY, FULL)
└── README.md             # Full project overview
```

---

## Commands
```bash
# Development
git pull origin main
git status

# Vault navigation
# Open vault/ in Obsidian

# To add new findings
# 1. Create in vault/40-research/ or vault/30-exploration/
# 2. Link from appropriate MOC
# 3. Commit and push
```

---

## Revenue Model (Current Target)
- 3-5 crypto projects @ $200-300/month each = $600-1500/month
- Covers API costs ($200/month) + sustainable margin
- Initial customer acquisition via crypto network + repos + content

---

## Next Check-In
Review customer discovery progress; validate one DeFi use case with real project
