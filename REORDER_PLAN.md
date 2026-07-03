# Act 1 reorder: Foundation → Data Analysis → Data Viz → Dev Tools

Decided 2026-07-03. Current order teaches visualization (matplotlib, lets-plot,
data storytelling) before pandas, which means Chapter 9 already builds and reads
`pd.DataFrame`s three chapters before pandas itself is taught. Reordering fixes
this and matches the real workflow: load and wrangle data, then visualize it.

---

## 1. Deferred: the data-storytelling capstone chapter

**Status: on hold until the reorder below lands.**

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

### Why it waits

Its chapter number, its backward references (which chapter is "the previous
one" depends on final Data Viz chapter order), and possibly its running
dataset all depend on the reorder below being settled first. Building it now
means rewriting it again once files move.

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

1. `git mv` the 9 files above to their new names
2. Each moved file: update its own `title: "Chapter N: ..."` front matter
   and the Colab/download badge URLs (cell 1) to the new filename
3. Sweep every `tutorials/01-python-basics/*.ipynb` and
   `tutorials/02-dev-tools/17-vscode-setup.qmd` for `Chapter N` / `Sec. N`
   cross-references and remap using the table above; verify by content, not
   just number, since Chapter 16's meaning changes
4. Update `_quarto.yml` navigation order
5. Unify the running dataset: rewrite Chapters 14-16 (matplotlib, lets-plot,
   data-storytelling) to use the pandas-taught `university_analytics.csv`
   as their primary example instead of hand-built numpy `DataFrame`s, since
   pandas is now taught first
6. Re-execute every touched notebook end-to-end; zero tolerance for errors
7. Commit on `feature/act1-reorder`, off `main`
