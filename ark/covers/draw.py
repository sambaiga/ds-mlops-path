"""Draw the cover of "From Data to Impact": the front, the back and the spine, as vectors, on one sheet.

Everything is drawn in millimetres. Text is converted to outlines so that no font has to be embedded or found by the
printer, and every colour is a flat RGB value that the CMYK step converts. The front is drawn on an A4 sheet and scaled
to the trim; the back and the spine are drawn in the physical millimetres of the sheet.
"""

from dataclasses import dataclass, field
from pathlib import Path
import textwrap

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, PathPatch, Polygon, Rectangle
from matplotlib.path import Path as MPath
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D
import numpy as np

from ark.covers import art
from ark.covers.spec import DESIGN, MIN_SPINE_TEXT, SAFE, SPINE_CLEAR, PrintSpec

mpl.rcParams["pdf.compression"] = 0  # the CMYK step rewrites colour operators in place and needs plain streams
mpl.rcParams["svg.fonttype"] = "path"

FONTS = Path(__file__).resolve().parents[2] / "fonts"
NIGHT, SHEET_TOP, SKY, BLUE = "#0B1220", "#1E293B", "#38BDF8", "#0369A1"
ORANGE, WHITE, PALE, SLATE = "#E26029", "#FFFFFF", "#E2E8F0", "#94A3B8"
GUIDE = "#FF2D95"  # the colour of the guides on the check sheet, never in the print file

TITLE = FontProperties(fname=str(FONTS / "Jost-Bold.ttf"))
HEAD = FontProperties(fname=str(FONTS / "Jost-SemiBold.ttf"))
BODY = FontProperties(fname=str(FONTS / "LibreFranklin-Regular.ttf"))

URL = "sambaiga.github.io/ds-mlops-path"
LEAD = "Build it properly. Make it matter."
EYEBROW = "A PRACTICAL BOOK FOR DATA SCIENTISTS"
BLURB = (
    "A model that trains and scores well is not yet work that matters. This book puts the three sides together: "
    "the technical depth to understand what you build, the engineering discipline to build it properly, and the "
    "thinking that makes it change a decision. Every chapter is a notebook to run from top to bottom, on real "
    "data, with tested code."
)
ACTS = (
    ("1", "Build the foundation", "Python, data wrangling, visualization and engineering practice"),
    ("2", "Master the models", "Classical machine learning, deep learning and language models"),
    ("3", "Ship to production", "Pipelines, deployment, monitoring and operations"),
    ("4", "Design for impact", "Machine learning system design and value-driven AI"),
)


def _outline(s: str, size: float, font: FontProperties, track: float) -> tuple[MPath, float, float, float]:
    """Convert text to a path, with optional letter spacing.

    Args:
        s: The text.
        size: The em size, in millimetres.
        font: The font.
        track: Extra space between letters, as a fraction of the em size.

    Returns:
        The path, its width and height in millimetres, and the left edge of its ink.
    """
    if not track:
        path = TextPath((0, 0), s, size=size, prop=font)
        box = path.get_extents()
        return path, box.width, box.height, box.x0
    pen, paths = 0.0, []
    bar = TextPath((0, 0), "|", size=size, prop=font).get_extents().width
    for ch in s:
        if ch.isspace():
            pen += (0.3 + track) * size
            continue
        paths.append(TextPath((pen, 0), ch, size=size, prop=font))
        pen += TextPath((0, 0), ch + "|", size=size, prop=font).get_extents().x1 - bar + track * size
    vertices = np.concatenate([p.vertices for p in paths])
    codes = np.concatenate([np.asarray(p.codes) for p in paths])
    width = vertices[:, 0].max() - vertices[:, 0].min()
    height = vertices[:, 1].max() - vertices[:, 1].min()
    return MPath(vertices, codes), width, height, vertices[:, 0].min()


