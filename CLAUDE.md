# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Quarto book (`_quarto.yml`) published to GitHub Pages. It contains:

- **`tutorials/01-python-basics/`** — Jupyter notebooks (Parts 1–2)
- **`tutorials/02-dev-tools/`** — QMD files (Part 3: VS Code, uv, ruff, type annotations, git, pytest, pre-commit, pydantic)
- **`ark/`** — installable Python package with plot/table utilities used by the notebooks
- **`tutorials/data/`** — shared CSV datasets (`university_analytics.csv`, `courses.csv`, etc.) used across all notebooks

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

**Common CI failure causes and fixes:**

- `ruff format . --check` fails: run `ruff format .` locally, re-stage, and commit again (a second commit, not amend)
- `nbstripout (ci)` hook on push: it strips output; re-add the changed notebooks and push again
- QMD "unlabelled fence": opening ```` ``` ```` line without a language tag — add `text`, `python`, `bash`, `toml`, `yaml`, `json`, etc. Closing fences are always bare ```` ``` ```` and are fine
- QMD em-dash check: the `check-qmd.yml` validate job uses a stateful Python parser (tracking `in_block`) to distinguish closing fences from unlabelled opening fences

## Commit conventions

All commits must use Conventional Commits (enforced by `commitizen` hook on `commit-msg`):

```text
feat: add rolling window section to 09-pandas-operations
fix: repair cross-ref check in check-qmd.yml
chore: bump ruff to 0.5.0
```

Branches are protected by `no-commit-to-branch` — never commit directly to `main`. Feature branches use `feature/<name>`; fixes use `fix/<name>`. The pre-commit hooks sometimes auto-format files on the first commit attempt and exit 1; simply re-stage the modified files and commit again (do not amend).

---

## Writing style and content rules

These rules apply to every notebook and QMD file:

