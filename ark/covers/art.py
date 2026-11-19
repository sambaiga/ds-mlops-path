"""The three parts of the cover picture: scattered data, a small network and a rising impact curve.

The picture is the one of the web book's landing page, redrawn for print: data flows through a model and ends as impact.
Positions and values come from a seeded simulation, so a rebuild changes no byte. Functions return arrays in unit boxes;
the drawing places them on the page.
"""

import numpy as np

SEED = 20261118
#: The number of nodes in each layer of the network, from the input to the output.
LAYERS = (4, 3, 2)


def data(rng: np.random.Generator, count: int = 15) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int]]]:
    """Scattered data points, their sizes and the links between neighbours.

    Points are drawn on a jittered grid, so that they scatter without overlapping.

    Args:
        rng: The random generator.
        count: The number of points.

    Returns:
        The positions in the unit box, one size from 0 to 1 for each point, and the pairs of neighbours that are linked.
    """
    rows = 5
    cols = int(np.ceil(count / rows))
    cells = [(c, r) for r in range(rows) for c in range(cols)][:count]
    points = np.array([[(c + rng.uniform(0.15, 0.85)) / cols, (r + rng.uniform(0.15, 0.85)) / rows] for c, r in cells])
    sizes = rng.uniform(0.2, 1.0, count)
    links = []
    for i in range(count):
        distance = np.hypot(*(points - points[i]).T)
        near = int(np.argsort(distance)[1])
        links.append((min(i, near), max(i, near)))
    return points, sizes, sorted(set(links))


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


def impact(points: int = 7) -> tuple[np.ndarray, np.ndarray]:
    """The impact curve: a quantity that grows slowly at first and then fast, as value does once a model is in use.

    Args:
        points: The number of marked points.

    Returns:
        The x and y of the marked points in the unit box, and the smooth curve through them is the same function on a
        finer grid, so ``y`` rises and ends at 1.
    """
    x = np.linspace(0.0, 1.0, points)
    y = (np.exp(2.6 * x) - 1.0) / (np.exp(2.6) - 1.0)
    return x, y
