"""Build the cover files: ``python -m ark.covers [--pages N] [--trim WxH] [--out DIR]``."""

import argparse
from pathlib import Path

from ark.covers.draw import front_only, sheet
from ark.covers.spec import PrintSpec


def parse_trim(text: str) -> tuple[float, float]:
    """Read a trim size such as ``170x240``.

    Args:
        text: The text, in millimetres.

    Returns:
        The width and the height.
    """
    width, height = text.lower().split("x")
    return float(width), float(height)


def main() -> None:
    """Write the wrap (RGB and CMYK), the check sheet and the front cover."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", type=int, default=400, help="pages of the printed book, which set the spine")
    parser.add_argument("--trim", type=parse_trim, default=(170.0, 240.0))
    parser.add_argument("--out", type=Path, default=Path("assets"))
    args = parser.parse_args()
    spec = PrintSpec(trim=args.trim, pages=args.pages)
    out = args.out / "print"
    out.mkdir(parents=True, exist_ok=True)
    fig, _ = sheet(spec)
    fig.savefig(out / "wrap-rgb.pdf")
    fig, _ = sheet(spec, guides=True, barcode_label=True)
    fig.savefig(out / "wrap-guides.png", dpi=110)
    fig, _ = front_only()
    fig.savefig(args.out / "cover-full.pdf")
    fig.savefig(args.out / "cover.png", dpi=130)
    from kinyonga.cmyk import convert

    (out / "wrap-cmyk.pdf").write_bytes(convert((out / "wrap-rgb.pdf").read_bytes()))


if __name__ == "__main__":
    main()
