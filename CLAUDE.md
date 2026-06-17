# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Quarto book (`_quarto.yml`) published to GitHub Pages. It contains:

- **`tutorials/01-python-basics/`** — Jupyter notebooks (Parts 1–2)
- **`tutorials/02-dev-tools/`** — QMD files (Part 3: uv, ruff, type annotations, git, pytest, pre-commit, pydantic)
- **`ark/`** — installable Python package with plot/table utilities used by the notebooks
- **`tutorials/data/`** — shared CSV datasets (`university_analytics.csv`, `courses.csv`, etc.) used across notebooks

## Commands

```bash
# Install all dependencies (first time / after uv.lock changes)
uv sync --extra modelling --extra dev --extra test

# Install pre-commit hooks (required after every fresh clone)
uv run pre-commit install

# Run ruff linter (notebooks + Python files)
uv run ruff check .
uv run ruff check . --fix          # auto-fix safe issues

# Run ruff formatter
uv run ruff format .
uv run ruff format . --check       # CI mode: exit 1 if anything would change

# Run tests (ark package only; notebooks are tested separately)
uv run pytest
uv run pytest tests/path/to/test_file.py::test_name   # single test

# Execute notebooks as tests (slow; mirrors CI)
uv run --with nbmake pytest --nbmake tutorials/01-python-basics/

# Render the Quarto book locally
uv run quarto render

# Preview the book with live reload
uv run quarto preview
```

## CI workflows

Four workflows run on PRs:

| Workflow | Trigger | What it checks |
|---|---|---|
| `ARK CID` | every PR | pre-commit hooks, ruff lint+format, pytest on `ark/`, Quarto render |
| `Check Notebooks` | `.ipynb` or `ark/` changes | executes notebooks via `nbmake` |
| `Check QMD Files` | `.qmd` or `_quarto.yml` changes | em-dashes, code block syntax, inline callout styles, cross-ref targets, unlabelled fences |
| `Publish Book` | merge to `main` | full `quarto render` → deploys to GitHub Pages |

**Common CI failure causes:**
- `ruff format . --check` fails: run `ruff format .` locally and re-commit
- `nbstripout (ci)` hook on push: it strips output; re-add changed notebooks and push again
- QMD "unlabelled fence": opening ` ``` ` without a language tag — add `text`, `python`, `bash`, etc.
- QMD em-dash: replace `—` with `:` or `,`

## Commit conventions

All commits must use Conventional Commits (enforced by `commitizen` hook on `commit-msg`):

```
feat: add rolling window section to 09-pandas-operations
fix: repair cross-ref check in check-qmd.yml
chore: bump ruff to 0.5.0
```

Branches are protected by `no-commit-to-branch` — never commit directly to `main`. Feature branches use `feature/<name>`; fixes use `fix/<name>`.

## Notebook conventions

- **No em-dashes** (`—`) anywhere: replace with `:` or `,`
- **Callout divs in notebooks** use inline `style=` attributes (needed for Colab/Jupyter compatibility). In QMD files, use CSS classes instead (`.ark-concept`, `.ark-activity`, `.ark-tip`, `.ark-mistake`, `.ark-example`)
- The five callout types and their colours:

  | Class / inline colour | Purpose |
  |---|---|
  | `.ark-concept` / `#0369A1` | Key concept |
  | `.ark-activity` / `#009E73` | Hands-on activity |
  | `.ark-tip` / `#7C3AED` | Pro tip |
  | `.ark-mistake` / `#DC2626` | Common mistake |
  | `.ark-example` / `#059669` | Example |

- Section headings in notebooks follow `## N. Title` (number + period + title)
- Activity callouts follow the format `Activity N - Title` with a `Goal:` line and a `TODO` code cell

## QMD-specific rules

- All QMD files must have `---\ntitle: "..."\n---` YAML frontmatter
- Display-only code blocks use ` ```python `, ` ```bash `, ` ```toml `, or ` ```text ` fences — never `{python eval=false}`
- Callout divs use CSS classes, not inline styles
- Cross-references to other files use relative paths; anchor-only links (e.g., `../../index.qmd#callout-guide`) are valid

## `ark` package

The `ark` package lives in `ark/` and is imported by notebooks as `from ark.plot import ...`. Its only current sub-package is `ark.plot`, which provides:

- `tokens.py` — brand colour constants (mirrors `sambaiga.github.io`'s `_defaults.scss`; update by hand if that palette changes)
- `theme.py` / `matplot_theme.py` — Lets-Plot and Matplotlib themes using those tokens
- `gt_style.py` — Great Tables styling
- `diagrams.py` — concept diagram helpers
- `basic_plots.py` — reusable plot wrappers

The package is installed in editable mode (`uv pip install -e .`); the build backend is `hatchling`.

## Theme / brand

- SCSS lives in `tutorials/_quarto/brand.scss`; it mirrors the palette from `sambaiga.github.io/assets/scss/_defaults.scss`
- Primary: `#1E293B`, link/info: `#0369A1`, body: `#171717`
- Fonts: **Jost** (headings), **Libre Franklin** (body), both loaded from Google Fonts
- Keep `ark/plot/tokens.py`, `tutorials/_quarto/brand.scss`, and the upstream site's SCSS in sync by hand
