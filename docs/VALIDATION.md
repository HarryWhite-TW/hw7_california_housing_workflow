# Validation Record

## Baseline Sandbox Smoke Validation

Date: 2026-06-15

The repository baseline was validated inside ChatGPT's isolated Linux/Python sandbox with the deterministic offline fixture at:

```text
tests/fixtures/california_housing_sample.csv
```

Commands:

```powershell
python -m pytest
python run_workflow.py --config configs/smoke_test.json
python -m py_compile run_workflow.py src\config.py src\data_io.py src\modeling.py src\reporting.py src\visualization.py src\workflow.py
```

Latest observed smoke-workflow result:

```text
Tests: 2 passed
Rows: 72
Test R2: 0.9957
Test MAE: 4,276.66
Test RMSE: 4,837.41
3-fold CV mean R2: 0.9951
```

The smoke run generated non-empty model, JSON, CSV, Markdown, and seven PNG artifacts. These figures validate execution only. They are not the final California Housing results and must not be presented as such.

## Windows Local Real-Data Validation

Date: 2026-06-15

Python 3.12.10 was installed from the official Python.org 64-bit installer:

```text
https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
```

Authenticode verification:

```text
Status: Valid
StatusMessage: 簽章已驗證。
Signer: CN=Python Software Foundation, O=Python Software Foundation, L=Beaverton, S=Oregon, C=US
```

Python paths:

```text
Installed Python: C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe
Virtual environment Python: C:\Users\admin\Desktop\hw7_california_housing_workflow\.venv\Scripts\python.exe
Virtual environment version: Python 3.12.10
```

Setup and validation commands:

```powershell
$installer = Join-Path $env:TEMP "python-3.12.10-amd64.exe"
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe" -OutFile $installer
$signature = Get-AuthenticodeSignature $installer
$targetDir = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312"
Start-Process -FilePath $installer -ArgumentList @("/quiet", "InstallAllUsers=0", "TargetDir=$targetDir", "PrependPath=0", "Include_launcher=0", "Include_pip=1", "Include_test=0", "Shortcuts=0") -Wait -PassThru
& "$targetDir\python.exe" --version
& "$targetDir\python.exe" -m pip --version
& "$targetDir\python.exe" -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe run_workflow.py --config configs\california_housing.json
.\.venv\Scripts\python.exe -m pytest
```

Requirements installation result:

```text
pip upgraded from 25.0.1 to 26.1.2.
requirements.txt installed successfully.
```

Initial pytest result after the local Windows temp-directory fix:

```text
2 passed in 3.72s
```

Final pytest result after documentation updates:

```text
2 passed in 3.68s
```

Real workflow result:

```text
HW7 workflow completed successfully
Dataset rows: 20,640
Test R2: 0.6254
Test MAE: 50,670.49
Test RMSE: 70,059.19
CV R2 mean: 0.6433
```

Real dataset shape:

```text
Rows: 20,640
Columns: 10
Configured features: 9
Target column: median_house_value
Categorical feature: ocean_proximity
```

Model metrics from `outputs/metrics.json`:

```text
R2: 0.6254382675296286
MAE: 50670.48923565587
RMSE: 70059.19333924996
CV R2 mean: 0.6432846133282536
CV R2 std: 0.0200522297447311
CV RMSE mean: 68881.17625531893
CV RMSE std: 1988.1036723885318
Train rows: 16,512
Test rows: 4,128
CV folds: 5
```

Verified output files:

```text
outputs/actual_vs_predicted.png
outputs/california_housing_model.pkl
outputs/correlation_heatmap.png
outputs/dataset_overview_dashboard.png
outputs/dataset_summary.json
outputs/feature_coefficients.csv
outputs/feature_coefficients.png
outputs/homework_infographic.png
outputs/metrics.json
outputs/model_metrics_summary.png
outputs/predictions.csv
outputs/residual_diagnostics.png
outputs/workflow_report.md
site/results.js
```

Additional verification:

- `site/results.js` has `status: complete`.
- `site/results.js` metrics exactly match `outputs/metrics.json`.
- `outputs/dataset_summary.json` records the full California Housing dataset, not the 72-row smoke fixture.
- Every required PNG is non-empty, readable by `matplotlib.image.imread`, and has normal dimensions.
- Every local file referenced by `index.html` exists.
- `outputs/california_housing_model.pkl` loads with `joblib`.
- The saved model is a scikit-learn `Pipeline` with steps `preprocessor` and `regressor`.
- The `preprocessor` step is a `ColumnTransformer`.
- The regression step is `LinearRegression`.
- The workflow report explicitly states that coefficients should not automatically be interpreted as causal importance.

## Local Compatibility Fix

On this Windows environment, pytest could not create temporary directories under:

```text
C:\Users\admin\AppData\Local\Temp\pytest-of-admin
```

The project was updated so `python -m pytest` uses a repository-local ignored temp directory:

```ini
addopts = -q --basetemp=.pytest-tmp -p no:cacheprovider
```

This change does not remove, skip, or lower any tests. It only avoids an environment-specific temp-directory permission failure.

## Known Limitations

- The GitHub Pages URL is linked as the intended dashboard location, but this validation did not enable Pages or verify a deployed public site.
- The model is a linear regression workflow demonstration. Coefficients and correlations are not causal evidence.
- `data/housing.csv` is intentionally ignored by Git because it is downloaded/generated input data.
