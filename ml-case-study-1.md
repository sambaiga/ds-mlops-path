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
they meet.

**Correction after review**: the module cannot be pre-built and simply
imported by the notebook. The book's own model, stated on its own cover
page, is "run top to bottom, not just read," with Activity callouts
where the reader fills in a `\`...\`` themselves before moving on. A
notebook that opens with `from ark.case_studies.spend_regression import
*` teaches nothing, the reader would be reading a finished library, not
building anything. So the module isn't written first and then narrated,
it's **built inside the notebook, function by function, with the reader
doing some of the writing**, and only *promoted* into
`ark/case_studies/spend_regression/` once each piece works, the same
prototype-then-productionize move a real practitioner makes. See "How
construction actually happens" below, it changes the build order from
what an earlier version of this plan said.

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
├── 33-spend-regression.ipynb  # the book chapter: builds each module function inline first,
│                                then promotes it, narrates each Ch30 workflow stage
└── data/                       # gitignored; populated by data.py at run time
```

## Section 1 is reasoning, not code: problem formulation before config.py

Corrected again after the same "imagine the learner as a data scientist"
test applied one stage earlier. The chapter's opening section is not
"write `config.py`", it's the thing Ch30 itself says comes first: **a
data scientist who has just been handed this dataset and a business ask,
with no code written yet.**

The section runs in this order, and the key correction from the previous
draft of this plan: **the ask that opens the chapter is vague, the way a
real stakeholder actually talks, not a pre-formed data science problem
in disguise.** The reader does the refining, the chapter doesn't do it
for them and then perform the refinement as theatre.

1. **The hook**: a real, verified moment from the actual downloaded
   data, not an invented anecdote. (Confirmed while drafting: one
   household in the dataset, single person, unremarkable income bracket,
   spends about $49 in a typical month, then in one specific week buys a
   65" TV, a PS4 Pro, a Surface tablet, an Apple Watch, a GoPro, a
   trampoline, and a kayak, roughly $12,000 in eight days, then goes back
   to normal. Nothing in the demographics explains it. That's the hook.)
2. **The vague ask, stated the way it would actually arrive.** Not
   "predict household spend from demographics". Something closer to what
   a marketing or lifecycle team really says: "we want to know which
   customers are worth investing more in." That sentence is vague on
   purpose, "worth investing in" could mean total spend, growth,
   frequency, loyalty, or something else entirely, and the chapter does
   not resolve the ambiguity for the reader.
3. **Refine it on the page, as questions, not as a solved checklist.**
   The chapter asks the questions a data scientist would actually ask
   back: worth investing in *how*, over what time frame, measured
   against what, using what data the business actually has. Each
   question narrows the ask until it lands on one of Ch30's five spec-
   card components, in order, but arrived at through the questioning,
   not announced. This is the part that changed: earlier drafts of this
   plan had the chapter "work the five-component spec card as a
   discussion", which still risked reading as the data scientist
   explaining the five components *to* the reader. This version has the
   vague ask create genuine friction first, the five components are the
   resolution of that friction, not a framework introduced ahead of it.
4. **Activity, mirroring Ch30's own "write the Spec Card" activity**:
   before the resolved spec card is shown, the reader drafts their own
   answer to the refining questions first, the same fill-in-before-you-
   see-the-answer mechanism Ch30 already used for three *different*
   problems, now applied to this one.
5. **Only now, codify it.** "We've reasoned through this, now let's make
   it a real, importable object so the rest of the pipeline can't drift
   from what we just decided", and `config.py` is written as the
   codification of a decision already made, not the starting point of
   the chapter.

`config.py` existing is still correct, and it's still early, but it's
the *output* of Section 1's reasoning, not Section 1 itself. Everything
below (the five-beat build pattern) starts at Data Collection, once
there's an actual spec to build against.

## How construction actually happens: the notebook builds the module, not the reverse

From Data Collection onward (Problem Framing above is reasoning, nothing
to build yet), each section follows the same five-beat pattern, which is
also the real workflow a practitioner follows when a prototype earns its
way into a shared library:

1. **Motivate and build inline.** Write the function directly in a
   notebook cell against the real, already-loaded data, exactly like
   Ch31-32 already do for sklearn. One concept per cell, markdown before
   it explaining why this step matters *for this dataset*.
2. **Activity: the reader completes part of it.** At least one function
   per major stage (the household-aggregation groupby, the excluded-
   columns filter, the dollar-value formula) ships with a `\`...\`` the
   reader fills in themselves, the same mechanism every other chapter in
   the book already uses, not a new pattern invented for this one.
