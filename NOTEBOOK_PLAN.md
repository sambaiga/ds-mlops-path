# Python Foundations Notebook Improvement Plan

Each notebook must be implemented aligning with the skills and feedback in memory:

- [Writing principles](memory/feedback_writing_principles.md) -- hook before gate, reader as hero, contractions, one example fully told, "you" consistent
- [UX laws](memory/feedback_ux_laws.md) -- Von Restorff (max 1 KC per section), Peak-End Rule (strong ending), Chunking (one concept per cell), Hick's Law (concept density)
- [Notebook cell design](memory/feedback_notebook_cell_design.md) -- one executed concept per cell, every code cell preceded by a markdown explaining the why
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

## Prerequisite: rename notebooks from a/b to natural progression

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

## Chapter 1: Python core (`01-python-core.ipynb`) -- DONE

Completed in PR #31. Reference implementation for all subsequent notebooks.

Key decisions recorded:
- Section order: variables → operators → strings → collections overview → lists → tuples → dictionaries → sets → standard library tools
- Strong ending paragraph closes the opening CSV hook
- All ML-specific examples replaced with university/student data

---

## Chapter 2: Control flow (`02-control-flow.ipynb`)

**Hook (cell 2):** Replace ML training loop scenario. Suggested: "You have 2,400 student records to validate. Some have `None` scores. Some store grades as strings. You need code that checks conditions, skips bad rows, and processes only valid data -- that is control flow."

**Section structure:**
1. Branching with if and elif
2. Match and case *(add walrus `:=` here -- its natural home is `while (row := reader.next()):`)*
3. For loops
4. While loops, break, and continue
5. Comprehensions

**Issues to fix:**
- Title `## 1. Control Flow: if / elif / else & match / case` violates `&` rule and packs two constructs into one section; split into separate sections
- `### match / case: Structural Pattern Matching (Python 3.10+)` has version label in heading
- Cell 14 uses a `for` loop inside a match/case example before the for loop section is reached -- replace with a non-loop version
- `pip install tqdm` (cell 26) -- change to `uv add tqdm`
- Activity "Training Log with enumerate and zip" (cell 28) -- ML framing; replace with student record processing
- Cells 12, 14, 21, 28, 31: `epoch`, `train_loss` variable names -- replace with student data
- **Capstone (cells 51-58): Monte Carlo pi estimation does not fit the series** -- a learner on their first control flow notebook has no frame for why they'd estimate pi with random points. Replace with a capstone that processes the student CSV: iterate over records, apply if/elif to classify students (distinction / pass / fail), use a while loop to find the first student above a threshold, build a summary with a comprehension
- Add walrus operator section to the while loops area (removed from Chapter 1, belongs here)

**Placement note:** Add the walrus operator `:=` at the end of Section 4 (while loops). One code cell, one practical example (`while (line := f.readline()):`), one KC callout.

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

**`raise ValueError` before exceptions are covered (cell 9):** `score_summary` raises a `ValueError` but exception handling is not taught until Chapter 4. Either use an early return with `None` instead, or add a one-sentence forward reference ("Exception handling is covered in Chapter 4 -- for now, read `raise` as 'stop and report this problem'").

**`import statistics` (cell 13):** Statistics module moves to Chapter 5. Replace the `normalize()` function's dependency on `statistics` with inline `sum(x) / len(x)` and a manual standard deviation calculation, or remove the normalize function from this section.

