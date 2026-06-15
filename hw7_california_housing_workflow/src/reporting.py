from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import WorkflowConfig


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_report(
    config: WorkflowConfig,
    summary: dict,
    metrics: dict,
    coefficients: pd.DataFrame,
    visual_paths: list[Path],
) -> Path:
    top_rows = coefficients.head(10)
    coefficient_lines = "\n".join(
        f"- `{row.feature}`: coefficient `{row.coefficient:.4f}`"
        for row in top_rows.itertuples()
    )
    def display_path(path: Path) -> str:
        try:
            return path.relative_to(config.project_root).as_posix()
        except ValueError:
            return path.as_posix()

    visual_lines = "\n".join(f"- `{display_path(path)}`" for path in visual_paths)

    content = f"""# HW7 Workflow Report

## 1. Business Understanding

- Dataset: **{config.dataset_name}**
- Task: supervised regression
- Target: `{config.target_column}`
- Goal: demonstrate a reusable CRISP-DM workflow rather than claim causal housing research.

## 2. Data Understanding

- Rows: **{summary['rows']:,}**
- Columns: **{summary['columns']}**
- Configured features: **{summary['feature_count']}**
- Numerical features: `{', '.join(config.numeric_features)}`
- Categorical features: `{', '.join(config.categorical_features)}`
- Total missing cells: **{sum(summary['missing_values'].values()):,}**

## 3. Data Preparation

- Numerical missing values: median imputation
- Categorical missing values: most-frequent imputation
- Categorical encoding: OneHotEncoder with unknown-category handling
- Train/test split: `{1 - config.test_size:.0%}` / `{config.test_size:.0%}`
- Random state: `{config.random_state}`

## 4. Modeling

- Model: `LinearRegression`
- Structure: scikit-learn `Pipeline` + `ColumnTransformer`
- Saved artifact: `{display_path(config.model_path)}`

## 5. Evaluation

| Metric | Result |
|---|---:|
| Test R² | {metrics['r2']:.4f} |
| Test MAE | {metrics['mae']:,.2f} |
| Test RMSE | {metrics['rmse']:,.2f} |
| CV R² mean | {metrics['cv_r2_mean']:.4f} |
| CV R² std | {metrics['cv_r2_std']:.4f} |
| CV RMSE mean | {metrics['cv_rmse_mean']:,.2f} |
| CV RMSE std | {metrics['cv_rmse_std']:,.2f} |

### Largest coefficients

{coefficient_lines}

Coefficients are model parameters and should not automatically be interpreted as causal importance.

## 6. Deployment / Reuse

The saved pipeline includes preprocessing and regression. A compatible row can be passed to the model without manually repeating encoding or imputation.

## Generated visuals

{visual_lines}

## Reproducibility

```powershell
python run_workflow.py --config configs/california_housing.json
```
"""
    path = config.output_dir / "workflow_report.md"
    path.write_text(content, encoding="utf-8")
    return path


def write_site_results(config: WorkflowConfig, summary: dict, metrics: dict) -> Path:
    payload = {
        "status": "complete",
        "project_name": config.project_name,
        "dataset_name": config.dataset_name,
        "target_column": config.target_column,
        "rows": summary["rows"],
        "columns": summary["columns"],
        "features": summary["feature_count"],
        "metrics": metrics,
    }
    site_dir = config.project_root / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    path = site_dir / "results.js"
    content = "window.HW7_RESULTS = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n"
    path.write_text(content, encoding="utf-8")
    return path
