"""Hand-drawn concept diagrams for the tutorials, using matplotlib directly.

Unlike everything else in :mod:`ark.plot`, these are not data visualisations:
each function draws a fixed, illustrative diagram for one specific concept
(matplotlib's Figure/Axes model, NumPy broadcasting, ...). They are matplotlib
code on purpose, not Mermaid or a static image asset, so they render as a real
image everywhere a tutorial notebook is opened, including plain Jupyter and
VS Code, not just when processed by Quarto.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from ark.plot.tokens import INFO, PRIMARY, TEXT_MUTED, WARNING


def figure_axes_diagram() -> plt.Figure:
    """Draw a labelled diagram of one Figure containing two Axes.

    Illustrates the distinction Part 5 opens with: a Figure is the whole
    canvas, an Axes is one plot inside it, and a single Figure can hold
    more than one. The two panels are real Axes with real plotted data,
    annotated rather than drawn as abstract boxes.

    Returns:
        The matplotlib Figure, ready to display in a notebook cell.
    """
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.2))

    for ax, title in zip(axes, ["Axes object 1", "Axes object 2"], strict=True):
        x = np.linspace(0, 10, 60)
        ax.plot(x, np.sin(x) + rng.normal(0, 0.08, 60), color=PRIMARY, linewidth=1.4)
        ax.set_xlabel("x label")
        ax.set_ylabel("y label")
        ax.set_title(title, fontsize=10, color=INFO, fontweight="bold")

    fig.subplots_adjust(top=0.72, bottom=0.18, left=0.12, right=0.97, wspace=0.35)

    # Draw the Figure's own boundary explicitly - this is the one line in
    # the whole diagram that has no equivalent in the rendered chart itself.
    # Its top edge sits below the label text so the two never overlap.
    boundary = plt.Rectangle(
        (0.01, 0.01),
        0.98,
        0.85,
        transform=fig.transFigure,
        fill=False,
        edgecolor=WARNING,
        linewidth=2,
        linestyle="dashed",
        clip_on=False,
    )
    fig.add_artist(boundary)
    fig.text(
        0.5,
        0.93,
        "One Figure (the dashed boundary - the whole canvas, what fig.savefig() writes)",
        ha="center",
        fontsize=10,
        color=WARNING,
        fontweight="bold",
    )
    return fig


def broadcasting_diagram() -> plt.Figure:
    """Draw a grid diagram of a (3,) array broadcasting against a (5, 3) matrix.

    The single row at the top represents the smaller array; the dashed
    arrows show it being virtually repeated for every row of the larger
    array below, which is the mental model Part 4's broadcasting rule
    depends on.

    Returns:
        The matplotlib Figure, ready to display in a notebook cell.
    """
    n_rows, n_cols = 5, 3
    fig, ax = plt.subplots(figsize=(5, 4.5))

    # The (5, 3) matrix: a grid of cells, one row per sample.
    for r in range(n_rows):
        for c in range(n_cols):
            ax.add_patch(plt.Rectangle((c, -r), 0.92, 0.92, facecolor="#EAF3FA", edgecolor=INFO, linewidth=1))
    ax.text(n_cols / 2, -n_rows - 0.3, "shape (5, 3)", ha="center", color=INFO, fontweight="bold")

    # The (3,) array: one row, drawn above the matrix, with dashed arrows
    # showing it "stretching" down to every row it gets broadcast against.
    for c in range(n_cols):
        ax.add_patch(plt.Rectangle((c, 1.6), 0.92, 0.92, facecolor="#FFF1E6", edgecolor=WARNING, linewidth=1))
        ax.annotate(
            "",
            xy=(c + 0.46, -n_rows + 1.1),
            xytext=(c + 0.46, 1.55),
            arrowprops={"arrowstyle": "->", "color": WARNING, "linestyle": "dashed", "alpha": 0.6},
        )
    ax.text(n_cols / 2, 2.75, "shape (3,)", ha="center", color=WARNING, fontweight="bold")
    ax.text(
        n_cols / 2,
        -n_rows / 2 + 0.5,
        "broadcast\n(no data copied)",
        ha="center",
        va="center",
        fontsize=9,
        color=TEXT_MUTED,
        style="italic",
    )

    ax.set_xlim(-0.3, n_cols + 0.3)
    ax.set_ylim(-n_rows - 0.8, 3.1)
    ax.set_title("X - feature_mean: (5, 3) and (3,)", fontsize=11, color=PRIMARY, fontweight="bold")
    ax.axis("off")
    fig.tight_layout()
    return fig
