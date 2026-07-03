# Act 1 reorder: Foundation → Data Analysis → Data Viz → Dev Tools

Decided 2026-07-03. Current order teaches visualization (matplotlib, lets-plot,
data storytelling) before pandas, which means Chapter 9 already builds and reads
`pd.DataFrame`s three chapters before pandas itself is taught. Reordering fixes
this and matches the real workflow: load and wrangle data, then visualize it.

**Status: all three phases below are done** (renumbering, dataset unification,
capstone chapter + Dev Tools/ML shift). Book is now 32 chapters: Foundation
(1-7), Data analysis (8-13), Data visualization (14-17, capstone included),
Dev tools (18-27), ML landscape (28-32). This file is kept as the record of
what changed and why, in case a future pass needs the reasoning.

---

## 1. The data-storytelling capstone chapter

**Status: done.** Built as `tutorials/01-python-basics/17-storytelling-capstone.ipynb`.

### Why a new chapter, and why not yet

Analysis against four reference books (Wilkinson's *Grammar of Graphics*,
Knaflic's *Storytelling with Data*, Berinato's *Good Charts*, Dykes' *Effective
Data Storytelling*) found three genuine gaps not covered anywhere in the book:

1. **Audience-first framing** (Knaflic) — who the chart is for and what they
   need to decide, taught as a deliberate step before chart-type selection.
   Chapter 10 currently starts at "which chart to pick," skipping this.
2. **The Trifecta Checkup** (Berinato) — diagnosing whether a bad chart is a
   content problem, a story problem, or a visual-form problem, before touching
   the design. Chapter 10's capstone only exercises the visual-form fix.
3. **Explore vs. explain** (Dykes) — the deliberate transition from charts
   made to understand data yourself to charts made to inform someone else.
   Chapter 10's hook already gestures at this ("The chart was not wrong. It
   was just not a story.") but never names or teaches it as a step.

Wilkinson's grammar needs no new chapter: it is already the spine of the
lets-plot chapter (stat/position/coord pillars added 2026-07-03). Knaflic's
chart-craft content (declutter, preattentive attention, Gestalt) is already
substantially covered in Chapter 10.

These three gaps are workflow/judgment lessons, not new technical skills
(unlike ML-diagnostic visualization, e.g. confusion matrices, ROC curves,
which needs new code and belongs in Act 2, not here). Cramming three more
concept-sections into Chapter 10 (already 8 sections plus a capstone) would
violate the same Hick's Law chunking standard the rest of the book holds to.

### The plan once unblocked

A new **applied capstone chapter** for the Data Viz part, positioned last in
that part (immediately before Dev Tools), that makes the reader run the full
judgment loop against one real case rather than drilling isolated concepts:

1. Define the audience and their decision (Knaflic)
2. Diagnose a flawed chart with the Trifecta Checkup: content, story, or
   visual-form problem (Berinato)
3. Decide explore vs. explain for the situation (Dykes)
4. Pick the chart, write the narrative, build the explanatory version
5. Capstone artifact: one polished chart plus a one-paragraph "so what"

### What actually got built

