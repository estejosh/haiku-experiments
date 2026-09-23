# Haiku Crazy

**Test environment for sustainable revenue modeling with Claude Haiku.**

Generate \+/month revenue from Haiku-only operations to cover API costs independently.

## What This Is

Haiku Crazy is an exploration project designed to answer: *Can Claude Haiku, constrained to the cheapest model, generate enough revenue to sustain its own \/month API costs?*

The hypothesis: Haiku excels at high-volume, low-complexity tasks. By focusing on cost-efficient batch processing, classification, extraction, and automation, a Haiku-only service can hit profitability at 3–5 customers generating \–150/month each.

## Current Phase

**Phase 2: Exploration** — Testing three hypotheses:
1. **Crypto DeFi Automation** — Smart contract docs, DAO governance, transaction classification
2. **Legal Document Analysis** — Extract/summarize legal documents (processing, not advice)
3. **Batch Document Processing** — Generic high-volume document service

Infrastructure in place:
- Obsidian vault for exploration (local + git-backed)
- Independent AI email identity
- Git repo with protections against cross-repo contamination
- Economics model in development

## Repository Structure

\\\
haiku-crazy/
├── vault/              # Obsidian vault (exploration, research, hypotheses)
│   ├── 00-inbox/       # Raw captures
│   ├── 10-notes/       # Atomic notes
│   ├── 20-mocs/        # Maps of Content (navigation)
│   ├── 30-exploration/ # Active hypotheses & experiments
│   ├── 40-research/    # Validated findings
│   └── 90-assets/      # Images & attachments
├── .env                # API tokens (readonly PAT, full haiku PAT)
├── README.md           # This file
├── LICENSE             # UFL (Usufruct License)
└── REPO_ISOLATION.md   # Protection guidelines
\\\

## Key Constraints

- **Model**: Claude Haiku only (cheapest available)
- **Resources**: No access to Josh's network/infrastructure
- **Access**: Josh's brain for guidance/feedback only
- **Isolation**: Learning happens in read-only repos; code never merges back
- **Documentation**: All learning tracked in shared Obsidian vault + git

## Learning Repos

Read-only access to Josh's repositories for pattern analysis:
- Redaktly — legal document automation
- Ferryman — AI agent fleet communication & memory
- Speakeasy Automations — n8n automation workflows
- URSOS — multi-agent orchestration framework
- Telegram Tester — LLM-powered testing

**Important**: These are for learning *only*. Code/patterns are studied; code is never merged into haiku-crazy. See \REPO_ISOLATION.md\.

## API Economics (Target)

- **Revenue needed**: \–400/month (at ~50% margin)
- **Customer targets**: 3–5 at \–150/month each
- **Haiku costs**: ~\.80 per million input tokens, ~\ per million output tokens
- **Break-even**: ~400M tokens/month at reasonable margins

## Haiku Sweet Spots

- Classification & routing (email triage, transaction type detection)
- Data extraction from unstructured text
- Content summarization & briefing generation
- Structured data generation (JSON, CSV, metadata)
- High-volume, low-reasoning tasks

## What's Next

1. Deep dive into crypto/DeFi angles (Josh's expertise)
2. Identify 2–3 specific, solvable problems Haiku can tackle
3. Mock up one offering with cost model
4. Plan cold-start customer discovery
5. Iterate based on market feedback

## License

[UFL (Usufruct License)](https://github.com/estejosh/UFL-Usufruct-License) — Source-available, unrestricted use at any scale, redistribution reserved.

## Status

Started: 2026-09-23
Phase: Exploration (Learning)
Next: Hypothesis validation

---

**This is a learning project. All findings documented in the vault.**
