"""Give every Lets-Plot chart a static twin, so that the print edition shows the charts the web edition animates.

A Lets-Plot chart displays itself as HTML with a script, which a browser runs and a PDF cannot: without this module the
PDF prints the text of the Python object in place of the chart. This module adds to each chart a second representation,
an SVG, next to the HTML. The notebook output then holds both, and Quarto takes the interactive one for the web and the
static one for print. Call :func:`enable` once, before the first chart.
"""

from lets_plot.plot.core import PlotSpec
from lets_plot.plot.subplots import SupPlotsSpec

CHARTS = (PlotSpec, SupPlotsSpec)
HTML = "text/html"
SVG = "image/svg+xml"


def mimebundle(chart, include=None, exclude=None) -> dict[str, str]:
    """Return the representations of a chart: its interactive HTML and a static SVG.

    Args:
        chart: A Lets-Plot chart or a grid of charts.
        include: The representations asked for, as IPython passes them; ``None`` asks for all.
        exclude: The representations not wanted; ``None`` excludes none.

    Returns:
        The HTML and the SVG, as far as ``include`` and ``exclude`` allow.
    """
    bundle = {HTML: chart._repr_html_(), SVG: chart.to_svg()}
    if include:
        bundle = {mime: value for mime, value in bundle.items() if mime in include}
    if exclude:
        bundle = {mime: value for mime, value in bundle.items() if mime not in exclude}
    return bundle


def enable() -> None:
    """Make every Lets-Plot chart display itself as HTML and as SVG.

    Calling it more than once has no further effect.
    """
    for kind in CHARTS:
        kind._repr_mimebundle_ = mimebundle
