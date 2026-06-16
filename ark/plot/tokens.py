"""Brand tokens shared by every plot/table style in :mod:`ark.plot`.

These constants are extracted from the Anthony Faustine personal site's Quarto
theme (``assets/scss/_defaults.scss`` in the ``sambaiga.github.io`` repo) so
that figures and tables produced here read as part of the same brand when
embedded in a tutorial, a blog post, or a published book. They are plain
Python literals (not a live import) because the source of truth is an SCSS
file in a separate repo - update this module by hand if that file's palette
changes.
"""

from __future__ import annotations

# ── Grayscale ────────────────────────────────────────────────────────────────
WHITE = "#FFFFFF"
GRAY_100 = "#F8F9FA"
GRAY_300 = "#DEE2E6"
GRAY_400 = "#CED4DA"
GRAY_600 = "#6B7280"
GRAY_700 = "#495057"
GRAY_900 = "#212529"
BLACK = "#000000"

# ── Semantic brand colors (mirrors $primary/$success/... in _defaults.scss) ──
PRIMARY = "#1E293B"  # $teal -- slate-navy, the site's brand primary
SECONDARY = GRAY_700
SUCCESS = "#059669"  # $green
INFO = "#0369A1"  # $cyan -- also the site's link color
WARNING = "#EA580C"  # $orange
DANGER = "#DC2626"  # $red

# ── Accent colors (site-specific, beyond Bootstrap's semantic set) ───────────
ENERGY_ACCENT = "#10B981"
AI_ACCENT = "#8B5CF6"
PINK = "#FF777C"
YELLOW = "#CA8A04"

# ── Text colors ────────────────────────────────────────────────────────────
TEXT_DARK = "#171717"  # $body-color
TEXT_MUTED = GRAY_600

# ── Surfaces ───────────────────────────────────────────────────────────────
SURFACE = WHITE  # $body-bg
SURFACE_MUTED = GRAY_100  # $code-block-bg
BORDER = GRAY_300

# ── Typography ─────────────────────────────────────────────────────────────
# Loaded as web fonts on the site; matplotlib needs them installed locally to
# render text in the same face, so callers should resolve against installed
# fonts (see plot_theme.resolve_font) rather than assuming these are present.
BODY_FONT_STACK = "'Libre Franklin', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
HEADING_FONT_STACK = "'Jost', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
BODY_FONT_CANDIDATES = ["Libre Franklin", "Segoe UI", "Roboto", "Helvetica Neue", "Arial"]
HEADING_FONT_CANDIDATES = ["Jost", "Segoe UI", "Roboto", "Helvetica Neue", "Arial"]

# ── Qualitative palette for multi-series plots ────────────────────────────────
# Anchored on PRIMARY, then alternates hue families (blue/teal -> warm ->
# green -> red -> purple -> green again, placed away from the first green ->
# warm -> yellow -> neutral) so adjacent series stay distinguishable under
# the common red-green and blue-yellow colorblindness profiles, following
# the same design principle as Wong (2011) and Okabe-Ito.
BRAND_PALETTE = [
    PRIMARY,
    INFO,
    WARNING,
    SUCCESS,
    DANGER,
    AI_ACCENT,
    ENERGY_ACCENT,
    PINK,
    YELLOW,
    GRAY_600,
]
