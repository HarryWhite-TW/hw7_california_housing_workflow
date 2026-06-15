# Tabular Regression Workflow Output Contract

## Purpose

This contract defines the artifacts that prove the configured regression workflow completed successfully. It is used by humans, tests, and Codex verification.

## Required Files

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

## JSON Requirements

`metrics.json` must contain numeric values for:

- `r2`
- `mae`
- `rmse`
- `cv_r2_mean`
- `cv_r2_std`
- `cv_rmse_mean`
- `cv_rmse_std`
- `train_rows`
- `test_rows`
- `cv_folds`

`dataset_summary.json` must contain:

- dataset name;
- row and column counts;
- feature count;
- target column;
- numerical and categorical feature lists;
- missing-value counts;
- target summary statistics.

## CSV Requirements

`predictions.csv` must include:

- `actual`
- `predicted`
- `residual`

`feature_coefficients.csv` must include:

- `feature`
- `coefficient`
- `absolute_coefficient`

## Model Requirements

The joblib artifact must load successfully and must be a scikit-learn `Pipeline` with:

- `preprocessor`
- `regressor`

The preprocessor must be a `ColumnTransformer`. The regressor must be `LinearRegression`.

## PNG Requirements

Each required PNG must exist, be non-empty, and be readable by the installed image stack.

## Site Data Requirements

`site/results.js` must set `window.HW7_RESULTS` with:

- `status: "complete"`;
- dataset metadata matching `dataset_summary.json`;
- metrics matching `metrics.json`.

## Smoke Versus Real Data

The smoke fixture has 72 rows and is used only for fast tests. The published California Housing baseline must have:

- 20,640 rows;
- 10 columns;
- 9 configured features.

## Completion Criteria

The workflow is complete when tests pass, the verifier exits with code 0, the site data reports `complete`, and generated metrics match the documented California Housing baseline unless code or dependency changes intentionally alter the model.