@dataclass
class Canvas:
    """An axes in which text and shapes are drawn, and a record of where the text went.

    Attributes:
        ax: The axes, with data coordinates in millimetres.
        name: The name of the panel, for the records.
        texts: The text, panel, box ``(x0, y0, x1, y1)`` and em size of each text, for the safe-zone test.
    """

    ax: object
    name: str
    texts: list = field(default_factory=list)

    def text(
        self,
        s: str,
        x: float,
        y: float,
        size: float,
        font: FontProperties,
        colour: str,
        ha: str = "left",
        track: float = 0.0,
        zorder: float = 8.0,
    ) -> tuple[float, float]:
        """Draw text as an outline.

        Args:
            s: The text.
            x: The x position of the anchor, in millimetres.
            y: The y position of the baseline, in millimetres.
            size: The em size, in millimetres.
            font: The font.
            colour: The fill colour.
            ha: ``left``, ``center`` or ``right``.
            track: Extra space between letters, as a fraction of the em size.
            zorder: The drawing order.

        Returns:
            The width and the height of the text, in millimetres.
        """
        path, width, height, left = _outline(s, size, font, track)
        shift = {"left": 0.0, "center": -width / 2, "right": -width}[ha]
        patch = PathPatch(
            path,
            fc=colour,
            ec="none",
            lw=0,
            zorder=zorder,
            transform=Affine2D().translate(x + shift - left, y) + self.ax.transData,
        )
        self.ax.add_patch(patch)
        self.texts.append((s, self.name, (x + shift, y, x + shift + width, y + height), size))
        return width, height

    def measure(self, s: str, size: float, font: FontProperties, track: float = 0.0) -> float:
        """Measure the width of a text without drawing it.

        Args:
            s: The text.
            size: The em size, in millimetres.
            font: The font.
            track: Extra space between letters, as a fraction of the em size.

        Returns:
            The width, in millimetres.
        """
        return _outline(s, size, font, track)[1]

    def line(
        self, xs, ys, colour: str, width: float, dash: tuple | None = None, alpha: float = 1.0, zorder: float = 2.0
    ) -> None:
        """Draw a line, with a width in millimetres.

        Args:
            xs: The x values.
            ys: The y values.
            colour: The colour.
            width: The width, in millimetres.
            dash: The dash pattern as on and off lengths in millimetres, or ``None``.
            alpha: The opacity.
            zorder: The drawing order.
        """
        points = width / 25.4 * 72
        (artist,) = self.ax.plot(
            xs, ys, color=colour, lw=points, alpha=alpha, solid_capstyle="round", clip_on=False, zorder=zorder
        )
        if dash:
            artist.set_dashes([d / width for d in dash])


def gradient(ax, x0: float, y0: float, x1: float, y1: float, top: str, foot: str, steps: int = 80) -> None:
    """Fill a rectangle with a vertical gradient built from flat strips, so that it stays a vector.

    Args:
        ax: The axes.
        x0: Left edge.
        y0: Foot.
        x1: Right edge.
        y1: Top.
        top: The colour at the top.
        foot: The colour at the foot.
        steps: The number of strips.
    """
    a = np.array(mpl.colors.to_rgb(top))
    b = np.array(mpl.colors.to_rgb(foot))
    edges = np.linspace(y0, y1, steps + 1)
    for i in range(steps):
        t = i / (steps - 1)
        # each strip runs to the top and the next paints over it, so no hairline of the ground shows between them
        ax.add_patch(
            Rectangle((x0, edges[i]), x1 - x0, y1 - edges[i], fc=tuple(b + (a - b) * t), ec="none", lw=0, zorder=-5)
        )


