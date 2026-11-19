"""The parts of the cover picture: a stream of data that falls into order, a small network and a rising line.

The picture is the one of the web book's landing page, redrawn as one flow for print: data is scattered at first, finds
its lanes as it enters a model, and leaves as a single line that rises to the full stop of the title. Positions come
from a seeded simulation, so a rebuild changes no byte. Functions return numbers in unit ranges; the drawing places
them.
"""

import numpy as np

SEED = 20261118
#: The number of nodes in each layer of the network, from the input to the output.
LAYERS = (4, 3, 2)


def particles(rng: np.random.Generator, count: int = 150) -> dict[str, np.ndarray]:
    """The particles of the data stream.

    Each particle travels along the stream from ``t = 0`` to ``t = 1``, where it enters the network in one of the lanes
    of the input layer. Far from the network its height is scattered; near it, the particle is in its lane.

    Args:
        rng: The random generator.
        count: The number of particles.

    Returns:
        ``t``, the progress along the stream from 0 to 1; ``lane``, the input node it enters, from 0 to the number of
        inputs minus one; ``offset``, a scatter from -1 to 1 that is applied in proportion to the distance left;
        ``size``, a relative size from 0 to 1.
    """
    t = np.sort(rng.beta(1.25, 1.0, count))
    return {
        "t": t,
        "lane": rng.integers(0, LAYERS[0], count),
        "offset": rng.uniform(-1.0, 1.0, count),
        "size": rng.uniform(0.25, 1.0, count),
    }


def network() -> list[np.ndarray]:
    """The positions of the nodes of a small network, layer by layer, in the unit box.

    Returns:
        One array of positions for each layer, with the layers spread across x and the nodes spread down y.
    """
    xs = np.linspace(0.0, 1.0, len(LAYERS))
    layers = []
    for x, nodes in zip(xs, LAYERS, strict=True):
        ys = (np.arange(nodes) + 0.5) / nodes
        layers.append(np.column_stack([np.full(nodes, x), 1.0 - ys]))
    return layers


def rise(points: int = 120) -> np.ndarray:
    """The parameter of the rising line: slow at first and then fast, as value grows once a model is in use.

    Args:
        points: The number of samples.

    Returns:
        Values from 0 to 1 that rise slowly and then quickly, to be used as the progress along the line.
    """
    s = np.linspace(0.0, 1.0, points)
    return (np.exp(2.2 * s) - 1.0) / (np.exp(2.2) - 1.0)
