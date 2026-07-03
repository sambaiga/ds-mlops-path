from pathlib import Path

import pytest

from ark.case_studies.spend_regression.config import SpendRegressionSettings
from ark.case_studies.spend_regression.data import download_dataverse_file, load_survey


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
