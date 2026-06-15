# HW7 Workflow Report

## 1. Business Understanding

- Dataset: **California Housing**
- Task: supervised regression
- Target: `median_house_value`
- Goal: demonstrate a reusable CRISP-DM workflow rather than claim causal housing research.

## 2. Data Understanding

- Rows: **20,640**
- Columns: **10**
- Configured features: **9**
- Numerical features: `longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income`
- Categorical features: `ocean_proximity`
- Total missing cells: **207**

## 3. Data Preparation

- Numerical missing values: median imputation
- Categorical missing values: most-frequent imputation
- Categorical encoding: OneHotEncoder with unknown-category handling
- Train/test split: `80%` / `20%`
- Random state: `42`

## 4. Modeling

- Model: `LinearRegression`
- Structure: scikit-learn `Pipeline` + `ColumnTransformer`
- Saved artifact: `outputs/california_housing_model.pkl`

## 5. Evaluation

| Metric | Result |
|---|---:|
| Test R² | 0.6254 |
| Test MAE | 50,670.49 |
| Test RMSE | 70,059.19 |
| CV R² mean | 0.6433 |
| CV R² std | 0.0201 |
| CV RMSE mean | 68,881.18 |
| CV RMSE std | 1,988.10 |

### Largest coefficients

- `ocean_proximity_ISLAND`: coefficient `156065.7198`
- `ocean_proximity_INLAND`: coefficient `-39766.3987`
- `median_income`: coefficient `38760.4474`
- `longitude`: coefficient `-26430.4447`
- `latitude`: coefficient `-25173.2798`
- `ocean_proximity_NEAR OCEAN`: coefficient `4758.7536`
- `ocean_proximity_NEAR BAY`: coefficient `-3697.4017`
- `housing_median_age`: coefficient `1057.8161`
- `households`: coefficient `77.8044`
- `total_bedrooms`: coefficient `71.3449`

Coefficients are model parameters and should not automatically be interpreted as causal importance.

## 6. Deployment / Reuse

The saved pipeline includes preprocessing and regression. A compatible row can be passed to the model without manually repeating encoding or imputation.

## Generated visuals

- `outputs/dataset_overview_dashboard.png`
- `outputs/correlation_heatmap.png`
- `outputs/actual_vs_predicted.png`
- `outputs/residual_diagnostics.png`
- `outputs/feature_coefficients.png`
- `outputs/model_metrics_summary.png`
- `outputs/homework_infographic.png`

## Reproducibility

```powershell
python run_workflow.py --config configs/california_housing.json
```
