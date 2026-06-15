# Validation Record

## Baseline validation

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

The smoke run also generated non-empty model, JSON, CSV, Markdown, and seven PNG artifacts. These figures validate execution only. They are not the final California Housing results and must not be presented as such.

## Real-data validation still required

The sandbox used for baseline creation could not resolve `raw.githubusercontent.com`, so the teacher-provided full CSV could not be downloaded there.

Run the following on a machine that can reach the teacher-provided CSV URL, or first place the CSV at `data/housing.csv`:

```powershell
python run_workflow.py --config configs/california_housing.json
```

Completion requires real outputs in `outputs/` and updated real values in `site/results.js`.
