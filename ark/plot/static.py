"""Give charts and tables a static twin, so that the print edition shows what the web edition animates.

A Lets-Plot chart, a Great Tables table and a pandas data frame display themselves as HTML, which a browser draws and a
PDF cannot: without this module the PDF holds the text of the Python object for a chart and nothing at all for a table.
This module adds to each a second representation next to the HTML, an SVG for a chart and LaTeX for a table. The
notebook output then holds both, and Quarto takes the HTML for the web and the static form for print.

Call :func:`enable` once, before the first output. The print edition does it for every notebook through the startup
file of ``.ipython`` (see ``scripts/print.sh``), so that no notebook has to remember it.
"""

import re

import pandas as pd

HTML = "text/html"
SVG = "image/svg+xml"
LATEX = "text/latex"
#: How a table is fitted to the page: small type, scaled down only when it is wider than the text.
FIT = "\\begin{center}\n\\small\n%s\\begin{adjustbox}{max width=\\linewidth}\n%s\n\\end{adjustbox}\n%s\\end{center}\n"
TABLE = re.compile(
    r"\\begin\{table\}.*?\n(.*?)\\begin\{tabular\*?\}(.*?)\\end\{tabular\*?\}(.*?)\\end\{table\}", re.DOTALL
)
CAPTION = re.compile(r"\\caption\*\{\s*(.*?)\s*\}\s*(?=\\fontsize|\\begin|$)", re.DOTALL)


def fitted(latex: str, caption: str = "") -> str:
    """Fit a LaTeX table to the page, with its title above it and its notes below.

    Great Tables writes a floating ``table`` with a ``caption*``, which cannot sit inside a box that scales the table.
    The title is set above the box, the notes below it, and the floating environment is dropped.

    Args:
        latex: A ``tabular`` as LaTeX, or a Great Tables ``table`` that holds one.
        caption: A line to set above the table, if the LaTeX does not carry its own title.

    Returns:
        The table inside a centred, scaled box.
    """
    match = TABLE.search(latex)
    if match is None:
        return FIT % (caption, latex, "")
    head, body, notes = match.groups()
    title = CAPTION.search(head)
    above = f"{title.group(1)}\\par\\smallskip\n" if title else caption
    tabular = latex[match.start(2) - len("\\begin{tabular*}") : match.end(2) + len("\\end{tabular*}")]
    tabular = tabular if tabular.startswith("\\begin{tabular") else f"\\begin{{tabular*}}{body}\\end{{tabular*}}"
    return FIT % (above, tabular, notes.strip() + "\n" if notes.strip() else "")


MARKDOWN = re.compile(r"`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*")


def markdown_latex(text: str) -> str:
    """Convert the markdown of a table label to LaTeX: code, bold and italic, with everything else escaped.

    Great Tables cannot write ``md()`` text as LaTeX, so a table that labels a column with markdown would stay out of
    the print edition. This covers the three marks that labels use.

    Args:
        text: The markdown text.

    Returns:
        The text as LaTeX.
    """
    from great_tables._text import _latex_escape

    parts, last = [], 0
    for match in MARKDOWN.finditer(text):
        parts.append(_latex_escape(text[last : match.start()]))
        code, bold, italic = match.groups()
        parts.append(
            f"\\texttt{{{_latex_escape(code)}}}"
            if code
            else f"\\textbf{{{_latex_escape(bold)}}}"
            if bold
            else f"\\textit{{{_latex_escape(italic)}}}"
        )
        last = match.end()
    parts.append(_latex_escape(text[last:]))
    return "".join(parts)


def _limit(bundle: dict[str, str], include, exclude) -> dict[str, str]:
    """Keep the representations that were asked for.

    Args:
        bundle: The representations by media type.
        include: The media types asked for, as IPython passes them; ``None`` asks for all.
        exclude: The media types not wanted; ``None`` excludes none.

    Returns:
        The representations that remain.
    """
    if include:
        bundle = {mime: value for mime, value in bundle.items() if mime in include}
    if exclude:
        bundle = {mime: value for mime, value in bundle.items() if mime not in exclude}
    return bundle


def chart_bundle(chart, include=None, exclude=None) -> dict[str, str]:
    """Return the representations of a chart: its interactive HTML and a static SVG.

    Args:
        chart: A Lets-Plot chart or a grid of charts.
        include: The representations asked for, as IPython passes them; ``None`` asks for all.
        exclude: The representations not wanted; ``None`` excludes none.

    Returns:
        The HTML and the SVG, as far as ``include`` and ``exclude`` allow.
    """
    return _limit({HTML: chart._repr_html_(), SVG: chart.to_svg()}, include, exclude)