def front(canvas: Canvas) -> None:
    """Draw the front cover on an A4 sheet, in design millimetres: the title and one flow from data to impact.

    Data enters at the left, scattered; it finds its lanes as it enters a small network; and it leaves as one line that
    rises to the full stop of the title, drawn in orange. The idea is the one of the web book's landing page, drawn as
    one gesture instead of three separate pictures.

    Args:
        canvas: The canvas of the front panel.
    """
    ax, w = canvas.ax, DESIGN[0]
    canvas.text(EYEBROW, w / 2, 277.5, 3.0, HEAD, SLATE, "center", track=0.12)
    canvas.text("From Data", w / 2, 252, 20.5, TITLE, WHITE, "center")
    width, _ = canvas.text("to Impact", w / 2, 232, 20.5, TITLE, WHITE, "center")
    stop = (w / 2 + width / 2 + 7.2, 233.4)  # the full stop of the title, where the line ends
    rng = np.random.default_rng(art.SEED)
    # the network, in the middle of the page
    n0, n1, y_lo, y_hi = 84.0, 130.0, 108.0, 166.0
    layers = [np.column_stack([n0 + p[:, 0] * (n1 - n0), y_lo + p[:, 1] * (y_hi - y_lo)]) for p in art.network()]
    for left, right in zip(layers[:-1], layers[1:], strict=True):
        for a in left:
            for b in right:
                canvas.line([a[0], b[0]], [a[1], b[1]], SKY, 0.2, alpha=0.4)
    # the stream: scattered far from the network, in its lanes as it arrives
    stream = art.particles(rng)
    lanes = layers[0][:, 1]
    x0 = 16.0
    xs = x0 + stream["t"] * (n0 - 6.0 - x0)
    spread = 34.0 * (1.0 - stream["t"]) ** 1.5
    ys = lanes[stream["lane"]] + stream["offset"] * spread
    for x, y, t, size in zip(xs, ys, stream["t"], stream["size"], strict=True):
        canvas.line([x - 3.2 * t, x], [y, y], SKY, 0.18, alpha=0.35 * t)
        ax.add_patch(
            Circle(
                (x, y),
                0.45 + 0.95 * size * (0.5 + 0.5 * t),
                fc=SKY if t > 0.35 else SLATE,
                ec="none",
                alpha=0.35 + 0.6 * t,
                zorder=3,
            )
        )
    for y in lanes:
        canvas.line([n0 - 6.0, n0 - 3.6], [y, y], SKY, 0.3, alpha=0.7)
    for k, layer in enumerate(layers):
        for x, y in layer:
            ax.add_patch(
                Circle(
                    (x, y),
                    3.3 + 0.4 * k,
                    fc=NIGHT,
                    ec=SKY if k < 2 else WHITE,
                    lw=(0.5 + 0.2 * k) / 25.4 * 72,
                    zorder=4,
                )
            )
    # the line: from the two output nodes to one line that rises to the full stop
    start = np.array([n1 + 12.0, (y_lo + y_hi) / 2])
    for y in layers[-1][:, 1]:
        canvas.line([n1 + 3.8, start[0]], [y, start[1]], SKY, 0.35, alpha=0.8)
    end = np.array(stop) - np.array([0.0, 2.4])
    p0, p1, p2, p3 = start, start + np.array([58.0, 10.0]), end + np.array([24.0, -80.0]), end
    s = art.rise()
    s = (s - s.min()) / (s.max() - s.min())
    t = s
    curve = (
        ((1 - t)[:, None] ** 3) * p0
        + 3 * ((1 - t)[:, None] ** 2) * t[:, None] * p1
        + 3 * (1 - t)[:, None] * (t[:, None] ** 2) * p2
        + (t[:, None] ** 3) * p3
    )
    canvas.line(curve[:, 0], curve[:, 1], SKY, 1.0, zorder=3)
    for k in range(1, 7):
        x, y = curve[int(k / 7 * (len(curve) - 1))]
        ax.add_patch(Circle((x, y), 1.1, fc=SKY, ec="none", zorder=4))
    ax.add_patch(Circle(stop, 3.2, fc=ORANGE, ec="none", zorder=6))
    ax.add_patch(Circle(stop, 5.2, fc="none", ec=ORANGE, lw=0.5 / 25.4 * 72, alpha=0.8, zorder=6))
    # the two words of the picture
    canvas.text("DATA", (x0 + n0) / 2, y_lo - 18.0, 3.0, HEAD, SLATE, "center", track=0.14)
    canvas.text("MODEL", (n0 + n1) / 2, y_lo - 18.0, 3.0, HEAD, SLATE, "center", track=0.14)
    canvas.text("From Python fundamentals to production-ready ML systems", w / 2, 38.0, 4.5, BODY, PALE, "center")
    ax.add_patch(Rectangle((0, 0), w, 24, fc=NIGHT, ec="none", lw=0, zorder=70))
    canvas.text("Anthony Faustine", w / 2, 10.5, 6.2, HEAD, WHITE, "center")


