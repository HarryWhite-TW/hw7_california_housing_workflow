from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.config import WorkflowConfig


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)


def create_dataset_overview(frame: pd.DataFrame, config: WorkflowConfig, output_dir: Path) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    target = config.target_column

    axes[0, 0].hist(frame[target], bins=30)
    axes[0, 0].set_title(f"Target Distribution: {target}")
    axes[0, 0].set_xlabel(target)
    axes[0, 0].set_ylabel("Count")

    missing = frame[list(config.all_features)].isna().sum()
    axes[0, 1].barh(missing.index, missing.values)
    axes[0, 1].set_title("Missing Values by Feature")
    axes[0, 1].set_xlabel("Missing rows")

    if config.categorical_features:
        category = config.categorical_features[0]
        counts = frame[category].fillna("<missing>").value_counts()
        axes[1, 0].bar(counts.index.astype(str), counts.values)
        axes[1, 0].tick_params(axis="x", rotation=25)
        axes[1, 0].set_title(f"Category Counts: {category}")
        axes[1, 0].set_ylabel("Rows")
    else:
        axes[1, 0].axis("off")

    axes[1, 1].axis("off")
    summary_text = "\n".join(
        [
            f"Dataset: {config.dataset_name}",
            f"Rows: {len(frame):,}",
            f"Columns: {frame.shape[1]}",
            f"Configured features: {len(config.all_features)}",
            f"Target mean: {frame[target].mean():,.2f}",
            f"Target median: {frame[target].median():,.2f}",
            f"Total missing cells: {int(frame.isna().sum().sum()):,}",
        ]
    )
    axes[1, 1].text(0.05, 0.95, summary_text, va="top", fontsize=14, linespacing=1.6)
    axes[1, 1].set_title("Dataset Summary")

    fig.suptitle("California Housing — Dataset Overview", fontsize=18)
    path = output_dir / "dataset_overview_dashboard.png"
    _save(fig, path)
    return path


def create_correlation_heatmap(frame: pd.DataFrame, config: WorkflowConfig, output_dir: Path) -> Path:
    columns = list(config.numeric_features) + [config.target_column]
    corr = frame[columns].corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(11, 9))
    image = ax.imshow(corr, aspect="auto", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.index)), corr.index)
    ax.set_title("Numerical Feature Correlation Heatmap")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    for row in range(len(corr.index)):
        for column in range(len(corr.columns)):
            ax.text(column, row, f"{corr.iloc[row, column]:.2f}", ha="center", va="center", fontsize=8)

    path = output_dir / "correlation_heatmap.png"
    _save(fig, path)
    return path


