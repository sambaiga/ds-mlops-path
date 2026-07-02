# Python Foundations Notebook Improvement Plan

Each notebook must be implemented aligning with the skills and feedback in memory:

- [Writing principles](memory/feedback_writing_principles.md) -- hook before gate, reader as hero, contractions, one example fully told, "you" consistent
- [UX laws](memory/feedback_ux_laws.md) -- Von Restorff (max 1 KC per section), Peak-End Rule (strong ending), Chunking (one concept per cell), Hick's Law (concept density)
- [Notebook cell design](memory/feedback_notebook_cell_design.md) -- one executed concept per cell, every cell preceded by a markdown explaining the why
- [One concept per code cell](memory/feedback_one_concept_per_cell.md) -- each code cell demonstrates exactly one idea; split multi-concept cells
- [Chapter connections](memory/feedback_chapter_connections.md) -- cell 2 names what the previous chapter built and what this one enables next
- [Section titles](memory/feedback_section_titles.md) -- sentence case, no `&`, no `(Python X.Y+)` in headings
- [Diagram format](memory/feedback_diagram_format.md) -- SVG/PNG in `figs/`, never inline matplotlib
- [Diagrams and human voice](memory/feedback_diagrams_and_voice.md) -- at least one illustrative diagram per notebook; prose must sound like a person talking, not a reference manual
- [No em-dashes](memory/feedback_no_em_dash.md) -- never use `--` em-dash; use a comma, colon, or rewrite the sentence
- [No Python version labels in code](memory/feedback_no_version_labels.md) -- no `# Python 3.x+` comments; mention once in prose if genuinely notable
- [Bootstrap icons not emojis](memory/feedback_icons_not_emojis.md) -- `<i class="bi bi-*">` everywhere; no emoji characters
- [Example data](memory/feedback_example_data.md) -- university analytics domain throughout; no ML-specific variables before Part 4
- [Content placement](memory/feedback_nb_content_placement.md) -- NamedTuple/TypedDict in Chapter 4; walrus in Chapter 2; deque in Chapter 14; statistics in Chapter 5 or Chapter 11

---

## Introduction: The ML and data science landscape (`tutorials/00-landscape.qmd`) -- NEW

*A QMD file (no code cells) that sits at the top of the book before Chapter 1. Rewritten from the current Chapter 22 for complete beginners: no Python knowledge assumed.*

**Purpose:** Answer the question every learner brings on page one: "Why am I spending eight chapters on Python before touching ML?" The Introduction gives them the destination before they take the first step, then hands them back to Chapter 1 with a reason to continue.

**File location:** `tutorials/00-landscape.qmd` (root of tutorials, no subfolder).

**Format:** QMD, all diagrams as SVGs in `tutorials/figs/`, Bootstrap Icons throughout, no em-dashes, human voice writing consistent with book tone.

### Section structure

**Section 1: The problem that motivates this book**

Keep the energy theft hook from the current Chapter 22. It is the strongest motivating example in the book. Rewrite the framing for a complete beginner: no references to "chapters gave you Python," no code examples. End the section with the core insight: traditional programming gives the computer rules; machine learning gives it examples and lets it find the rules itself.

**Section 2: Precise terms for a noisy conversation**

First use of "AI": write the full term "Artificial Intelligence (AI)" before using the abbreviation. Then define the four terms the book actually uses, ordered from broadest to narrowest:

- **Artificial Intelligence (AI):** the broad goal of making machines behave intelligently; the umbrella term headlines use
- **Machine Learning (ML):** one approach to AI: a system that learns patterns from data instead of following rules written by hand
- **Data Science:** the practice of extracting insight and decisions from data, using ML as one of many tools
- **MLOps:** the engineering discipline that takes a trained model and puts it into production, keeps it monitored, and replaces it when it drifts

**Diagram: the relationship between AI, ML, Data Science, and MLOps.**

Replace the existing three-tier capability diagram (which shows AI, Deep Learning, ML as nested circles without MLOps). Use a new SVG that shows:

- Three nested ovals: AI (outermost), ML (inside AI), Deep Learning (inside ML) -- this shows the subset relationship
- A bracket outside the ovals labelled "Data Science" with a note: "uses ML as a tool, but also statistics, domain knowledge, and communication"
- A separate column or bracket labelled "MLOps" with a note: "the engineering practice that takes ML to production"
- Clear labels on every shape; no abbreviations on first appearance in the diagram itself

