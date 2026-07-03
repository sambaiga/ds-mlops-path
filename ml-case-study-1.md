# Case Study 1 (Ch33, Spend Regression): project strategy

Strategy only, no notebook or module code written yet. Goal: make this the
first case study a genuinely **self-sufficient project**, not a bigger
notebook, by applying every dev-tools chapter (18-27) and Ch30's workflow
discipline at once, on the Nature Open e-commerce dataset. If this works,
Case Studies 2-7 inherit the same skeleton instead of each reinventing it.

## Why this shape, not just a longer notebook

The book's own preface names three gaps: technical depth, engineering
discipline, and knowing what problem you're solving for whom. Ch31-32
(sklearn-core/pipeline) already prove the technical-depth side with
inline, type-annotated functions. Part 2 (dev-tools) taught the
engineering-discipline side as ten standalone chapters. Nothing in the book
yet forces those two sides together in one artifact. Case Study 1 is where
they meet, so the project should look like the smallest real thing a
practitioner would actually ship: a small tested library module plus a
notebook that narrates it, not one long cell sequence.

## Grounded in what's already in the repo, not invented fresh

- `ark/` is already an installed, importable, tested package
  (`ark.plot.*`) with `--cov=ark` wired into `pyproject.toml`. Case-study
  logic belongs at `ark/case_studies/spend_regression/`, not scattered
  inside the notebook, so it's real project code, not tutorial scratch.
- `tests/` doesn't exist yet anywhere in the repo. ARK CID
  (`check_pullrequest.yaml`) already runs `pytest --cov=ark` but currently
  tolerates exit code 5 ("no tests collected") because there's nothing to
  run. This case study would add the **first real test suite in the repo**,
  a concrete, visible payoff for Ch23 rather than an abstract lesson.
- `pydantic`, `pydantic-settings`, `pandera`, `loguru` are core
  dependencies already, not optional extras, they're meant to be used by
  default, not specially unlocked.
- `.pre-commit-config.yaml` caps `check-added-large-files` at **1200 KB**.
  The Nature dataset's purchase file (1.8M rows) will not fit under that
  cap the way `hotel_bookings.csv` (16.8 MB) did, that file predates the
  hook or bypassed it. This forces a real decision, not a shortcut: data
  acquisition must be a **download script**, run once and cached locally
  (gitignored), never a committed raw CSV. That constraint is itself a
  legitimate teaching moment (reproducible data pipelines don't commit
  their inputs).
- `check-notebooks.yml` runs changed notebooks through `nbmake` with a
  **300-second per-notebook timeout**. Whatever the notebook trains must
  fit inside that, which argues for a light final model (linear -> Ridge
  -> a small, time-boxed boosting fit) rather than an open-ended search.

## Project layout

```
ark/case_studies/spend_regression/
├── __init__.py
├── config.py       # pydantic-settings: data dir, seed, acceptable threshold from the spec card
├── schema.py       # pandera schemas: raw purchases, raw survey, engineered feature matrix
├── data.py         # download-and-cache from Harvard Dataverse; never commits the raw file
├── features.py     # type-annotated household-level aggregation + demographic join
└── model.py        # baseline -> Ridge -> boosting, evaluation, dollar-value calculator

tests/case_studies/
└── test_spend_regression.py   # schema validation (valid + deliberately invalid rows),
                                 # feature engineering on a small fixture, dollar-value
                                 # formula correctness

tutorials/05-classical-ml-projects/
├── 33-spend-regression.ipynb  # the book chapter: imports ark.case_studies.spend_regression,
│                                narrates each Ch30 workflow stage, shows the two feedback loops
└── data/                       # gitignored; populated by data.py at run time
```

The notebook becomes thin on purpose: it calls into the tested module and
narrates *why*, matching how Ch31-32 already treat sklearn, except the
reusable parts are promoted out of the notebook this time because this
project is meant to be re-run and extended, not just read once.

## Mapping to Ch30's nine-stage workflow (including both feedback loops)

The user's pasted diagram is the literal section structure of the
notebook, not just a reference image:

