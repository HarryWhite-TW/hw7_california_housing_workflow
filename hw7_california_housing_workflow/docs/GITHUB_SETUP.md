# GitHub Repository Setup

The project is prepared as a local Git repository baseline. Creating a new remote repository is the one GitHub account action that must be completed by the repository owner.

## 1. Create the empty repository

Create a new **public** repository named:

```text
hw7_california_housing_workflow
```

Do not initialize it with a README, `.gitignore`, or license because those files already exist locally.

## 2. Connect and push

From the project root in PowerShell:

```powershell
git remote add origin https://github.com/HarryWhite-TW/hw7_california_housing_workflow.git
git branch -M main
git push -u origin main
```

Alternatively, run:

```powershell
.\publish_to_github.ps1
```

## 3. Run the real workflow

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_workflow.py --config configs/california_housing.json
python -m pytest
```

Then commit and push the generated real outputs:

```powershell
git add outputs site/results.js
git commit -m "feat: publish California Housing workflow results"
git push
```

## 4. Enable GitHub Pages

In the repository:

```text
Settings → Pages → Build and deployment → Deploy from a branch
Branch: main
Folder: / (root)
```

Expected URL:

```text
https://harrywhite-tw.github.io/hw7_california_housing_workflow/
```
