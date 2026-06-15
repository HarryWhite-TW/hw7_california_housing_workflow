from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

import joblib
from PIL import Image
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


REQUIRED_METRICS = {
    "r2",
    "mae",
    "rmse",
    "cv_r2_mean",
    "cv_r2_std",
    "cv_rmse_mean",
    "cv_rmse_std",
    "train_rows",
    "test_rows",
    "cv_folds",
}

REQUIRED_PNGS = [
    "dataset_overview_dashboard.png",
    "correlation_heatmap.png",
    "actual_vs_predicted.png",
    "residual_diagnostics.png",
    "feature_coefficients.png",
    "model_metrics_summary.png",
    "homework_infographic.png",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify generated outputs for the repository tabular regression workflow."
    )
    parser.add_argument("--config", default="configs/california_housing.json")
    return parser.parse_args()


def fail(message: str) -> None:
    raise AssertionError(message)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Missing required JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def read_site_results(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Missing site results file: {path}")
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.HW7_RESULTS\s*=\s*(\{.*\})\s*;", text, re.S)
    if not match:
        fail("site/results.js does not assign window.HW7_RESULTS")
    return json.loads(match.group(1))


def assert_close(left: float, right: float, name: str, tolerance: float = 1e-9) -> None:
    if abs(float(left) - float(right)) > tolerance:
        fail(f"{name} mismatch: {left!r} != {right!r}")


def assert_csv_columns(path: Path, columns: set[str]) -> int:
    if not path.exists():
        fail(f"Missing required CSV file: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            fail(f"CSV has no header: {path}")
        missing = columns.difference(reader.fieldnames)
        if missing:
            fail(f"{path} missing columns: {sorted(missing)}")
        return sum(1 for _ in reader)


def verify_png(path: Path) -> None:
    if not path.exists():
        fail(f"Missing PNG file: {path}")
    if path.stat().st_size <= 0:
        fail(f"PNG file is empty: {path}")
    with Image.open(path) as image:
        image.verify()


def verify() -> list[str]:
    args = parse_args()
    root = Path(__file__).resolve().parents[4]
    config_path = resolve_path(root, args.config)
    config = read_json(config_path)

    output_dir = resolve_path(root, str(config.get("output_dir", "outputs")))
    model_path = output_dir / str(config.get("model_filename", "regression_model.pkl"))
    metrics_path = output_dir / "metrics.json"
    summary_path = output_dir / "dataset_summary.json"
    predictions_path = output_dir / "predictions.csv"
    coefficients_path = output_dir / "feature_coefficients.csv"
    report_path = output_dir / "workflow_report.md"
    site_results_path = root / "site" / "results.js"

    metrics = read_json(metrics_path)
    summary = read_json(summary_path)
    site = read_site_results(site_results_path)

    missing_metrics = REQUIRED_METRICS.difference(metrics)
    if missing_metrics:
        fail(f"metrics.json missing keys: {sorted(missing_metrics)}")
    for key in REQUIRED_METRICS:
        if not isinstance(metrics[key], (int, float)):
            fail(f"Metric {key} must be numeric")

    expected_features = list(config.get("numeric_features", [])) + list(
        config.get("categorical_features", [])
    )
    if summary.get("dataset_name") != config.get("dataset_name"):
        fail("dataset_summary.json dataset name does not match config")
    if summary.get("target_column") != config.get("target_column"):
        fail("dataset_summary.json target column does not match config")
    if summary.get("feature_count") != len(expected_features):
        fail("dataset_summary.json feature_count does not match config")
    if summary.get("numeric_features") != config.get("numeric_features"):
        fail("dataset_summary.json numeric_features do not match config")
    if summary.get("categorical_features") != config.get("categorical_features"):
        fail("dataset_summary.json categorical_features do not match config")

    if site.get("status") != "complete":
        fail("site/results.js status is not complete")
    if site.get("rows") != summary.get("rows"):
        fail("site/results.js row count does not match dataset summary")
    if site.get("columns") != summary.get("columns"):
        fail("site/results.js column count does not match dataset summary")
    if site.get("features") != summary.get("feature_count"):
        fail("site/results.js feature count does not match dataset summary")
    for key, value in metrics.items():
        assert_close(site["metrics"][key], value, f"site metric {key}")

    if summary.get("rows") == 72:
        fail("Outputs appear to be from the 72-row smoke fixture, not the real dataset")
    if config.get("dataset_name") == "California Housing":
        if summary.get("rows") != 20640 or summary.get("columns") != 10:
            fail("California Housing baseline must have 20,640 rows and 10 columns")

    prediction_rows = assert_csv_columns(
        predictions_path, {"actual", "predicted", "residual"}
    )
    if prediction_rows != int(metrics["test_rows"]):
        fail("predictions.csv row count does not match metrics test_rows")
    coefficient_rows = assert_csv_columns(
        coefficients_path, {"feature", "coefficient", "absolute_coefficient"}
    )
    if coefficient_rows < len(expected_features):
        fail("feature_coefficients.csv has fewer rows than configured features")

    if not report_path.exists() or report_path.stat().st_size <= 0:
        fail(f"Missing or empty report: {report_path}")
    for filename in REQUIRED_PNGS:
        verify_png(output_dir / filename)

    if not model_path.exists():
        fail(f"Missing model file: {model_path}")
    model = joblib.load(model_path)
    if not isinstance(model, Pipeline):
        fail("Saved model is not a scikit-learn Pipeline")
    if "preprocessor" not in model.named_steps or "regressor" not in model.named_steps:
        fail("Saved pipeline must include preprocessor and regressor steps")
    if not isinstance(model.named_steps["preprocessor"], ColumnTransformer):
        fail("preprocessor step is not a ColumnTransformer")
    if not isinstance(model.named_steps["regressor"], LinearRegression):
        fail("regressor step is not LinearRegression")

    return [
        "Config loaded",
        "Required JSON, CSV, PNG, report, model, and site data are present",
        "Metrics and site data match",
        "Dataset summary matches config",
        "Outputs are real California Housing results, not the smoke fixture",
        "Saved model contract is valid",
    ]


def main() -> int:
    try:
        messages = verify()
    except Exception as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 1
    print("Validation summary:")
    for message in messages:
        print(f"- {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
