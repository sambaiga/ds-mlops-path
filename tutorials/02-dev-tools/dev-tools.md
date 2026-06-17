# Part 3: Dev Tools — Implementation Plan

## Overview

Part 3 teaches the professional toolchain every DS/MLOps practitioner uses daily: project
management with uv, code quality with ruff, type safety with ty, version control with git,
testing with pytest, and automation with pre-commit. Each chapter advances a single running
mini-project called `grade-predictor` — a small Python package built on top of
`university_analytics.csv` — so every tool has a real codebase to act on.

## Running project thread: `grade-predictor`

Students build this package incrementally across all six chapters:

```
grade-predictor/
├── src/
│   └── grade_predictor/
│       ├── __init__.py
│       ├── core.py          ← grade computation and risk flagging
│       └── config.py        ← settings loaded from environment variables
├── tests/
│   ├── conftest.py          ← shared fixtures
│   └── test_core.py         ← unit tests
├── scripts/
│   └── report.py            ← CLI entry point
├── .env                     ← secrets, never committed
├── .gitignore
├── .pre-commit-config.yaml
└── pyproject.toml
```

The same dataset (`university_analytics.csv`) anchors every example.  
Callout colors, narrative voice, section numbering, and activity format are identical to Parts 1 and 2.

---

## Format decisions

| Chapter | File | Format | Reason |
|---|---|---|---|
| 01 | `01-uv-project-setup.qmd` | `.qmd` | Shell-heavy; `uv` commands change the filesystem |
| 02 | `02-code-quality-ruff.qmd` | `.qmd` | `ruff` runs as a CLI; inline HTML callout divs |
| 03 | `03-type-annotations.ipynb` | `.ipynb` | Live Python execution shows type errors inline |
| 04 | `04-git-github.qmd` | `.qmd` | Git commands require a real repo and credentials |
| 05 | `05-pytest-testing.qmd` | `.qmd` | Pytest runs as a CLI; `{python}` blocks for code examples |
| 06 | `06-pre-commit-automation.qmd` | `.qmd` | Hooks require git; YAML config shown statically |

All `.qmd` files use `{bash eval=false}` for shell display blocks and `{python}` for executed
Python examples. All use the same HTML div callouts as the notebooks (not Quarto-native callouts)
for visual consistency across the book.

---

## Chapter 01: uv — Project Setup and Reproducible Environments

**File:** `tutorials/02-dev-tools/01-uv-project-setup.qmd`

### Before you begin

Assumes completion of Part 1 and Part 2. No prior experience with virtual environments
required — but if you have used `pip` and `venv` before, every concept here maps directly.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Explain why isolated environments and lockfiles matter for reproducible DS work | Sec. 1 |
| 2 | Initialize a packaged Python project with `uv init --package` | Sec. 2 |
| 3 | Read and write the `[project]` and `[project.optional-dependencies]` sections of `pyproject.toml` | Sec. 3 |
| 4 | Add, remove, and sync dependencies with `uv add`, `uv remove`, and `uv sync` | Sec. 4 |
| 5 | Separate heavy ML dependencies into optional groups so CI stays fast | Sec. 5 |
| 6 | Manage secrets with a `.env` file and keep them out of version control | Sec. 6 |
| 7 | Run any command inside the project environment with `uv run` | Sec. 7 |

### Sections

**Sec. 1 — The reproducibility problem**

Open with the concrete failure: two colleagues, same code, different results because
`pandas 1.5` and `pandas 2.0` handle missing values differently. Show why `pip install`
with no lockfile cannot solve this. Explain what a virtual environment is (isolated Python
interpreter + packages), what a lockfile adds (exact versions of every dependency including
transitive ones), and why uv provides both in one tool.

*Key Concept callout:* "A lockfile is a snapshot of the exact environment that worked.
`uv.lock` is that snapshot for every project in this book."

**Sec. 2 — Initializing a project**

Walk through creating `grade-predictor`:

```bash
uv init grade-predictor --package
cd grade-predictor
```

Explain the generated files: `pyproject.toml` (project metadata and dependencies),
`src/grade_predictor/__init__.py` (the package), `.python-version` (pins the Python version),
`uv.lock` (generated on first sync). Explain the src layout: why the package lives inside `src/`
rather than at the root (import isolation during development prevents accidentally importing
from the wrong place).

*Activity 1:* Run `uv init grade-predictor --package`, inspect the generated files,
then open `pyproject.toml` and identify the `[project]` section.

**Sec. 3 — pyproject.toml anatomy**

Walk through every section relevant to a DS project:

- `[project]`: name, version, requires-python, authors, dependencies
- `[project.optional-dependencies]`: dev, test, modelling groups
- `[tool.pytest.ini_options]`: testpaths, addopts
- `[tool.ruff]`: target-version, line-length (covered in ch02 but introduced here)

Show the full `pyproject.toml` for `grade-predictor` with annotations. Explain `requires-python`
and why pinning `>=3.12` matters for reproducibility.

*Key Concept callout:* "`pyproject.toml` is the single source of truth for a Python project.
It replaces `setup.py`, `requirements.txt`, `setup.cfg`, and `pytest.ini`. Learn to read
it and you can understand any modern Python project in under five minutes."

**Sec. 4 — Adding and syncing dependencies**

```bash
uv add pandas numpy
uv add --dev pytest ruff
uv sync
uv run python -c "import pandas; print(pandas.__version__)"
```

Explain the difference between `uv add` (adds to `pyproject.toml` + updates `uv.lock`)
and `pip install` (installs to whatever environment is active, no record kept).
Show `uv.lock` and explain why it is committed to version control but `requirements.txt`
derived from it is not needed.

