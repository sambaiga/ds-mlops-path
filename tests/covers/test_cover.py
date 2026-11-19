"""The cover meets the rules of a printer: spine, safe zone, type size, ink limit and a picture that is computed."""

import re

import numpy as np
import pytest

from ark.covers import art
from ark.covers.draw import front_only, sheet
from ark.covers.spec import DESIGN, MIN_TYPE, SAFE, PrintSpec

SPEC = PrintSpec()


def test_the_spine_is_the_page_count_times_the_paper_and_the_sheet_adds_the_bleed():
    assert PrintSpec(pages=400).spine == pytest.approx(22.88)
    assert SPEC.width == pytest.approx(2 * 170 + SPEC.spine + 2 * 3.175)
    assert SPEC.height == pytest.approx(240 + 2 * 3.175)


def test_the_artwork_proportions_fit_the_trim():
    assert SPEC.artwork_fit < 0.02
    assert PrintSpec(trim=(155.0, 235.0)).artwork_fit > 0.02


def test_every_text_is_inside_the_safe_zone_and_large_enough_to_print():
    _, records = sheet(SPEC)
    margin = SAFE / SPEC.scale
    for text, panel, (x0, y0, x1, y1), size in records:
        assert margin <= x0 and x1 <= DESIGN[0] - margin, f"{text!r} on the {panel} is outside the safe zone"
        assert margin <= y0 and y1 <= DESIGN[1] - margin, f"{text!r} on the {panel} is outside the safe zone"
        assert size * SPEC.scale >= MIN_TYPE, f"{text!r} is too small to print"


def test_the_front_alone_has_the_same_texts_as_the_front_of_the_wrap():
    _, wrap = sheet(SPEC)
    _, alone = front_only()
    assert [r[0] for r in wrap if r[1] == "front"] == [r[0] for r in alone]


def test_the_cmyk_file_has_no_rgb_colour_and_never_exceeds_the_ink_limit(tmp_path):
    from kinyonga.cmyk import INK_LIMIT, convert

    fig, _ = sheet(SPEC)
    rgb = tmp_path / "wrap.pdf"
    fig.savefig(rgb)
    text = convert(rgb.read_bytes()).decode("latin-1")
    assert not re.search(r"\b(rg|RG)\b", text)
    inks = [tuple(map(float, m.groups())) for m in re.finditer(r"([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) [kK]\b", text)]
    assert inks
    assert max(sum(ink) for ink in inks) <= INK_LIMIT + 1e-6


def test_the_pictures_are_computed_and_a_rebuild_changes_nothing():
    first = art.table(np.random.default_rng(art.SEED))[0]
    second = art.table(np.random.default_rng(art.SEED))[0]
    assert np.array_equal(first, second)


def test_the_stages_have_the_shape_of_their_task():
    rng = np.random.default_rng(art.SEED)
    fpr, tpr = art.roc()
    assert np.all(tpr >= fpr - 1e-3)  # the classifier is better than chance everywhere
    bars, p95 = art.latency(rng)
    assert bars.max() == pytest.approx(1.0)
    assert 0.0 < p95 < 1.0
    index, crossing = art.drift(rng)
    assert index[crossing] > 0.25 >= index[:crossing].max()  # the first crossing of the threshold
    corr = art.correlation(rng)
    assert np.allclose(corr, corr.T)
    assert np.allclose(np.diag(corr), 1.0)