def back(canvas: Canvas) -> None:
    """Draw the back cover on an A4 sheet, in design millimetres.

    Args:
        canvas: The canvas of the back panel.
    """
    ax = canvas.ax
    left = 20.0
    canvas.text(EYEBROW, left, 268, 3.0, HEAD, SLATE, track=0.12)
    width, _ = canvas.text(LEAD, left, 253, 8.2, HEAD, WHITE)
    canvas.line([left, left + width * 0.42], [249.4, 249.4], SKY, 0.6)
    for i, line in enumerate(textwrap.wrap(BLURB, 62)):
        canvas.text(line, left, 238 - i * 5.9, 3.7, BODY, PALE)
    top = 188.0
    for i, (number, name, line) in enumerate(ACTS):
        y = top - i * 21.5
        colour = ORANGE if number == "4" else SKY
        ax.add_patch(Circle((left + 5, y + 2.6), 5.2, fc=NIGHT, ec=colour, lw=0.5 / 25.4 * 72))
        canvas.text(number, left + 5, y + 0.6, 4.6, HEAD, colour, "center")
        canvas.text(name, left + 15, y + 3.4, 4.7, HEAD, WHITE)
        canvas.text(line, left + 15, y - 2.2, 3.3, BODY, SLATE)
    canvas.text("IN EVERY CHAPTER", left, 96, 2.8, HEAD, SLATE, track=0.12)
    canvas.text("Key concept   Activity   Common mistake   Pro tip", left, 89, 3.6, BODY, SKY)
    canvas.text("THE TOOLS", left, 76, 2.8, HEAD, SLATE, track=0.12)
    canvas.text("uv, ruff, pytest, pandas, polars, scikit-learn,", left, 69, 3.5, BODY, PALE)
    canvas.text("pydantic, MLflow, FastAPI, Docker and Prefect", left, 63.5, 3.5, BODY, PALE)
    canvas.text("READ ONLINE", left, 52, 2.8, HEAD, SLATE, track=0.12)
    canvas.text(URL, left, 45, 4.2, HEAD, SKY)


def spine(ax, spec: PrintSpec) -> bool:
    """Draw the spine in sheet millimetres: a mark at the head, then the title and the author turned to read downward.

    Args:
        ax: The axes of the whole sheet.
        spec: The print specification.

    Returns:
        Whether the spine is wide enough to carry text.
    """
    x0 = spec.bleed + spec.trim[0]
    centre = x0 + spec.spine / 2
    top = spec.bleed + spec.trim[1]
    ax.add_patch(Rectangle((x0, 0), spec.spine, spec.height, fc=NIGHT, ec="none", lw=0, zorder=1))
    ax.add_patch(Rectangle((x0, top - 26), spec.spine, 26 + spec.bleed, fc=SHEET_TOP, ec="none", lw=0, zorder=2))
    ax.add_patch(Circle((centre, top - 13), min(2.2, spec.spine / 4), fc=ORANGE, ec="none", zorder=3))
    if spec.spine < MIN_SPINE_TEXT:
        return False
    for s, size, font, colour, y in (
        ("From Data to Impact", 5.4, TITLE, WHITE, top - 34),
        ("Anthony Faustine", 3.4, BODY, PALE, spec.bleed + 34),
    ):
        path = TextPath((0, 0), s, size=size, prop=font)
        box = path.get_extents()
        place = Affine2D().translate(-box.x0, -box.height / 2 + 0.0).rotate_deg(-90).translate(centre, y)
        ax.add_patch(PathPatch(path, fc=colour, ec="none", lw=0, transform=place + ax.transData, zorder=3))
    return True


