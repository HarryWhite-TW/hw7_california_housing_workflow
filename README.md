# HW7 California Housing Reusable Regression Workflow

## Interactive Demo

[Open the GitHub Pages dashboard](https://harrywhite-tw.github.io/hw7_california_housing_workflow/)

```text
Workflow: Completed & Verified
Codex Skill: Completed & Verified
Explicit activation: Passed
Implicit activation: Passed
Artifact verification: Passed
Public deployment: Verified
```

![California Housing CRISP-DM Workflow Infographic](outputs/homework_infographic.png)

![California Housing Linear Regression Model Metrics](outputs/model_metrics_summary.png)

## Project Overview

This project extracts a repeatable CRISP-DM regression workflow from the earlier HW6 analysis and validates it on the full California Housing dataset. The workflow downloads or reads a CSV, validates schema, preprocesses numerical and categorical features, trains a linear regression pipeline, writes metrics, saves artifacts, and publishes static dashboard data.

The repository-scoped Codex Skill is a controlled operating guide around the tested workflow. It tells Codex when to run, verify, adapt, and report the workflow without rewriting the analysis.

## Why This Project Exists

The goal is not to chase the highest possible score. The goal is to make the analysis reusable, inspectable, and safe to run on another machine. Humans, scripts, tests, and Codex all use the same workflow contract.

## Verified Results

Real California Housing baseline:

- Dataset: 20,640 rows, 10 columns, 9 configured features
- Target: `median_house_value`
- Test R2: 0.6254382675296286
- MAE: 50,670.48923565587
- RMSE: 70,059.19333924996
- CV R2 mean/std: 0.6432846133282536 / 0.0200522297447311
- CV RMSE mean/std: 68,881.17625531893 / 1,988.1036723885318

## Workflow And Skill At A Glance

| Layer | Responsibility | Used by |
| --- | --- | --- |
| Workflow | Executes deterministic analysis | Humans, CI, scripts, Codex |
| Skill | Guides Codex to select, run and verify Workflow | Codex |
| Config | Defines dataset-specific schema | Workflow |
| Verification | Checks outputs and consistency | Humans, CI, Codex |

## Architecture

```text
configs/california_housing.json
  -> run_workflow.py
  -> src/config.py
  -> src/data_io.py
  -> src/modeling.py
  -> src/visualization.py
  -> src/reporting.py
  -> outputs/
  -> site/results.js
```

The saved model is a scikit-learn `Pipeline` containing a `ColumnTransformer` preprocessor and `LinearRegression` regressor.

## Manual Execution

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe run_workflow.py --config configs\california_housing.json
.\.venv\Scripts\python.exe .agents\skills\tabular-regression-workflow\scripts\verify_outputs.py --config configs\california_housing.json
```

If `data/housing.csv` is missing, the workflow downloads the configured source automatically.

## Codex Usage

The workflow remains the source of truth for the analysis. The repository skill is the Codex operating guide: it selects the configured workflow, runs validation, and reports results without redesigning the model. The verifier is the deterministic quality gate for generated artifacts.

Minimal validation prompt:

```text
Use $tabular-regression-workflow to validate the current
California Housing workflow outputs.
Do not modify, commit, or push.
```

Full regeneration prompt:

```text
Regenerate and verify the configured California Housing regression
metrics, model, charts, report, and static site data.
Do not redesign the analysis.
```

## Documentation Hub

- [Canonical workflow specification](WORKFLOW.md)
- [Workflow guide](docs/WORKFLOW_GUIDE.md)
- [Skill guide](docs/SKILL_GUIDE.md)
- [Skill validation](docs/SKILL_VALIDATION.md)
- [Design notes](docs/DESIGN.md)
- [Implementation plan](docs/HW7_IMPLEMENTATION_PLAN.md)
- [Validation record](docs/VALIDATION.md)
- [Repository skill](.agents/skills/tabular-regression-workflow/SKILL.md)
- [Output contract](.agents/skills/tabular-regression-workflow/references/output-contract.md)

## Generated Artifacts

- `outputs/metrics.json`
- `outputs/dataset_summary.json`
- `outputs/predictions.csv`
- `outputs/feature_coefficients.csv`
- `outputs/california_housing_model.pkl`
- `outputs/workflow_report.md`
- `outputs/dataset_overview_dashboard.png`
- `outputs/correlation_heatmap.png`
- `outputs/actual_vs_predicted.png`
- `outputs/residual_diagnostics.png`
- `outputs/feature_coefficients.png`
- `outputs/model_metrics_summary.png`
- `outputs/homework_infographic.png`
- `site/results.js`

## Reuse With Another Dataset

1. Copy `configs/california_housing.json`.
2. Update the dataset path or source URL.
3. Update the target, numeric features, and categorical features.
4. Choose a separate output directory and model filename.
5. Run tests, workflow execution, and the verifier.

## Validation And Quality Gates

- `python -m pytest` passes.
- `verify_outputs.py` exits with code 0.
- `site/results.js` status is `complete`.
- `site/results.js` metrics match `outputs/metrics.json`.
- Output files are real California Housing outputs, not 72-row smoke fixture outputs.
- Saved model loads as the expected pipeline.
- `git diff --check` passes.
- Fresh-session explicit and implicit Codex Skill activation are recorded as passed in `docs/SKILL_VALIDATION.md`.

## Scope And Limitations

This is an educational, reusable workflow demonstration. It is not AutoML. It does not prove causal relationships. Coefficients and correlations are model evidence only.

## Repository Structure

```text
.
|-- .agents/skills/tabular-regression-workflow/
|-- configs/
|-- docs/
|-- outputs/
|-- site/
|-- src/
|-- tests/
|-- AGENTS.md
|-- WORKFLOW.md
|-- index.html
|-- requirements.txt
`-- run_workflow.py
```