def create_prediction_plot(predictions: pd.DataFrame, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.scatter(predictions["actual"], predictions["predicted"], alpha=0.65)
    lower = min(predictions["actual"].min(), predictions["predicted"].min())
    upper = max(predictions["actual"].max(), predictions["predicted"].max())
    ax.plot([lower, upper], [lower, upper], linestyle="--")
    ax.set_xlabel("Actual value")
    ax.set_ylabel("Predicted value")
    ax.set_title("Actual vs Predicted House Values")
    ax.grid(alpha=0.25)
    path = output_dir / "actual_vs_predicted.png"
    _save(fig, path)
    return path


def create_residual_plot(predictions: pd.DataFrame, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(predictions["predicted"], predictions["residual"], alpha=0.65)
    ax.axhline(0, linestyle="--")
    ax.set_xlabel("Predicted value")
    ax.set_ylabel("Residual")
    ax.set_title("Residual Diagnostics")
    ax.grid(alpha=0.25)
    path = output_dir / "residual_diagnostics.png"
    _save(fig, path)
    return path


def create_coefficient_plot(coefficients: pd.DataFrame, output_dir: Path) -> Path:
    top = coefficients.head(14).sort_values("absolute_coefficient")
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top["feature"], top["coefficient"])
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("Linear regression coefficient")
    ax.set_title("Largest Model Coefficients")
    path = output_dir / "feature_coefficients.png"
    _save(fig, path)
    return path


def create_metrics_summary(metrics: dict, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis("off")
    cards = [
        ("Test R²", f"{metrics['r2']:.4f}"),
        ("MAE", f"{metrics['mae']:,.2f}"),
        ("RMSE", f"{metrics['rmse']:,.2f}"),
        ("CV R² mean", f"{metrics['cv_r2_mean']:.4f}"),
        ("CV RMSE mean", f"{metrics['cv_rmse_mean']:,.2f}"),
        ("Train / Test", f"{metrics['train_rows']} / {metrics['test_rows']}"),
    ]

    for index, (label, value) in enumerate(cards):
        row, column = divmod(index, 3)
        x = 0.04 + column * 0.32
        y = 0.72 - row * 0.42
        ax.text(x, y, label, fontsize=12, transform=ax.transAxes)
        ax.text(x, y - 0.12, value, fontsize=22, weight="bold", transform=ax.transAxes)

    ax.set_title("Linear Regression Model Metrics", fontsize=18, pad=20)
    path = output_dir / "model_metrics_summary.png"
    _save(fig, path)
    return path


def create_infographic(
    frame: pd.DataFrame,
    predictions: pd.DataFrame,
    coefficients: pd.DataFrame,
    metrics: dict,
    config: WorkflowConfig,
    output_dir: Path,
) -> Path:
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    target = config.target_column

    axes[0, 0].hist(frame[target], bins=28)
    axes[0, 0].set_title("Target Distribution")
    axes[0, 0].set_xlabel(target)

    missing = frame[list(config.all_features)].isna().sum()
    axes[0, 1].barh(missing.index, missing.values)
    axes[0, 1].set_title("Missing Values")

    axes[0, 2].scatter(predictions["actual"], predictions["predicted"], alpha=0.6)
    low = min(predictions["actual"].min(), predictions["predicted"].min())
    high = max(predictions["actual"].max(), predictions["predicted"].max())
    axes[0, 2].plot([low, high], [low, high], linestyle="--")
    axes[0, 2].set_title("Actual vs Predicted")
    axes[0, 2].set_xlabel("Actual")
    axes[0, 2].set_ylabel("Predicted")

    axes[1, 0].scatter(predictions["predicted"], predictions["residual"], alpha=0.6)
    axes[1, 0].axhline(0, linestyle="--")
    axes[1, 0].set_title("Residual Diagnostics")
    axes[1, 0].set_xlabel("Predicted")
    axes[1, 0].set_ylabel("Residual")

    top = coefficients.head(8).sort_values("absolute_coefficient")
    axes[1, 1].barh(top["feature"], top["coefficient"])
    axes[1, 1].axvline(0, linewidth=1)
    axes[1, 1].set_title("Largest Coefficients")

    axes[1, 2].axis("off")
    metrics_text = "\n".join(
        [
            f"Rows: {len(frame):,}",
            f"Features: {len(config.all_features)}",
            "",
            f"Test R²: {metrics['r2']:.4f}",
            f"MAE: {metrics['mae']:,.2f}",
            f"RMSE: {metrics['rmse']:,.2f}",
            "",
            f"CV R² mean: {metrics['cv_r2_mean']:.4f}",
            f"CV R² std: {metrics['cv_r2_std']:.4f}",
            f"CV RMSE mean: {metrics['cv_rmse_mean']:,.2f}",
        ]
    )
    axes[1, 2].text(0.05, 0.95, metrics_text, va="top", fontsize=14, linespacing=1.5)
    axes[1, 2].set_title("Workflow Results")

    fig.suptitle("HW7 California Housing CRISP-DM Workflow Infographic", fontsize=21)
    path = output_dir / "homework_infographic.png"
    _save(fig, path)
    return path


def create_all_visuals(
    frame: pd.DataFrame,
    predictions: pd.DataFrame,
    coefficients: pd.DataFrame,
    metrics: dict,
    config: WorkflowConfig,
) -> list[Path]:
    cache_dir = config.output_dir / "matplotlib_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
    config.output_dir.mkdir(parents=True, exist_ok=True)

    return [
        create_dataset_overview(frame, config, config.output_dir),
        create_correlation_heatmap(frame, config, config.output_dir),
        create_prediction_plot(predictions, config.output_dir),
        create_residual_plot(predictions, config.output_dir),
        create_coefficient_plot(coefficients, config.output_dir),
        create_metrics_summary(metrics, config.output_dir),
        create_infographic(frame, predictions, coefficients, metrics, config, config.output_dir),
    ]
