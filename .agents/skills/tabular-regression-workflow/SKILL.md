---
name: tabular-regression-workflow
description: Use this repository-scoped skill when Codex is asked to run, regenerate, adapt, or verify the configured California Housing reusable tabular regression workflow and its metrics, charts, model, report, static site data, or compatible CSV regression variants.
---

# Tabular Regression Workflow

## 1. Purpose

This skill tells Codex how to operate the repository's deterministic tabular regression workflow. The workflow is implemented by the project code; the skill is an execution and verification guide, not a second model implementation.

## 2. Trigger Conditions

Use this skill when the user asks to:

- run or validate the California Housing HW7 workflow;
- regenerate metrics, charts, the model file, the Markdown report, or static site data;
- verify that generated outputs are complete and internally consistent;
- adapt the existing configured workflow to another compatible CSV regression dataset;
- explain how Codex should use the repository workflow.

## 3. Non-Trigger Conditions

Do not use this skill for:

- classification;
- time-series forecasting;
- image, audio, video, or unstructured-data modeling;
- arbitrary AutoML;
- causal inference claims;
- replacing the repository workflow with a new framework or service.

## 4. Required Repository Context

Before acting, read:

- `AGENTS.md`
- `WORKFLOW.md`
- `configs/california_housing.json` or the selected config file
- `docs/WORKFLOW_GUIDE.md`
- `docs/SKILL_GUIDE.md`
- `.agents/skills/tabular-regression-workflow/references/output-contract.md`

## 5. Python Interpreter Selection

Prefer the repository virtual environment:

```text
Windows: .venv\Scripts\python.exe
POSIX:   .venv/bin/python
Fallback: python3, python
```

Do not assume a global interpreter. If `.venv` is absent, select an available compatible Python interpreter, create `.venv`, and install only packages already declared in `requirements.txt`.

## 6. Preflight Checks

Run or confirm:

```powershell
git status --short
git branch --show-current
git remote -v
```

Then confirm:

- the configured CSV exists or `download_if_missing` is allowed;
- the config lists a continuous target column;
- numerical and categorical feature names are explicit;
- no unexpected local changes will be overwritten;
- no commit or push will be made without explicit user approval.

## 7. Execution Procedure

Install dependencies only from the repository manifest:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run the workflow:

```powershell
.\.venv\Scripts\python.exe run_workflow.py --config configs\california_housing.json
```

Verify outputs:

```powershell
.\.venv\Scripts\python.exe .agents\skills\tabular-regression-workflow\scripts\verify_outputs.py --config configs\california_housing.json
```

## 8. Output Verification

The verifier must check the output contract for:

- config readability;
- required output files;
- `metrics.json`;
- `dataset_summary.json`;
- `site/results.js` status `complete`;
- site metrics matching `metrics.json`;
- real California Housing results rather than the 72-row smoke fixture;
- feature schema consistency;
- predictions and coefficients CSV structure;
- non-empty readable PNG files;
- loadable joblib model;
- scikit-learn `Pipeline` with `preprocessor` and `regressor`;
- `ColumnTransformer` preprocessor;
- `LinearRegression` regressor.

## 9. Adaptation To Another Dataset

When reusing the workflow with another compatible CSV:

1. Copy the existing config to a new file in `configs/`.
2. Change the dataset name, data path or source URL, target column, feature lists, output directory, and model filename.
3. Keep the same workflow entry point.
4. Run tests and the verifier against the new config.
5. Do not overwrite the California Housing baseline unless the user explicitly requests that.

## 10. Failure Handling

If a check fails:

- report the exact command and failure;
- preserve existing outputs unless regeneration was requested;
- inspect the config, dataset schema, and generated artifacts before changing code;
- make the smallest repository-consistent fix;
- rerun tests and verification.

## 11. Safety Boundaries

- Do not add undeclared dependencies.
- Do not introduce Streamlit, React, Vite, Docker, APIs, databases, or cloud services.
- Do not silently change the target column or feature schema.
- Do not claim coefficients prove causality.
- Do not make destructive Git changes.
- Do not commit or push unless the user explicitly approves.

## 12. Final Reporting Contract

Report:

- Git sync state and latest commit;
- Python interpreter and dependency setup;
- files changed;
- skill package structure;
- verifier coverage;
- guide updates;
- README and GitHub Pages updates;
- pytest result;
- verifier result;
- GitHub Pages HTTP verification status, if checked;
- whether metrics changed;
- `git status --short`;
- fresh-session skill activation status from `docs/SKILL_VALIDATION.md`;
- whether a commit or push was performed, and whether it was explicitly approved.
