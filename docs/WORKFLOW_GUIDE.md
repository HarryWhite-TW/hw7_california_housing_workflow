# Reusable Tabular Regression Workflow Guide

## 1. Executive Summary

This repository turns one homework analysis into a reusable, configuration-driven tabular regression workflow. The verified baseline uses the California Housing dataset and produces metrics, model artifacts, charts, a Markdown report, and GitHub Pages data.

## 2. Problem Statement

Given a CSV, a continuous target column, and explicit feature lists, train and evaluate a reproducible linear regression pipeline while publishing the artifacts needed to inspect the result.

## 3. Scope

Supported:

- tabular CSV regression;
- numerical and categorical features;
- deterministic train/test and K-fold evaluation;
- static report and dashboard artifacts.

Not supported:

- classification;
- forecasting;
- image, audio, or text modeling;
- AutoML;
- causal claims.

## 4. Inputs Contract

The workflow requires one JSON config and one CSV source. The CSV can exist locally or be downloaded from the configured source URL when `download_if_missing` is true.

## 5. Config Schema

The config defines:

- project and dataset names;
- data path and optional source URL;
- target column;
- numeric feature list;
- categorical feature list;
- split and cross-validation settings;
- output directory;
- model filename;
- site publication flag.

## 6. Repository Architecture

```text
config -> data_io -> modeling -> visualization/reporting -> outputs/site
```

`run_workflow.py` is the human and Codex entry point. `src/workflow.py` orchestrates loading, validation, training, artifact writing, and site data generation.

## 7. Processing Stages

```text
CSV or source URL
  -> schema validation
  -> dataset summary
  -> median numeric imputation
  -> most-frequent categorical imputation
  -> one-hot encoding
  -> train/test split
  -> LinearRegression pipeline
  -> test and CV metrics
  -> model, CSV, JSON, PNG, report, site data
```

## 8. CRISP-DM Mapping

- Business understanding: define the homework and regression goal.
- Data understanding: summarize rows, columns, missingness, target distribution.
- Data preparation: impute and encode inside a saved pipeline.
- Modeling: fit `LinearRegression`.
- Evaluation: calculate R2, MAE, RMSE, and CV stability.
- Deployment: publish static artifacts and GitHub Pages data.

## 9. Preprocessing Design

Numerical columns use median imputation. Categorical columns use most-frequent imputation followed by one-hot encoding with `drop="first"` and `handle_unknown="ignore"`. The full preprocessing graph is stored in the model artifact.

## 10. Model Design

The model is intentionally simple: `LinearRegression` inside a scikit-learn `Pipeline`. This keeps the workflow beginner-readable and reproducible.

## 11. Evaluation

The workflow reports test R2, MAE, RMSE, 5-fold CV R2, and 5-fold CV RMSE. California Housing baseline metrics are stored in `outputs/metrics.json` and mirrored in `site/results.js`.

## 12. Artifact Generation

Generated artifacts include JSON summaries, predictions, coefficients, a joblib model, seven PNG visuals, a Markdown report, and static site data.

## 13. Static Site Publication

The site is plain HTML, CSS, and JavaScript. It reads `site/results.js` and local images under `outputs/`. It does not require React, Vite, Streamlit, or a backend.

## 14. Human Execution

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe run_workflow.py --config configs\california_housing.json
```

## 15. Codex Execution

Codex should use `.agents/skills/tabular-regression-workflow/SKILL.md`, run the same commands, and then run the verifier:

```powershell
.\.venv\Scripts\python.exe .agents\skills\tabular-regression-workflow\scripts\verify_outputs.py --config configs\california_housing.json
```

## 16. Reuse With Another CSV

Copy the config, update dataset-specific fields, choose a separate output directory and model filename, run the workflow, and verify. Keep the California Housing baseline intact.

## 17. Quality Gates

- Unit and smoke tests pass.
- Output verifier passes.
- `site/results.js` reports `complete`.
- Metrics match between output JSON and site data.
- Model artifact loads as the expected pipeline.

## 18. Failure Modes

Common failures include missing CSV files, schema mismatch, incompatible Python environments, missing generated outputs, and site data that still reflects smoke or stale metrics.

## 19. Reproducibility

Random state and CV folds are configured. The saved model contains preprocessing and regression steps so inference uses the same transformations.

## 20. Security And Privacy

Only use datasets the user is allowed to process. Do not upload local data. Do not add external services. Treat generated artifacts as local repository files.

## 21. Known Limitations

The workflow is educational and linear. Metrics describe predictive performance, not causality. Coefficients are model parameters, not proof of real-world causes.

## 22. Completion Criteria

The workflow is complete when tests pass, real outputs exist, the verifier exits with code 0, documentation links are current, and no unapproved commit or push was made.
