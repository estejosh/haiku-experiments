# Repository Isolation Guidelines

## Purpose

Haiku Crazy has read-only access to Josh's learning repositories. This document 
ensures we learn *from* those repos without accidentally merging their code or 
violating their isolation.

## Learning Repos (Read-Only)

- \stejosh/redaktly\ — Legal document automation CLI
- \stejosh/ferryman\ — AI agent fleet communication
- \stejosh/speakeasy-automations\ — n8n workflow patterns
- \stejosh/ursos\ — Multi-agent orchestration
- \stejosh/telegram-tester\ — LLM testing utilities

## Rules

### What We DO
- ✅ Read and analyze code patterns
- ✅ Learn from architecture/design decisions
- ✅ Document findings in \ault/40-research/\
- ✅ Apply *lessons learned* to our own code
- ✅ Cite which repo inspired a pattern
- ✅ Reference repos in exploration notes

### What We DON'T DO
- ❌ Copy code directly from learning repos
- ❌ Merge branches from learning repos
- ❌ Import private modules/packages from Josh's repos
- ❌ Use Josh's infrastructure (n8n, credentials, API keys)
- ❌ Expose learning repo names in public documentation
- ❌ Treat learning repos as dependencies

## Protection Mechanisms

1. **Separate Git Remotes**: Learning repos on different remotes, haiku-crazy isolated
2. **No Submodules**: Learning happens via reading, not git submodules
3. **.env Isolation**: Tokens kept separate; readonly PAT limits surface area
4. **Documentation**: \ault/40-research/\ documents what we learned, not what we copied
5. **Code Review**: All haiku-crazy code is original, inspired by patterns only

## If We Discover Something Worth Reusing

1. Document the learning in \ault/40-research/\
2. Implement *from scratch* in haiku-crazy code
3. Cite the original source in comments
4. Get Josh's approval before using any patterns from private repos

Example good comment:
\\\
// Pattern inspired by ferryman's agent-routing design
// See vault/40-research/Agent-Routing-Pattern.md for analysis
\\\

## Violations to Catch

Red flags:
- Identical function/variable names across repos
- Importing from Josh's private packages
- Using credentials/keys from Josh's .env
- Merging branches from learning repos
- Pushing learning repos into haiku-crazy

## Review Checklist

Before committing to haiku-crazy:
- [ ] No code copied from learning repos
- [ ] All inspirations documented in vault/40-research/
- [ ] Original implementation in haiku-crazy codebase
- [ ] .env file references only haiku-crazy secrets
- [ ] No git submodules or external package imports
- [ ] Commit message notes what learning informed the code

