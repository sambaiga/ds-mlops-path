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

## Open questions: resolved

1. **Coverage gate: correction after CI actually failed on PR #53.** The
   first version of this fix assumed setting `--cov-fail-under=80` now
   would safely no-op until real tests exist, matching the existing
   tolerance for pytest's plain "no tests collected" exit code (5). That
   assumption was wrong, verified empirically: with zero test data
   collected, pytest-cov hard-fails (exit 1) for *any*
   `--cov-fail-under > 0`, it does not fall back to exit 5. It failed
   immediately against `ark/plot/*`'s existing 0% coverage. Fixed by (a)
   reverting `--cov-fail-under` to 0 for now, and (b) adding
   `.coveragerc` (didn't exist despite `pyproject.toml` already
   referencing it) with `omit = */ark/plot/*`, so that when the gate is
   raised to 80 **in the same PR that adds `ark/case_studies/spend_regression`
   and its tests**, it measures coverage against that tested project
   surface, not blended with the pre-existing, untested plotting module.
   This is also the fix for "test of 80 should be per project not the
   entire codebase." The gate cannot be turned on ahead of the code it's
   meant to measure, that was the actual mistake, not just the omit
   scoping.
2. **Branch alignment: done.** `feature/case-study-1-spend-regression` was
   rebased onto current `main` (picks up the Pages revert, the chapter-
   number fix, and the ML-workflow diagram fix) and force-pushed.
3. **Dataverse mechanics: confirmed against the live dataset via its
   REST API**, not just the dataset page (which is a JS-rendered SPA that
   doesn't expose file details to a plain fetch):
   - License is **CC0 1.0** (public domain), cite as courtesy
     (Berke et al. 2024, *Scientific Data*), no DUA or access-request
     approval actually gates the files despite the dataset showing
     `fileAccessRequest: true`, every file itself is `restricted: false`
     and downloads with a plain unauthenticated `GET`.
   - Download endpoint: `https://dataverse.harvard.edu/api/access/datafile/{id}`
     (redirects to a presigned S3 URL, works with `requests`/`curl -L`,
     no API token needed). Confirmed file IDs: `amazon-purchases.csv` =
     7616235 (**298.5 MB**), `survey.csv` = 7616231 (**1.5 MB**),
     `fields.csv` = 7616233 (2.5 KB, a column dictionary for
     `survey.csv`). Two PDFs (survey instruments) exist but aren't needed
     by the pipeline.
   - **Gotcha confirmed**: `survey.csv` is tab-separated despite the
     `.csv` extension (`Content-Type: text/tab-separated-values`).
     `data.py` must load it with `sep="\t"`, a plain `pd.read_csv` would
     silently produce a single garbage column.
   - Both `amazon-purchases.csv` (298.5 MB) and `survey.csv` (1.5 MB)
     confirm the download-script decision above; neither fits the 1200 KB
     pre-commit cap.
   - Join key confirmed: `Survey ResponseID` in both files.
     `amazon-purchases.csv` columns: `Order Date`, `Purchase Price Per
     Unit`, `Quantity`, `Shipping Address State`, `Title`,
     `ASIN/ISBN (Product Code)`, `Category`, `Survey ResponseID`.
     `Category` is genuinely blank on some real rows, a real missingness
     case for the pandera schema to declare nullable, not a synthetic one.
   - **New finding, changes `features.py`'s scope**: `survey.csv` includes
     sensitive fields alongside demographics, substance use
     (`Q-substance-use-cigarettes/marijuana/alcohol`), a disability/health
     question (`Q-personal-diabetes`, `Q-personal-wheelchair`), and
     sexual orientation (`Q-sexual-orientation`). `features.py` will use
     only non-sensitive demographic/lifestyle/usage fields (age
     bracket, education, income bracket, household size, state, Amazon
     usage frequency) and **explicitly exclude** the health,
     substance-use, and orientation columns from the feature set, an
     explicit exclusion list in `config.py`, not just an omission. Worth
     one sentence in the notebook itself: predicting spend doesn't need
     those fields, and training on them by default (because they happen
     to be in the file) is exactly the kind of feature-selection
     carelessness the book's later Value-driven AI part will name
     directly.

## Writing approach: balancing hands-on and theory

Checked the book's own writing-practice memory (Pressfield/Dicks/Zinsser
principles, notebook cell design, chapter connections and openings, UX
laws, diagram/voice rules) against what this specific chapter needs to do.
The short version: **theory share should be small on purpose**. Every
concept this chapter touches, the spec card, the nine-stage workflow,
train/test splits, MAE/MAPE, pandera, pydantic, pytest, loguru, was
already taught and named in Ch18-32. Re-explaining any of them here would
violate "concept earned before named" in reverse, and it wastes the one
thing this chapter is actually for: showing what happens when all of that
meets a dataset nobody designed to be clean.

