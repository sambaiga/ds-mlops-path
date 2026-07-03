# Book Standards Fix Plan

Generated: 2026-07-02. All issues verified against the live `main` branch.

---

## 0. Design decisions

| Question | Decision |
|---|---|
| Callout guide link | Keep in **Ch01, Ch17, Ch27** only (one per book section). Remove from all other chapters. |
| File numbering | Rename dev-tools `00-09` → `17-26`; ml-intro `01-05` → `27-31` to match the chapter number = file prefix convention. |
| Deep learning in tool stack | Add to Modelling tier in `figs/tool-stack.svg`: `scikit-learn, XGBoost, PyTorch`. |
| Value-driven AI/ML mention | Add one closing paragraph in `00-landscape.qmd` section 2 connecting the stack to outcomes. |
| Ch03 function diagram | Widen SVG to 900px; increase label spacing to remove visual crowding. |
| Book coherence | Dev-tools section opener (Ch17) must state why these tools are needed before ML. Ch27 must not repeat the landscape — it opens the trail. |

---

## 1. File renames + `_quarto.yml` update

### Dev-tools (`tutorials/02-dev-tools/`)

| Current name | New name | Chapter |
|---|---|---|
| `00-vscode-setup.qmd` | `17-vscode-setup.qmd` | 17 |
| `01-uv-project-setup.qmd` | `18-uv-project-setup.qmd` | 18 |
| `02-code-quality-ruff.qmd` | `19-code-quality-ruff.qmd` | 19 |
| `03-type-annotations.ipynb` | `20-type-annotations.ipynb` | 20 |
| `04-git-github.qmd` | `21-git-github.qmd` | 21 |
| `05-pytest-testing.qmd` | `22-pytest-testing.qmd` | 22 |
| `06-pre-commit-automation.qmd` | `23-pre-commit-automation.qmd` | 23 |
| `07-pydantic-validation.ipynb` | `24-pydantic-validation.ipynb` | 24 |
| `08-pandera-schema-validation.ipynb` | `25-pandera-schema-validation.ipynb` | 25 |
| `09-logging.ipynb` | `26-logging.ipynb` | 26 |

### ML-intro (`tutorials/04-ml-intro/`)

| Current name | New name | Chapter |
|---|---|---|
| `01-ml-introduction.qmd` | `27-ml-introduction.qmd` | 27 |
| `02-ml-what-is-ml.qmd` | `28-ml-what-is-ml.qmd` | 28 |
| `03-ml-workflow.qmd` | `29-ml-workflow.qmd` | 29 |
| `04-sklearn-core.ipynb` | `30-sklearn-core.ipynb` | 30 |
| `05-sklearn-pipeline.ipynb` | `31-sklearn-pipeline.ipynb` | 31 |

`_quarto.yml`: update all 15 chapter paths to new filenames.

---

## 2. Python basics notebooks

### Ch01 — `01-python-core.ipynb` (97 cells)

| Issue | Count | Fix |
|---|---|---|
| `bi-info-circle-fill` | 8 | → `bi-key-fill` |
| Inline divs | 19 | → ark classes |
| Python version mentions in prose | 10 | Remove: `Python 3.9+`, `3.10+`, `3.8+`, `3.0+`, `3.6+`, `3.7+`, `3.8` |
| Section heading: `Before You Begin` | 1 | → `Before you begin` |
| Callout guide link | missing | Add link to `index.qmd#callout-guide` in cell 2 |
| Consecutive code cells | 1 pair | Add bridge markdown |
| Chapter connection | missing forward | Cell 2 opener: name Ch02 control flow as the next chapter |

### Ch02 — `02-control-flow.ipynb` (89 cells)

