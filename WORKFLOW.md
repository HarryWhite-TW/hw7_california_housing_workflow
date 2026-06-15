# Canonical Workflow Specification

## Status

Version: HW7 baseline, validated for California Housing.

## Purpose

This workflow turns a configured tabular CSV regression problem into reproducible metrics, a saved preprocessing/model pipeline, visual artifacts, a Markdown report, and static GitHub Pages data.

## Supported Task Class

Supported: supervised tabular regression with explicit numerical and categorical feature lists and a continuous target column.

Not supported: classification, time-series forecasting, image/audio/text modeling, arbitrary AutoML, or causal inference.

## Input Contract

The workflow accepts:

- one JSON config under `configs/`;
- one CSV file or a configured source URL;
- one target column;
- zero or more numeric features;
- zero or more categorical features;
- at least one configured feature.

## Processing Contract

```text
CSV / source URL
  -> schema validation
  -> dataset summary
  -> train/test split
  -> numeric median imputation
  -> categorical most-frequent imputation
  -> one-hot encoding
  -> LinearRegression pipeline
  -> test and cross-validation metrics
  -> generated artifacts
```

## Output Contract

Required generated outputs:

- `outputs/metrics.json`
- `outputs/dataset_summary.json`
- `outputs/predictions.csv`
- `outputs/feature_coefficients.csv`
- `outputs/california_housing_model.pkl`
- `outputs/workflow_report.md`
- seven PNG artifacts under `outputs/`
- `site/results.js`

The detailed output contract lives at `.agents/skills/tabular-regression-workflow/references/output-contract.md`.

## Invariants

- Config values define dataset-specific behavior.
- `run_workflow.py` remains the main entry point.
- Preprocessing is saved with the model.
- Smoke fixture outputs must not be presented as real California Housing results.
- Coefficients and correlations are not causal evidence.

## Execution Command

```powershell
.\.venv\Scripts\python.exe run_workflow.py --config configs\california_housing.json
```

## Verification Command

```powershell
.\.venv\Scripts\python.exe .agents\skills\tabular-regression-workflow\scripts\verify_outputs.py --config configs\california_housing.json
```

## Adaptation Rules

To reuse the workflow with another compatible regression CSV:

1. Copy `configs/california_housing.json`.
2. Update dataset name, path or URL, target, feature lists, output directory, and model filename.
3. Run tests, workflow execution, and output verification.
4. Keep the California Housing baseline intact unless explicitly asked otherwise.

## Failure Behavior

Failures should stop the run with a clear error. Fix schema, config, dependency, or artifact issues before reporting completion.

## Acceptance Criteria

- `python -m pytest` passes.
- The workflow command completes.
- The verification command exits with code 0.
- `site/results.js` reports `status: "complete"`.
- GitHub Pages files are plain static HTML/CSS/JavaScript.
- No unapproved commit or push has occurred.

## References

- `docs/WORKFLOW_GUIDE.md`
- `docs/SKILL_GUIDE.md`
- `docs/SKILL_VALIDATION.md`
- `.agents/skills/tabular-regression-workflow/SKILL.md`