*Activity 2:* Add `polars` as a core dependency, then add `jupyter` to the `dev` group.
Confirm with `uv run python -c "import polars"`.

**Sec. 5 — Optional dependency groups for heavy ML dependencies**

This is the gap in all standard references. Show why separating heavy dependencies matters:

```toml
[project.optional-dependencies]
modelling = [
    "scikit-learn>=1.7",
    "xgboost>=3.0",
    "torch>=2.0",
]
test = [
    "pytest>=8.0",
    "pytest-cov>=6.0",
]
dev = [
    "ruff>=0.5",
    "pre-commit>=4.0",
]
```

Then show `uv sync` (core only, CI fast path), `uv sync --extra test` (add test deps),
`uv sync --all-extras` (full local development). Explain: CI installs core + test only.
Local development installs everything. Docker production images install core only.

*Pro Tip callout:* "Keep `torch` in an optional group. A cold CI run that installs PyTorch
takes 3-4 minutes. One that installs only `pandas` and `pytest` takes under 30 seconds."

*Activity 3:* Add a `modelling` group with `scikit-learn`. Run `uv sync` and confirm
scikit-learn is NOT installed. Run `uv sync --extra modelling` and confirm it is.

**Sec. 6 — Secret management with `.env`**

Introduce the concrete failure: a database password or API key committed to a public GitHub
repository is searchable, permanent (even after deletion from history), and a real security
incident. Show the correct pattern:

Create `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/grades
OPENAI_API_KEY=sk-...
```

Add to `.gitignore`:
```
.env
*.env
```

Load in Python with `python-dotenv`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
```

Add `.env.example` (committed, no real values) so collaborators know which variables to set.

*Common Mistake callout:* "Never put secrets in `pyproject.toml`, `config.yaml`, or any
committed file — even as defaults. If the default is the real value, it will end up in git."

*Activity 4:* Create `.env` with a `REPORT_TITLE` variable. Load it in a Python script
with `python-dotenv`. Confirm `.env` is in `.gitignore` before committing anything.

**Sec. 7 — uv run: the universal entry point**

Show that `uv run` is the correct way to execute anything inside the project environment:

```bash
uv run python scripts/report.py          # run a script
uv run pytest                             # run tests
uv run ruff check .                       # lint
uv run jupyter lab                        # open Jupyter
uv run --with httpx python -c "import httpx"  # one-off tool without installing
```

Explain: `uv run` automatically activates the project environment without requiring
`source .venv/bin/activate`, so shell state never leaks between projects.

**Capstone:** Build the complete `grade-predictor` project structure from scratch:
create the project, add dependencies, write `src/grade_predictor/core.py` with a
`compute_grade(midterm, final, project)` function, run it with `uv run`, and confirm
the environment is isolated.

### Further Reading

| Resource | Why it matters |
|---|---|
| [uv documentation — Projects](https://docs.astral.sh/uv/concepts/projects/) | The authoritative reference for every `uv` command |
| fmind MLOps course, [1.2 uv](https://mlops-coding-course.fmind.dev/1.%20Initializing/1.2.%20uv.html) | MLOps-specific framing of uv's role in CI and Docker |
| pybit.es, [Developing packages with uv](https://pybit.es/articles/developing-and-testing-python-packages-with-uv/) | Src layout explained with editable installs |
| [python-dotenv documentation](https://saurabh-kumar.com/python-dotenv/) | The standard library for `.env` loading |
| PEP 517/518 — [pyproject.toml specification](https://peps.python.org/pep-0518/) | The spec behind every `pyproject.toml` field |

### Summary

| Concept | Key rule |
|---|---|
| Virtual environment | One per project. Never install into the system Python. |
| `uv init --package` | Src layout is the safe default: it prevents accidental imports from the wrong place |
| `uv.lock` | Commit it. It pins the exact environment that worked. |
| Optional dependency groups | Keep heavy ML deps in `modelling`/`gpu` groups. CI syncs core + test only. |
| `.env` | Never commit it. Commit `.env.example` instead. |
| `uv run` | Use it for everything. No manual venv activation needed. |

---

## Chapter 02: Code Quality with ruff

**File:** `tutorials/02-dev-tools/02-code-quality-ruff.qmd`

### Before you begin

Assumes completion of Ch01. The `grade-predictor` project from Ch01 is the codebase
ruff will run on. If starting here, clone the companion repo and `cd` into `grade-predictor`.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Explain what a linter checks vs what a formatter changes | Sec. 1 |
| 2 | Run `ruff check` and interpret its output | Sec. 2 |
| 3 | Run `ruff format` and understand why formatting is a team decision | Sec. 3 |
| 4 | Configure ruff in `pyproject.toml` with rules relevant to DS code | Sec. 4 |
| 5 | Identify the lint rules that catch the most common DS bugs | Sec. 5 |
| 6 | Use `# noqa` and per-file ignores correctly | Sec. 6 |

### Sections

**Sec. 1 — Linter vs formatter: two different jobs**

A formatter rewrites code layout (indentation, line length, quotes) without changing behavior.
A linter reads code and flags patterns that are wrong, suspicious, or inconsistent — some
of which can silently produce bad results in DS code. Ruff does both, but they are separate
commands with separate purposes.

*Key Concept callout:* "Formatting is about style. Linting is about correctness. A formatter
can never catch `df.drop('column')` without `inplace=True` doing nothing silently. A linter can."

**Sec. 2 — Running ruff check**