The key message: ML is the technical substance; AI is the umbrella. Data Science is a practice that uses ML. MLOps is the engineering layer that operationalises the output.

**Section 3: The tool stack**

Two-column diagram: left column is what this book covers in full; right column shows where it connects to the wider ecosystem.

Left column (what the book teaches, bottom to top):

- Python (language foundation)
- NumPy, Pandas (data manipulation)
- Matplotlib, Lets-Plot, Great Tables (data communication)
- scikit-learn, XGBoost (model building)
- MLflow, Docker (model deployment and tracking)

Right column (connects to, but not covered in depth):

- System design: how ML services fit into software architecture
- Value-driven AI/ML: how business value, ethics, and stakeholder needs shape what gets built
- Deep Learning: PyTorch, TensorFlow (introduced but not the primary focus)

One sentence per layer. The right column makes explicit that the book covers a focused path, not the entire field.

**Section 4: Why you learn Python before ML**

The microscope analogy. A biology student who wants to study cells spends their first lab session learning the microscope: not because microscopes are interesting in themselves, but because the tool is what makes the science possible. ML is the goal; Python, NumPy, and Pandas are the microscope. Three sentences max.

**Section 5: Your learning path**

A clean roadmap table using "Chapter" consistently, not "Part":

| Chapters | Topic | What you build | What it unlocks |
| --- | --- | --- | --- |
| 1-5 | Python foundations | Variables, control flow, functions, classes, standard library | You can write and reason about Python programs |
| 6-10 | Scientific Python | NumPy, Matplotlib, Lets-Plot, data storytelling | You can process and visualise numerical data |
| 11-16 | Data tools | Pandas, time series, Polars, Great Tables | You can load, clean, transform, and present real datasets |
| 17+ | Machine learning | sklearn, evaluation, MLflow, deployment | You can build, evaluate, and ship ML models |

End with one sentence connecting back to Chapter 1: "Chapter 1 starts with Python because everything else is built on it."

### What changes from the current Chapter 22

- Remove the "Before you begin" prerequisites block (nothing precedes the Introduction)
- Remove all references to "chapters gave you Python" and similar
- Remove forward references to specific chapter numbers (numbering is changing)
- Remove the Learning Objectives table (the Introduction is orientation, not a skill chapter)
- Keep: energy theft hook, rules-vs-patterns framing
- Replace: the AI/ML/Deep Learning nested diagram -- add MLOps, Data Science, and the two-column tool stack
- Fix: "AI" always written as "Artificial Intelligence (AI)" on first use, then abbreviated

---

## Prerequisite: rename notebooks from a/b to natural progression -- DONE

The current `03a`/`03b`/`04a`/`04b` naming breaks natural reading order and makes the ToC confusing. Before implementing any individual notebook, rename every file and update `_quarto.yml` and all internal cross-references.

### New chapter map

| New file | Old file | Title |
|---|---|---|
| `01-python-core.ipynb` | `01-python-core.ipynb` | Python core |
| `02-control-flow.ipynb` | `02-control-flow.ipynb` | Control flow |
| `03-functions.ipynb` | `03a-python-patterns.ipynb` | Functions |
| `04-classes.ipynb` | `03b-python-patterns.ipynb` | Classes and patterns |
| **`05-math-statistics.ipynb`** | *(new)* | Python math and statistics |
| `06-numpy.ipynb` | `04a-numpy.ipynb` | NumPy basics |
| `07-numpy-advanced.ipynb` | `04b-numpy.ipynb` | NumPy advanced |
| `08-matplotlib.ipynb` | `05-matplotlib.ipynb` | Matplotlib and Seaborn |
| `09-lets-plot.ipynb` | `06-lets-plot.ipynb` | Lets-Plot |
| `10-data-storytelling.ipynb` | `07-data-storytelling.ipynb` | Data storytelling |
| `11-pandas-core.ipynb` | `08-pandas-core.ipynb` | Pandas core |
| `12-pandas-operations.ipynb` | `09-pandas-operations.ipynb` | Pandas operations |
| `13-combining-reshaping.ipynb` | `10-combining-reshaping.ipynb` | Combining and reshaping |
| `14-time-series.ipynb` | `11-time-series.ipynb` | Time series |
| `15-polars.ipynb` | `11-polars.ipynb` | Polars |
| `16-great-tables.ipynb` | `12-great-tables.ipynb` | Great Tables |

