# Token Setup

## Files

- .env.local — Local token storage (DO NOT COMMIT)
- setup-tokens.ps1 — Script to configure tokens

## Usage

1. Get your two GitHub PATs:
   - **READONLY**: Read-only access to all Josh's repos
   - **FULL**: Read/write access to estejosh/haiku-experiments

2. Run the setup script:
\\\powershell
.\setup-tokens.ps1 -ReadonlyToken "ghp_xxxxx" -FullToken "ghp_yyyyy"
\\\

3. Then you can:
   - Clone Josh's repos with readonly token
   - Push to haiku-experiments with full token

## Security

- .env.local is in .gitignore (never committed)
- Tokens are only set for the local git config
- Each token has minimal required permissions

