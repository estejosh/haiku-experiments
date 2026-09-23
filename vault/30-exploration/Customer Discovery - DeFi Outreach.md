---
name: Customer Discovery - DeFi Outreach
description: Strategy and execution plan for validating DeFi use cases with real projects
---

# Customer Discovery: DeFi Outreach

**Goal**: Validate that identified DeFi problems are urgent and solvable  
**Target**: 2-3 customers (or problem validation signals) within 90 days  
**Status**: Planning (2026-09-23)

---

## Problem Validation Strategy

### Phase 1: Audience Identification (Week 1-2)
Identify projects in top 100 by market cap with specific pain points:

**Scoring Criteria**:
- Problem urgency: Does the use case represent >$200/month value?
- Solvability: Can Haiku-based solution deliver within 4 weeks?
- Accessibility: Can we reach decision-makers within 2 weeks?

**Target Projects by Use Case**:

1. **Transaction Classification** (whale activity, MEV detection)
   - Audience: CEX/DEX operators, trading venues
   - Examples: dYdX (DAO governance + MEV), 1Inch (DEX + MEV focus), Uniswap (governance + volumes)
   - Decision-maker: Head of Ops, Research Lead, Engineering Lead

2. **DAO Governance Summarization** (proposal extraction, voting analysis)
   - Audience: Large DAOs with active governance
   - Examples: Aave (70+ proposals/month), Compound, Curve
   - Decision-maker: Governance Lead, Community Manager

3. **Bridge/Cross-Chain Monitoring** (transaction routing, asset tracking)
   - Audience: Bridge operators, DEX aggregators
   - Examples: Stargate, Across, LayerZero ecosystem projects
   - Decision-maker: VP Engineering, Security Lead

4. **Compliance Scanning** (suspicious contract detection)
   - Audience: Wallets, custody providers, infrastructure
   - Examples: MetaMask (user security), Ledger (transaction verification)
   - Decision-maker: Head of Security, Compliance Officer

### Phase 2: Outreach (Week 2-6)
Multiple contact channels per project:

**Channel 1: Direct Email**
- Research decision-makers on LinkedIn
- Find emails via: (name)@(company).eth on Discord/Twitter, official bios
- Template: Problem statement → specific use case → 15-min call offer

**Channel 2: Discord/Community**
- Join official Discord servers
- Engage in dev/ops channels with specific questions
- Request intro with specific problem context

**Channel 3: Twitter/GitHub**
- Follow maintainers and engineers
- Comment on relevant issues (MEV, bridge, governance challenges)
- DM with problem-specific request

**Template Outreach Message**:
```
Hi [Name],

We've been analyzing Haiku LLM for high-volume crypto tasks. 
Saw your work on [specific problem: MEV detection | governance | bridges].

We think we can reduce operational overhead by 40% for [specific task].
Would you have 15 min this week to explore if it's worth investigating?

Link: [github/demo]
```

### Phase 3: Discovery Call Framework (Week 2-8)
Structure for 15-30 min conversations:

**Goals**:
1. Confirm the problem exists and is urgent
2. Estimate impact (hours saved, cost reduction)
3. Get commitment to pilot (or clear rejection)

**Agenda**:
- **5 min**: Intro + context
- **5 min**: Their current approach (pain point validation)
- **5 min**: Proposed solution outline
- **5 min**: Next steps (pilot terms, timeline)

**Pilot Criteria** (to move to PoC):
- Problem: Addressing >4 hours/week of manual work OR >$500/month operational cost
- Budget: Willing to allocate <$300/month for 3-month pilot
- Timeline: Can integrate within 4 weeks of API availability
- Feedback: Will provide data + qualitative feedback on solution

---

## Proof-of-Concept (PoC) Execution

### Use Case Selection
Pick **ONE** use case for first PoC (2-week sprint):

**Recommendation**: Transaction Classification
- Rationale: Highest volume, lowest complexity, fastest to ship
- Scope: Classify Ethereum transactions (whale, MEV, liquidation, arbitrage)
- Deliverable: API endpoint + documentation + 1000-transaction test run

### PoC Scope (2 weeks max)
```
Week 1:
- Day 1-2: API design + sample data
- Day 3-4: Haiku integration + batching logic
- Day 5: Testing + cost measurement

Week 2:
- Day 1-2: Documentation + runbook
- Day 3: Customer integration setup
- Day 4-5: Feedback iteration
```

### Success Metrics
- Latency: <100ms per transaction (batched)
- Cost: <$0.50/1M transactions processed
- Accuracy: >85% precision on whale classification
- Customer ready: Can deploy on Monday after 2 weeks

---

## Revenue Model (Pilot Terms)

### Pilot Pricing (3 months)
- **Transaction Classification**: $300/month for 100M transactions/month
- **DAO Governance**: $250/month for 50 proposals/month
- **Bridge Monitoring**: $400/month for continuous monitoring
- **Compliance Scanning**: $200/month for 1000 contracts/month

**Pilot Commitment**:
- Customer provides test data
- We provide API endpoint + 30-day SLA
- Monthly check-in on impact

### Production Pricing (Post-Pilot)
- Scale to actual usage (e.g., $0.001 per transaction)
- Minimum: $200/month
- Volume discounts: 20%+ reduction at $1000+/month

---

## Content + Growth Strategy

### Parallel: Blog/Content (During outreach)
Posts to build awareness:
1. "Haiku for High-Volume Classification" (technical deep-dive)
2. "DeFi Operations: The Token-Efficiency Angle" (use case overview)
3. Case Study: Transaction Classification (post-pilot)

**Distribution**:
- Dev.to, Medium, Substack (crypto dev audience)
- Shared in crypto Discord servers + Twitter
- Target: <2 week creation cycle

### GitHub Visibility
- Star haiku-experiments repo + add crypto tag
- Link to blog posts in README
- Open-source one PoC as example

---

## Success Metrics

**90-Day Goals**:
- [ ] 10+ discovery conversations
- [ ] 2-3 pilot commitments
- [ ] 1 PoC shipped + integrated
- [ ] $200-500/month pilot revenue
- [ ] 5-10 blog post views (validation signal)

**Beyond 90 Days**:
- [ ] 1+ production customer
- [ ] $400+/month recurring revenue
- [ ] 3-5 use cases PoC'd + available

---

## Current Status

**Completed**:
- ✓ Problem validation via code pattern research
- ✓ Use case identification (5 specific problems)
- ✓ Economics modeling (50%+ margins achievable)

**In Progress**:
- Project list compilation (top 100 by market cap)
- Decision-maker research (LinkedIn, public sources)

**Next**:
- Start outreach (Week 1 of customer discovery)
- Build transaction classification PoC (parallel)