| Issue | Count | Fix |
|---|---|---|
| DS-MLOps header block | 1 | Remove `**Python 3.12+ \| Author: Anthony Faustine**` line |
| `bi-info-circle-fill` | 2 | → `bi-key-fill` |
| Inline divs | 9 | → ark classes |
| Python version in prose | 3 | Remove: cell 13 (3.10), cell 48 (3.8), cell 70 (3.12) |
| Section heading `## Capstone: Processing a student record set` | 1 | → `## Capstone: processing a student record set` |
| Section heading `## Further Reading` | 1 | → `## Further reading` |
| Callout guide link | missing | Add in cell 2 |
| Consecutive code cells | 3 pairs | Add bridge markdowns (cells 66+67, 83+84+85) |
| Chapter connection | missing Ch03 forward | Cell 2: "functions (Chapter 3)" |

### Ch06 — `06-numpy.ipynb` (partial)

| Issue | Count | Fix |
|---|---|---|
| `bi-info-circle-fill` | 2 | → `bi-key-fill` |

### Ch07 — `07-numpy-advanced.ipynb` (partial)

| Issue | Count | Fix |
|---|---|---|
| `bi-info-circle-fill` | present | → `bi-key-fill` |

### Ch10 — `10-data-storytelling.ipynb` (62 cells)

| Issue | Count | Fix |
|---|---|---|
| DS-MLOps header block | 1 | Remove |
| `bi-info-circle-fill` | 5 | → `bi-key-fill` |
| Inline divs | 20 | → ark classes |
| Double-dashes ` -- ` | 8 | → `: ` |
| Python version in prose (`Python 3.12+`) | 1 | Remove |
| Title-case section headings | 12+ | Sentence case (e.g. `Before You Begin` → `Before you begin`, `Learning Objectives` → `Learning objectives`) |
| Part reference: `Parts 5 and 6` | 1 | → `Chapters 8 and 9` |
| Callout guide link | present (keep) | Already present — no action |
| Consecutive code cells | 1 pair (30+31) | Add bridge markdown |

### Ch12 — `12-pandas-operations.ipynb` (84 cells)

| Issue | Count | Fix |
|---|---|---|
| DS-MLOps header block | 1 | Remove |
| `bi-info-circle-fill` | 5 | → `bi-key-fill` |
| Inline divs | 20 | → ark classes |
| Double-dashes ` -- ` | 6 | → `: ` |
| Python version in prose (`Python 3.12+`) | 1 | Remove |
| Section heading `## What's New in Pandas 3` | 1 | → `## What's new in Pandas 3` |
| Other title-case section headings | 10+ | Sentence case |
| Part reference: `Part 8` | 1 | → `Chapter 11` |
| Consecutive code cells | 1 pair (52+53) | Add bridge markdown |

### Ch13 — `13-combining-reshaping.ipynb` (90 cells)

| Issue | Count | Fix |
|---|---|---|
| `bi-info-circle-fill` | 5 | → `bi-key-fill` |
| Inline divs | 28 | → ark classes |
| Double-dashes ` -- ` | 9 | → `: ` |
| Title-case section headings | 10+ | Sentence case |

### Ch16 — `16-great-tables.ipynb` (62 cells)

| Issue | Count | Fix |
|---|---|---|
| DS-MLOps header block | 1 | Remove |
| `bi-info-circle-fill` | 5 | → `bi-key-fill` |
| Inline divs | 18 | → ark classes |
| Double-dashes ` -- ` | 6 | → `: ` |
| Consecutive code cells | 2 pairs | Add bridge markdowns |

---

## 3. Dev-tools files (all unpatched)

### Standard fixes applied to ALL dev-tools files

- Title: drop `Part N:` prefix; sentence-case the remainder
- Section headings: `## Learning Objectives` → `## Learning objectives`; all numbered sections sentence case
- `bi-info-circle-fill` → `bi-key-fill`
- Double-dashes ` -- ` → `: `
- Part references → Chapter N references
- Activity titles: `Activity N - Title` → `Activity N: lowercase title`; remove `<b>Goal:</b>` prefix
- Callout guide link: **keep in Ch17 only**; remove from Ch18-Ch26

### Ch17 — `17-vscode-setup.qmd` (was `00-vscode-setup.qmd`)

