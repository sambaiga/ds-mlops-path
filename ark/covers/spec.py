"""The physical sheet of the printed cover and the rules that keep artwork and text where a printer can use them."""

from dataclasses import dataclass

#: The front cover is drawn on an A4 sheet, in millimetres, and scaled to the trim.
DESIGN = (210.0, 297.0)
#: The thinnest spine, in millimetres, that carries text (KDP asks for at least 79 pages).
MIN_SPINE_TEXT = 6.4
#: Text stays this far inside the trim, in millimetres, so that trimming never touches it (printers ask for 3 to 6).
SAFE = 6.0
#: The picture stays this far from the fold at the spine, where binding moves the sheet by a millimetre or two.
SPINE_CLEAR = 4.0
#: The thinnest line and the smallest type that survive printing, in millimetres.
MIN_LINE = 0.12
MIN_TYPE = 2.1


@dataclass(frozen=True)
class PrintSpec:
    """The sheet of a printed cover: back, spine and front, with bleed.

    The defaults are a trim of 170 by 240 mm, within the range of print-on-demand printers and academic publishers,
    with the 3.175 mm (an eighth of an inch) bleed that IngramSpark and KDP ask for. The spine is the page count times
    the thickness of a page, 0.0572 mm for 80 gsm white paper.

    Attributes:
        trim: Width and height of one cover after trimming, in millimetres.
        bleed: Artwork past the trim on the outer sides, in millimetres.
        pages: The number of pages of the book.
        paper: The thickness of one page, in millimetres.

    Examples:
        >>> spec = PrintSpec(pages=400)
        >>> round(spec.spine, 1), round(spec.width, 1)
        (22.9, 369.2)
    """

    trim: tuple[float, float] = (170.0, 240.0)
    bleed: float = 3.175
    pages: int = 400
    paper: float = 0.0572

    @property
    def spine(self) -> float:
        """The width of the spine, in millimetres."""
        return self.pages * self.paper

    @property
    def width(self) -> float:
        """The width of the sheet, in millimetres."""
        return 2 * self.trim[0] + self.spine + 2 * self.bleed

    @property
    def height(self) -> float:
        """The height of the sheet, in millimetres."""
        return self.trim[1] + 2 * self.bleed

    @property
    def scale(self) -> float:
        """Physical millimetres per design millimetre."""
        return self.trim[0] / DESIGN[0]

    @property
    def artwork_fit(self) -> float:
        """How far the proportions of the trim are from those of the A4 artwork, as a fraction; up to 0.02 fits.

        Examples:
            >>> round(PrintSpec().artwork_fit, 3), round(PrintSpec(trim=(155.0, 235.0)).artwork_fit, 2)
            (0.002, 0.07)
        """
        return abs(self.trim[0] / self.trim[1] / (DESIGN[0] / DESIGN[1]) - 1.0)

    @property
    def back_x(self) -> float:
        """The left edge of the back cover trim on the sheet, in millimetres."""
        return self.bleed

    @property
    def front_x(self) -> float:
        """The left edge of the front cover trim on the sheet, in millimetres."""
        return self.bleed + self.trim[0] + self.spine