**ML-specific *args/**kwargs examples (cells 30, 34, 42):**
- `ensemble_predict(*predictions)` -- replace with `aggregate_scores(*score_lists)`
- `build_config(model, **hyperparams)` -- replace with `build_student_profile(name, **attributes)`
- `log_metrics(epoch, **metrics)` -- replace with `log_cohort_stats(semester, **metrics)`

**Dataclass section (Section 4):** Move entirely to Chapter 4 (classes). A dataclass is a shorthand for a class -- it must follow the class section so the reader understands what the shorthand replaces.

**Modules section (Section 5):** Keep `math`, `json`. Remove `random` (it is moving to Chapter 5 math/statistics). Remove `statistics` (moving to Chapter 5). The `random` module in the current notebook is introduced as a demo but Chapter 5 covers it properly.

**Section title:** `## 5. Modules & the Standard Library` has `&` -- fix to `## 5. Modules and the standard library`.

---

## Chapter 4: Classes and patterns (`04-classes.ipynb`)

*Renamed from `03b-python-patterns.ipynb`. Receives dataclass, NamedTuple, TypedDict, and type aliases from Chapter 1.*

**Hook (cell 2):** Current hook is reasonable ("three functions that belong together...") but can be sharpened. "A student record is not three separate variables -- it is one thing. A class lets you treat it that way: one name, one `repr()`, one place where the rules about valid scores live."

**New section structure:**
1. Classes (`__init__`, `__repr__`, `@property`, `@classmethod`)
2. Inheritance and abstract base classes
3. Dataclasses *(moved from Chapter 3)*
4. NamedTuple *(moved from Chapter 1)*
5. TypedDict and type aliases *(moved from Chapter 1)*
6. Exception handling
7. File I/O with pathlib
8. Python gotchas *(trimmed -- see below)*

**sklearn/pandas references (cells 11, 20):**
- Cell 11: "pandas provides `DataFrame.from_dict()`. scikit-learn provides `Pipeline.from_config()`." -- replace with: "You could write `StudentRecord.from_csv_row(row)` instead of calling `StudentRecord(name, scores, program)` directly -- that is a factory method."
- Cell 20: Activity "ModelCard Class" -- replace with a `CourseRecord` or `StudentProfile` class activity

**Repeated gotchas from Chapter 1:**
- Gotcha 3 (`/` vs `//`) is already in Chapter 1 operators section -- remove
- Gotcha 4 (`{}` is a dict, not a set) is already in Chapter 1 sets section -- remove
Replace with two gotchas relevant to classes and functions that the learner hasn't seen before:
- Late binding in closures (a function defined in a loop captures the loop variable by reference, not by value)
- Class-level vs instance-level attributes (a mutable class attribute is shared across all instances)

**"Five reproducible patterns" vs actual count:** Learning Objectives claim five patterns but only three unique-to-this-notebook gotchas exist after removing the two repeats. Either add two new ones (late binding, class attributes as above) to genuinely reach five, or change the claim to "three patterns not yet covered."

**Section title fixes:** `### Reading & Writing Files`, `### Creating & Checking Directories` -- replace `&` with `and`.

---

## Chapter 5: Python math and statistics (`05-math-statistics.ipynb`) -- NEW

*New notebook. Bridges pure Python (Chapters 1-4) to scientific Python (Chapters 6+).*

**Why here:** After learning functions and classes, the learner can reason about what `math.sqrt()` and `statistics.mean()` are doing. Before NumPy, they need a mental model of "single-value math" vs "array math." This chapter provides the Python-only tools, then ends with "these work on one number at a time; NumPy works on thousands at once -- that is Part 6."

**Section structure:**
1. The `math` module -- precise arithmetic for single values (`sqrt`, `log`, `ceil`, `floor`, `pi`, `e`, `isnan`, `isinf`)
2. The `statistics` module -- descriptive stats without any library (`mean`, `median`, `stdev`, `mode`, `NormalDist`)
3. The `random` module -- sampling and shuffling (`random.sample`, `random.choices`, `random.shuffle`, `random.seed`)
4. Combining them: a student grade report using only standard library tools

**Hook:** "You can already store a list of scores. Now what? You need the highest, the average, and whether a score is unusually low. Before you reach for pandas or NumPy, Python's standard library gives you everything you need for these calculations -- no install required."

**Connection to next chapter:** End with: "These functions work on one list, one value at a time. If you have 100,000 measurements, they are too slow. Chapter 6 shows you NumPy -- the same ideas, but running across thousands of values at once, in compiled code."

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

**Emojis (cell 40):** `❌` and `✅` characters -- replace with Bootstrap Icons or prose.

**"Feature matrix" framing:** Setup cell uses `X` and ML terminology -- reframe as student data matrix.

**Add strides section:** Strides are how NumPy knows where each element lives in memory. Understanding `arr.strides` and `arr.itemsize` is what makes broadcasting make sense -- you stop seeing it as magic and start seeing it as "NumPy is adjusting the step size, not copying data." Add one section after broadcasting:

- Show what `arr.strides` returns and how it relates to `arr.shape` and `arr.itemsize`
- Demonstrate how a 2D array is just a 1D block of memory with two step sizes
- Keep it conceptual -- the practical rolling-window application belongs in Chapter 14

Do NOT teach `np.lib.stride_tricks.as_strided()` here. It is dangerous (silently reads memory outside the array if the shape is wrong) and the safe modern API lives in Chapter 14.

Detailed review to follow when this chapter is reached.

---

## Chapter 8: Matplotlib and Seaborn (`08-matplotlib.ipynb`)

*Renamed from `05-matplotlib.ipynb`.*

**Plotting ecosystem callout missing:** The current "Python's Plotting Landscape" section only mentions matplotlib and seaborn. Add a brief orientation to the wider ecosystem:
- **Matplotlib / Seaborn:** static, publication-quality charts; integrates directly with NumPy and pandas
- **Plotly / Bokeh:** interactive charts with hover, zoom, and web embedding; reach for these when the chart will live in a dashboard or notebook shared with non-technical stakeholders
- **Altair:** grammar-of-graphics approach; concise declarative syntax for smaller datasets

One sentence per library. Not a tutorial -- just enough that the learner knows these exist and when to reach for them.

**Seaborn new features missing:** The seaborn section covers the classic function-based API but does not mention the `seaborn.objects` interface (introduced in v0.12, stabilised in v0.13). Add one concrete example using `so.Plot()` on university data to show the new declarative style. This signals that seaborn is actively developed and gives the reader a pointer to explore further.

**Seaborn section references pandas early:** Cell 39+ creates a DataFrame before pandas is introduced. Either frame it as "a preview of what pandas makes easy -- we will cover it properly in Chapter 11" or restructure to use plain arrays where possible.

Detailed review to follow when this chapter is reached.

---

## Chapters 9-16: deferred review

Chapters 9-16 will be reviewed and improved one at a time after the foundations (Chapters 1-8) are complete. Key notes flagged during the overall review:

- **Chapter 9 (Lets-Plot):** Review for consistency with the plotting ecosystem framing in Chapter 8
- **Chapter 14 (Time series):** This is where `deque` (removed from Chapter 1) and `sliding_window_view` come together. Introduce two tools for rolling windows side by side:
  - `np.lib.stride_tricks.sliding_window_view(arr, window_shape=n)` -- NumPy-speed batch computation over the whole array at once; preferred when you need to process all windows in one pass
  - `collections.deque(maxlen=n)` -- append one value at a time in a live stream; preferred when data arrives incrementally
  - Show both non-overlapping (`[::step]` on the view) and overlapping (default step=1) patterns
  - Do NOT use `as_strided` directly -- `sliding_window_view` is the safe modern API (NumPy 1.20+) and the right level of abstraction for a learner
- **Chapter 11 (Pandas core):** This is where the `statistics` module comparison belongs ("before pandas you'd write `statistics.mean(scores)` -- now you write `df['score'].mean()`")
- **Chapter 15 (Polars):** Review for connection to Chapter 11 and 12

---

## Implementation checklist per notebook

For every notebook implementation, verify before finishing:

- [ ] Hook does not assume ML knowledge (no epochs, loss, training loops before Chapter 6)
- [ ] Cell 2 names what the previous chapter built and what this one enables
- [ ] Each section intro adds one sentence connecting to the opening scenario
- [ ] No `&` in any section heading
- [ ] No `(Python X.Y+)` version labels in headings
- [ ] No emoji characters -- Bootstrap Icons only
- [ ] No for/while loops used before loops are introduced (Chapter 2)
- [ ] No functions used before functions are introduced (Chapter 3)
- [ ] No classes used before classes are introduced (Chapter 4)
- [ ] No pandas/sklearn/numpy references before those chapters
- [ ] All code examples use university analytics domain (student IDs, scores, courses, GPA)
- [ ] `uv add <package>` not `pip install <package>`
- [ ] Max 1 KC callout per section (Von Restorff)
- [ ] At least one diagram per notebook (SVG in `figs/`, not inline matplotlib)
- [ ] Strong ending paragraph closes the opening hook (Peak-End Rule)
- [ ] No em-dashes anywhere (`grep '\-\-' *.ipynb` before finishing)
- [ ] Prose sounds like a person explaining something, not a reference manual
