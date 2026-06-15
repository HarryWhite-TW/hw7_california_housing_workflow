---
name: tabular-regression-workflow
description: Run or verify this repository's reusable CSV regression workflow when the user asks to analyze California Housing or another configured tabular regression dataset. Do not use for classification, time-series forecasting, image data, or unsupported arbitrary AutoML requests.
---

# Tabular Regression Workflow

Use the repository's existing workflow. Do not rewrite the analysis from scratch.

## Trigger conditions

Use this skill when the request involves:

- running the California Housing HW7 analysis;
- applying the configured regression workflow to a compatible CSV;
- regenerating metrics, charts, model artifacts, report, or GitHub Pages results;
- validating that the workflow works on another device or clean environment.

## Procedure

1. Read root `AGENTS.md`, `WORKFLOW.md`, and the selected file in `configs/`.
2. Confirm the CSV exists or that the configured source URL may be downloaded.
3. Confirm the target and configured feature columns are present.
4. Install only dependencies already declared in `requirements.txt`.
5. Run `python -m pytest` before changing behavior.
6. Run:

```powershell
python run_workflow.py --config configs/california_housing.json
```

7. Verify these outputs:

- `outputs/metrics.json`
- `outputs/dataset_summary.json`
- `outputs/predictions.csv`
- `outputs/feature_coefficients.csv`
- `outputs/california_housing_model.pkl`
- `outputs/workflow_report.md`
- `outputs/homework_infographic.png`
- `site/results.js`

8. Open or inspect the generated charts and verify they are non-empty and consistent with metrics.
9. Run `python -m pytest` again after modifications.
10. Report exact changed files, commands, test results, metrics, and unresolved limitations.

## Boundaries

- Do not silently change the target column.
- Do not infer that coefficients are causal effects.
- Do not add unrelated frameworks or services.
- Do not commit or push unless explicitly approved.
- When adapting to a new CSV, create a new config rather than overwriting the California Housing config.
