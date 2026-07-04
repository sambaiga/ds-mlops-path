from loguru import logger
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    """The Chapter 32 ColumnTransformer shape: impute+scale numeric, impute+one-hot categorical."""
    num_pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    cat_pipe = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        OneHotEncoder(handle_unknown="ignore", sparse_output=False),
    )
    return ColumnTransformer([("num", num_pipe, numeric_features), ("cat", cat_pipe, categorical_features)])


def top_decile_lift(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Ratio of actual spend among the top decile of predictions to the overall mean.

    This is the spec card's success metric, not a generic sklearn scorer:
    a household doesn't need an accurate spend forecast to be worth
    targeting, it needs to rank near the top.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    threshold = np.quantile(y_pred, 0.9)
    return y_true[y_pred >= threshold].mean() / y_true.mean()


def evaluate_model(pipe: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, name: str) -> dict[str, float | str]:
    """Fit metrics for one candidate, in the row shape metrics_report() expects."""
    preds = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    lift = top_decile_lift(y_test, preds)
    logger.info(f"{name}: MAE={mae:.2f}, top-decile lift={lift:.2f}x")
    return {"Model": name, "MAE": mae, "Lift": lift}


def estimate_incremental_value(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    total_households: int,
    conversion_rate: float,
) -> float:
    """Back-of-envelope incremental revenue from targeting the top decile.

    (top-decile mean spend - overall mean spend), scaled by the number of
    households a 10%-of-base loyalty budget would target and by an assumed
    conversion rate: the fraction of that spend gap the program actually
    captures, not the full gap, since not every targeted household responds.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    threshold = np.quantile(y_pred, 0.9)
    spend_gap = y_true[y_pred >= threshold].mean() - y_true.mean()
    n_targeted = round(total_households * 0.1)
    value = spend_gap * n_targeted * conversion_rate
    logger.info(f"Estimated incremental value: ${value:,.2f} ({n_targeted} households targeted)")
    return value
