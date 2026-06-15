# Reusable California Housing Workflow

## Purpose

HW6 demonstrated one completed 50 Startups CRISP-DM project. HW7 extracts the repeatable method into a configuration-driven workflow, then validates it with the California Housing dataset.

## Workflow contract

### Inputs

- One CSV file
- One JSON configuration
- A continuous target column
- Explicit numerical and categorical feature lists

### Processing

```text
CSV / source URL
→ schema validation
→ data understanding summary
→ median imputation for numerical features
→ most-frequent imputation for categorical features
→ one-hot encoding
→ train/test split
→ LinearRegression pipeline
→ test metrics and K-fold cross-validation
→ model, tables, charts, report, and site data
```

### Outputs

- Reusable serialized preprocessing + model pipeline
- R², MAE, RMSE, cross-validation statistics
- Predictions and residuals
- Model coefficient table
- Dataset summary
- Seven visual artifacts including an all-in-one infographic
- Markdown workflow report
- Static GitHub Pages data

## Main execution

```powershell
python run_workflow.py --config configs/california_housing.json
```

When `data/housing.csv` is missing, the workflow downloads the configured source automatically.

## Reuse with another regression dataset

1. Copy `configs/california_housing.json`.
2. Change dataset path or URL.
3. Change the target, numerical features, and categorical features.
4. Choose a separate output directory and model filename.
5. Run the same entry point with the new config.

This bounded design supports compatible tabular regression tasks. It is intentionally not a general-purpose AutoML system.