Concretely:

- **Don't open with a recap.** "Chapters 18-32 taught you X, Y, Z, now
  let's apply them" is exactly the gated, recap-first opening the
  chapter-openings rule warns against. Open on something specific and
  real from the data itself, a household whose spend pattern does
  something the demographics don't explain, and let the "this is where
  the spec card finally meets messy data" framing arrive as the second
  or third sentence, not the first.
- **One line of attribution per concept, not a re-derivation.** When a
  cell uses a pandera schema, one sentence: "this is the Ch26 pattern,
  applied to a file where `Category` really is sometimes blank." Then
  move on. The reader either remembers Ch26 (in which case more would be
  patronising) or doesn't (in which case a link back, not a re-teach, is
  the right amount of help).
- **One executed concept per cell, markdown-before-code explaining why
  now, not what.** Since logic lives in `ark.case_studies.spend_regression`
  rather than inline, most cells become "call one function, look at one
  result." The markdown above each cell should say why this step matters
  *for this dataset*, not describe the function signature.
- **Spend the craft budget on the ending, not the setup.** Peak-End
  Rule: this chapter is remembered by how it closes far more than how it
  opens. The dollar-value estimate and the monitoring/problem-framing
  forward-pointer deserve real sentences, not a bullet list bolted onto
  the end. This is also where the preface's whole thesis ("technically
  solid isn't enough") gets its first concrete payoff in the book, so it
  should land like one.
- **Reserve callout treatment for what's actually novel here** (Von
  Restorff: scarcity is what makes a callout mean something). The one
  Key Concept callout worth using is the live feedback loop (first pass
  under-performs, add a behavioral feature, re-evaluate), because that's
  the one thing this chapter demonstrates that no earlier chapter could
  (Ch30 only described the loop; this is the first time the book actually
  runs it). Everything else can stay plain prose.
- **One diagram, used for the one genuinely abstract step.** The
  household-level aggregation (many transaction rows plus one survey row
  collapsing into a single feature row per household) is the one step
  that benefits from a picture; an EDA scatter plot already handles
  everything else visually. Doesn't need a second diagram for the
  feedback loop, a simple before/after metrics table communicates that
  more precisely than a picture would.
- **Hick's Law in the model-selection section**: baseline -> Ridge -> one
  boosting model, per the existing project spine. Don't add a fourth or
  fifth candidate for completeness, more options here would read as
  padding, not rigor, and the point of this chapter is the workflow, not
  a model bake-off.

Net effect: a chapter where the code is doing most of the teaching and
the prose is doing the framing, connective tissue, and the close, which
is the opposite ratio of Ch28-30 (where prose taught concepts the code
hadn't earned yet) and the intended one for a project chapter.

## Not doing in this pass

No code, no notebook, no module. This is the strategy only, per the
request. Next step, if approved, is `ark/case_studies/spend_regression/`
first (with tests), then the notebook that narrates it.
