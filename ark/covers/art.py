"""The five stages of the cover, each the characteristic picture of one stage of a machine learning system.

The picture shows the system the book teaches, not one task: a data table, the feature matrix, a model's ROC curve, the
latency of the service that serves it, and the drift that tells a team to retrain. Each is computed from a seeded
simulation, so a rebuild changes no byte. Functions return arrays and plain numbers; the drawing is in ``draw.py``.
"""

from dataclasses import dataclass
from math import erf, sqrt
from statistics import NormalDist

import numpy as np

SEED = 20261118
_NORMAL = NormalDist()


@dataclass(frozen=True)
class Stage:
    """One row of the system picture.

    Attributes:
        name: The label of the stage, in capitals.
        tools: The tools of the book that do the work of the stage, one line each.
    """

    name: str
    tools: tuple[str, ...]


STAGES = (
    Stage("DATA", ("pandas, polars", "pandera schemas")),
    Stage("FEATURES", ("scikit-learn", "pydantic configs")),
    Stage("MODEL", ("Optuna, MLflow", "pytest, ruff")),
    Stage("SERVE", ("FastAPI", "Docker")),
    Stage("MONITOR", ("Prefect", "drift and alerts")),
)


def table(rng: np.random.Generator, rows: int = 4, cols: int = 10) -> tuple[np.ndarray, tuple[int, int]]:
    """A small data table: cell values in 0 to 1 and the one cell that fails its schema.

    Args:
        rng: The random generator.
        rows: The number of rows.
        cols: The number of columns.

    Returns:
        The values, and the row and column of the invalid cell.
    """
    values = rng.beta(2.0, 2.6, (rows, cols))
    return values, (int(rng.integers(1, rows)), int(rng.integers(2, cols - 2)))


def correlation(rng: np.random.Generator, size: int = 9) -> np.ndarray:
    """The correlation of features that share two hidden factors, as a feature-engineering step would show.

    Args:
        rng: The random generator.
        size: The number of features.

    Returns:
        The correlation matrix, ``size`` by ``size``.
    """
    factors = rng.normal(size=(600, 2))
    loading = rng.normal(0, 0.9, (2, size))
    data = factors @ loading + rng.normal(0, 0.8, (600, size))
    return np.corrcoef(data, rowvar=False)


def roc(points: int = 200, separation: float = 1.3) -> tuple[np.ndarray, np.ndarray]:
    """The receiver operating characteristic of a binormal classifier.

    Args:
        points: The number of points.
        separation: The distance between the two class means, in standard deviations.

    Returns:
        The false positive rate and the true positive rate.
    """
    fpr = np.linspace(1e-4, 1 - 1e-4, points)
    tpr = np.array([0.5 * (1 + erf((separation + _NORMAL.inv_cdf(f)) / sqrt(2))) for f in fpr])
    return fpr, tpr


def latency(rng: np.random.Generator, bins: int = 28) -> tuple[np.ndarray, float]:
    """The latency of the prediction service: a histogram and the 95th percentile.

    Args:
        rng: The random generator.
        bins: The number of bars.

    Returns:
        The bar heights scaled to 0 to 1, and the position of the 95th percentile on the bar axis, from 0 to 1.
    """
    sample = rng.lognormal(mean=np.log(24), sigma=0.38, size=6000)
    edges = np.linspace(8, 110, bins + 1)
    counts, _ = np.histogram(sample, bins=edges)
    p95 = (np.percentile(sample, 95) - edges[0]) / (edges[-1] - edges[0])
    return counts / counts.max(), float(p95)


def drift(rng: np.random.Generator, weeks: int = 60, threshold: float = 0.25) -> tuple[np.ndarray, int]:
    """The population stability index of a live feature against its training data, week by week.

    Args:
        rng: The random generator.
        weeks: The number of weeks.
        threshold: The index above which a team retrains.

    Returns:
        The index for each week, and the first week at which it exceeds the threshold.
    """
    t = np.arange(weeks)
    index = 0.03 + 0.0000075 * t**3 + rng.normal(0, 0.006, weeks)
    index = np.maximum.accumulate(np.clip(index, 0.0, None)) * 0.35 + index * 0.65
    crossing = int(np.argmax(index > threshold))
    return index, crossing
