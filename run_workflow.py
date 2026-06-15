from __future__ import annotations

import argparse
from pathlib import Path

from src.workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the reusable HW7 tabular regression workflow."
    )
    parser.add_argument(
        "--config",
        default="configs/california_housing.json",
        help="Path to a workflow JSON configuration file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_workflow(Path(args.config))
    metrics = result["metrics"]

    print()
    print("HW7 workflow completed successfully")
    print(f"Dataset rows: {result['summary']['rows']:,}")
    print(f"Test R2: {metrics['r2']:.4f}")
    print(f"Test MAE: {metrics['mae']:,.2f}")
    print(f"Test RMSE: {metrics['rmse']:,.2f}")
    print(f"CV R2 mean: {metrics['cv_r2_mean']:.4f}")
    print(f"Model: {result['model_path']}")
    print(f"Report: {result['report_path']}")


if __name__ == "__main__":
    main()