---

## Chapter 1: Python core (`01-python-core.ipynb`) -- DONE (partial revision needed)

Restructured in PR #31. Reference implementation for all subsequent notebooks.

Key decisions recorded:
- Section order: variables, operators, strings, collections overview, lists, tuples, dictionaries, sets, standard library tools
- Strong ending paragraph closes the opening CSV hook
- All ML-specific examples replaced with university/student data

**Additional issues to fix in a follow-up pass:**

**Hook needs rewriting for first-time programmers.** The current hook ("You receive a CSV file...") assumes the learner already knows what a CSV is and why it matters. A person learning programming for the first time needs a hook about giving precise instructions to a computer: no ambiguity, no common sense, no inference. The computer does exactly what you say, nothing more. That is why every word in a program matters.

**Collections Section 4: duplication and missing guidance.**
- The "when to use which collection" guidance and "key operations at a glance" content are scattered across multiple subsections rather than anchored once in the overview.
- Move "when to use" to the Section 4 overview (before any individual collection): one table, four rows, one-line answer per type.
- Each collection subsection (lists, tuples, dicts, sets) keeps its own "key operations" block, but remove any content that duplicates what the overview already said.
- Check for any cells that repeat the same operation across two subsections and consolidate.

---

## Chapter 2: Control flow (`02-control-flow.ipynb`) -- DONE

Completed on branch `fix/python-basics-ch02-control-flow`.

Key decisions recorded:
- Hook replaced: ML training loop with epochs/loss replaced by student record validation scenario
- Sections: branching with if and elif (1), match and case (2), for loops (3), while loops/break/continue (4), comprehensions (5)
- All match/case examples use student enrollment records
- For loops removed from sections 1 and 2 (before loops are introduced)
- Walrus operator added to section 4 with `io.StringIO` example
- Monte Carlo capstone replaced with student CSV processing capstone
- One concept per code cell throughout

---

## Chapter 3: Functions (`03-functions.ipynb`)

*Renamed from `03a-python-patterns.ipynb`.*

**Issues to fix:**

**No KC callouts (0 in entire notebook):** Add at minimum: one for function definition syntax, one for docstrings, one for the mutable default argument danger.

**First function too complex (cell 5):** The very first code cell shows a 4-parameter function with type hints, tuple defaults, and a full Google-style docstring. A learner seeing functions for the first time needs to start with the simplest possible case:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
Then build up: add a second parameter, then a default, then the return type annotation, then finally the docstring.

**Docstrings never introduced:** The section intro (cell 4) does not explain what a docstring is, why it exists, or how to write one. But every function from cell 5 onward already has a full `Args:/Returns:/Raises:` block. Add a dedicated markdown cell that introduces docstrings before the first function that uses one. Explain: what it is (a string literal as the first statement), why it matters (IDEs, `help()`, auto-generated docs), and what the Google style looks like.

**`raise ValueError` before exceptions are covered (cell 9):** `score_summary` raises a `ValueError` but exception handling is not taught until Chapter 4. Either use an early return with `None` instead, or add a one-sentence forward reference ("Exception handling is covered in Chapter 4; for now, read `raise` as 'stop and report this problem'").

**`import statistics` (cell 13):** Statistics module moves to Chapter 5. Replace the `normalize()` function's dependency on `statistics` with inline `sum(x) / len(x)` and a manual standard deviation calculation, or remove the normalize function from this section.

