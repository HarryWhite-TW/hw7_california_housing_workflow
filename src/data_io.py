from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

from src.config import WorkflowConfig


def ensure_dataset(config: WorkflowConfig) -> Path:
    if config.data_path.exists():
        return config.data_path

    if not config.download_if_missing:
        raise FileNotFoundError(f"Dataset not found: {config.data_path}")
    if not config.source_url:
        raise FileNotFoundError("Dataset is missing and source_url is empty.")

    config.data_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(config.source_url, headers={"User-Agent": "hw7-regression-workflow/1.0"})

    with urlopen(request, timeout=60) as response:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            shutil.copyfileobj(response, temp_file)
            temp_path = Path(temp_file.name)

    temp_path.replace(config.data_path)
    return config.data_path


def load_dataset(config: WorkflowConfig) -> pd.DataFrame:
    path = ensure_dataset(config)
    frame = pd.read_csv(path)
    validate_dataset(frame, config)
    return frame


def validate_dataset(frame: pd.DataFrame, config: WorkflowConfig) -> None:
    required = list(config.all_features) + [config.target_column]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if frame.empty:
        raise ValueError("Dataset is empty.")
    if frame[config.target_column].isna().any():
        raise ValueError("Target column contains missing values.")
    if len(frame) < max(12, config.cv_folds * 2):
        raise ValueError("Dataset is too small for the configured evaluation workflow.")


def build_dataset_summary(frame: pd.DataFrame, config: WorkflowConfig) -> dict:
    return {
        "dataset_name": config.dataset_name,
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "feature_count": len(config.all_features),
        "target_column": config.target_column,
        "numeric_features": list(config.numeric_features),
        "categorical_features": list(config.categorical_features),
        "missing_values": {column: int(value) for column, value in frame.isna().sum().items()},
        "target_min": float(frame[config.target_column].min()),
        "target_max": float(frame[config.target_column].max()),
        "target_mean": float(frame[config.target_column].mean()),
        "target_median": float(frame[config.target_column].median()),
    }
