from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SpecCard(BaseModel):
    """The five-component spec resolved in Chapter 33, Section 1, kept as data, not prose."""

    target_variable: str = "Household's total spend over the coming 12 months"
    task_type: str = "Regression, supervised"
    success_metric: str = "Rank quality (top-decile lift over random), MAE as a secondary check"
    acceptable_threshold: str = (
        "Top-decile households must outspend a random household by a margin the loyalty program's budget can justify"
    )
    data_specification: str = (
        "One-time demographic and lifestyle survey plus multi-year, "
        "transaction-level purchase history, 5,027 U.S. households"
    )


class SpendRegressionSettings(BaseSettings):
    """Paths, source data, and policy decisions for the spend-regression case study."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SPEND_", case_sensitive=False)

    spec: SpecCard = SpecCard()

    data_dir: Path = Path("data")
    dataverse_base_url: str = "https://dataverse.harvard.edu/api/access/datafile"
    purchases_file_id: int = 7616235  # amazon-purchases.csv, ~298.5 MB
    survey_file_id: int = 7616231  # survey.csv, tab-separated despite the .csv extension

    random_seed: int = 42

    # Present in survey.csv, never used as a feature: predicting spend doesn't
    # need a household's substance use, disability status, or sexual orientation,
    # and training on them by default just because they're in the file is the
    # kind of feature-selection carelessness worth refusing on purpose.
    excluded_survey_columns: list[str] = [
        "Q-substance-use-cigarettes",
        "Q-substance-use-marijuana",
        "Q-substance-use-alcohol",
        "Q-personal-diabetes",
        "Q-personal-wheelchair",
        "Q-sexual-orientation",
    ]