| Issue | Fix |
|---|---|
| Title `Part 12: VS Code setup` | → `VS Code setup` |
| `bi-info-circle-fill` × 1 | → `bi-key-fill` |
| Double-dashes × 11 | Fix |
| Section headings title-case | Sentence case |
| Callout link | **Keep** (section opener) |
| Chapter connection in opener | Explain: "Python basics (Ch1-16) ends here; dev tools bridge notebook experiments to reproducible pipelines." Forward: Ch18 uv |

### Ch18 — `18-uv-project-setup.qmd` (was `01-uv-project-setup.qmd`)

| Issue | Fix |
|---|---|
| Title `Part 13:…` | → `Project setup with uv` |
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Double-dashes × 14 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch17 VS Code setup. Forward: Ch19 Ruff |

### Ch19 — `19-code-quality-ruff.qmd` (was `02-code-quality-ruff.qmd`)

| Issue | Fix |
|---|---|
| Title | → `Code quality with Ruff` |
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Double-dashes × 12 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch18 uv. Forward: Ch20 type annotations |

### Ch20 — `20-type-annotations.ipynb` (was `03-type-annotations.ipynb`)

| Issue | Fix |
|---|---|
| DS-MLOps header | Remove |
| Title | → `Type annotations` |
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Inline divs × 8 | → ark classes |
| Double-dashes × 4 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch18/19. Forward: Ch21 Git |

### Ch21 — `21-git-github.qmd` (was `04-git-github.qmd`)

| Issue | Fix |
|---|---|
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Double-dashes × 7 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch20. Forward: Ch22 pytest |

### Ch22 — `22-pytest-testing.qmd` (was `05-pytest-testing.qmd`)

| Issue | Fix |
|---|---|
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Double-dashes × 15 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch21. Forward: Ch23 pre-commit |

### Ch23 — `23-pre-commit-automation.qmd` (was `06-pre-commit-automation.qmd`)

| Issue | Fix |
|---|---|
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Double-dashes × 8 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch22. Forward: Ch24 Pydantic |

### Ch24 — `24-pydantic-validation.ipynb` (was `07-pydantic-validation.ipynb`)

| Issue | Fix |
|---|---|
| DS-MLOps header | Remove |
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Inline divs × 13 | → ark classes |
| Double-dashes × 2 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch20 type annotations. Forward: Ch25 Pandera |

### Ch25 — `25-pandera-schema-validation.ipynb` (was `08-pandera-schema-validation.ipynb`)

| Issue | Fix |
|---|---|
| DS-MLOps header | Remove |
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Inline divs × 12 | → ark classes |
| Double-dashes × 0 | Already clean |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch24 Pydantic. Forward: Ch26 logging |

### Ch26 — `26-logging.ipynb` (was `09-logging.ipynb`)

| Issue | Fix |
|---|---|
| DS-MLOps header | Remove |
| `bi-info-circle-fill` × 1 | → `bi-key-fill` |
| Inline divs × 7 | → ark classes |
| Double-dashes × 5 | Fix |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Consecutive code cells × 3 pairs | Add bridge markdowns |
| Chapter connection | Backward: Ch24/25. Forward: Ch27 ML landscape |

---

## 4. ML-intro files

### Ch27 — `27-ml-introduction.qmd` (was `01-ml-introduction.qmd`)

| Issue | Fix |
|---|---|
| `bi-info-circle-fill` × 0 | Already clean |
| Double-dashes × 0 | Already clean |
| Part refs | None found |
| Callout link | **Keep** (section opener, like Ch17) |
| Section headings | Verify sentence case |
| Role distinction from `00-landscape.qmd` | Opener must focus on "first step on the trail" (concrete problem framing), not re-draw the landscape map |

### Ch28 — `28-ml-what-is-ml.qmd` (was `02-ml-what-is-ml.qmd`)

| Issue | Fix |
|---|---|
| Title `Part 23: What Is Machine Learning?` | → `What is machine learning?` |
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Double-dashes × 2 | Fix |
| Part refs | → Chapter N |
| Section headings: `What Machine Learning Is`, `Learning Objectives`, `The ML Taxonomy` | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch27. Forward: Ch29 |

