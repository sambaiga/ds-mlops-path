from pathlib import Path
import urllib.request

from loguru import logger
import pandas as pd

from ark.case_studies.spend_regression.config import SpendRegressionSettings


def download_dataverse_file(file_id: int, dest: Path, base_url: str) -> Path:
    """Download a Dataverse file by numeric id, caching it at dest on first call."""
    if dest.exists():
        logger.info(f"Using cached file: {dest}")
        return dest
    url = f"{base_url}/{file_id}"
    if not url.startswith("https://"):
        raise ValueError(f"Refusing to fetch a non-https URL: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # noqa: S310
    with urllib.request.urlopen(request) as response, dest.open("wb") as f:  # noqa: S310
        while chunk := response.read(1 << 20):
            f.write(chunk)
    logger.success(f"Downloaded {dest.stat().st_size:,} bytes to {dest}")
    return dest


def load_survey(settings: SpendRegressionSettings) -> pd.DataFrame:
    """Load the demographic and lifestyle survey, downloading on first call."""
    path = download_dataverse_file(
        settings.survey_file_id, settings.data_dir / "survey.tsv", settings.dataverse_base_url
    )
    df = pd.read_csv(path, sep="\t")
    logger.info(f"Loaded {len(df):,} survey responses")
    return df
