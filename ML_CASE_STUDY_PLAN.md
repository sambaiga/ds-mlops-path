# Classical ML case-study part: design and dataset plan

## Context

Chapters 28-32 (ML landscape) teach the *concepts*: the five-component spec
card and nine-stage workflow (Ch30), and the sklearn mechanics (Ch31-32,
using Hotel Booking Demand for regression + classification). `PLAN.md`
already sketches a follow-on "Part 5: Classical ML Projects" with five
case-study notebooks and an 8-step project spine anchored to Ch30's spec
card, but that plan is stale (old chapter numbering, university-data
framing) and was never built, none of its files exist yet.

The user wants each case study to (1) teach one core ML concept/task type,
(2) literally walk through Ch30's problem-formulation stages rather than
gesture at them narratively, and (3) read as authentic industrial ML,
tying back to the preface's thesis: technically-solid work is not enough,
the point is knowing what business problem you're solving and for whom.
Research this session (see `DATASET_RESEARCH.md`) surfaced three concrete
datasets to draw on: Nature *Scientific Data*'s "Open e-commerce 1.0"
(2018-2022 U.S. Amazon purchases linked to household demographics, Harvard
Dataverse), Kaggle's Olist Brazilian E-Commerce (multi-table real orders),
and HF's Amazon Reviews 2023 (large-scale reviews). Two of PLAN.md's five
original picks are thin (Customer Personality Analysis: 2,240 rows;
MovieLens is fine but off the e-commerce narrative thread); Telco churn is
already strong and authentic (has a worked spec card in Ch30). User
confirmed: new dedicated book part (not folded into ML landscape), a
dataset mix built around the Nature dataset, and, in follow-up messages, a
reliability-engineering real case study for anomaly detection instead of
the originally-planned energy-theft/smart-meter pick, then a request to
find something more recent and real than the NASA C-MAPSS simulation, and
finally an explicit ask to cover **survival analysis and Remaining Useful
Life (RUL) prediction**, topics most ML books skip, alongside ranking and
recommendation.

