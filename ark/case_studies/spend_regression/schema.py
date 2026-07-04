import pandera as pa
from pandera.typing import Series


class FeatureMatrixSchema(pa.DataFrameModel):
    """Schema for the output of build_feature_matrix."""

    early_spend: Series[float] = pa.Field(ge=0)
    n_purchases: Series[int] = pa.Field(ge=1)
    n_categories: Series[int] = pa.Field(ge=1)
    target_spend: Series[float] = pa.Field(ge=0)

    demos_age: Series[str] = pa.Field(alias="Q-demos-age")
    demos_hispanic: Series[str] = pa.Field(alias="Q-demos-hispanic")
    demos_race: Series[str] = pa.Field(alias="Q-demos-race")
    demos_education: Series[str] = pa.Field(alias="Q-demos-education")
    demos_income: Series[str] = pa.Field(alias="Q-demos-income")
    demos_gender: Series[str] = pa.Field(alias="Q-demos-gender")
    demos_state: Series[str] = pa.Field(alias="Q-demos-state")
    amazon_use_hh_size: Series[str] = pa.Field(alias="Q-amazon-use-hh-size")
    amazon_use_how_oft: Series[str] = pa.Field(alias="Q-amazon-use-how-oft")

    class Config:
        strict = True