- **No em-dashes** (`—`) anywhere. Replace with a colon, comma, or rephrase the sentence. Enforced by a pre-commit hook and a CI check.
- **`ty` not `mypy`**: type checking references use `ty` (Astral's type checker), not `mypy`.
- **No `eval=false`** in code block fences. Use plain language fences (```` ```python ````) for display-only blocks.
- **Narrative-first**: introduce concepts in prose before showing code. State the "why" before the "how".
- **No inline callout styles in QMD**: use CSS classes (`.ark-concept`, etc.). Inline `style=` is only for `.ipynb` files (Colab/Jupyter compatibility).
- **Images**: link externally from authoritative sources (official docs, GitHub, VS Code Marketplace). Always include `alt` text and a `> Source: [Name](url)` citation line. Never commit binary image assets.

---

## Notebook structure and conventions

Every notebook follows this structure:

1. **Badge row** — PDF download badge
2. **Header** — `**DS-MLOps [Part Name]**` / `**Python 3.12+ | Author: Anthony Faustine**`
3. **Before you begin** — cross-reference to callout guide in `index.qmd#callout-guide`, then a table of prerequisite concepts:

   ```markdown
   | Concept | Why you need it |
   |---|---|
   | DataFrames | ... |
   ```

4. **Learning Objectives** — table of numbered skills with section references:

   ```markdown
   | # | Skill | Covered in |
   |---|---|---|
   | 1 | ... | Sec. 1 |
   ```
5. **Sections** numbered `## N. Title` (number + period + title)
6. **Capstone** — a final activity tying sections together
7. **Summary** — table of `| Concept | Key rule |` rows
8. **Further Reading** — table of `| Resource | Why it matters |` rows

**The callout guide lives only in `index.qmd`** — never repeat it in notebook cells. Notebooks reference it with a one-liner:

```markdown
> Callout markers used throughout this notebook are explained on the [book cover page](../../index.qmd#callout-guide).
```

### Activity format

Activities follow this exact pattern (Activity N uses a dash, not a colon, before the title):

```html
<div style='background:#EBF5F0;border-left:5px solid #009E73;padding:14px 18px;border-radius:6px;margin:16px 0'>
<span style='color:#065F46;font-weight:bold'><i class="bi bi-puzzle-fill"></i> Activity N - Title</span><br><br>
<b>Goal:</b> One sentence describing what the learner must do.
<pre>starter code here</pre>
</div>
```

Followed immediately by a code cell:

```python
# TODO: your solution here
```

### Callout divs in notebooks (inline styles — required for Colab)

| Type | Background | Border | Title colour |
| --- | --- | --- | --- |
| Key Concept | `#EAF3FA` | `#0369A1` | `#0369A1` |
| Activity | `#EBF5F0` | `#009E73` | `#065F46` |
| Pro Tip | `#F5F3FF` | `#7C3AED` | `#5B21B6` |
| Common Mistake | `#FEF2F2` | `#DC2626` | `#991B1B` |
| Example | `#EAF7F0` | `#059669` | `#059669` |

---

## QMD-specific rules

- All QMD files must have `---\ntitle: "..."\n---` YAML frontmatter as the very first line
- Display-only code blocks use ` ```python `, ` ```bash `, ` ```toml `, ` ```yaml `, ` ```text `, ` ```json ` fences — never `{python eval=false}`
- Callout divs use CSS classes: `.ark-concept`, `.ark-activity`, `.ark-tip`, `.ark-mistake`, `.ark-example`
- All QMD chapters start with `## Before you begin` and the callout guide cross-ref
- Learning Objectives table is required in every chapter
- Cross-references use relative paths; anchor-only fragments like `../../index.qmd#callout-guide` are valid and the CI validator strips the `#fragment` before checking file existence

---

## Batch-editing notebooks

**Never use `NotebookEdit` for inserting multiple cells** — the tool errors with "file modified since read" when a formatter runs between edits. Instead, manipulate the notebook JSON directly with a Python script:

```python
import json, uuid

def make_cell(cell_type, source):
    c = {"cell_type": cell_type, "id": uuid.uuid4().hex[:8], "metadata": {}, "source": source}
    if cell_type == "code":
        c.update({"outputs": [], "execution_count": None})
    return c

with open("tutorials/01-python-basics/08-pandas-core.ipynb") as f:
    nb = json.load(f)

# Find insertion point
insert_after = next(i for i, c in enumerate(nb["cells"])
                    if "## Capstone" in "".join(c["source"]))

new_cells = [make_cell("markdown", "## 8. New Section\n\nContent here."),
             make_cell("code", "# code here")]

for c in reversed(new_cells):
    nb["cells"].insert(insert_after, c)

with open("tutorials/01-python-basics/08-pandas-core.ipynb", "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")
```

Always call `uv run ruff format <notebook>` after writing and before committing — CI checks formatting on notebooks too.

---

## Dataset: `university_analytics.csv`

2,400 rows × 18 columns, seed=42, generated by `tutorials/data/generate_dataset.py`. Used in all Part 2 notebooks and the `grade-predictor` dev-tools project thread.

Key columns and their types:

| Column | Type | Notes |
|---|---|---|
| `student_id` | str | Format `S0001`..`S2400` |
| `program` | str | `CS`, `DS`, `IT`, `Engineering`, `Sciences` |
| `semester` | str | `Fall`, `Spring`, `Summer` |
| `midterm_score` | float | 0–100 |
| `final_score` | float | 0–100 |
| `project_score` | float | 0–100 |
| `average_marks` | float | Weighted mean of the three scores |
| `passed` | bool | `average_marks >= 60` |
| `has_internet` | bool | Home internet access |
| `school_id` | str | For attendance join examples |

Companion file `courses.csv` (6 rows) has `course_id`, `course_name`, `credits` — used for merge/join examples in `10-combining-reshaping.ipynb`.

**Column name history**: an older dataset used `mathematics/english/science_marks`, `caste`, `internet`. The current column names above are the canonical ones. Do not use the old names.

---

## The `grade-predictor` project thread

All Part 3 chapters build on a single project called `grade-predictor` created with `uv init grade-predictor --package`. Its `core.py` exposes three public functions that grow chapter by chapter:

- `compute_grade(midterm, final, project, weights)` — weighted average
- `grade_to_letter(midterm, final, project)` — returns `A`/`B`/`C`/`D`/`F`
- `flag_at_risk(df, threshold)` — boolean Series, students below threshold

Chapters add to this codebase: ruff cleans it (Part 14), type annotations are added (Part 15), git tracks it (Part 16), pytest tests it (Part 17), pre-commit automates checks (Part 18), and Pydantic validates its inputs (Part 19).

---

## Content audit criteria

When reviewing a tutorial for "important content we can add", check for:

- **Missing DS/ML best practice**: does the section show what actually happens in production? (e.g., timezone handling, lag features, memory profiling)
- **Silent bug patterns**: fan-out in merges, mutable defaults, over-mocking, mixing tz-naive and tz-aware timestamps
- **Missing conceptual comparisons**: when introducing a tool, compare it to the alternatives the reader already knows
- **Install/setup gap**: if a chapter uses a CLI tool, check that installation and first-time configuration are covered before the first use
- **Activity coverage**: every major section needs at least one Activity callout with a `Goal:` and a `TODO` code cell
- **Summary and Further Reading tables**: required at the end of every chapter

---

## Chapter content added (Part 2 notebooks)

Sections added in the `feature/dev-tools-part3` branch — do not duplicate these:

- `08-pandas-core`: Sec 8 — `memory_usage(deep=True)`, `.astype("category")`, low-cardinality auto-detection
- `09-pandas-operations`: Sec 5 — `rolling(n).mean()`, `expanding().mean()`, per-group rolling via `groupby().transform()`, `df.query("expr @var")`
- `10-combining-reshaping`: many-to-one vs one-to-many merge fan-out, `assert len(before) == len(after)` diagnostic
- `11-polars`: Sec 7 — `pl.col().mean().over("group")`, `rolling_mean().over()`, `scan_csv`/`scan_parquet`, `.collect(streaming=True)`
- `11-time-series`: Sec 5 — `tz_localize`, `tz_convert`, UTC storage rule; Sec 6 — `shift(n)` lag/lead, `rolling().mean()` as features, `autocorr(lag=n)`

---

## Chapter content added (Part 3 QMD files)

Sections added in the `feature/dev-tools-part3` branch — do not duplicate these:

- `02-code-quality-ruff.qmd`: Sec 6 — Google docstring style, ruff `D` rule group with `convention = "google"`, `[tool.ruff.lint.pydocstyle]`, codespell pre-commit hook with `--write-changes`, `[tool.codespell]` in `pyproject.toml`
- `05-pytest-testing.qmd`: Sec 8 — `unittest.mock.patch`, patch-at-import-location rule (`"grade_predictor.io.requests.get"` not `"requests.get"`), pandas `read_csv` mocking, `pytest-mock` mocker fixture, over-mocking anti-pattern
- `07-pydantic-validation.qmd`: full new chapter — `BaseModel`, `Field` with `ge`/`le`, `field_validator`, `model_validator(mode="after")`, `BaseSettings` with `env_prefix`, nested `WeightConfig`/`PipelineConfig`, batch validation with error collection, `TypeAdapter`

Sections added in the `feature/dev-tools-improvements` branch:

- `00-vscode-setup.qmd`: new chapter — install VS Code, 9 extensions with marketplace IDs, `settings.json` for ruff format-on-save, `.venv` interpreter setup, Jupyter kernel, GitLens, integrated terminal
- `01-uv-project-setup.qmd`: Sec 0 — what uv is, comparison table vs pip/Poetry/conda, install commands
- `04-git-github.qmd`: Sec 0 — install git, `git config --global`, GitHub vs GitLab comparison, SSH key setup
- `06-pre-commit-automation.qmd`: Sec 0 — what pre-commit is, install via uv/pipx/brew

---

## `ark` package

The `ark` package lives in `ark/` and is imported by notebooks as `from ark.plot import ...`. Its only current sub-package is `ark.plot`, which provides:

- `tokens.py` — brand colour constants (mirrors `sambaiga.github.io`'s `_defaults.scss`; update by hand if that palette changes)
- `theme.py` / `matplot_theme.py` — Lets-Plot and Matplotlib themes using those tokens
- `gt_style.py` — Great Tables styling
- `diagrams.py` — concept diagram helpers
- `basic_plots.py` — reusable plot wrappers

The package is installed in editable mode (`uv pip install -e .`); the build backend is `hatchling`.

---

## Theme and brand

- SCSS lives in `tutorials/_quarto/brand.scss`; it mirrors the palette from `sambaiga.github.io/assets/scss/_defaults.scss`
- Primary: `#1E293B`, link/info: `#0369A1`, body: `#171717`
- Fonts: **Jost** (headings), **Libre Franklin** (body), both loaded from Google Fonts
- Keep `ark/plot/tokens.py`, `tutorials/_quarto/brand.scss`, and the upstream site's SCSS in sync by hand

CSS classes added to `brand.scss` for the cover page: `.part-card` (with `.part-complete`, `.part-in-progress`, `.part-coming-soon` modifiers), `.part-badge` (with `.badge-complete`, `.badge-in-progress`, `.badge-coming-soon`), `.cover-hero`, `.cover-stat-row`, `.cover-stat`, `.btn-cover` (with `.btn-primary-cover`, `.btn-secondary-cover`), `.section-label`.

---

## Cover page (`index.qmd`) conventions

- Parts with all chapters merged to `main` get the `part-complete` card with green badge and full chapter link list
- Parts in active development get `part-in-progress` (blue badge)
- Future parts get `part-coming-soon` (grey badge, no chapter links)
- The hero section stats (Parts / Chapters / Complete) must be updated when new parts complete
- "Jump to Part N" CTA button points to the first chapter of that part
