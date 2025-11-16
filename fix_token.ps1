# Script to remove Hugging Face token from git history
$token = "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"
$replacement = "YOUR_HF_TOKEN"

# Use git filter-branch to replace token in all commits
git filter-branch -f --tree-filter "if (Test-Path DEPLOY_TO_HF.md) { (Get-Content DEPLOY_TO_HF.md) -replace '$token', '$replacement' | Set-Content DEPLOY_TO_HF.md }" --prune-empty HEAD~4..HEAD

Write-Host "Token removed from git history. You can now push."