def plain_cells(frame: pd.DataFrame, width: int = 40) -> pd.DataFrame:
    """Shorten the cells of a data frame that hold long text or lists, so that they fit a printed column.

    Args:
        frame: The data frame.
        width: The most characters a cell keeps.

    Returns:
        A copy in which every cell that is not a plain number or short text is its text, cut to ``width`` characters.
    """

    def cut(value):
        text = str(value)
        return text if len(text) <= width else text[: width - 3] + "..."

    return frame.map(lambda value: value if isinstance(value, int | float) else cut(value))


def table_bundle(table, include=None, exclude=None) -> dict[str, str]:
    """Return the representations of a Great Tables table: its HTML and the same table in LaTeX.

    Great Tables cannot write every feature as LaTeX (row groups, summary rows and sparklines). A table that uses one is
    printed as its data, with the title above it, so that the print edition holds the numbers; the web edition keeps
    the full table.

    Args:
        table: A Great Tables table.
        include: The representations asked for, as IPython passes them; ``None`` asks for all.
        exclude: The representations not wanted; ``None`` excludes none.

    Returns:
        The HTML and the LaTeX, as far as ``include`` and ``exclude`` allow.
    """
    try:
        latex = fitted(table.as_latex())
    except NotImplementedError:
        data = table._tbl_data
        data = data if isinstance(data, pd.DataFrame) else data.to_pandas()
        latex = fitted(
            plain_cells(shown(data)).to_latex(escape=True, float_format=lambda v: f"{v:.6g}", na_rep="", index=False)
        )
    return _limit({HTML: table._repr_html_(), LATEX: latex}, include, exclude)


def shown(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the rows of a data frame that its display shows: all of them, or the first and last few with a gap.

    Args:
        frame: The data frame.

    Returns:
        The frame itself when it is short enough, otherwise its head, a row of ellipses and its tail, as pandas does.
    """
    limit = pd.get_option("display.max_rows")
    if limit is None or len(frame) <= limit:
        return frame
    edge = (pd.get_option("display.min_rows") or 10) // 2
    gap = pd.DataFrame({column: ["..."] for column in frame.columns}, index=["..."]).astype(object)
    return pd.concat([frame.head(edge).astype(object), gap, frame.tail(edge).astype(object)])


def frame_bundle(frame: pd.DataFrame, include=None, exclude=None) -> dict[str, str]:
    """Return the representations of a data frame: its HTML and the same rows in LaTeX.

    Args:
        frame: A data frame.
        include: The representations asked for, as IPython passes them; ``None`` asks for all.
        exclude: The representations not wanted; ``None`` excludes none.

    Returns:
        The HTML and the LaTeX, as far as ``include`` and ``exclude`` allow.
    """
    latex = shown(frame).to_latex(escape=True, float_format=lambda value: f"{value:.6g}", na_rep="")
    return _limit({HTML: frame._repr_html_(), LATEX: fitted(latex)}, include, exclude)


def polars_bundle(frame, include=None, exclude=None) -> dict[str, str]:
    """Return the representations of a polars data frame: its HTML and the same rows in LaTeX.

    Args:
        frame: A polars data frame.
        include: The representations asked for, as IPython passes them; ``None`` asks for all.
        exclude: The representations not wanted; ``None`` excludes none.

    Returns:
        The HTML and the LaTeX, as far as ``include`` and ``exclude`` allow.
    """
    latex = shown(frame.to_pandas()).to_latex(
        escape=True, float_format=lambda value: f"{value:.6g}", na_rep="", index=False
    )
    return _limit({HTML: frame._repr_html_(), LATEX: fitted(latex)}, include, exclude)


def enable() -> None:
    """Make charts and tables display themselves as HTML and in a static form for print.

    Calling it more than once has no further effect.
    """
    from great_tables import GT
    import great_tables._text
    from lets_plot.plot.core import PlotSpec
    from lets_plot.plot.subplots import SupPlotsSpec

    for kind in (PlotSpec, SupPlotsSpec):
        kind._repr_mimebundle_ = chart_bundle
    great_tables._text._md_latex = markdown_latex
    GT._repr_mimebundle_ = table_bundle
    pd.DataFrame._repr_mimebundle_ = frame_bundle
    try:
        import polars as pl
    except ImportError:
        return
    pl.DataFrame._repr_mimebundle_ = polars_bundle
