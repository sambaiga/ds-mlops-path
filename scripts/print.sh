#!/bin/sh
# Render the print edition: the PDF of the parts that are complete (see _quarto-print.yml).
#
# Usage: scripts/print.sh
#
# The notebooks run with the `ark` kernel and with IPYTHONDIR set to this project's .ipython folder, whose startup file
# gives every chart and table a static form (an SVG, LaTeX) next to its HTML, so that the PDF shows them. Needs Quarto
# 1.11 (`uv run quarto`), a LaTeX engine (`uv run quarto install tinytex`) and `rsvg-convert`.
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
IPYTHONDIR="$here/.ipython" QUARTO_PYTHON="$here/.venv/bin/python" \
  uv run quarto render --profile print --to kinyonga-book-pdf
