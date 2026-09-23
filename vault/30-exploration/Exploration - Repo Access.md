---
title: Exploration - Repo Access & Authentication
aliases: [token setup, private repos]
tags: [exploration, infrastructure]
type: note
created: 2026-09-23
updated: 2026-09-23
status: seedling
related: ["[[AI Email Setup]]"]
---

# Exploration: Accessing Josh's Private Repos

## Status

Attempted to clone redaktly (estejosh/redaktly) for pattern analysis.
**Result**: 403 — Private repository requires authentication.

## What I Found

The learning repos are private. To access them, I need:
1. GitHub readonly PAT token (GITHUB_PAT_READONLY env var)
2. Proper git/authentication configuration
3. OR: Josh provides access links/temporary credentials

## Next Steps

Need clarification:
1. Should I request the actual token values?
2. Are any repos public I can start with?
3. Should I set up SSH keys instead of HTTP auth?
4. Or shall I explore via GitHub web interface / API?

## Alternative Approach

While waiting for auth:
- Can I search Josh's public gists/docs for patterns?
- Can I find blog posts/writeups describing the architecture?
- Can I explore public crypto projects using similar patterns?

