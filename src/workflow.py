from __future__ import annotations

from pathlib import Path

import joblib

from src.config import load_config
from src.data_io import build_dataset_summary, load_dataset
from src.modeling import train_and_evaluate
from src.reporting import write_json, write_report, write_site_results
from src.visualization import create_all_visuals


def run_workflow(config_path: str | Path, project_root: str | Path | None = None) -> dict:
    config = load_config(config_path, project_root=project_root)
    config.output_dir.mkdir(parents=True, exist_ok=True)

    frame = load_dataset(config)
    summary = build_dataset_summary(frame, config)
    result = train_and_evaluate(frame, config)

    joblib.dump(result["model"], config.model_path)
    result["predictions"].to_csv(config.output_dir / "predictions.csv", index=True)
    result["coefficients"].to_csv(config.output_dir / "feature_coefficients.csv", index=False)
    write_json(config.output_dir / "metrics.json", result["metrics"])
    write_json(config.output_dir / "dataset_summary.json", summary)

    visual_paths = create_all_visuals(
        frame=frame,
        predictions=result["predictions"],
        coefficients=result["coefficients"],
        metrics=result["metrics"],
        config=config,
    )
    report_path = write_report(
        config=config,
        summary=summary,
        metrics=result["metrics"],
        coefficients=result["coefficients"],
        visual_paths=visual_paths,
    )
    site_results_path = None
    if config.publish_site_results:
        site_results_path = write_site_results(config, summary, result["metrics"])

    return {
        "config": config,
        "summary": summary,
        "metrics": result["metrics"],
        "model_path": config.model_path,
        "report_path": report_path,
        "site_results_path": site_results_path,
        "visual_paths": visual_paths,
    }
