from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.config import WorkflowConfig


def build_pipeline(config: WorkflowConfig) -> Pipeline:
    transformers: list[tuple] = []

    if config.numeric_features:
        numeric_pipeline = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median"))]
        )
        transformers.append(("numeric", numeric_pipeline, list(config.numeric_features)))

    if config.categorical_features:
        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "encoder",
                    OneHotEncoder(
                        drop="first",
                        handle_unknown="ignore",
                        sparse_output=False,
                    ),
                ),
            ]
        )
        transformers.append(
            ("categorical", categorical_pipeline, list(config.categorical_features))
        )

    preprocessor = ColumnTransformer(transformers=transformers)
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression()),
        ]
    )


def train_and_evaluate(frame: pd.DataFrame, config: WorkflowConfig) -> dict:
    X = frame[list(config.all_features)]
    y = frame[config.target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    model = build_pipeline(config)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    kfold = KFold(
        n_splits=config.cv_folds,
        shuffle=True,
        random_state=config.random_state,
    )
    cv_r2 = cross_val_score(model, X, y, cv=kfold, scoring="r2")
    cv_rmse = -cross_val_score(
        model,
        X,
        y,
        cv=kfold,
        scoring="neg_root_mean_squared_error",
    )

    metrics = {
        "r2": float(r2_score(y_test, y_pred)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "cv_r2_mean": float(cv_r2.mean()),
        "cv_r2_std": float(cv_r2.std()),
        "cv_rmse_mean": float(cv_rmse.mean()),
        "cv_rmse_std": float(cv_rmse.std()),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "cv_folds": int(config.cv_folds),
    }

    predictions = pd.DataFrame(
        {
            "actual": y_test.to_numpy(),
            "predicted": y_pred,
            "residual": y_test.to_numpy() - y_pred,
        },
        index=y_test.index,
    ).sort_index()

    final_model = build_pipeline(config)
    final_model.fit(X, y)
    coefficients = extract_coefficients(final_model)

    return {
        "model": final_model,
        "metrics": metrics,
        "predictions": predictions,
        "coefficients": coefficients,
    }


def extract_coefficients(model: Pipeline) -> pd.DataFrame:
    preprocessor = model.named_steps["preprocessor"]
    regressor = model.named_steps["regressor"]
    names = preprocessor.get_feature_names_out()
    coefficients = np.asarray(regressor.coef_).reshape(-1)

    frame = pd.DataFrame(
        {
            "feature": [name.replace("numeric__", "").replace("categorical__", "") for name in names],
            "coefficient": coefficients,
        }
    )
    frame["absolute_coefficient"] = frame["coefficient"].abs()
    return frame.sort_values("absolute_coefficient", ascending=False).reset_index(drop=True)
