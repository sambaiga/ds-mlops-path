"""Charts and tables carry a static twin once the hook is on."""

from great_tables import GT, md
from lets_plot import aes, geom_point, gggrid, ggplot
import pandas as pd
import pytest

from ark.plot import static

DATA = pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})


@pytest.fixture(autouse=True)
def hook():
    static.enable()


def chart():
    return ggplot(DATA, aes("x", "y")) + geom_point()


def test_a_chart_gives_html_and_svg():
    bundle = chart()._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.SVG}
    assert bundle[static.SVG].lstrip().startswith("<svg")
    assert "<script" in bundle[static.HTML]


def test_a_grid_of_charts_gives_both_too():
    assert set(gggrid([chart(), chart()])._repr_mimebundle_()) == {static.HTML, static.SVG}


def test_include_and_exclude_limit_the_representations():
    assert set(chart()._repr_mimebundle_(include={static.SVG})) == {static.SVG}
    assert set(chart()._repr_mimebundle_(exclude={static.SVG})) == {static.HTML}


def test_a_great_tables_table_gives_html_and_latex():
    table = GT(pd.DataFrame({"course": ["A", "B"], "score": [71.234, 64.5]})).fmt_number("score", decimals=1)
    bundle = table._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.LATEX}
    assert "\\begin{tabular" in bundle[static.LATEX]
    assert "71.2" in bundle[static.LATEX]
    assert "adjustbox" in bundle[static.LATEX]
    assert "\\begin{table}" not in bundle[static.LATEX]  # a float cannot sit inside the scaled box


def test_a_data_frame_gives_html_and_latex_with_escaped_text_and_short_numbers():
    frame = pd.DataFrame({"course": ["A_x"], "score": [71.234]})
    bundle = frame._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.LATEX}
    assert "A\\_x" in bundle[static.LATEX]
    assert "71.234 " in bundle[static.LATEX]
    assert "71.234000" not in bundle[static.LATEX]
    assert "\\toprule" in bundle[static.LATEX]


def test_a_long_frame_is_shown_as_pandas_shows_it_with_a_gap():
    frame = pd.DataFrame({"n": range(200)})
    rows = static.shown(frame)
    assert len(rows) == 5 + 1 + 5
    assert rows.index[5] == "..."
    assert static.shown(DATA) is DATA


def test_enabling_twice_changes_nothing():
    first = pd.DataFrame._repr_mimebundle_
    static.enable()
    assert pd.DataFrame._repr_mimebundle_ is first


def test_a_title_and_a_source_note_are_set_around_the_scaled_table():
    table = GT(DATA).tab_header(title="Squares").tab_source_note("Source: test")
    latex = table._repr_mimebundle_()[static.LATEX]
    assert latex.index("Squares") < latex.index("\\begin{adjustbox}") < latex.index("Source: test")


def test_markdown_labels_become_latex_instead_of_stopping_the_table():
    assert static.markdown_latex("**MAE** of `fit_1` & more") == "\\textbf{MAE} of \\texttt{fit\\_1} \\& more"
    table = GT(DATA).cols_label(x=md("**x** value"))
    assert "\\textbf{x} value" in table._repr_mimebundle_()[static.LATEX]


def test_a_polars_frame_gives_html_and_latex():
    polars = pytest.importorskip("polars")
    bundle = polars.DataFrame({"course": ["A_x"], "score": [71.234]})._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.LATEX}
    assert "A\\_x" in bundle[static.LATEX]


def test_a_table_that_latex_cannot_write_is_printed_as_its_data():
    table = GT(pd.DataFrame({"a": [1.0, 2.0], "b": [4.0, 5.0]})).grand_summary_rows(fns={"Mean": lambda x: x.mean()})
    bundle = table._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.LATEX}
    assert "\\begin{tabular" in bundle[static.LATEX]
    assert "5" in bundle[static.LATEX]


def test_long_cells_are_cut_to_fit_a_printed_column():
    frame = pd.DataFrame({"values": [[1.5] * 40]})
    assert len(static.plain_cells(frame).iloc[0, 0]) == 40
