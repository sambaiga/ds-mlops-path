import pandas as pd

from ark.case_studies.spend_regression.config import SpendRegressionSettings

DEMOGRAPHIC_COLUMNS = [
    "Q-demos-age",
    "Q-demos-hispanic",
    "Q-demos-race",
    "Q-demos-education",
    "Q-demos-income",
    "Q-demos-gender",
    "Q-demos-state",
    "Q-amazon-use-hh-size",
    "Q-amazon-use-how-oft",
]

FEATURE_WINDOW_DAYS = 365
TARGET_WINDOW_END_DAYS = 730


def build_feature_matrix(
    purchases_df: pd.DataFrame, survey_df: pd.DataFrame, settings: SpendRegressionSettings
) -> pd.DataFrame:
    """Build the feature matrix and target for the spend-regression model.

    Features come only from each household's first 365 days of purchase
    history. The target is total spend in the following 365 days. Building
    both from the same window would leak the target into the input, see
    Chapter 33 Section 4.

    Returns one row per household with early_spend, n_purchases,
    n_categories, the columns in DEMOGRAPHIC_COLUMNS, and target_spend.
    Households missing from either window are dropped, not imputed.
    """
    if set(DEMOGRAPHIC_COLUMNS) & set(settings.excluded_survey_columns):
        raise ValueError("a demographic column overlaps the exclusion list, remove it")

    first_purchase = purchases_df.groupby("Survey ResponseID")["Order Date"].transform("min")
    purchases = purchases_df.assign(days_since_first=(purchases_df["Order Date"] - first_purchase).dt.days)

    target_window = purchases[purchases["days_since_first"].between(FEATURE_WINDOW_DAYS, TARGET_WINDOW_END_DAYS - 1)]
    household_target = target_window.groupby("Survey ResponseID")["total"].sum().rename("target_spend")

    feature_window = purchases[purchases["days_since_first"] < FEATURE_WINDOW_DAYS]
    feature_window = feature_window[feature_window["Survey ResponseID"].isin(household_target.index)]

    early_spend = feature_window.groupby("Survey ResponseID")["total"].sum().rename("early_spend")
    n_purchases = feature_window.groupby("Survey ResponseID").size().rename("n_purchases")
    n_categories = (
        feature_window.assign(Category=feature_window["Category"].fillna("UNKNOWN"))
        .groupby("Survey ResponseID")["Category"]
        .nunique()
        .rename("n_categories")
    )
    purchase_features = pd.concat([early_spend, n_purchases, n_categories], axis=1)

    demographics = survey_df.set_index("Survey ResponseID")[DEMOGRAPHIC_COLUMNS]

    return purchase_features.join(demographics, how="inner").join(household_target, how="inner")
