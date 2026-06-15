# HW7 California Housing Reusable Regression Workflow

> **Workflow first. Skill second. Reproducibility throughout.**

Planned GitHub Pages URL after repository creation:

```text
https://harrywhite-tw.github.io/hw7_california_housing_workflow/
```

## 專案定位

HW6 完成了一次 50 Startups CRISP-DM 分析；HW7 將其中可重複的部分抽離成設定檔驅動的 Workflow，再使用老師提供的 California Housing CSV 驗證它能在另一份資料上產生同類型成果。

這不是任意資料都能自動處理的 AutoML。它是一套範圍清楚、可解釋、可測試的**表格型迴歸 Workflow**。

## Core deliverables

- California Housing regression configuration
- Automatic CSV download when local data is absent
- Schema validation
- Numerical median imputation
- Categorical most-frequent imputation
- One-hot encoding
- scikit-learn Pipeline + ColumnTransformer
- Multiple linear regression
- Train/test R², MAE, RMSE
- K-fold CV R² and RMSE
- Saved preprocessing + model pipeline
- Predictions, residuals, and coefficient table
- Seven PNG visual artifacts
- CRISP-DM Markdown report
- Static GitHub Pages showcase
- Automated smoke test
- Lightweight Codex repository Skill

## Repository structure

```text
.
├── .agents/skills/tabular-regression-workflow/SKILL.md
├── configs/
├── data/
├── docs/
├── outputs/
├── site/
├── src/
├── tests/
├── AGENTS.md
├── WORKFLOW.md
├── index.html
├── requirements.txt
└── run_workflow.py
```

## Quick start

### 1. 建立虛擬環境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 安裝依賴

```powershell
python -m pip install -r requirements.txt
```

### 3. 執行測試

```powershell
python -m pytest
```

### 4. 執行 California Housing Workflow

```powershell
python run_workflow.py --config configs/california_housing.json
```

也可以在 Windows 雙擊：

```text
run_hw7.bat
```

如果 `data/housing.csv` 不存在，主設定會從老師提供的公開網址下載資料。

## Generated outputs

成功執行後，`outputs/` 將包含：

- `metrics.json`
- `dataset_summary.json`
- `predictions.csv`
- `feature_coefficients.csv`
- `california_housing_model.pkl`
- `workflow_report.md`
- `dataset_overview_dashboard.png`
- `correlation_heatmap.png`
- `actual_vs_predicted.png`
- `residual_diagnostics.png`
- `feature_coefficients.png`
- `model_metrics_summary.png`
- `homework_infographic.png`

`site/results.js` 也會更新為真實資料與模型結果，供 `index.html` 顯示。

## Workflow and Skill

- [`WORKFLOW.md`](WORKFLOW.md) 是任何使用者或裝置可遵循的主要流程。
- [`.agents/skills/tabular-regression-workflow/SKILL.md`](.agents/skills/tabular-regression-workflow/SKILL.md) 是給 Codex 的輕量使用說明。
- Skill 不包含第二套模型邏輯；它只負責正確呼叫與驗證 Workflow。

## Documents

- [Approved implementation plan](docs/HW7_IMPLEMENTATION_PLAN.md)
- [Design notes](docs/DESIGN.md)
- [Codex finalization task packet](docs/CODEX_TASK_PACKET.md)
- [Validation record](docs/VALIDATION.md)
- [GitHub setup](docs/GITHUB_SETUP.md)

## Interpretation boundary

This is an educational workflow demonstration. Model coefficients and correlations do not prove causal effects on housing prices.