The by-course framing sketched below ("which course needs a tutoring
session") turned out to have a real-data problem once written against the
actual dataset: course explains almost nothing in the three-course, three-
Fall-cohort slice used throughout Chapters 14-17 (a one-point spread in
`final_score`, under one percentage point in pass rate). Building a capstone
around a gap that thin would have made its own central "so what" false
stakes, exactly what Section 2's Trifecta Checkup teaches you to catch.

Pivoted to study-hours buckets instead, which show a real ~10-point spread
in `final_score` (correlation 0.29 with study hours) — a genuine, honest
finding to build the explore-to-explain narrative around. Same three-step
structure (audience/decision/medium, Trifecta Checkup, explore vs. explain),
same capstone exercise shape, different and truer running example.

This chapter landed as Chapter 17, which meant Dev Tools (17-26) and ML
landscape (27-31) both had to shift by one (see Part 3 below) — the
renumbering cascade flagged as a risk when this was first deferred.

---

## 2. The reorder itself

### New chapter map (`tutorials/01-python-basics/`)

| Old file | Old # | New file | New # |
|---|---|---|---|
| `01-python-core.ipynb` | 1 | unchanged | 1 |
| `02-control-flow.ipynb` | 2 | unchanged | 2 |
| `03-functions.ipynb` | 3 | unchanged | 3 |
| `04-classes.ipynb` | 4 | unchanged | 4 |
| `05-math-statistics.ipynb` | 5 | unchanged | 5 |
| `06-numpy.ipynb` | 6 | unchanged | 6 |
| `07-numpy-advanced.ipynb` | 7 | unchanged | 7 |
| `11-pandas-core.ipynb` | 11 | `08-pandas-core.ipynb` | 8 |
| `12-pandas-operations.ipynb` | 12 | `09-pandas-operations.ipynb` | 9 |
| `13-combining-reshaping.ipynb` | 13 | `10-combining-reshaping.ipynb` | 10 |
| `14-time-series.ipynb` | 14 | `11-time-series.ipynb` | 11 |
| `15-polars.ipynb` | 15 | `12-polars.ipynb` | 12 |
| `16-great-tables.ipynb` | 16 | `13-great-tables.ipynb` | 13 |
| `08-matplotlib.ipynb` | 8 | `14-matplotlib.ipynb` | 14 |
| `09-lets-plot.ipynb` | 9 | `15-lets-plot.ipynb` | 15 |
| `10-data-storytelling.ipynb` | 10 | `16-data-storytelling.ipynb` | 16 |

Dev-tools (17-26) and ml-intro (27-31) numbers are unaffected, but their
**content** now sits behind a different Chapter 16: Chapter 17's backward
reference currently says "Ch16 great-tables" and must become "Ch16
data-storytelling."

### Work items

1. `git mv` the 9 files above to their new names — **done**
2. Each moved file: update its own `title: "Chapter N: ..."` front matter
   and the Colab/download badge URLs (cell 1) to the new filename — **done**
3. Sweep every `tutorials/01-python-basics/*.ipynb` and
   `tutorials/02-dev-tools/17-vscode-setup.qmd` for `Chapter N` / `Sec. N`
   cross-references and remap using the table above — **done**. This also
   surfaced pre-existing chapter-number/filename mismatches that predate
   the reorder (e.g. Chapter 9's own cell 2 cited "Chapter 10" pointing at
   `13-combining-reshaping.ipynb`, off by 3, likely stale from an even
   earlier numbering pass). Fixed using the filename as ground truth.
   Chapter 8's and Chapter 16's connective prose needed a rewrite, not just
   a number swap, since their neighbors changed entirely: Chapter 8 no
   longer follows visualization (it now opens Data Analysis, right after
   Chapter 7), and Chapter 16 no longer precedes pandas-core (it's now the
   last chapter before Dev Tools) — added its missing "Next:" pointer to
   Chapter 17 to match every other chapter's convention.
4. Update `_quarto.yml` navigation order — **done**. Split the old
   "Python foundations" part (which held both language basics and
   visualization together) into three: "Python foundations" (1-7),
   "Data analysis" (8-13), "Data visualization" (14-16).
5. Re-execute every touched notebook end-to-end; zero tolerance for errors — **done**
6. Commit on `feature/let-plot-udate` — **done**

## 3. Unify the running dataset

**Status: done.** Chapters 14-16 (matplotlib, lets-plot, data-storytelling)
now load `university_analytics.csv` and filter to three courses that share
the same Fall track (Machine Learning, Data Structures, Python Programming)
across three real cohorts (Fall 2022-24) — the one real subset whose shape
matched the existing pedagogy closely enough that exercises and activity
instructions carried over almost unchanged. `exam_score` (synthetic) was
retired in favor of the real `final_score` column throughout. Chapter 16 was
already loading the real CSV but aliasing `final_score` back to the fake
`exam_score` name; that aliasing is gone too.

Two things deliberately stayed synthetic: Chapter 16's Datasaurus/Anscombe
demonstration needs precisely engineered matching-statistics-different-shape
data that real data will not reliably produce, and one isolated practice
drill in Chapter 14 that was never part of the running dataset to begin with.

Sweeping this also surfaced several pre-existing citation bugs unrelated to
the dataset itself (wrong chapter numbers, a plural "Chapters N and M" the
regex sweep missed the first time, one external citation to Wilke's own book
that a later, broader sweep almost mis-remapped as if it were this book's
numbering) — all fixed along the way.

## 4. Dev Tools and ML landscape shift

**Status: done.** Adding the capstone as Chapter 17 pushed Dev Tools from
17-26 to 18-27 and ML landscape from 27-31 to 28-32. Same sweep methodology
as Part 2: file renames, badge URLs, `Chapter N` remapping via a filename-
verified script, `_quarto.yml` nav update, full re-execution. One more
pre-existing mis-citation caught here too: pandas-operations' Further
Reading pointed its Wickham "Tidy data" citation at Chapter 16 (data
storytelling) when the `.melt()`/`.pivot_table()` material it actually
describes lives in Chapter 10 (combining-reshaping).