**ML-specific *args/**kwargs examples (cells 30, 34, 42):**
- `ensemble_predict(*predictions)` -- replace with `aggregate_scores(*score_lists)`
- `build_config(model, **hyperparams)` -- replace with `build_student_profile(name, **attributes)`
- `log_metrics(epoch, **metrics)` -- replace with `log_cohort_stats(semester, **metrics)`

**Dataclass section (Section 4):** Move entirely to Chapter 4 (classes). A dataclass is a shorthand for a class; it must follow the class section so the reader understands what the shorthand replaces.

**Modules section (Section 5):** Keep `math`, `json`. Remove `random` (moving to Chapter 5 math/statistics). Remove `statistics` (moving to Chapter 5).

**Section title:** `## 5. Modules & the Standard Library` has `&`; fix to `## 5. Modules and the standard library`.

---

## Chapter 4: Classes and patterns (`04-classes.ipynb`)

*Renamed from `03b-python-patterns.ipynb`. Receives dataclass, NamedTuple, TypedDict, and type aliases from Chapter 1.*

**Hook (cell 2):** Current hook is reasonable ("three functions that belong together...") but can be sharpened. "A student record is not three separate variables; it is one thing. A class lets you treat it that way: one name, one `repr()`, one place where the rules about valid scores live."

**New section structure:**
1. Classes (`__init__`, `__repr__`, `@property`, `@classmethod`)
2. Inheritance and abstract base classes
3. Dataclasses *(moved from Chapter 3)*
4. NamedTuple *(moved from Chapter 1)*
5. TypedDict and type aliases *(moved from Chapter 1)*
6. Exception handling
7. File I/O with pathlib
8. Python gotchas *(trimmed)*

**sklearn/pandas references (cells 11, 20):**
- Cell 11: replace pandas/sklearn examples with `StudentRecord.from_csv_row(row)` factory method example
- Cell 20: replace "ModelCard Class" activity with `CourseRecord` or `StudentProfile` class activity

**Repeated gotchas from Chapter 1:**
- Gotcha 3 (`/` vs `//`) is already in Chapter 1 operators section; remove
- Gotcha 4 (`{}` is a dict, not a set) is already in Chapter 1 sets section; remove
- Replace with: late binding in closures and class-level vs instance-level mutable attributes

**"Five reproducible patterns" vs actual count:** Change the claim in Learning Objectives to match the actual count after trimming.

**Section title fixes:** `### Reading & Writing Files`, `### Creating & Checking Directories`; replace `&` with `and`.

---

## Chapter 5: Python math and statistics (`05-math-statistics.ipynb`) -- NEW

*New notebook. Bridges pure Python (Chapters 1-4) to scientific Python (Chapters 6+).*

**Why here:** After learning functions and classes, the learner can reason about what `math.sqrt()` and `statistics.mean()` are doing. Before NumPy, they need a mental model of "single-value math" vs "array math." This chapter provides the Python-only tools, then ends with "these work on one number at a time; NumPy works on thousands at once."

**Section structure:**
1. The `math` module: precise arithmetic for single values (`sqrt`, `log`, `ceil`, `floor`, `pi`, `e`, `isnan`, `isinf`)
2. The `statistics` module: descriptive stats without any library (`mean`, `median`, `stdev`, `mode`, `NormalDist`)
3. The `random` module: sampling and shuffling (`random.sample`, `random.choices`, `random.shuffle`, `random.seed`)
4. Combining them: a student grade report using only standard library tools

**Hook:** "You can already store a list of scores. Now what? You need the highest, the average, and whether a score is unusually low. Before you reach for pandas or NumPy, Python's standard library gives you everything you need for these calculations; no install required."

**Connection to next chapter:** End with: "These functions work on one list, one value at a time. If you have 100,000 measurements, they are too slow. Chapter 6 shows you NumPy: the same ideas, but running across thousands of values at once, in compiled code."

**Examples:** All university data. `statistics.NormalDist` to detect outlier scores. `random.sample` to simulate drawing a test cohort.

---

## Chapter 6: NumPy basics (`06-numpy.ipynb`)

*Renamed from `04a-numpy.ipynb`.*

**Primary issue:** Review for ML-specific framing. The feature matrix (`X`, `feature_names` as ML terminology) should be reframed as a student data matrix: "5 students, 3 measurements each."

**Connection sentence (cell 2):** Should explicitly name Chapter 5 as the "single-value math" that NumPy replaces at scale.

Detailed review to follow when this chapter is reached.

---

## Chapter 7: NumPy advanced (`07-numpy-advanced.ipynb`)

*Renamed from `04b-numpy.ipynb`.*

**Emojis (cell 40):** Replace with Bootstrap Icons or prose.

**"Feature matrix" framing:** Setup cell uses `X` and ML terminology; reframe as student data matrix.

**Add strides section:** After broadcasting, add one section on `arr.strides` and `arr.itemsize`:
- Show what `arr.strides` returns and how it relates to `arr.shape` and `arr.itemsize`
- Demonstrate how a 2D array is just a 1D block of memory with two step sizes
- Keep it conceptual; the rolling-window application belongs in Chapter 14
- Do NOT teach `np.lib.stride_tricks.as_strided()`: it is dangerous (reads outside the array silently)

Detailed review to follow when this chapter is reached.

---

## Chapter 8: Matplotlib and Seaborn (`08-matplotlib.ipynb`)

*Renamed from `05-matplotlib.ipynb`.*

**Plotting ecosystem callout missing:** Add a brief orientation covering Matplotlib/Seaborn (static, publication-quality), Plotly/Bokeh (interactive, dashboards), and Altair (grammar of graphics, concise for smaller datasets). One sentence per library.

**Seaborn new features missing:** Add one concrete example using `so.Plot()` on university data to show the `seaborn.objects` declarative interface.

**Seaborn section references pandas early:** Frame it as "a preview of what pandas makes easy; we will cover it properly in Chapter 11" or restructure to use plain arrays where possible.

Detailed review to follow when this chapter is reached.

---

## Chapters 9-16: deferred review

Chapters 9-16 are reviewed and improved one at a time after the foundations (Chapters 1-8) are complete. The individual chapter plans below reflect the actual state of each file.

---

## Chapter 9: Grammar of graphics with lets-plot (`09-lets-plot.ipynb`)

**Issues found (62 cells):**

**DS-MLOps header block in cell 2.** `**DS-MLOps Python Foundations**` and `**Python 3.12+ | Author: Anthony Faustine**` must be removed. After removal, the opener reads "Part 5 built charts by calling functions..." -- the contrast framing is good but "Part 5" must become "Chapter 8".

**Cell 2 and cell 3 duplicate content.** Cell 2 explains that Matplotlib required separate function calls for each visual channel. Cell 3 opens "You have already drawn scatter plots with Matplotlib. You called `ax.scatter(x, y, c=color, s=size)`..." -- same argument, same code reference. Remove the first two paragraphs of cell 3; keep from "There is another way to think about it. A chart isn't a list of drawing commands..." onward. This mirrors the fix applied to Ch8 and Ch11.

**8 title-case headings to fix:**

- `## Before You Begin` -- `## Before you begin`
- `## Why Grammar of Graphics?` -- `## Why the grammar of graphics?`
- `## Learning Objectives` -- `## Learning objectives`
- `## 1. Declarative vs. Imperative` -- `## 1. Declarative vs. imperative`
- `## 3. Mapping vs. Setting` -- `## 3. Mapping vs. setting`
- `## 4. Layering: Raw Data and a Statistical Summary Together` -- `## 4. Layering: raw data and a statistical summary together`
- `## 5. Faceting: One Plot, Many Panels` -- `## 5. Faceting: one plot, many panels`
- `## 6. Titles, Labels, and Scales` -- `## 6. Titles, labels, and scales`
- `## Capstone: The Three-Panel Report, Declaratively` -- `## Capstone: the three-panel report, declaratively`

**3 double-dashes** (`--`) in cell 2 prose. Fix each to a comma or colon.

**20 inline `<div style='background:#'>` callouts** need ark class conversion (same pattern as Ch8: concept, activity, mistake, tip). Apply the same ARK_CONV table used for Ch8.

**`pip install lets-plot`** in cell 2 "Before you begin" -- replace with `uv add lets-plot`.

**"Part 5", "Part 6", "Part 7" refs** throughout -- replace with "Chapter 8", "Chapter 9", "Chapter 10" respectively.

**Consistency with Ch8 ecosystem table:** Cell 3 already mentions Vega-Altair in the "Alternatives that use the same grammar" table. This is consistent with the Altair row added to Ch8. No change needed here.

**`By the end of Part 5`** in Learning Objectives cell -- replace with "Chapter 9".

---

## Chapter 11: Pandas core (`11-pandas-core.ipynb`)

**Issues found (73 cells):**

**DS-MLOps header block in cell 2.** `**DS-MLOps Data Analysis**` and `**Python 3.12+ | Author: Anthony Faustine**` must be removed. After removal, cell 2 opens "You have a CSV. It has 2,400 rows, 10 columns, and three questions from your manager..." -- this is the correct problem-first hook, keep it.

**Cell 3 duplicates cell 2 hook.** Cell 3 section "## The Tool That Thinks in Tables" opens with the exact same sentences: "You have a CSV. It has 2,400 rows, 10 columns, and three questions from your manager..." Remove those two opening paragraphs from cell 3; keep from "**pandas** ([pandas.pydata.org](https://pandas.pydata.org)) was created at AQR Capital in 2008..." onward.

**8 title-case headings to fix:**

- `## Before You Begin` -- `## Before you begin`
- `## The Tool That Thinks in Tables` -- `## The tool that thinks in tables`
- `## Learning Objectives` -- `## Learning objectives`
- `## 1. Series and DataFrame` -- `## 1. Series and DataFrame` (acronym, keep capitalisation)
- `## 2. Reading and Inspecting Data` -- `## 2. Reading and inspecting data`
- `## 3. Selecting Rows and Columns` -- `## 3. Selecting rows and columns`
- `## 4. Boolean Filtering` -- `## 4. Boolean filtering` (Boolean is a proper noun, keep)
- `## 8. Memory Usage and the Categorical Dtype` -- `## 8. Memory usage and the categorical dtype`

**7 double-dashes** in prose -- fix each to comma or colon.

**22 inline `<div style='background:#'>` callouts** need ark class conversion.

**2 `pip install pandas` references** -- replace with `uv add pandas`.

**Part refs** (Part 3, 4, 7, 8, 9, 11) -- replace with Chapter numbers throughout.

**`By the end of Part X`** in LO cell -- replace with "Chapter 11".

**Missing `statistics` module comparison.** Add one markdown cell in the Series and DataFrame section (Section 1) that reads: "Before pandas, you'd write `statistics.mean(scores)` to get the mean of a list. With pandas, you write `df['score'].mean()` -- the same idea, but it works across any column in a table, handles missing values automatically, and stays readable when you chain it with other operations." This is the canonical comparison the plan identified for this chapter.

---

## Chapter 14: Time series (`14-time-series.ipynb`)

**Issues found (57 cells):**

**Opener is strong.** "The attendance report says 87% for Monday. Is that better or worse than last month?" -- no change needed.

**3 double-dashes** in cell 2 and later cells -- fix to commas or colons.

**17 inline `<div style='background:#'>` callouts** need ark class conversion. One non-standard color variant: `background:#EAF7F0;border-left:5px solid #059669` (a lighter green used for "Example" callouts) -- map to `ark-activity` since it is a worked example for the learner.

**5 title-case headings to fix:**

- `## Learning Objectives` -- `## Learning objectives`
- `## 1. Date and Time Data Types` -- `## 1. Date and time data types`
- `## 3. Selecting Data from a Time Series` -- `## 3. Selecting data from a time series`
- `## 4. The Power of Pandas: resample` -- `## 4. The power of pandas: resample` (The Power = title case)
- `## 6. Lag, Lead, and Autocorrelation` -- `## 6. Lag, lead, and autocorrelation`

**Part refs** (Part 3, 10, 11, 12) -- replace with Chapter numbers.

**`By the end of Part 11`** in LO -- replace with "Chapter 14".

**Missing `deque` and `sliding_window_view` section.** Section 6 currently shows only pandas `.rolling()`. Add a new Section 7 that introduces two lower-level tools side by side, with clear "when to use each" framing:

- `np.lib.stride_tricks.sliding_window_view(arr, window_shape=n)`: produces a 2D view where each row is one window; compute statistics across all windows in a single vectorised call. Use when the full dataset fits in memory and you want batch computation.
- `collections.deque(maxlen=n)`: processes one value at a time; the oldest value drops off automatically as new ones arrive. Use when data arrives as a stream and you cannot load it all at once.

Do NOT use `np.lib.stride_tricks.as_strided()` directly -- it reads outside the array silently. `sliding_window_view` is the safe wrapper (NumPy 1.20+).

Keep all examples on the attendance data already in the notebook. A 7-day rolling window is a natural use case.

---

## Chapter 15: Polars (`15-polars.ipynb`)

**Issues found (84 cells):**

**Opener is strong.** "Your pandas pipeline handles 10,000 rows without complaint. Then the dataset grows to 10 million rows..." -- contrast hook, keep it.

**Cell 2 and cell 4 partial overlap.** Cell 2 says "10 million rows and a groupby takes 40 seconds." Cell 4 (## When pandas Is Not Enough) opens "Your pandas pipeline works perfectly at 50,000 rows. The groupby runs in a second..." -- different numbers but the same argument. Remove the opening two sentences of cell 4; start from "This isn't a pandas bug. It is a design trade-off..." or from the sentence that explains WHY pandas is slow (single-threaded, Python object model).

**7 double-dashes** in prose -- fix to commas or colons.

**25 inline `<div style='background:#'>` callouts** need ark class conversion -- the heaviest conversion task in Chapters 9-16.

**6 title-case headings to fix:**

- `## When pandas Is Not Enough` -- `## When pandas is not enough`
- `## 1. DataFrame Construction` -- `## 1. DataFrame construction` (DataFrame is a proper noun compound, capitalise D and F)
- `## 2. The Expression API: select, filter, with_columns` -- `## 2. The expression API: select, filter, with_columns`
- `## 3. GroupBy and Aggregation` -- `## 3. GroupBy and aggregation` (GroupBy is the pandas/polars term, keep capitalisation)
- `## 4. LazyFrame and Lazy Evaluation` -- `## 4. LazyFrame and lazy evaluation` (LazyFrame is a type name, keep; "Lazy Evaluation" is not)
- `## 4.5 SQL Interface` -- rename to `## 5. SQL interface` and renumber subsequent sections accordingly

**Part refs** (Part 7, 8, 9, 10, 11) -- replace with Chapter numbers.

**Stale ref in cell 2:** "Polars concepts carry forward into the MLOps section and streaming pipelines in Part 7" -- "Part 7" is ambiguous. Replace with the specific chapter reference (Chapter 10 or the relevant MLOps chapter).

**Missing Chapter 12 connection.** Cell 2 connects to Chapter 13 (combining/reshaping) but not Chapter 12 (pandas operations). The Polars expression API (`select`, `filter`, `groupby`) maps directly to Chapter 12 operations (`df.groupby()`, `df.merge()`). Add one sentence to cell 2: "The expression API in Section 2 mirrors the groupby and merge patterns from Chapter 12 (`12-pandas-operations.ipynb`), so you can compare both styles on the same problems."

---

## Chapter 22: The ML landscape (`tutorials/04-ml-intro/01-ml-introduction.qmd`)

Chapter 22 stays in place. By the time a learner reaches it, they have Python, NumPy, and Pandas. They can appreciate the technical depth that the Introduction only sketched.

**Hook change: done.** "The Introduction showed you the destination. You have now built the tools to understand it properly." -- this matches the plan's intent. No change needed.

**4 callout issues remaining:**

**`bi-info-circle-fill` in two concept callouts** -- replace with `bi-key-fill` (the correct icon for `ark-concept` callouts, as established in Ch8).

**Activity title format:** `Activity 1 - Map the System` -- fix to `Activity 1: map the system` (colon separator, sentence case, consistent with Ch8 format).

**`<b>Goal:</b>` in activity body** -- remove the `<b>Goal:</b>` prefix from the activity description (same pattern applied to Ch8 and Ch4).

**3 title-case headings to fix:**

- `## Learning Objectives` -- `## Learning objectives`
- `## 1. The AI Landscape` -- `## 1. The AI landscape` (AI is an acronym, keep; "Landscape" is not a proper noun)
- `## Further Reading` -- `## Further reading`

**Part refs** (Part 12, 21, 22, 23, 24) -- replace with Chapter numbers throughout. "Part 22" in the Learning Objectives self-reference becomes "this chapter". "Part 23", "Part 24" become Chapter 23, Chapter 24.

---

## Implementation checklist per notebook

For every notebook implementation, verify before finishing:

- [ ] Hook does not assume ML knowledge (no epochs, loss, training loops before Chapter 6)
- [ ] Cell 2 names what the previous chapter built and what this one enables
- [ ] Each section intro adds one sentence connecting to the opening scenario
- [ ] No `&` in any section heading
- [ ] No `(Python X.Y+)` version labels in headings
- [ ] No emoji characters; Bootstrap Icons only
- [ ] No for/while loops used before loops are introduced (Chapter 2)
- [ ] No functions used before functions are introduced (Chapter 3)
- [ ] No classes used before classes are introduced (Chapter 4)
- [ ] No pandas/sklearn/numpy references before those chapters
- [ ] All code examples use university analytics domain (student IDs, scores, courses, GPA)
- [ ] `uv add <package>` not `pip install <package>`
- [ ] Max 1 KC callout per section (Von Restorff)
- [ ] At least one diagram per notebook (SVG in `figs/`, not inline matplotlib)
- [ ] Strong ending paragraph closes the opening hook (Peak-End Rule)
- [ ] No em-dashes anywhere
- [ ] Prose sounds like a person explaining something, not a reference manual
- [ ] One concept per code cell; every code cell preceded by a markdown cell