Start with intentionally messy `core.py` (unused imports, bare `except`, mutable default argument,
undefined variable). Show `ruff check .` output. Explain the rule code format (`F401`, `E501`, etc.),
what each finding means, and how to fix each one. Show `ruff check . --fix` for auto-fixable issues.

*Activity 1:* Add three intentional issues to `core.py` (an unused import, a bare `except:`,
and a variable defined but never used). Run `ruff check .` and read the output. Fix each one.

**Sec. 3 — Running ruff format**

Show `ruff format .` (formats in place) and `ruff format . --check` (exits non-zero if anything
would change, used in CI). Explain: the formatter is opinionated and non-configurable by design.
The only decision is line length. Show before/after on a messy function.

*Pro Tip callout:* "Set up your editor to run `ruff format` on save. Never think about
indentation again. CI catches the rare case where auto-format didn't run."

**Sec. 4 — Configuration in pyproject.toml**

Walk through a practical DS configuration:

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "N", "UP", "SIM"]
ignore = ["E402"]                        # module-level imports not at top: notebooks need this

[tool.ruff.lint.per-file-ignores]
"notebooks/**" = ["E501", "F811"]        # notebooks: long lines and redefined names are ok
"tests/**" = ["S101"]                    # tests: assert is expected
```

Explain each rule group: `E`/`W` (pycodestyle), `F` (pyflakes, catches real bugs), `I` (isort),
`B` (bugbear, DS-relevant), `N` (naming), `UP` (pyupgrade), `SIM` (simplifications).

**Sec. 5 — The lint rules that catch real DS bugs**

Focus on the bugbear rules most relevant to DS work:

- `B006`: mutable default argument — `def train(config: dict = {})` creates one dict shared
  across all calls
- `B007`: loop variable unused — for loop that never uses the iteration variable
- `B023`: function defined in loop — a common ML gotcha with callbacks and closures
- `F841`: local variable assigned but never used — silent dead code in pipeline steps
- `SIM108`: ternary simplification — cleaner transformations

Show each with a concrete grade-predictor example.

*Common Mistake callout:* "The mutable default argument (`B006`) is the most common silent
bug in DS code. `def split(df, cols=[])` shares the same list object across every call.
The second call gets the first call's leftover data."

**Sec. 6 — noqa and when to use it**

Show `# noqa: E501` (suppress one rule on one line) and when suppressing is legitimate
(a URL that cannot be shortened, a regex that must stay on one line). Contrast with
`per-file-ignores` for notebooks. Emphasize: a `noqa` comment is a decision, not a fix.

*Activity 2:* Configure ruff in `pyproject.toml` with the DS ruleset above. Run `ruff check .`
on `grade-predictor/src`. Fix every finding without using `noqa`.

**Capstone:** Apply ruff check and ruff format to the full `grade-predictor` project.
Fix all findings. Add a ruff CI step to `pyproject.toml` that fails if formatting is needed.

### Further Reading

