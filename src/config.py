from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WorkflowConfig:
    project_name: str
    dataset_name: str
    data_path: Path
    source_url: str
    target_column: str
    numeric_features: tuple[str, ...]
    categorical_features: tuple[str, ...]
    test_size: float
    random_state: int
    cv_folds: int
    output_dir: Path
    model_filename: str
    download_if_missing: bool
    publish_site_results: bool
    project_root: Path

    @property
    def all_features(self) -> tuple[str, ...]:
        return self.numeric_features + self.categorical_features

    @property
    def model_path(self) -> Path:
        return self.output_dir / self.model_filename


def _resolve_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return project_root / path


def load_config(config_path: str | Path, project_root: str | Path | None = None) -> WorkflowConfig:
    config_file = Path(config_path).resolve()
    root = Path(project_root).resolve() if project_root else Path(__file__).resolve().parents[1]
    raw: dict[str, Any] = json.loads(config_file.read_text(encoding="utf-8"))

    config = WorkflowConfig(
        project_name=str(raw["project_name"]),
        dataset_name=str(raw["dataset_name"]),
        data_path=_resolve_path(root, str(raw["data_path"])),
        source_url=str(raw.get("source_url", "")),
        target_column=str(raw["target_column"]),
        numeric_features=tuple(raw.get("numeric_features", [])),
        categorical_features=tuple(raw.get("categorical_features", [])),
        test_size=float(raw.get("test_size", 0.2)),
        random_state=int(raw.get("random_state", 42)),
        cv_folds=int(raw.get("cv_folds", 5)),
        output_dir=_resolve_path(root, str(raw.get("output_dir", "outputs"))),
        model_filename=str(raw.get("model_filename", "regression_model.pkl")),
        download_if_missing=bool(raw.get("download_if_missing", True)),
        publish_site_results=bool(raw.get("publish_site_results", True)),
        project_root=root,
    )
    validate_config(config)
    return config


def validate_config(config: WorkflowConfig) -> None:
    if not config.numeric_features and not config.categorical_features:
        raise ValueError("At least one feature must be configured.")
    if config.target_column in config.all_features:
        raise ValueError("The target column cannot also be a feature.")
    if len(set(config.all_features)) != len(config.all_features):
        raise ValueError("Feature names must be unique.")
    if not 0 < config.test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    if config.cv_folds < 2:
        raise ValueError("cv_folds must be at least 2.")
    if not config.model_filename.endswith(".pkl"):
        raise ValueError("model_filename must end with .pkl.")