### Ch29 — `29-ml-workflow.qmd` (was `03-ml-workflow.qmd`)

| Issue | Fix |
|---|---|
| Title | Sentence case, no Part prefix |
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Double-dashes × 3 | Fix |
| Part refs | → Chapter N |
| Section headings | Sentence case |
| Callout link | **Remove** |
| Chapter connection | Backward: Ch28. Forward: Ch30 |

### Ch30 — `30-sklearn-core.ipynb` (was `04-sklearn-core.ipynb`)

| Issue | Fix |
|---|---|
| No YAML frontmatter | Add `title: "Classical ML with scikit-learn"` |
| `bi-info-circle-fill` × 3 | → `bi-key-fill` |
| Double-dashes × 34 | Fix |
| Part refs | → Chapter N |
| Section headings | Sentence case |
| Dataset | Hotel Booking Demand — **keep** (confirmed exception) |

### Ch31 — `31-sklearn-pipeline.ipynb` (was `05-sklearn-pipeline.ipynb`)

| Issue | Fix |
|---|---|
| No YAML frontmatter | Add `title: "Sklearn pipelines and hyperparameter search"` |
| `bi-info-circle-fill` × 2 | → `bi-key-fill` |
| Double-dashes × 31 | Fix |
| Part refs | → Chapter N |
| Section headings | Sentence case |
| Dataset | Hotel Booking Demand — **keep** |

---

## 5. `00-landscape.qmd`

| Issue | Fix |
|---|---|
| `bi-info-circle-fill` × 1 | → `bi-key-fill` |
| Tool stack: deep learning missing | Update `figs/tool-stack.svg` Modelling tier: add PyTorch alongside scikit-learn/XGBoost |
| Value-driven AI/ML, system design: not mentioned | Add one paragraph at end of section 2: connect the stack layers to the outcome ("value-driven product, observable system") |

---

## 6. Ch03 function diagram — `tutorials/01-python-basics/figs/function-anatomy.svg`

| Issue | Fix |
|---|---|
| Bottom labels 8px apart | Widen viewBox to `0 0 900 280`; spread bottom labels so gap >= 20px |
| Code line element crowding | Increase spacing around the `(` separator; separate highlighted rects by at least 4px visual gap |

---

## 7. Implementation order

1. Create branch `fix/book-standards-batch2`
2. File renames (dev-tools + ml-intro) + `_quarto.yml`
3. Python basics: Ch01, Ch02, Ch06, Ch07, Ch10, Ch12, Ch13, Ch16
4. Dev-tools: Ch17-Ch26 (QMDs then notebooks)
5. ML-intro: Ch27-Ch31
6. `00-landscape.qmd` + tool stack SVG
7. Ch03 function diagram SVG
8. Final grep sweep: `bi-info-circle-fill`, ` -- `, `DS-MLOps`, `Part [0-9]`, `background:#EA`
9. Commit and open PR

---

## 8. Definition of done

Run these checks before merging:

```bash
# No old icons
grep -r "bi-info-circle-fill" tutorials/ --include="*.qmd" --include="*.ipynb"

# No double-dashes in prose
grep -r " -- " tutorials/ --include="*.qmd" --include="*.ipynb"

# No DS-MLOps headers
grep -r "DS-MLOps\|Author: Anthony" tutorials/ --include="*.ipynb"

# No old inline divs
grep -r "background:#EAF3FA\|background:#EBF5F0" tutorials/ --include="*.ipynb"

# No Part N references (except valid "Part" words in prose)
grep -rn "Part [0-9]\{1,2\}[^a-z]" tutorials/ --include="*.qmd" --include="*.ipynb"

# No Python version labels in prose (in markdown cells)
grep -r "Python 3\.[0-9]" tutorials/ --include="*.ipynb" --include="*.qmd"

# Old filenames gone
ls tutorials/02-dev-tools/0*.qmd tutorials/04-ml-intro/0*.qmd 2>/dev/null
```