| Workflow stage | What happens in this project |
|---|---|
| Problem framing | The five-component spec card (Ch30 Section 1), rendered as a pydantic model in `config.py` so the acceptable threshold is a real, importable value, not just a table in markdown |
| Data collection | `data.py` downloads and caches the Nature dataset; logged with loguru (row counts, date range, cache hit/miss) |
| EDA | Notebook-only (exploratory, not something to freeze into a tested function): spend distributions, the COVID-era shift, missingness |
| Feature engineering | `features.py`: household-level aggregation, demographic join, validated on the way out by a pandera schema |
| Model selection | Baseline (predict the mean) -> Ridge -> a small boosting model, per the project spine in `ML_CASE_STUDY_PLAN.md` |
| Training | `model.py`, logged per step |
| Evaluation | MAE/MAPE against the baseline, per Ch30 Section 4 |
| **Feedback loop 1: Evaluation -> Feature engineering** | Made literal, not decorative: the notebook runs a first pass with demographics only, evaluates, under-performs the threshold, then returns to `features.py` to add a behavioral feature (purchase frequency), re-evaluates, and shows the improvement. This is the one loop the project can actually execute in code |
| Deployment / Monitoring | Not implemented (that's the MLOps part's job, per `ML_CASE_STUDY_PLAN.md`'s template). The closing section names what a monitor would watch (drift in the demographic mix, spend-distribution shift) |
| **Feedback loop 2: Monitoring -> Problem framing** | Stated, not coded: one paragraph on what a monitoring alert on that drift would force a team to revisit in the spec card (is "predict spend" even the right target anymore, or did the population being sold to change) |

## Dev-tools chapters, each with a concrete touchpoint (not a checklist mention)

| Ch | Practice | Where it shows up here |
|---|---|---|
| 19 uv project setup | `uv run`/`uv sync`, no new dependency needed (everything used is already a core dep) |
| 20 Ruff | `ark/case_studies/spend_regression/*.py` and the notebook both pass `ruff check` + `ruff format`, already enforced by pre-commit and ARK CID, nothing new to configure |
| 21 Type annotations | Every function in `features.py` and `model.py` fully typed; this is the first case-study module, so it sets the standard the other six will match |
| 22 Git/GitHub | Already in motion: dedicated branch, PR at the end, atomic commits (module, tests, notebook as separate commits) |
| 23 pytest | `tests/case_studies/test_spend_regression.py`, the repo's first real test suite |
| 24 pre-commit | No new hooks needed; the large-file cap is the one that actively shapes a design decision here (see data acquisition above) |
| 25 Pydantic | `config.py`: the spec card as a typed, importable object, not just a markdown table |
| 26 Pandera | `schema.py`: a real data contract on both the raw input and the engineered feature matrix, fails loudly on a bad row instead of training on garbage |
| 27 Logging | `loguru` at every stage transition in `data.py`/`model.py`, replacing ad hoc prints |

Ch18 (VS Code setup) has no natural code touchpoint, it's an environment
prerequisite, not something a notebook demonstrates.

## Closing section (per `ML_CASE_STUDY_PLAN.md`'s required template)

Same four-part close as every other case study in the plan: spec card
already covered above, so the notebook's last section states (1) the
business decision this model changes and for whom, (2) the dollar-value
estimate and its assumptions (targeting the top-decile predicted spenders
vs. random targeting, per the plan's formula for Ch33), and (3) the
monitoring/problem-framing forward-pointer from the table above.

## Open questions to confirm before writing code

1. **Coverage gate**: once `tests/` exists with real tests, do we also flip
   ARK CID's `--cov-fail-under=0` back toward the `pyproject.toml` default
   of 80% for `ark`? Not decided here, flagging it since this case study
   is what would make that gate meaningful for the first time.
2. **This branch is currently behind `main`** (created before PR #50's
   revert merged), needs a rebase before any of this ships.
3. Exact Dataverse download mechanics (auth needed or not, file size,
   license/DUA terms) still need to be confirmed against the live dataset
   page before `data.py` is written, per the open item already flagged in
   `ML_CASE_STUDY_PLAN.md`.

## Not doing in this pass

No code, no notebook, no module. This is the strategy only, per the
request. Next step, if approved, is `ark/case_studies/spend_regression/`
first (with tests), then the notebook that narrates it.
