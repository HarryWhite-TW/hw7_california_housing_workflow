$ErrorActionPreference = "Stop"

$remoteUrl = "https://github.com/HarryWhite-TW/hw7_california_housing_workflow.git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or is not available in PATH."
}

if (-not (Test-Path ".git")) {
    git init
    git config user.name "HarryWhite-TW"
    git config user.email "harry061892@gmail.com"
    git add .
    git commit -m "feat: scaffold reusable California Housing workflow"
}

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $remoteUrl
} elseif ($existingRemote -ne $remoteUrl) {
    throw "An origin remote already exists and points to: $existingRemote"
}

git branch -M main
git push -u origin main
