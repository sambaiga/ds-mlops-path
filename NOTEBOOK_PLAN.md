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

## Part 0: The ML and data science landscape (`tutorials/00-landscape.qmd`) -- NEW

*A QMD file (no code cells) that sits at the top of the book before Chapter 1. Rewritten from the current Part 22 for complete beginners: no Python knowledge assumed.*

**Purpose:** Answer the question every learner brings on page one: "Why am I spending eight chapters on Python before touching ML?" Part 0 gives them the destination before they take the first step, then hands them back to Chapter 1 with a reason to continue.

**File location:** `tutorials/00-landscape.qmd` (root of tutorials, no subfolder).

**Format:** QMD, all diagrams as SVGs in `tutorials/figs/`, Bootstrap Icons throughout, no em-dashes, human voice writing consistent with book tone.

### Section structure

**Section 1: The problem that motivates this book**

Keep the energy theft hook from the current Part 22. It is the strongest motivating example in the book. Rewrite the framing for a complete beginner: no references to "Parts 1-3 gave you Python," no code examples. End the section with the core insight: traditional programming gives the computer rules; machine learning gives it examples and lets it find the rules itself.

**Section 2: Precise terms for a noisy conversation**

Open directly with the claim: "AI is what headlines use. It covers everything from a chess engine to a chatbot. What this book is about is more specific." Then define the three terms the book actually uses:

- **Machine Learning:** a system that learns patterns from data instead of following rules written by hand
- **Data Science:** the practice of extracting insight and decisions from data, using ML as one of many tools
- **MLOps:** the engineering discipline that puts models into production and keeps them working

Adapt the existing three-tier capability diagram from Part 22. The key message: ML is the technical substance; AI is the umbrella term that business and journalism use for all of it.

**Section 3: The tool stack**

One diagram: Python at the base, NumPy and Pandas above it, then sklearn and XGBoost, then MLflow and Docker at the top. One sentence per layer. The learner sees their full destination before taking the first step. No code.

**Section 4: Why you learn Python before ML**

The microscope analogy. A biology student who wants to study cells spends their first lab session learning the microscope: not because microscopes are interesting in themselves, but because the tool is what makes the science possible. ML is the goal; Python, NumPy, and Pandas are the microscope. Three sentences max.

**Section 5: Your learning path**

A clean roadmap table (own simplified version, not a copy of the index.qmd Acts cards):

| Part | Chapters | What you build | What it unlocks |
|------|----------|----------------|-----------------|
| Python foundations | 1-8 | Variables, control flow, functions, classes, data tools | You can write Python and work with structured data |
| Data tools | 9-16 | NumPy, Pandas, Matplotlib, Polars, Great Tables | You can load, clean, transform, and visualise real datasets |
| Machine learning | 17+ | sklearn, model evaluation, MLflow, deployment | You can build, evaluate, and ship ML models |

End with one sentence connecting back to Chapter 1: "Chapter 1 starts with Python because everything else is built on it."

### What changes from the current Part 22

- Remove the "Before you begin" prerequisites block (nothing precedes Part 0)
- Remove all references to "Parts 1-3 gave you Python" and similar
- Remove forward references to specific part numbers (numbering is changing)
- Remove the Learning Objectives table (Part 0 is orientation, not a skill chapter)
- Keep: energy theft hook, rules-vs-patterns framing, capability diagram

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

Chapters 9-16 will be reviewed and improved one at a time after the foundations (Chapters 1-8) are complete. Key notes:

- **Chapter 9 (Lets-Plot):** Review for consistency with the plotting ecosystem framing in Chapter 8
- **Chapter 11 (Pandas core):** This is where the `statistics` module comparison belongs ("before pandas you'd write `statistics.mean(scores)`; now you write `df['score'].mean()`")
- **Chapter 14 (Time series):** This is where `deque` and `sliding_window_view` come together. Introduce two tools for rolling windows side by side:
  - `np.lib.stride_tricks.sliding_window_view(arr, window_shape=n)`: NumPy-speed batch computation; preferred when you process all windows in one pass
  - `collections.deque(maxlen=n)`: append one value at a time in a live stream; preferred when data arrives incrementally
  - Do NOT use `as_strided` directly; `sliding_window_view` is the safe modern API (NumPy 1.20+)
- **Chapter 15 (Polars):** Review for connection to Chapters 11 and 12

---

## Part 22: The ML landscape (`tutorials/04-ml-intro/01-ml-introduction.qmd`) -- REVISE HOOK ONLY

Part 22 stays in place. By the time a learner reaches it, they have Python, NumPy, and Pandas. They can appreciate the technical depth that Part 0 only sketched.

**The only change needed:** The current hook opens with "Parts 1-3 gave you Python, data tools, and a professional dev setup." Replace that with a connection back to Part 0: "Part 0 showed you the destination. You have now built the tools to understand it properly." Then continue into the deeper ML taxonomy as currently written.

**Why keep it:** Part 0 is orientation for a beginner. Part 22 is a deeper look at the same landscape, now that the learner has the vocabulary and tools to appreciate the distinctions. This is the spiral curriculum: the same idea revisited at increasing depth.

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
