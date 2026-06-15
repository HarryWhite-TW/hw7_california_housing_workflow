from pathlib import Path

from src.config import load_config


def test_california_config_has_expected_schema():
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "configs" / "california_housing.json", project_root=root)

    assert config.target_column == "median_house_value"
    assert "median_income" in config.numeric_features
    assert config.categorical_features == ("ocean_proximity",)
    assert len(config.all_features) == 9