3. **Sanity-check on real data.** Run it, look at the actual output
   (row counts, a `themed_gt()` preview), confirm it did what section 1
   said it would.
4. **Promote it.** "This works, now let's make it reusable": the same
   code moves into `ark/case_studies/spend_regression/{file}.py`, gains
   full type annotations, a docstring, and (where relevant) a pandera
   schema guarding its input. This is the extraction step, shown
   happening, not assumed to have already happened.
5. **Test it, live, in the notebook.** A cell runs the new pytest test
   for what was just promoted (e.g. `!uv run pytest
   tests/case_studies/test_spend_regression.py -k features -v`) so the
   reader watches it pass. The *first* time this happens in Ch33 is the
   repo's first real test suite going green on the page, in front of the
   reader, not a fact buried in CI logs they'll never open.

**Exception, confirmed while building Data Collection**: not every
function earns the full five-beat treatment. Infrastructure, the
Dataverse download-and-cache utility specifically, isn't a data science
concept, it's plumbing a working data scientist would just import rather
than reinvent. For utilities like this, the notebook imports it directly,
highlights the specific practices baked into it (idempotent caching,
chunked reads, an HTTPS-only guard, the browser-like User-Agent header
Dataverse's server actually requires) as a short prose list, and still
proves it with a live test run, but skips building it inline and skips
the fill-in-the-blank Activity. The five-beat treatment is reserved for
code that teaches a data science or ML idea: the household aggregation in
`features.py`, the model training and evaluation in `model.py`. The
distinction is "is this something the reader needs to be able to build,"
not "is this code worth having."

From that point on in the notebook, later cells `import` the promoted
version rather than redefine it, so the reader sees the module actually
get used once it exists, the same way Case Studies 2-7 will import it
later. The module and the notebook are therefore written together, in
notebook order, not module-first-then-narrated.

## Mapping to Ch30's nine-stage workflow (including both feedback loops)

The user's pasted diagram is the literal section structure of the
notebook, not just a reference image:

| Workflow stage | What happens in this project |
|---|---|
| Problem framing | Reasoned through in prose first, as the data scientist facing the business ask, per "Section 1 is reasoning, not code" above. `config.py` codifies the resolved spec card afterward, it isn't the starting point |
| Data collection | `data.py` downloads and caches the Nature dataset; logged with loguru (row counts, date range, cache hit/miss) |
| EDA | Notebook-only (exploratory, not something to freeze into a tested function): spend distributions, the COVID-era shift, missingness, all charted with `lets_plot` + `ark.plot` theming, per the visualization section below |
| Feature engineering | `features.py`: household-level aggregation, demographic join, validated on the way out by a pandera schema |
| Model selection | Baseline (predict the mean) -> Ridge -> a small boosting model, per the project spine in `ML_CASE_STUDY_PLAN.md` |
| Training | `model.py`, logged per step |
| Evaluation | MAE/MAPE against the baseline, per Ch30 Section 4 |
| **Feedback loop 1: Evaluation -> Feature engineering** | Made literal, not decorative: the notebook runs a first pass with demographics only, evaluates, under-performs the threshold, then returns to `features.py` to add a behavioral feature (purchase frequency), re-evaluates, and shows the improvement. This is the one loop the project can actually execute in code |
| Deployment / Monitoring | Not implemented (that's the MLOps part's job, per `ML_CASE_STUDY_PLAN.md`'s template). The closing section names what a monitor would watch (drift in the demographic mix, spend-distribution shift) |
| **Feedback loop 2: Monitoring -> Problem framing** | Stated, not coded: one paragraph on what a monitoring alert on that drift would force a team to revisit in the spec card (is "predict spend" even the right target anymore, or did the population being sold to change) |

## Dev-tools chapters (Part 2), each with a concrete touchpoint

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

## Data analysis and visualization chapters (Part 1), each with a concrete touchpoint

Checked what Part 1 actually taught, section by section, rather than
gesturing at "pandas skills" generally. Every touchpoint below is a named
section a learner already sat through:

| Ch | Practice | Where it shows up here |
|---|---|---|
| 05 Math and statistics | The `statistics` module's mean/stdev is literally the baseline model (Ch30's "compute a baseline first": predict the mean) |
| 08 Pandas core | Boolean filtering and Section 7 "Handling Missing Data" apply directly to the real blank `Category` rows in `amazon-purchases.csv` |
| 09 Pandas operations | Section 4 "Descriptive Statistics and Summarization" is the EDA pass before any modelling |
| 10 Combining and reshaping | Section 2 "Joining Data with `pd.merge`" is exactly the `amazon-purchases.csv` + `survey.csv` join on `Survey ResponseID`; Section 3 "Group by Operations" is the household-level aggregation in `features.py` |
| 11 Time series | `Order Date` parsing and any recency/frequency features reuse Section 1 (date/time dtypes) and Section 3 (selecting from a time series), the heavier resampling/lag content is Case Study 3's job (forecasting), not this one |
| 13 Great Tables | Section 8 "Model Comparison with `metrics_report()`" is not a new technique here, it's the exact function (`ark.plot.gt_style.metrics_report`) Ch31-32 already used and this project reuses again |
| 15 lets-plot | The grammar (`ggplot`, `aes`, `geom`, layering, faceting) is how every EDA and results chart in this notebook gets built, see below |
| 16 Data storytelling | Section 1 ("picking the right chart"), Section 6 (preattentive attributes), and Section 7 (annotation as narrative) directly shape which EDA chart gets built and how the one striking finding (whatever surfaces from the data) gets annotated rather than left for the reader to spot unaided |

## Visualization: lets-plot and the `ark.plot` house style, not matplotlib

Ch14 teaches matplotlib/Seaborn and Ch15 teaches lets-plot, the book
teaches both, but Ch31-32 (the closest precedent to this project, not a
Part 1 fundamentals chapter) already settled on a single convention for
ML chapters that this case study should match exactly rather than pick
its own:

- **Charts**: `lets_plot` (`ggplot`, `aes`, `geom_*`), styled with
  `ark.plot.theme.modern_theme()` and coloured from `ark.plot.tokens`
  (`PRIMARY`, `SUCCESS`, `INFO`, `WARNING`, `DANGER`, `AI_ACCENT`, the
  same brand palette used everywhere else in the book), never raw
  matplotlib/Seaborn defaults.
- **Tables, without exception**: every DataFrame the notebook shows a
  reader goes through `ark.plot.gt_style`, never a bare `print(df)` or an
  unstyled `df.head()`/`df.describe()`. Concretely, every one of these is
  a `themed_gt()` call with `title`/`subtitle` set (Ch13's own
  convention):
  - the spec card itself (Ch30's five components, rendered from the
    `config.py` pydantic model, not a markdown table)
  - the raw-data preview and the EDA descriptive-statistics summary
  - the categorical feature cardinality table (the same pattern Ch32
    already used for Hotel Booking)
  - the pandera schema-validation summary (rows passed/failed, which
    rule caught what)
  - baseline -> Ridge -> boosting model comparison, via
    `ark.plot.gt_style.metrics_report()` specifically, the exact
    function Ch13 Section 8 names and Ch31-32 already call
  - the feature-importance table for the chosen model
  - the closing dollar-value estimate and the model-card summary
  This doesn't override Ch16's "when a table beats a chart" judgement,
  distributions and trends still get a `lets_plot` chart, not a table.
  It's a styling rule: whichever output *is* a table, it's always a
  `themed_gt()` table, not a raw pandas dump.
- No new plotting or table code needs writing, `ark.plot` already has
  everything this case study needs. The only new work is calling it
  consistently, everywhere, rather than reaching for `print()` out of
  habit partway through.

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