That last request changed the shape of the reliability-engineering slot.
Research surfaced the SCANIA Component X dataset (Kolar et al., *Scientific
Data*, 2025, [DOI 10.1038/s41597-025-04802-6](https://www.nature.com/articles/s41597-025-04802-6)):
real, anonymized time-series and repair records from a fleet of Scania
trucks, released specifically as a benchmark for classification,
regression, **survival analysis**, and anomaly detection in predictive
maintenance. It is real (not simulated), current (2025), Nature-published
like the Open e-commerce dataset, and built for exactly the task types the
user wants. It replaces NASA C-MAPSS entirely and now drives two case
studies instead of one, the same "one honest dataset, several business
questions" pattern already used for Nature Open e-commerce.

**Continuity flag, resolved**: Ch28's opening scenario and Ch29-30's worked
examples currently use energy-theft detection as the running motivating
problem. Rather than keep energy theft as a seventh case study, the user
will revisit and update the Ch28-30 narrative (opening scenario, worked
spec-card example, activities) once the turbofan case study is written, so
the book's motivating example lines up with the anomaly-detection case
study that actually gets built in code. This is a follow-up edit to Ch28-30
after Ch37 exists, not something to do now.

## Revision of 20 November 2026: scope against the two mbuga volumes

The author is writing two further books in the repository `mbuga`: Volume 1, *Finding Structure in Time Series*
(clustering, ranking, retrieval, recommendation and anomaly detection), and Volume 2, *Forecasting for Operations*
(signals, forecasters, probabilistic forecasting, retail structure and decisions). Four of the seven case studies below
cover the same methods. This book does not repeat them.

**Principle.** This book teaches the workflow and the craft of a data science project: framing the problem, building the
pipeline, evaluating honestly, shipping and monitoring, and stating the value. The two volumes teach the methods in
depth, with their mathematics, assumptions and failure modes. Where a method belongs to a volume, this book shows the
workflow on one small case and then points to the volume instead of deriving the method.

**Revised case studies.**

| Ch | Task | Decision | Reason |
|---|---|---|---|
| 33 | Regression (spend) | Keep, as built | In neither volume |
| 34 | Classification (churn) | Keep | In neither volume |
| 35 | Forecasting (spend) | Keep as the single forecasting case: baseline, chronological split, dollar value | Depth (probabilistic forecasts, hierarchies, intermittent demand) is Volume 2 |
| 36 | Clustering (segmentation) | Replace by a short framing chapter | Clustering is Volume 1, Part II |
| 37 | Survival analysis and remaining useful life (SCANIA) | Keep, and give it the most care | In neither volume, and most books skip it |
| 38 | Anomaly detection (SCANIA) | Replace by a short framing chapter | Anomaly detection is Volume 1, Part IV |
| 39 | Recommendation and ranking (Olist) | Replace by a short framing chapter | Retrieval, ranking and recommendation are Volume 1, Part III |

A framing chapter is a few pages: the business question, the spec card, the choice of success metric and the decision it
changes, one small worked example, and a pointer to the volume for the method. It carries no new method.

**The empty parts hold what neither volume covers.**

| Part | Scope |
|---|---|
| MLOps | Pipelines, CI/CD, serving, experiment tracking, reproducibility |
| Production monitoring | Data and prediction drift, performance decay, retraining triggers, alerting |
| ML system design | Decision-first framing, cost and latency trade-offs, build against buy |
| Value-driven AI | Stating and checking the value of a model, communicating results to a stakeholder |
| Deep learning and LLMs | At project level: when to use them, how to adapt and evaluate them, without time-series specifics |

**Datasets.** The datasets of this book (Nature Open e-commerce, SCANIA Component X, Olist, IBM Telco churn, Hotel
Booking Demand) differ from those of the volumes (M5, VN1, VN2, FreshRetailNet-50K and energy data). They stay different,
so that no worked example repeats and the methods are seen to generalise.

**Cross-references.** A pointer names the volume and its part, not a chapter number, because the volumes are drafts and
their numbering will move. Volume 1, Parts III and IV, and Volume 2 are not yet published; a framing chapter links to a
volume only once the target chapter is public. Until then it says that the method is treated in the volume and gives the
title. Each volume stays self-contained and does not require this book.

**Open decisions for the author.**

1. Whether pointers should cite chapter numbers once the volumes are published, or stay at the level of part and title.
2. Where the shared vocabulary of the spec card is defined, so that both volumes can cite one source.
3. Whether the short chapter on data contracts, testing and reproducibility for machine learning code belongs to the
   "Dev tools" part or to "MLOps".

**What this changes in the repository.** `_quarto.yml` lists only chapter 33 under "Classical ML projects"; chapters
34, 35 and 37 are added as they are written, and the framing chapters for 36, 38 and 39 are written last. The section
below, "Decisions", is the original plan and stands except where this revision replaces it.

## Decisions (original plan of the first revision; superseded where the revision above says so)

**Structure**: new part "Classical ML Projects" in `_quarto.yml`, inserted
between "ML landscape" (ends Ch32) and "Deep learning". New directory
`tutorials/05-classical-ml-projects/`, chapters 33-39.

**Seven case studies, one core task type each:**

| Ch | File | Task type | Dataset | Why |
|---|---|---|---|---|
| 33 | `33-spend-regression.ipynb` | Regression | Nature Open e-commerce | Predict household/category spend from demographics; real behavioral + demographic linkage rarely available openly |
| 34 | `34-churn-classification.ipynb` | Classification | IBM Telco Churn | Unchanged from PLAN.md. Directly implements the exact churn spec card already worked out in Ch30 Section 1.1, strong continuity |
| 35 | `35-spend-forecasting.ipynb` | Forecasting | Nature Open e-commerce | Monthly per-household/category spend, 2018-2022 real time series including the COVID demand shock; forces the chronological-split lesson from Ch30 Section 3.2 with a real distribution shift, not a toy one |
| 36 | `36-customer-segmentation.ipynb` | Clustering/segmentation | Nature Open e-commerce | Consumer personas from purchase-category mix + demographics; domain-validatable segments (Ch30 Section 4.3) since demographics let you sanity-check clusters against real household types |
| 37 | `37-survival-analysis-rul.ipynb` | **Survival analysis / Remaining Useful Life prediction** | SCANIA Component X (Nature *Scientific Data*, 2025) | The differentiator topic the user asked for: Kaplan-Meier curves, censored data, Cox proportional hazards, RUL regression under censoring. Real anonymized truck-fleet component data, built by its authors specifically for this task, rarely covered in ML books |
| 38 | `38-component-anomaly-detection.ipynb` | Anomaly detection | SCANIA Component X (same dataset, second lens) | Unsupervised fault/degradation detection on the same real sensor and repair-record data as Ch37, replacing the NASA C-MAPSS simulation with real 2025 fleet data. Algorithm family unchanged from PLAN.md: Isolation Forest -> Autoencoder baseline |
| 39 | `39-product-recommendation.ipynb` | Recommendation/ranking | Kaggle Olist | Real multi-table marketplace orders/reviews keep the case study in the same e-commerce business world as 33/35/36, unlike MovieLens' entertainment domain |

Nature Open e-commerce drives three notebooks (33, 35, 36) and Nature's
SCANIA Component X drives two (37, 38), each pair/trio reusing one EDA
pass across several business questions on the same honest dataset. HF
Amazon Reviews 2023 is deliberately **not** used here; it's reserved as
the flagship dataset for the future LLMs part (sentiment classification,
review summarization, RAG), since its value is the review text, not
tabular structure.

**Scope note on survival analysis**: Ch30's task-type taxonomy (the 7-8
types in its metrics table) does not name survival analysis as a distinct
category, it is closer to censored regression. Ch37 introduces the
concept self-contained (built from regression/classification foundations
already taught), rather than editing Ch30's taxonomy in this pass. Flag
for later: Ch30 may be worth a short addendum once this case study exists,
so the taxonomy and the case study agree.

**Template every notebook must open with** (formalizes Ch30's spec card,
which currently exists only as prose, no notebook has used it as a literal
header yet):

1. **Spec card** - same table format as Ch30 Section 1 (`ark-concept` div,
   reuse existing CSS class): Target variable | Task type and paradigm |
   Success metric | Acceptable threshold | Data specification.
2. **Problem framing** narrative: one paragraph connecting to the
   preface's "what problem does this solve, and for whom" question.
3. Sections then follow PLAN.md's 8-step spine, mapped explicitly onto
   Ch30's nine workflow stages: Data collection/EDA -> Feature engineering
   -> Model selection (baseline -> simple -> boosting) -> Training ->
   Evaluation (metric from Ch30 Section 4) -> Learning curve diagnosis
   (Ch30 Section 5) -> Decision framework if short of threshold (Ch30
   Section 6).
4. **Closing "Key findings and recommendation"** section: must name the
   business decision the model changes and for whom, state a **back-of-
   envelope dollar-value estimate** (not just a qualitative claim) with its
   formula and assumptions shown, and forward-point to where
   Deployment/Monitoring (not covered here) will be picked up in the MLOps
   part.

**Dollar-value framing per case study** (the explicit formula each closing
section will build, stated as an estimate with assumptions, not a false-
precision number):

| Ch | Dollar-value estimate |
|---|---|
| 33 Regression | Value of ranking households by predicted spend: incremental revenue from targeting the top-decile predicted spenders vs. random targeting, at an assumed marketing conversion rate |
| 34 Classification | Standard churn ROI: (customers correctly flagged x average customer lifetime value) minus (all flagged customers x retention-offer cost), compared against the cost of doing nothing |
| 35 Forecasting | Forecast-error cost: assumed per-unit overstock (holding cost) and understock (lost-sale) cost, multiplied by the forecast error reduction versus a naive baseline |
| 36 Clustering | Value of targeting efficiency: reallocating a fixed marketing budget toward the highest-propensity segment, at an assumed lift in conversion rate over untargeted spend |
| 37 Survival/RUL | Avoided-failure cost: (predicted failures acted on early x cost difference between a scheduled repair and an unplanned breakdown) minus the cost of unnecessary early replacements (false positives) |
| 38 Anomaly detection | Same avoided-failure-cost logic as 37, framed around inspection cost per flagged component vs. cost of a missed failure, to show the anomaly-detection framing trades off differently than the survival-analysis framing on identical data |
| 39 Recommendation | Incremental revenue per session/order from recommended items, at an assumed click-through and conversion rate, the standard recsys ROI story (cited industry figures, e.g., ~35% of Amazon's revenue attributed to recommendations, are a useful anchor, not a claim to reproduce exactly) |

Every dollar figure must be presented as "here is the estimate and the
assumption behind it," not a hard number. The point is to teach readers to
attach a monetary reasoning chain to a model's metric, matching the
preface's thesis that a technically-solid model without a stated business
value is half the job.

## Files to touch when this is implemented

- `_quarto.yml`: insert the new part block (lines ~96-97, between ML
  landscape and Deep learning).
- New directory `tutorials/05-classical-ml-projects/` with 7 notebooks
  above, plus a `data/` subfolder and a `PLAN.md` (successor to the stale
  `tutorials/04-ml-intro/PLAN.md` Part 5 section, which should be trimmed
  once superseded).
- Data acquisition: Olist, the Nature Open e-commerce dataset (Harvard
  Dataverse), and SCANIA Component X (Swedish National Data Service, DOI
  10.1038/s41597-025-04802-6) need to be fetched and checked for file size
  before deciding whether to commit raw CSVs directly (as
  `hotel_bookings.csv` is, 16.8MB) or add a small download script instead.
  Confirm each dataset's redistribution terms (Olist: CC BY-NC-SA 4.0;
  Dataverse and SND datasets: check the usage terms on each page) before
  committing.

## Not in scope / unchanged

- Part 1 synthetic `university_analytics.csv` stays as-is (fundamentals,
  deliberately noise-free).
- Ch31-32 keep Hotel Booking Demand (already-confirmed exception).
- No notebook content is written in this pass, this plan only fixes the
  structure, task-type assignments, dataset choices, and the mandatory
  spec-card/workflow/dollar-value template. Writing the seven notebooks is
  follow-up work, one at a time.

## Verification

Once a notebook is written against this plan: render it via `quarto
render tutorials/05-classical-ml-projects/<file>` and confirm (a) the
spec-card table appears before any code cell, (b) section headers name
the corresponding Ch30 workflow stage, (c) the closing section states a
concrete business decision with an explicit dollar-value estimate and
its assumptions, and (d) `_quarto.yml` builds the full book without a
broken TOC entry.