def sheet(spec: PrintSpec, guides: bool = False, barcode_label: bool = False) -> tuple[Figure, list]:
    """Draw the whole wrap: back cover, spine and front cover with bleed.

    Args:
        spec: The print specification.
        guides: Whether to draw the check-sheet guides (trim, bleed, safe zone and folds); never in the print file.
        barcode_label: Whether to write on the barcode box that it is a place holder, for the check sheet only.

    Returns:
        The figure and the records of every text drawn, as ``(text, panel, box, size)`` in design millimetres.
    """
    fig = Figure(figsize=(spec.width / 25.4, spec.height / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, spec.width)
    ax.set_ylim(0, spec.height)
    ax.axis("off")
    gradient(ax, 0, 0, spec.width, spec.height, SHEET_TOP, NIGHT)
    records: list = []
    for name, x0 in (("back", spec.back_x), ("front", spec.front_x)):
        panel = fig.add_axes(
            [x0 / spec.width, spec.bleed / spec.height, spec.trim[0] / spec.width, spec.trim[1] / spec.height]
        )
        panel.set_xlim(0, DESIGN[0])
        panel.set_ylim(0, DESIGN[1])
        panel.axis("off")
        panel.set_clip_on(False)
        canvas = Canvas(panel, name)
        (front if name == "front" else back)(canvas)
        records += canvas.texts
    spine(ax, spec)
    bx = spec.back_x + spec.trim[0] - 12 - 50
    ax.add_patch(Rectangle((bx, spec.bleed + 12), 50, 30, fc=WHITE, ec="none", lw=0, zorder=6))
    if barcode_label:
        Canvas(ax, "sheet").text("ISBN BARCODE 50 x 30 mm", bx + 25, spec.bleed + 26, 2.6, BODY, "#64748B", "center")
    if guides:
        _guides(ax, spec, bx)
    return fig, records


def _guides(ax, spec: PrintSpec, bx: float) -> None:
    """Draw the check-sheet guides: the trim, the bleed edge, the safe zone, the spine folds and the barcode box.

    Args:
        ax: The axes of the whole sheet.
        spec: The print specification.
        bx: The left edge of the barcode box, in millimetres.
    """
    pts = 0.25 / 25.4 * 72
    for x0 in (spec.back_x, spec.front_x):
        ax.add_patch(Rectangle((x0, spec.bleed), spec.trim[0], spec.trim[1], fc="none", ec=GUIDE, lw=pts, zorder=9))
        ax.add_patch(
            Rectangle(
                (x0 + SAFE, spec.bleed + SAFE),
                spec.trim[0] - 2 * SAFE,
                spec.trim[1] - 2 * SAFE,
                fc="none",
                ec=GUIDE,
                lw=pts,
                ls=(0, (2, 2)),
                zorder=9,
            )
        )
    for x in (spec.back_x + spec.trim[0], spec.front_x):
        ax.plot([x, x], [0, spec.height], color=GUIDE, lw=pts, zorder=9)
    for x in (spec.front_x + SPINE_CLEAR, spec.back_x + spec.trim[0] - SPINE_CLEAR):
        ax.plot([x, x], [0, spec.height], color=GUIDE, lw=pts, ls=(0, (1, 2)), zorder=9)
    ax.add_patch(Rectangle((bx, spec.bleed + 12), 50, 30, fc="none", ec=GUIDE, lw=pts, zorder=9))


def front_only() -> tuple[Figure, list]:
    """Draw the front cover alone on an A4 sheet, without bleed, for the LaTeX edition and the web.

    Returns:
        The figure and the records of every text drawn.
    """
    fig = Figure(figsize=(DESIGN[0] / 25.4, DESIGN[1] / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, DESIGN[0])
    ax.set_ylim(0, DESIGN[1])
    ax.axis("off")
    gradient(ax, 0, 0, DESIGN[0], DESIGN[1], SHEET_TOP, NIGHT)
    canvas = Canvas(ax, "front")
    front(canvas)
    return fig, canvas.texts
