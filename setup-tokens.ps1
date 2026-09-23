# setup-tokens.ps1
# Run this with your actual token values

param(
    [Parameter(Mandatory=$true)]
    [string]$ReadonlyToken,
    
    [Parameter(Mandatory=$true)]
    [string]$FullToken
)

# Set environment variables
$env:GITHUB_PAT_READONLY = $ReadonlyToken
$env:GITHUB_PAT_FULL = $FullToken

# Configure git to use tokens
Set-Location "X:\haiku_crazy"

# Store tokens for authentication
git config --local credential.helper store
git config --local url."https://oauth2:$FullToken@github.com/estejosh/haiku-experiments.git".insteadOf "https://github.com/estejosh/haiku-experiments.git"

Write-Host "Tokens configured"
Write-Host "GITHUB_PAT_READONLY: set (length: $($ReadonlyToken.Length) chars)"
Write-Host "GITHUB_PAT_FULL: set (length: $($FullToken.Length) chars)"
Write-Host ""
Write-Host "Ready to:"
Write-Host "  - git clone with $env:GITHUB_PAT_READONLY for Josh's repos"
Write-Host "  - git push with $env:GITHUB_PAT_FULL to haiku-experiments"
