"""Every Lets-Plot chart carries a static twin once the hook is on."""

from lets_plot import aes, geom_point, gggrid, ggplot
import pandas as pd

from ark.plot import static

DATA = pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})


def chart():
    return ggplot(DATA, aes("x", "y")) + geom_point()


def test_a_chart_gives_html_and_svg_once_the_hook_is_on():
    static.enable()
    bundle = chart()._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.SVG}
    assert bundle[static.SVG].lstrip().startswith("<svg")
    assert "<script" in bundle[static.HTML]


def test_a_grid_of_charts_gives_both_too():
    static.enable()
    bundle = gggrid([chart(), chart()])._repr_mimebundle_()
    assert set(bundle) == {static.HTML, static.SVG}


def test_include_and_exclude_limit_the_representations():
    static.enable()
    assert set(chart()._repr_mimebundle_(include={static.SVG})) == {static.SVG}
    assert set(chart()._repr_mimebundle_(exclude={static.SVG})) == {static.HTML}


def test_enabling_twice_changes_nothing():
    static.enable()
    first = type(chart())._repr_mimebundle_
    static.enable()
    assert type(chart())._repr_mimebundle_ is first