| Resource | Why it matters |
|---|---|
| [ruff documentation](https://docs.astral.sh/ruff/) | Complete rule reference and configuration guide |
| [Bugbear rules](https://docs.astral.sh/ruff/rules/#flake8-bugbear-b) | The rules most likely to catch real DS bugs |
| [ruff vs Black/Flake8](https://docs.astral.sh/ruff/faq/#how-does-ruff-compare-to-flake8) | Why ruff replaced a two-tool workflow |
| [pyupgrade rules](https://docs.astral.sh/ruff/rules/#pyupgrade-up) | Automatic modernization of Python syntax |

### Summary

| Concept | Key rule |
|---|---|
| `ruff check` | Finds bugs and style issues. Does not rewrite code unless `--fix` is passed. |
| `ruff format` | Rewrites layout only. Cannot introduce bugs. |
| Rule groups | `E/F` always. `B` for DS. `I` for import order. Add others as needed. |
| `per-file-ignores` | Use for notebooks and tests, not for hiding real problems. |
| CI check | `ruff format . --check` exits 1 if anything would change. Always run in CI. |

---

## Chapter 03: Type Annotations and Static Analysis

**File:** `tutorials/02-dev-tools/03-type-annotations.ipynb`  
**Format:** `.ipynb` (executed Python in Jupyter)

### Before you begin

Assumes completion of Ch01 and Ch02. This is the one notebook in Part 3 because type
annotations are pure Python: running annotated functions live shows the gap between what
Python accepts at runtime vs what a type checker rejects statically.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Write type-annotated function signatures for DS functions | Sec. 1 |
| 2 | Use `int | float | None`, `list[...]`, `tuple[...]`, and `dict[...]` correctly | Sec. 2 |
| 3 | Annotate numpy arrays and pandas DataFrames | Sec. 3 |
| 4 | Use `TypeAlias` and `Protocol` to name complex DS types | Sec. 4 |
| 5 | Configure ty in `pyproject.toml` and interpret its output | Sec. 5 |
| 6 | Apply gradual typing: where to start and what to skip | Sec. 6 |

### Sections

**Sec. 1 — Why type annotations matter in DS code**

Show two versions of the same function: with and without annotations. The annotated version
is self-documenting, catches the wrong-unit bug (`score` passed as 0-1 when 0-100 expected)
before runtime, and makes autocomplete work. Python does not enforce annotations at runtime
by default — that is what a type checker does.

*Key Concept callout:* "Annotations are documentation that a machine can check. They tell
collaborators (and your future self) what a function expects and returns, without writing
a word of prose."

**Sec. 2 — Basic annotations**

Cover: `int`, `float`, `str`, `bool`, `None`, `int | float`, `float | None`,
`list[float]`, `tuple[float, float, float]`, `dict[str, float]`. All with grade-predictor examples:

```python
def compute_grade(
    midterm: float,
    final: float,
    project: float,
    weights: tuple[float, float, float] = (0.30, 0.45, 0.25),
) -> float:
    return midterm * weights[0] + final * weights[1] + project * weights[2]
```

Show that Python happily runs `compute_grade("82", 91.0, 88.0)` — the annotation does not
enforce at runtime. Show that ty would flag this as a type error.

*Activity 1:* Annotate three functions in `core.py`. Include one with a `float | None`
parameter (for a nullable score) and one that returns `dict[str, float]`.

**Sec. 3 — Annotating numpy arrays and pandas DataFrames**

This is the gap in all standard references. Show the practical patterns:

```python
import numpy as np
import pandas as pd
from numpy.typing import NDArray

# numpy: use NDArray[np.float64] for typed arrays
def normalize(X: NDArray[np.float64]) -> NDArray[np.float64]:
    return (X - X.mean(axis=0)) / X.std(axis=0)

# pandas: DataFrame and Series are generic in recent pandas versions
def flag_at_risk(df: pd.DataFrame, threshold: float = 50.0) -> pd.Series:
    return df["average_marks"] < threshold
```

Explain the limitation: `pd.DataFrame` does not carry column-level type information at the
Python type system level. For that, introduce `pandera` briefly as the next step (in the
testing chapter). For `numpy`, `NDArray[np.float64]` is the correct annotation from
`numpy.typing`.

*Pro Tip callout:* "For pandas, `pd.DataFrame` is a practical annotation even though it
carries no column info. The alternative is `pandera.typing.DataFrame[Schema]` — introduced
in Ch05. Start with `pd.DataFrame` and graduate to pandera when you need column-level guarantees."

**Sec. 4 — TypeAlias and Protocol for complex DS types**

Show `TypeAlias` for naming recurring types:

```python
from typing import TypeAlias

ScoreVector: TypeAlias = list[float]
GradeMap: TypeAlias = dict[str, float]
```

Show `Protocol` for duck-typed DS objects (any object with a `.predict` method):

```python
from typing import Protocol

class Predictor(Protocol):
    def predict(self, X: NDArray[np.float64]) -> NDArray[np.float64]: ...
```

Explain when to use each. TypeAlias: when you write the same complex type in three or more
places. Protocol: when you want to accept any sklearn-compatible model without importing sklearn.

**Sec. 5 — Configuring ty**

Show a minimal `pyproject.toml` configuration:

```toml
[tool.ty]
python-version = "3.12"
```

Run `uv run ty check src/` on `grade-predictor`. Show how to read the output.
Explain the difference between an error (must fix) and a warning (consider fixing).
Show `--ignore-missing-imports` for third-party packages without stubs.

*Activity 2:* Add type annotations to all functions in `core.py`. Run `ty check src/`.
Fix every error. Leave the output clean before moving to Ch04.

**Sec. 6 — Gradual typing: where to start**

Concrete priorities for a DS codebase:
1. Public function signatures first (what callers see)
2. Return types before argument types (catches more bugs)
3. Skip internal helpers and notebooks initially
4. Add `Any` as a placeholder when you need to annotate something complex you will refine later

*Common Mistake callout:* "Trying to annotate everything at once is the wrong approach.
`Any` is not giving up — it is a marker that says 'this is untyped, I know it, I will return
to it'. A codebase with 80% annotated functions and no `Any` is better than 40% annotated
functions with 40% annotated badly."

**Capstone:** Fully annotate `grade-predictor/src/grade_predictor/core.py`.
Run `ty check src/` and bring the output to zero errors.

### Further Reading

| Resource | Why it matters |
|---|---|
| [ty documentation](https://github.com/astral-sh/ty) | Astral's type checker, integrated with the uv/ruff toolchain |
| [numpy.typing](https://numpy.org/doc/stable/reference/typing.html) | `NDArray` and array annotation reference |
| [ty documentation](https://github.com/astral-sh/ty) | Astral type checker; authoritative reference for ty errors and configuration |
| PEP 544 — [Protocols](https://peps.python.org/pep-0544/) | The spec behind structural subtyping for duck-typed ML objects |
| [pandas type stubs](https://github.com/pandas-dev/pandas-stubs) | Official stubs for IDE-level type inference on DataFrames |

### Summary

| Concept | Key rule |
|---|---|
| Runtime vs static | Python does not enforce annotations at runtime. A type checker does. |
| `NDArray[np.float64]` | The correct annotation for a typed numpy array |
| `pd.DataFrame` | Practical but untyped at the column level. Pandera adds column types. |
| `TypeAlias` | Name a complex type you repeat three or more times |
| `Protocol` | Accept any object with a given method, without importing its concrete class |
| Gradual typing | Start with public function signatures. Use `Any` as a placeholder, not a cop-out. |

---

## Chapter 04: Git and GitHub for Data Science

**File:** `tutorials/02-dev-tools/04-git-github.qmd`

### Before you begin

Assumes completion of Ch01–Ch03. The `grade-predictor` project should be fully set up
with type-annotated code and ruff clean. This chapter versions that project with git.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Initialize a git repository and write a correct `.gitignore` for a DS project | Sec. 1 |
| 2 | Understand the three-state model: working tree, staging area, and commit history | Sec. 2 |
| 3 | Write conventional commits that serve as a searchable project log | Sec. 3 |
| 4 | Use branches for experiments without breaking working code | Sec. 4 |
| 5 | Open a pull request and understand why code review matters for DS | Sec. 5 |
| 6 | Write a GitHub Actions workflow that runs tests on every push | Sec. 6 |

### Sections

**Sec. 1 — What git tracks and what it must not**

Explain git as a time machine for code, not data. A DS-specific `.gitignore` is not optional:

```gitignore
# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
dist/

# Environment and secrets
.env
*.env
.env.local

# Data files (large; use DVC or cloud storage instead)
*.csv
*.parquet
*.pkl
*.h5
data/raw/
data/processed/

# Model artifacts
models/
*.pt
*.onnx

# Jupyter artifacts
.ipynb_checkpoints/
*-checkpoint.ipynb

# IDE
.idea/
.vscode/settings.json
```

Explain each group. Emphasize: secrets in git are permanent. Even after `git rm`, the file
exists in history and is searchable on GitHub.

*Key Concept callout:* "Git tracks code. Data, models, and secrets belong elsewhere.
A 2GB CSV committed by accident is hard to remove cleanly. It is easier to never commit it."

**Sec. 2 — The three-state model**

Explain working tree (what is on disk), staging area (what will go into the next commit),
and commit history (what is permanent). Show the flow:

```bash
git init
git status                            # see the three states
git add src/grade_predictor/core.py   # move to staging
git commit -m "feat: add compute_grade function"
git log --oneline                     # inspect history
```

*Common Mistake callout:* "`git add .` adds everything, including `.env`, `data/`, and
generated files. Always use `git add <specific files>` or `git add -p` to stage
interactively. Run `git status` before every commit."

**Sec. 3 — Conventional commits**

Explain the format: `type(scope): description`. Types used in DS/MLOps work:

| Type | When to use |
|---|---|
| `feat` | New capability: a new model, a new data pipeline step, a new API endpoint |
| `fix` | Corrects a bug: wrong normalization, off-by-one in a split, a missing fillna |
| `refactor` | Restructures code without changing behavior: extract a function, rename a variable |
| `test` | Adds or updates tests only |
| `docs` | Documentation only: docstrings, README, notebook prose |
| `chore` | Tooling and housekeeping: update dependencies, fix CI, bump versions |
| `data` | Data changes: new dataset version, updated schema, changed preprocessing |

Show real examples from a DS workflow:

```
feat(model): add gradient boosting baseline with 5-fold CV
fix(preprocessing): normalize features before train/test split
data(university): update university_analytics.csv to include 2025 cohort
refactor(core): extract grade_to_letter from compute_grade
test(core): parametrize grade boundary tests for all letter grades
```

Explain commitizen (`cz commit`) as the tool that enforces this format and generates
changelogs automatically.

**Sec. 4 — Branches for experiments**

Show the branch workflow for a DS experiment:

```bash
git checkout -b experiment/xgboost-baseline
# ... make changes ...
git add src/
git commit -m "feat(model): add xgboost baseline, acc=0.84"
git checkout main
git merge experiment/xgboost-baseline
```

Explain why a separate branch per experiment keeps `main` always working and makes
comparing experiments straightforward. Note: this is different from MLflow experiment
tracking (runs) — branches track code changes, MLflow tracks metric outcomes.

*Pro Tip callout:* "Name experiment branches `experiment/<what-you-tried>`, not `feature/<name>`.
The naming communicates that the branch may be abandoned without guilt. A dead experiment
branch costs nothing to delete."

**Sec. 5 — Pull requests and code review**

Explain what a PR is (a request to merge a branch into main, plus a conversation).
Show: `git push -u origin experiment/xgboost-baseline`, then open a PR on GitHub.
Explain what to put in a PR description for DS work: what changed, why, what metrics
were observed, what tests were added. Explain what reviewers look for.

**Sec. 6 — GitHub Actions for automated testing**

Walk through the exact CI workflow that this book uses for its own notebooks, adapted
for `grade-predictor`:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --extra test
      - run: uv run pytest tests/ --override-ini=addopts=
```

Explain each step. Explain `--override-ini=addopts=` (strips local pytest flags that
reference local paths not present in CI). Show how to read the Actions log when CI fails.

*Activity:* Write a GitHub Actions workflow for `grade-predictor` and push it.
Watch it run on GitHub. Fix a failing test by reading the CI log.

**Capstone:** Git-initialize `grade-predictor`, write a proper `.gitignore`, make three
conventional commits (one for each file added), push to GitHub, and confirm the Actions
workflow runs green.

### Further Reading

| Resource | Why it matters |
|---|---|
| [Conventional Commits specification](https://www.conventionalcommits.org/) | The format this book uses throughout |
| [commitizen documentation](https://commitizen-tools.github.io/commitizen/) | The tool that enforces and automates conventional commits |
| [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) | Official guide with uv and pytest examples |
| [gitignore.io](https://www.toptal.com/developers/gitignore) | Generator for `.gitignore` files by language and IDE |
| [DVC documentation](https://dvc.org/doc) | Data Version Control: the git equivalent for datasets and models |

### Summary

| Concept | Key rule |
|---|---|
| `.gitignore` | Secrets, data files, model weights, and virtualenvs never go in git |
| Staging area | `git add <specific files>`. Never `git add .` without checking `git status` first |
| Conventional commits | `type(scope): description`. The type and scope make `git log` searchable |
| Branches | One branch per experiment or feature. `main` stays working at all times |
| CI | Every push runs tests. A red CI flag is a blocker, not a suggestion |

---

## Chapter 05: Testing Data Science Code with pytest

**File:** `tutorials/02-dev-tools/05-pytest-testing.qmd`

### Before you begin

Assumes completion of Ch01–Ch04. `grade-predictor` has typed, linted code and a git history.
This chapter writes tests for it. The testing patterns here apply to any DS function or
data pipeline step.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Write and run pytest tests for DS functions | Sec. 1 |
| 2 | Use `@pytest.mark.parametrize` to test multiple inputs without duplicating code | Sec. 2 |
| 3 | Write fixtures that provide reusable sample data | Sec. 3 |
| 4 | Test pandas and polars transforms with `assert_frame_equal` and schema checks | Sec. 4 |
| 5 | Test exception handling with `pytest.raises` | Sec. 5 |
| 6 | Measure test coverage and interpret the report | Sec. 6 |
| 7 | Organize tests for a DS project: unit vs integration | Sec. 7 |

### Sections

**Sec. 1 — Why DS code needs tests**

Open with a concrete DS bug that tests would have caught: a normalization function applied
before the train/test split, so test data leaked into the scaler's fit. Explain: in DS,
silent bugs (wrong output, no exception) are more common than crashing bugs and harder to find.
A test suite converts a "I think this is right" into a "this is verifiably correct".

Show the first test:

```python
# tests/test_core.py
from grade_predictor.core import compute_grade

def test_compute_grade_defaults():
    result = compute_grade(midterm=80.0, final=85.0, project=90.0)
    assert abs(result - 84.25) < 0.01  # 0.30*80 + 0.45*85 + 0.25*90
```

*Key Concept callout:* "A test is an executable specification. `test_compute_grade_defaults`
says: given these inputs, this function must return this value. If the function ever changes
and breaks this, the test fails immediately."

**Sec. 2 — Parametrize: one test, many inputs**

Show the DS-specific use: testing grade boundary conditions:

```python
@pytest.mark.parametrize("midterm,final,project,expected_grade", [
    (90.0, 92.0, 88.0, "A"),   # composite >= 85
    (75.0, 78.0, 80.0, "B"),   # composite >= 70
    (55.0, 60.0, 58.0, "C"),   # composite >= 55
    (40.0, 42.0, 45.0, "D"),   # composite >= 45
    (20.0, 25.0, 30.0, "F"),   # composite < 45
])
def test_grade_letter(midterm, final, project, expected_grade):
    assert grade_to_letter(midterm, final, project) == expected_grade
```

Explain: parametrize runs the test body once per row. Adding a new edge case is one line.
Without it, five separate functions with near-identical code.

*Activity 1:* Write a parametrized test for a `normalize_score(raw, min_val, max_val)`
function that maps a raw score to 0-100. Cover the boundary: raw == min_val returns 0,
raw == max_val returns 100.

**Sec. 3 — Fixtures for reusable test data**

Show `conftest.py` with a minimal `sample_df` fixture:

```python
# tests/conftest.py
import pandas as pd
import pytest

@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "student_id": ["S0001", "S0002", "S0003"],
        "midterm_score": [80.0, None, 60.0],
        "final_score": [85.0, 70.0, 55.0],
        "project_score": [90.0, 75.0, 65.0],
        "program": ["CS", "DS", "IT"],
        "passed": [True, True, False],
    })
```

Show how to use it:

```python
def test_flag_at_risk(sample_df):
    result = flag_at_risk(sample_df, threshold=65.0)
    assert result.sum() == 1  # only S0003 is at risk
```

Explain fixture scope: `function` (default, re-created each test), `module` (one per file),
`session` (one per run). Use `session` scope for loading a large CSV once.

*Activity 2:* Write a `session`-scoped fixture that loads a 50-row sample from
`university_analytics.csv`. Use it in three different test functions.

**Sec. 4 — Testing pandas and polars transforms**

This is the gap in all standard references. Cover three patterns:

**Pattern 1: Shape and column assertions**
```python
def test_add_average_marks_column(sample_df):
    result = add_average_marks(sample_df)
    assert "average_marks" in result.columns
    assert result.shape == (3, 7)              # one new column added
    assert result["average_marks"].notna().all()
```

**Pattern 2: `pd.testing.assert_frame_equal`**
```python
def test_filter_passing_students(sample_df):
    result = filter_passing(sample_df)
    expected = sample_df.iloc[[0, 1]].reset_index(drop=True)
    pd.testing.assert_frame_equal(result, expected, check_like=True)
```

**Pattern 3: dtype and schema assertions**
```python
def test_output_dtypes(sample_df):
    result = add_average_marks(sample_df)
    assert result["average_marks"].dtype == "float64"
    assert result["passed"].dtype == "bool"
```

For polars:
```python
def test_polars_filter():
    import polars as pl
    df = pl.read_csv("data/university_analytics.csv")
    result = filter_high_scorers(df, threshold=90.0)
    assert result["midterm_score"].min() >= 90.0
```

*Common Mistake callout:* "`assert result.equals(expected)` is almost never right for
DataFrames with floats. Floating-point arithmetic makes exact equality fail for values
that are correct to any practical precision. `pd.testing.assert_frame_equal` has a
`check_exact=False` and `rtol` parameter for this reason."

**Sec. 5 — Testing exception handling**

```python
def test_invalid_weights_raises():
    with pytest.raises(ValueError, match="weights must sum to 1"):
        compute_grade(80.0, 85.0, 90.0, weights=(0.5, 0.5, 0.5))
```

Show `match` for asserting the error message content. Explain why testing exceptions
matters: a function that silently accepts invalid weights and returns wrong output is
worse than one that raises clearly.

**Sec. 6 — Coverage**

Show `uv run pytest --cov=grade_predictor --cov-report=term-missing tests/`.
Interpret the output: uncovered lines are dead code or error paths never tested.
Explain: 80% coverage is a reasonable target for DS library code. 100% is often
counterproductive (forces testing trivial getters). What matters is covering every
code path that could produce a wrong answer silently.

Configure in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=grade_predictor --cov-report=term-missing --cov-fail-under=80"
```

**Sec. 7 — Test organization**

```
tests/
├── conftest.py            ← shared fixtures and sample data
├── unit/
│   ├── test_core.py       ← individual function tests
│   └── test_config.py
└── integration/
    └── test_pipeline.py   ← end-to-end: load CSV → transform → grade
```

Explain unit vs integration: unit tests test one function in isolation with synthetic data.
Integration tests test the full pipeline with real data from disk. Run unit tests always.
Run integration tests in CI and before releases.

**Capstone:** Write a test suite for `grade-predictor` with at least: one parametrized test
covering all five grade boundaries, one fixture loading from `university_analytics.csv`,
one `assert_frame_equal` test on a DataFrame transform, and one `pytest.raises` test.
Reach 80% coverage.

### Further Reading

| Resource | Why it matters |
|---|---|
| BetterStack, [pytest guide](https://betterstack.com/community/guides/testing/pytest-guide/) | Comprehensive walkthrough of parametrize, fixtures, and plugins |
| pydevtools, [pytest + uv](https://pydevtools.com/handbook/tutorial/setting-up-testing-with-pytest-and-uv/) | The exact uv + pytest integration workflow |
| [pandas testing utilities](https://pandas.pydata.org/docs/reference/testing.html) | `assert_frame_equal` and `assert_series_equal` reference |
| [pytest-cov documentation](https://pytest-cov.readthedocs.io/) | Coverage measurement and HTML report generation |
| [pandera documentation](https://pandera.readthedocs.io/) | Schema-level DataFrame validation: the next step after dtype assertions |

### Summary

| Concept | Key rule |
|---|---|
| Test function naming | `test_<what_it_does>`. Describes behavior, not implementation. |
| `parametrize` | One test body, N inputs. Boundary cases belong in parametrize, not separate functions. |
| Fixtures | `conftest.py` for shared data. Session scope for large files loaded from disk. |
| `assert_frame_equal` | Never `assert df1.equals(df2)` for floats. Use `pd.testing.assert_frame_equal`. |
| Coverage | 80% target. What matters is covering every silent-failure path, not every trivial line. |

---

## Chapter 06: Automation with pre-commit

**File:** `tutorials/02-dev-tools/06-pre-commit-automation.qmd`

### Before you begin

Assumes completion of Ch01–Ch05. `grade-predictor` has typed, tested, linted code under
version control. This chapter makes the quality checks automatic so they never need to be
remembered. The `.pre-commit-config.yaml` in this book's own repository is the live reference
for every pattern shown.

### Learning objectives

| # | Skill | Covered in |
|---|---|---|
| 1 | Explain what a git hook is and how pre-commit manages them | Sec. 1 |
| 2 | Write a `.pre-commit-config.yaml` with the essential DS hooks | Sec. 2 |
| 3 | Use `nbstripout` to keep notebook outputs out of git history | Sec. 3 |
| 4 | Configure commitizen to enforce conventional commits | Sec. 4 |
| 5 | Understand `stages: [pre-commit]` vs `stages: [pre-push]` | Sec. 5 |
| 6 | Debug a hook failure and use the `SKIP` escape hatch correctly | Sec. 6 |

### Sections

**Sec. 1 — What git hooks are and why pre-commit manages them**

Explain: a git hook is a script that git runs at a specific point in the workflow
(`pre-commit`, `commit-msg`, `pre-push`). Without pre-commit, each hook is a raw shell
script in `.git/hooks/` that is not version-controlled and is lost when the repo is cloned.
Pre-commit manages hooks as config, keeps them version-controlled in `.pre-commit-config.yaml`,
installs them with `pre-commit install`, and runs each hook in an isolated environment.

*Key Concept callout:* "`pre-commit install` must be run once after every clone. The hooks
live in `.pre-commit-config.yaml` (versioned), not in `.git/hooks/` (not versioned).
Add `pre-commit install` to your onboarding README so new collaborators do not skip it."

**Sec. 2 — The essential DS hooks**

Walk through a complete `.pre-commit-config.yaml` for a DS project, explaining each hook:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
        args: [--maxkb=1200]
      - id: detect-private-key
      - id: check-merge-conflict
      - id: no-commit-to-branch

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: nbstripout-dev
        name: nbstripout (dev)
        entry: nbstripout --keep-output
        language: python
        types: [jupyter]
        additional_dependencies: [nbstripout]
        stages: [pre-commit]
```

Explain each choice. `check-added-large-files` catches data files. `detect-private-key`
catches secrets. `no-commit-to-branch` prevents direct pushes to main.

**Sec. 3 — nbstripout: keeping notebooks clean**

This hook is not covered in any standard reference but is essential for DS projects. Explain:

Jupyter saves cell outputs (plots, tables, printed values) inside the `.ipynb` JSON.
Without stripping, every notebook re-run creates a diff of hundreds of changed lines — even
if the code itself did not change. This makes `git diff` unreadable and `git blame` useless.

Two modes:
- `nbstripout --keep-output` (pre-commit stage): strips only metadata, keeps outputs for
  review. Use when you want reviewers to see outputs.
- `nbstripout --drop-empty-cells` (pre-push stage): strips outputs and empty cells before
  pushing. Use for CI-facing pushes where clean JSON matters.

Show before/after: a notebook `git diff` with and without nbstripout.

*Activity 1:* Add nbstripout to `grade-predictor`. Run a Jupyter cell, save the notebook,
then `git diff` to confirm outputs are stripped before staging.

**Sec. 4 — commitizen: enforcing conventional commits**

Show the commitizen configuration:

```toml
[tool.commitizen]
bump_message = "bump: v$current_version to v$new_version"
tag_format = "v$version"
update_changelog_on_bump = true
version_provider = "pep621"
```

And the hook:
```yaml
  - repo: local
    hooks:
      - id: commitizen
        name: commitizen
        entry: cz check
        args: [--commit-msg-file]
        language: system
        stages: [commit-msg]
```

Show `cz commit` as the interactive alternative to `git commit -m`. Show that a bare
`git commit -m "update stuff"` fails the hook. Show `cz bump` for version bumping and
`cz changelog` for automatic changelog generation.

*Pro Tip callout:* "`cz bump` reads the commit history since the last tag and increments
the version automatically: `feat` commits bump the minor version, `fix` commits bump the
patch version. With `update_changelog_on_bump = true`, the `CHANGELOG.md` writes itself."

**Sec. 5 — pre-commit vs pre-push stages**

Explain when each stage is appropriate:

| Stage | When it runs | Right for |
|---|---|---|
| `pre-commit` | Before every local commit | Fast checks: ruff, end-of-file-fixer, nbstripout |
| `commit-msg` | After writing the commit message | Message validation: commitizen |
| `pre-push` | Before `git push` | Slow checks: type checking (ty), heavier linting |

Show how to assign a hook to a stage with `stages: [pre-push]`. Explain the tradeoff:
a slow pre-commit hook makes every commit painful. A slow pre-push hook runs less often
and tolerates more latency.

**Sec. 6 — Debugging and the SKIP escape hatch**

Show what happens when a hook fails: the commit is blocked, the hook outputs the error,
and the modified files are left unstaged for manual review.

Show `SKIP=ruff git commit -m "wip: draft"` to bypass a specific hook for a work-in-progress
commit. Explain: `SKIP` is legitimate for `wip` commits on a personal branch. It is not
legitimate for commits going into main.

Show `pre-commit run --all-files` to run all hooks on every file (not just staged files)
as a one-time audit.

*Common Mistake callout:* "Adding `--no-verify` to `git commit` to skip all hooks is
almost always the wrong answer. It disables commitizen, ruff, nbstripout, and every
other quality gate at once. Use `SKIP=<hook-id>` to bypass only the specific hook
that is blocking you."

**Capstone:** Set up the complete pre-commit pipeline for `grade-predictor`: all
pre-commit-hooks, ruff, nbstripout, and commitizen. Run `pre-commit run --all-files`
and bring the output to clean. Make a final conventional commit with `cz commit`.

### Further Reading

| Resource | Why it matters |
|---|---|
| [pre-commit documentation](https://pre-commit.com/) | Hook configuration, staging, and custom hook authoring |
| [nbstripout documentation](https://github.com/kynan/nbstripout) | Options for output stripping in DS projects |
| [commitizen documentation](https://commitizen-tools.github.io/commitizen/) | `cz commit`, `cz bump`, `cz changelog` reference |
| [pre-commit hooks list](https://pre-commit.com/hooks.html) | Full list of community hooks searchable by language and tool |

### Summary

| Concept | Key rule |
|---|---|
| `pre-commit install` | Run once after every clone. Without it, no hooks run. |
| nbstripout | Every DS project with notebooks needs this. Unstripped outputs make `git diff` unreadable. |
| `stages: [pre-commit]` | Fast checks only. Slow hooks belong at `pre-push`. |
| commitizen | Enforces conventional commits automatically. `cz commit` replaces `git commit -m`. |
| `SKIP=<id>` | Bypass one specific hook for `wip` commits. Never use `--no-verify`. |

---

## Implementation notes

### Callout div colors (identical to Parts 1 and 2)

| Type | Border | Background | Text |
|---|---|---|---|
| Key Concept (info) | `#0369A1` | `#EAF3FA` | `#0369A1` |
| Pro Tip | `#7C3AED` | `#F5F3FF` | `#5B21B6` |
| Activity | `#009E73` | `#EBF5F0` | `#065F46` |
| Common Mistake | `#DC2626` | `#FEF2F2` | `#991B1B` |
| Example | `#059669` | `#EAF7F0` | `#059669` |

### Quarto `.qmd` code block syntax

Shell display (not executed):
````
```{bash eval=false}
uv init grade-predictor --package
```
````

Python executed:
````
```{python}
from grade_predictor.core import compute_grade
compute_grade(80.0, 85.0, 90.0)
```
````

### Cross-references between chapters

Each chapter opens with "Before you begin" that names the prior chapter explicitly
and states exactly what state the `grade-predictor` project should be in.
Use `[Ch01](01-uv-project-setup.qmd)` style links for cross-references within the part.

### _quarto.yml addition (add when first chapter is complete)

```yaml
- part: "Part 3: Dev Tools"
  chapters:
    - tutorials/02-dev-tools/01-uv-project-setup.qmd
    - tutorials/02-dev-tools/02-code-quality-ruff.qmd
    - tutorials/02-dev-tools/03-type-annotations.ipynb
    - tutorials/02-dev-tools/04-git-github.qmd
    - tutorials/02-dev-tools/05-pytest-testing.qmd
    - tutorials/02-dev-tools/06-pre-commit-automation.qmd
```
