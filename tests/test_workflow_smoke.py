import json
from pathlib import Path

from src.workflow import run_workflow


def test_workflow_generates_required_artifacts(tmp_path):
    root = Path(__file__).resolve().parents[1]
    base = json.loads((root / "configs" / "smoke_test.json").read_text(encoding="utf-8"))
    base["data_path"] = str(root / "tests" / "fixtures" / "california_housing_sample.csv")
    base["output_dir"] = str(tmp_path / "outputs")
    base["model_filename"] = "smoke_model.pkl"

    config_path = tmp_path / "smoke_config.json"
    config_path.write_text(json.dumps(base), encoding="utf-8")

    result = run_workflow(config_path, project_root=root)
    output_dir = tmp_path / "outputs"

    assert result["summary"]["rows"] >= 40
    assert result["model_path"].exists()
    assert (output_dir / "metrics.json").exists()
    assert (output_dir / "workflow_report.md").exists()
    assert (output_dir / "homework_infographic.png").exists()
    assert (output_dir / "actual_vs_predicted.png").exists()
    assert set(result["metrics"]) >= {"r2", "mae", "rmse", "cv_r2_mean"}
