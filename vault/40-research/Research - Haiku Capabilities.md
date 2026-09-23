---
title: Research - Haiku Capabilities
aliases: [Haiku specs, model constraints]
tags: [research, haiku, capabilities]
type: note
created: 2026-09-23
updated: 2026-09-23
status: growing
related: []
---

# Haiku Capabilities & Constraints

## Core Facts
- **Speed**: 5-10x faster than Sonnet/Opus
- **Cost**: ~\.80 per million input tokens, ~\ per million output tokens
- **Context**: 200k tokens (sufficient for most docs)
- **Quality**: Excellent at categorization, extraction, summarization; weaker on complex reasoning/creativity

## Sweet Spots for Haiku
- [ ] Transaction/event classification
- [ ] Data extraction from unstructured text
- [ ] Content summarization (news, contracts, proposals)
- [ ] Routing & decision trees
- [ ] Email/support triage
- [ ] Structured data generation (JSON, CSV)
- [ ] Link/relationship extraction
- [ ] Format conversion

## Weak Spots (Avoid)
- [ ] Complex reasoning (multi-step logic)
- [ ] Creative writing
- [ ] Code generation for novel problems
- [ ] Legal interpretation/advice
- [ ] Research synthesis

## Economics at Scale
- To make \/month revenue: ~\-400/month inflow at typical B2B rates
- Break-even: Process ~400M tokens/month at 50% margin (depends on pricing model)
- With batch processing: 3-5 customers at \-150/month = sustainable

