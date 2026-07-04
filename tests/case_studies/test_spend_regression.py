from pathlib import Path

import numpy as np
import pandas as pd
import pandera.errors
import pytest

from ark.case_studies.spend_regression.config import SpendRegressionSettings
from ark.case_studies.spend_regression.data import download_dataverse_file, load_survey
from ark.case_studies.spend_regression.features import DEMOGRAPHIC_COLUMNS, build_feature_matrix
from ark.case_studies.spend_regression.model import estimate_incremental_value, top_decile_lift
from ark.case_studies.spend_regression.schema import FeatureMatrixSchema


def test_download_dataverse_file_returns_cached_path_without_network(tmp_path: Path) -> None:
    dest = tmp_path / "cached.csv"
    dest.write_text("already here")

    result = download_dataverse_file(file_id=1, dest=dest, base_url="https://example.invalid")

    assert result == dest
    assert dest.read_text() == "already here"


def test_download_dataverse_file_rejects_non_https_urls(tmp_path: Path) -> None:
    dest = tmp_path / "new-file.csv"

    with pytest.raises(ValueError, match="https"):
        download_dataverse_file(file_id=1, dest=dest, base_url="http://example.invalid")


def test_load_survey_parses_tab_separated_data(tmp_path: Path) -> None:
    survey_path = tmp_path / "survey.tsv"
    survey_path.write_text(
        "Survey ResponseID\tQ-demos-age\tQ-demos-income\nR_test1\t35 - 44 years\t$25,000 - $49,999\n"
    )
    settings = SpendRegressionSettings(data_dir=tmp_path)

    df = load_survey(settings)

    assert list(df.columns) == ["Survey ResponseID", "Q-demos-age", "Q-demos-income"]
    assert len(df) == 1
    assert df.loc[0, "Q-demos-age"] == "35 - 44 years"


def _make_purchases_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Survey ResponseID": ["R_a", "R_a", "R_a", "R_b"],
            "Order Date": pd.to_datetime(["2020-01-01", "2020-01-15", "2021-02-01", "2020-01-01"]),
            "total": [50.0, 30.0, 100.0, 20.0],
            "Category": ["ELECTRONICS", None, "BOOKS", "TOYS"],
        }
    )


def _make_survey_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Survey ResponseID": ["R_a", "R_b"],
            "Q-demos-age": ["25 - 34 years", "35 - 44 years"],
            "Q-demos-hispanic": ["No", "No"],
            "Q-demos-race": ["White", "White"],
            "Q-demos-education": ["Bachelor's degree", "Bachelor's degree"],
            "Q-demos-income": ["$25,000 - $49,999", "$50,000 - $74,999"],
            "Q-demos-gender": ["Female", "Male"],
            "Q-demos-state": ["California", "Texas"],
            "Q-amazon-use-hh-size": ["2", "1"],
            "Q-amazon-use-how-oft": ["Daily", "Weekly"],
        }
    )


def test_build_feature_matrix_drops_households_without_a_target(tmp_path: Path) -> None:
    settings = SpendRegressionSettings(data_dir=tmp_path)

    result = build_feature_matrix(_make_purchases_df(), _make_survey_df(), settings)

    assert list(result.index) == ["R_a"]


def test_build_feature_matrix_computes_features_only_from_the_feature_window(tmp_path: Path) -> None:
    settings = SpendRegressionSettings(data_dir=tmp_path)

    result = build_feature_matrix(_make_purchases_df(), _make_survey_df(), settings)

    # R_a's feature window (days 0-364) is the $50 and $30 purchases, not the
    # $100 purchase on day 397, which belongs to the target window instead.
    assert result.loc["R_a", "early_spend"] == 80.0
    assert result.loc["R_a", "n_purchases"] == 2
    assert result.loc["R_a", "target_spend"] == 100.0


def test_build_feature_matrix_fills_missing_category_before_counting(tmp_path: Path) -> None:
    settings = SpendRegressionSettings(data_dir=tmp_path)

    result = build_feature_matrix(_make_purchases_df(), _make_survey_df(), settings)

    # ELECTRONICS and the missing-category row (filled to UNKNOWN) are two
    # distinct categories, not one, the naive nunique() would say one.
    assert result.loc["R_a", "n_categories"] == 2


def test_build_feature_matrix_rejects_a_sensitive_demographic_column(tmp_path: Path) -> None:
    settings = SpendRegressionSettings(data_dir=tmp_path, excluded_survey_columns=[*DEMOGRAPHIC_COLUMNS[:1]])

    with pytest.raises(ValueError, match="overlaps the exclusion list"):
        build_feature_matrix(_make_purchases_df(), _make_survey_df(), settings)


def test_feature_matrix_schema_rejects_negative_spend(tmp_path: Path) -> None:
    settings = SpendRegressionSettings(data_dir=tmp_path)
    result = build_feature_matrix(_make_purchases_df(), _make_survey_df(), settings)
    invalid = result.assign(early_spend=-1.0)

    with pytest.raises(pandera.errors.SchemaError):
        FeatureMatrixSchema.validate(invalid)


def test_top_decile_lift_is_one_for_a_constant_prediction() -> None:
    y_true = np.array([10.0, 20.0, 30.0, 100.0])
    y_pred = np.full_like(y_true, 5.0)

    assert top_decile_lift(y_true, y_pred) == pytest.approx(1.0)


def test_estimate_incremental_value_scales_with_conversion_rate() -> None:
    # Top decile (>=90th pctile of predictions) is the household worth 100,
    # a $60 gap over the mean of 40. 10% of 10 households is 1, so a 50%
    # conversion rate should return half of that $60 gap.
    y_true = np.array([10.0, 20.0, 30.0, 100.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0])
    y_pred = y_true.copy()

    value = estimate_incremental_value(y_true, y_pred, total_households=10, conversion_rate=0.5)

    assert value == pytest.approx(30.0)
