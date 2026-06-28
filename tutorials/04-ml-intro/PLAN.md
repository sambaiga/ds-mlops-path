# Part 4: The Machine Learning Landscape — Implementation Plan

> **Role in the book:** Conceptual bridge between "Dev Tools" (Parts 1–3) and all hands-on ML parts (Parts 5+). Readers finish this part knowing *what* ML is, *how* to think about ML problems, *where* every major paradigm fits, and *why* uncertainty matters — before touching a single algorithm notebook.

---

## Structure Overview

| Chapter | Title | Primary Theme |
| --- | --- | --- |
| 1 | What Is Machine Learning? | Taxonomy, AI/ML/DL hierarchy, applicability |
| 2 | The ML Workflow and Problem Framing | Formulation, evaluation, bias-variance, strategy |
| 3 | The ML Algorithm Panorama | Survey of all paradigms + decision framework |
| 4 | Probabilistic and Bayesian Thinking | Uncertainty, priors, PyMC, credible intervals |

**File layout:**
```
tutorials/04-ml-intro/
├── 01-ml-introduction.qmd
├── 02-ml-workflow.qmd
├── 03-ml-panorama.qmd
└── 04-bayesian-thinking.qmd
```

**`_quarto.yml` addition:**
```yaml
- part: "Part 4: The Machine Learning Landscape"
  chapters:
    - tutorials/04-ml-intro/01-ml-introduction.qmd
    - tutorials/04-ml-intro/02-ml-workflow.qmd
    - tutorials/04-ml-intro/03-ml-panorama.qmd
    - tutorials/04-ml-intro/04-bayesian-thinking.qmd
```

---

## Running Scenario Strategy

**Primary domain: Smart Energy Analytics**
Authentic to the author's research expertise (NILM, load forecasting, smart-grid, anomaly detection). Every concept is demonstrated first through an energy lens.

**Supporting domains: "In Practice" callout boxes**
Each major section includes a brief multi-domain callout showing the same concept in 2–3 other contexts, so learners from different backgrounds connect. Domains to rotate through:

| Domain | Concept Fit |
| --- | --- |
| E-commerce / retail | A/B testing (Bayesian), customer churn (classification), sales forecasting, recommendation |
| Healthcare / clinical | Patient readmission (classification), drug dosage (regression), diagnostic uncertainty (Bayesian) |
| Finance / banking | Credit scoring (classification), fraud detection (anomaly), risk quantification (Bayesian) |
| HR / people analytics | Employee attrition (classification), salary modelling (regression), skill clustering |

**Why multi-domain matters:** The energy example alone risks alienating learners who cannot picture their problem in that domain. The callout boxes add breadth without breaking the narrative thread.

---

## Chapter 1: What Is Machine Learning?

**File:** `01-ml-introduction.qmd`

### Learning Objectives
- Explain what ML is and how it differs from traditional rule-based programming
- Describe the AI ⊃ ML ⊃ DL ⊃ Gen AI hierarchy and where each sits
- Classify problems by ML paradigm (supervised, unsupervised, self-supervised, RL)
- Identify when ML is and is not the right tool

### Section Outline

**§1 The Limits of Rules**
Open with the spam-filter problem (`MLfundamentals.pdf`): can you write a hand-coded energy-theft detector? Rules break when patterns are complex, variable, or unknown. ML learns the pattern instead. This is the "why" before the "what."

**§2 What ML Actually Is**
Formal definition ("programming computers to learn from data, improve with experience, without being explicitly programmed") and the three core capabilities: detect patterns, build explanatory models, use models for inference and prediction. Draw from `2017-06-01-ml-introduction.md` and `2017-09-20-ml-intro.md`.

**§3 The AI Landscape**
Clean hierarchy: AI ⊃ ML ⊃ DL ⊃ Gen AI. Where does Data Science overlap? Where do LLMs sit? Source the Venn diagram from `AI4Public_slide.pdf` and `Systematic_review_paper/AI_ML_datascince.pdf`. One precise paragraph per term.

**§4 The ML Taxonomy**
Single reference diagram with four paradigms and their sub-types:
- **Supervised** — regression, classification, ranking, forecasting
- **Unsupervised** — clustering, dimensionality reduction, anomaly detection, generation
- **Self-supervised / Semi-supervised** — foundation models, limited-label settings
- **Reinforcement learning** — agent, environment, reward (brief; expanded in Chapter 3 §7)

**§5 When to Use ML (and When Not To)**
Decision checklist: use ML when the problem is too complex for rules, needs to adapt, data exists, scale matters. Do *not* use ML when a simple rule works, data is absent, full causal interpretability is legally required, or the problem is highly unstable. This sets up the engineering discipline thread.

**§6 Real-World Impact**
Draw from `AI4Public_slide.pdf` (government AI: 1.2B hours, $41B potential savings) and `BeyondPhD.pdf` (smart energy, NILM, industrial maintenance, forecasting). Rotate through the multi-domain callout: healthcare diagnostics, e-commerce personalisation, financial risk.

### Markers
| Type | Content |
| --- | --- |
| Key Concept | Formal ML definition |
| Key Concept | Supervised vs. unsupervised distinction |
| Common Mistake | "ML solves everything" — when not to use it |
| Activity | Given 5 problem descriptions, classify each as supervised / unsupervised / RL / not-ML |
| Pro Tip | Write the problem statement and success metric before touching data |

### Source Assets
| Asset | File |
| --- | --- |
| AI ⊃ ML ⊃ DL ⊃ DS Venn | `AI4Public_slide.pdf`, `Systematic_review_paper/AI_ML_datascince.pdf` |
| Spam filter / rules-vs-ML | `MLfundamentals.pdf` |
| ML taxonomy diagram | `2017-06-01-ml-introduction.md` |
| Real-world impact stats | `AI4Public_slide.pdf`, `BeyondPhD.pdf` |

---

## Chapter 2: The ML Workflow and Problem Framing

**File:** `02-ml-workflow.qmd`

### Learning Objectives
- Translate a business problem into a precisely specified ML problem
- Design a sound train/validation/test split (including temporal splits)
- Choose evaluation metrics matched to the problem type
- Diagnose underfitting and overfitting from learning curves
- Apply a structured decision framework when model performance is unsatisfactory

### Section Outline

**§1 From Business Problem to ML Problem**
The translation step (`MLstrategy.pdf`): "reduce energy waste" → "predict next-hour consumption within 5% MAPE for 10k meters, using 12 months of historical readings." Teach: what is the prediction target? What metric represents real-world success? What counts as good enough? Include the e-commerce version: "increase revenue" → "predict 7-day customer churn probability, threshold at 0.4, optimise for recall."

**§2 The End-to-End ML Workflow**
Single reference diagram:
```
Problem framing → Data collection → EDA → Feature engineering
→ Model selection → Training → Evaluation → Deployment → Monitoring
```
Brief description of each stage; later parts cover each in depth. This map is what readers return to for the rest of the book.

**§3 Train / Validation / Test — The Right Way**
Splits, leakage, why the test set is sacred. Temporal split callout: for time series, never shuffle — always split chronologically. Source: `MLstrategy.pdf` and `2017-06-01-ml-introduction.md`.

**§4 Evaluation That Actually Measures What Matters**
Metric families:
- Regression: MAE, RMSE, MAPE, R² — when each is appropriate
- Classification: accuracy, precision, recall, F1, AUC-ROC — the precision/recall tradeoff for imbalanced data
- Forecasting: MASE, coverage / prediction interval metrics
- Reference table: problem type → recommended primary metric → common mistake metric

In Practice callout: healthcare — optimise recall for disease screening (missing a case is worse than a false alarm); finance — optimise precision for fraud alerts (false positives cost customer trust).

**§5 Bias, Variance, and the Underfitting/Overfitting Diagnosis**
Bias-variance tradeoff diagram from `MLstrategy.pdf`. Learning curves, how to read them, what each failure mode looks like. Give readers a mental model for diagnosing failures before they've seen a single algorithm.

**§6 ML Strategy: Given X Performance, What Next?**
The structured decision framework from `MLstrategy.pdf` — if model performance is insufficient, which lever? More data, better features, bigger model, regularisation, error analysis. This is rare in intro ML material and directly supports the book's "three gaps" philosophy.

### Markers
| Type | Content |
| --- | --- |
| Key Concept | Train / validation / test split |
| Key Concept | Bias-variance tradeoff |
| Common Mistake | Data leakage (temporal and feature) |
| Common Mistake | Accuracy on imbalanced classes |
| Activity | Given a learning curve plot, diagnose: underfitting, overfitting, or well-fitted |
| Activity | Translate "predict churn" into a fully specified ML problem (target, metric, threshold, data) |
| Pro Tip | Write down evaluation metric and acceptable threshold before training anything |

### Source Assets
| Asset | File |
| --- | --- |
| Problem formulation framework | `MLstrategy.pdf` |
| Bias-variance tradeoff diagram | `MLstrategy.pdf` |
| "Given 90% accuracy, what next?" | `MLstrategy.pdf` |
| Dataset split philosophy | `2017-06-01-ml-introduction.md` |

---

## Chapter 3: The ML Algorithm Panorama

**File:** `03-ml-panorama.qmd`

### Learning Objectives
- Describe the intuition behind each major ML paradigm (no math, no code)
- Distinguish when to use classical ML vs. deep learning vs. LLMs
- Identify the role of ranking, recommendation, and optimisation in production systems
- Apply a decision framework to choose the right approach for a new problem

### Section Outline

**§1 Classical Supervised Learning**

*Regression*: linear regression intuition, polynomial extension, regularisation (Ridge/Lasso). Primary example: predicting monthly building energy consumption from weather + occupancy features. In Practice: house price prediction, medical dosage estimation.

*Classification*: logistic regression → decision boundary, tree-based models (random forest, gradient boosting). Primary example: appliance state detection (on/off) from current waveform. In Practice: customer churn prediction, medical diagnosis.

*The model complexity spectrum*: linear → kernel → tree-based → neural — when each wins. Source: `2017-04-15-ml-classification.markdown`, `2017-07-02-ml-classification.md`.

**§2 Time-Series Forecasting**
A dedicated section — not an afterthought — because forecasting is a distinct problem class that trips up engineers who treat it as i.i.d. regression.
- What makes time series different: temporal dependence, stationarity, seasonality, trend
- Three families: classical statistical (ARIMA, ETS), ML (lag features + gradient boosting), deep learning (LSTM, Temporal Fusion Transformer)
- Forecasting as supervised learning: lag features, rolling windows
- Connect to the author's `twiga` forecasting library as a real-world anchor
- In Practice: retail demand planning, ICU patient vital sign prediction, server load forecasting

**§3 Unsupervised Learning**

*Clustering*: K-means intuition, when to use (household segmentation by usage pattern), evaluation without labels (silhouette, elbow). In Practice: customer segmentation (e-commerce), patient phenotyping (healthcare).

*Dimensionality reduction*: PCA for noise reduction and visualisation; t-SNE/UMAP for visualisation only — a common misuse callout.

*Anomaly detection*: isolation forest, autoencoder-based detection. Primary example: energy-theft detection. In Practice: credit card fraud, manufacturing defect detection. Source: `2020-01-01-anamaly-detection-ml.md`.

**§4 Ranking and Recommendation**
Often omitted from ML curricula but dominant in industry systems.
- Learning to rank: pointwise / pairwise / listwise, NDCG metric
- Collaborative filtering: "users like you also…" — matrix factorisation intuition
- Content-based filtering: item features, cold-start problem
- Hybrid systems: how Netflix, Spotify, and Amazon combine both
- Primary example: ranking energy-saving actions by expected impact for a household profile
- In Practice: search engine ranking, e-commerce product recommendations, content feeds

**§5 Deep Learning**
- Universal approximation: why layers build complex patterns from simple ones (`DeepLearningFoundation.pdf`)
- CNNs: spatial patterns — image classification, then NILM signal decomposition as a 1-D signal analogue (`DeepVision.pdf`)
- RNNs/LSTMs/GRUs: sequential data, vanishing gradient problem, how gated units fix it (`DeepSeq.pdf`)
- Transformers: attention in one paragraph — "every token attends to every other token"
- When deep learning wins: large data, complex patterns, structured inputs (images, sequences, text)
- When it loses: small tabular datasets, interpretability requirements, limited compute

**§6 LLMs and Generative AI**
- Foundation models: trained on massive corpora, adapted via fine-tuning or prompting
- The generative spectrum: text (GPT/Claude), image (Stable Diffusion), code (Codex/Cursor)
- LLMs in ML systems: RAG, agents, tool use
- Primary example: energy-aware assistant that answers "why did my bill spike?" using RAG over meter data
- Responsible use: hallucination, bias, data privacy, training energy cost
- In Practice: customer support automation, clinical note generation, code completion

**§7 Decision-Making and Optimisation**
*The layer after prediction.* Many ML systems don't just predict — they act. This section briefly surveys the decision space without going deep (not a full chapter unless the book adds a dedicated RL part).
- *Reinforcement learning*: agent, environment, state, action, reward — intuition via an energy dispatch agent that decides when to charge/discharge a battery (`2017-06-01-ml-introduction.md` defines RL)
- *Contextual bandits*: exploration-exploitation tradeoff, the bridge between recommendation and RL
- *Constrained optimisation*: LP/MIP for scheduling and dispatch problems — when the solution space is enumerable
- *Why this matters now*: as models move into production, the prediction is never the end — it feeds a decision. Frame the pipeline: predict → rank → decide → act → observe → retrain
- In Practice: ad bid optimisation (contextual bandit), route optimisation (integer programming), clinical treatment selection (RL)

**§8 Choosing the Right Tool: A Decision Framework**
Single visual decision tree tying all seven sections together:
```
What type of data? (tabular / image / sequence / text)
→ Do you have labels? (supervised / unsupervised)
→ What is the output? (value / class / ranking / action)
→ How much data? (<10k / 10k–1M / >1M rows)
→ Interpretability required? (linear / tree / neural)
→ Recommended approach
```
This becomes the reference card readers use throughout Parts 5–10.

### Markers
| Type | Content |
| --- | --- |
| Key Concept | Per paradigm (7 total) |
| Common Mistake | Using deep learning on small tabular datasets |
| Common Mistake | Treating time series as i.i.d. regression (temporal leakage) |
| Common Mistake | t-SNE for anything other than visualisation |
| Activity | Given a problem description, walk the decision framework |
| Pro Tip | Start with the simplest model that could work; escalate only when justified |

### Source Assets
| Asset | File |
| --- | --- |
| MLP: simple → complex patterns | `DeepLearningFoundation.pdf` |
| CNN spatial feature learning | `DeepVision.pdf` |
| RNN/LSTM gated unit diagrams | `DeepSeq.pdf` |
| Classification intuition | `2017-04-15-ml-classification.markdown`, `2017-07-02-ml-classification.md` |
| RL definition (state/action/reward) | `2017-06-01-ml-introduction.md` |
| Anomaly detection | `2020-01-01-anamaly-detection-ml.md` |

---

## Chapter 4: Probabilistic and Bayesian Thinking

**File:** `04-bayesian-thinking.qmd`

> **Why a dedicated chapter?** Bayesian ML is underrepresented in standard curricula but central to real-world decision-making under uncertainty — and it is deep expertise of the author. The two blog posts and rich note collection (7 files) make this a natural chapter rather than a section. It also fills the "uncertainty gap" that classical ML leaves open.

### Learning Objectives
- Explain why uncertainty quantification matters in production ML systems
- Describe Bayes' theorem and the prior → likelihood → posterior update
- Distinguish MLE, MAP, and full Bayesian inference
- Implement a simple Bayesian model in PyMC
- Interpret credible intervals and compare them to confidence intervals
- Identify when Bayesian methods are preferable to classical approaches

### Section Outline

**§1 Why Uncertainty Matters**
Open with the industrial machine failure example from the Bayesian foundations blog post: you have 3 months of data for a decision about a 10-year-lifespan asset. Classical statistics needs large datasets; Bayesian methods let you combine sparse data with engineering expertise. In Practice: healthcare (confidence in a rare-disease diagnosis), finance (risk of a credit default), energy (remaining battery capacity uncertainty from the Bayesian regression blog post).

**§2 The Bayesian Update**
Bayes' theorem: Posterior ∝ Likelihood × Prior. Intuitive coin-flip example from `2017-04-25-probabilistic-models.markdown`. Then the beta-binomial model for the A/B test from the Bayesian foundations blog post: 200 visitors, 15 conversions, prior from historical baseline, posterior distribution over conversion rate. Show that the result is a *distribution*, not a point estimate.

**§3 From MLE to Full Bayesian Inference**
Connect to classical ML:
- **MLE**: maximise the likelihood — the objective behind logistic regression, linear regression
- **MAP**: add a prior, maximise posterior — equivalent to L2/L1 regularisation
- **Full Bayes**: marginalise over parameters — get a distribution, not a point
Source: `2017-04-25-probabilistic-models.markdown`, `2018-06-08-bayesian_inference.md`.

**§4 Bayesian Regression in Practice**
Walk through the battery degradation example from the Bayesian regression blog post:
- Why bounded capacity [0,1] needs beta regression, not Gaussian
- Prior specification encoding engineering knowledge (degradation rate, precision)
- MCMC inference with PyMC
- Posterior trace plots and convergence diagnostics (R-hat, ESS)
- Credible intervals vs. confidence intervals
- Evaluation: PICP, prediction interval width alongside classical R², MAE
In Practice: e-commerce — Bayesian A/B test instead of t-test; clinical — Bayesian dose-response model.

**§5 Probabilistic Programming with PyMC**
Minimal code walkthrough — model + guide structure, `pm.sample()`, posterior predictive check. Source: `2020-01-08-ppl-pyro.md` (Pyro concepts, translated to PyMC). Keep code light: this is a conceptual chapter; hands-on notebooks follow in later parts.

**§6 When to Use Bayesian Methods**
Decision checklist:
- Use when: data is scarce, domain knowledge is strong, uncertainty is a first-class output, decisions are high-stakes and asymmetric
- Use classical ML when: data is plentiful, speed matters, interpretability of parameters is not required
- Source: `2018-06-08-bayesian_inference.md`, blog post framing

**§7 Advanced Topics: A Forward Pointer**
Brief signpost to concepts covered later in the book (or in the author's blog series):
- Variational inference as scalable alternative to MCMC (`2018-06-08-stochastic_variational_bayes.md`)
- Probabilistic graphical models (`2018-06-08-bayesian_inference.md`)
- Gaussian processes for non-parametric Bayes
- Bayesian deep learning and uncertainty in neural networks

### Markers
| Type | Content |
| --- | --- |
| Key Concept | Bayes' theorem and the prior/likelihood/posterior relationship |
| Key Concept | MLE vs. MAP vs. full Bayesian inference |
| Common Mistake | Interpreting a 95% credible interval as "95% probability parameter is in this range" — that IS what it means; contrast with frequentist confidence interval |
| Common Mistake | Using uninformative priors when domain knowledge exists |
| Activity | Given a prior and observed data, compute and plot the posterior by hand (conjugate beta-binomial) |
| Activity | Modify the battery degradation PyMC model to use a different prior; observe effect on posterior |
| Pro Tip | Always run prior predictive checks before fitting — verify the prior generates plausible data |

### Source Assets
| Asset | File |
| --- | --- |
| Industrial machine failure motivation | Blog post: Bayesian foundations |
| A/B test e-commerce example | Blog post: Bayesian foundations |
| Beta-binomial coin-flip | `2017-04-25-probabilistic-models.markdown` |
| MLE / MAP connection | `2017-04-25-probabilistic-models.markdown`, `2018-06-08-bayesian_inference.md` |
| Battery degradation Bayesian regression | Blog post: Bayesian regression |
| Bayesian inference / VI foundations | `2018-06-08-bayesian_inference.md` |
| PyMC / Pyro PPL patterns | `2020-01-08-ppl-pyro.md` |
| Probability / information theory bridge | `2018-06-08-intro_probability_information_theory.md` |

---

## Improvement Suggestions

### 1. Multi-Domain Example Strategy (High Priority)
Energy is authentic and technically rich, but risks alienating learners who can't map their problem to power systems. **Recommendation:** keep energy as the primary running example but add an "In Practice" callout box in each major section with 2–3 parallel examples from e-commerce, healthcare, and finance. This pattern is already threaded through the plan above. The A/B testing example from the Bayesian foundations blog post is particularly strong for the e-commerce audience.

### 2. Bayesian ML as Chapter 4 (High Priority)
The two blog posts + seven sermon notes represent deep, mature material that deserves its own chapter rather than a section in Chapter 3. Key arguments:
- Bayesian thinking is a distinct *paradigm*, not just another algorithm family
- Uncertainty quantification is increasingly required in production systems (regulation, safety-critical applications)
- The blog posts already provide polished, pedagogically structured content to draw from
- It fills the gap in the panorama: classical ML and DL give point estimates; Bayesian ML gives distributions
- The battery degradation example from the blog is an ideal demonstration case that resonates across domains

### 3. Decision Layer / Optimisation (Medium Priority)
RL and constrained optimisation are valuable to include briefly but should **not** become a full chapter in Part 4 — the book's current plan doesn't allocate a dedicated RL part, and treating it fully would inflate scope. The recommendation above (§7 in Chapter 3) covers the key insight — that prediction feeds a decision — without requiring readers to learn policy gradients. If a future Part 10 ("Value-driven AI") or Part 9 ("ML System Design") is written, the decision layer material can be expanded there.

### 4. Probabilistic Models Bridge (Medium Priority)
The 2017 notes (`2017-04-25-probabilistic-models.markdown`, `2018-06-08-intro_probability_information_theory.md`) contain strong foundational material on MLE, beta distributions, entropy, and KL divergence. This sits naturally in Chapter 4 §3 as the bridge from classical ML (which secretly uses MLE) to full Bayesian inference. It also previews the math behind cross-entropy loss in neural networks.

### 5. Teaching Style Consistency (Low Priority — Implementation Note)
All four chapters should follow the book's existing conventions:
- Collapsible **Topics / Learning Objectives / Further Reading / Summary** blocks (from the existing QMD polish pattern)
- Four recurring markers: **Key Concept** / **Activity** / **Common Mistake** / **Pro Tip**
- Minimal code in this part — conceptual diagrams and light illustrative snippets only
- Each chapter is a self-contained `.qmd` file, not a notebook (contrast with the existing `.ipynb` files in `04-ml-intro/` which are deeper hands-on content)

### 6. Connection to Existing `04-ml-intro/` Notebooks (Low Priority — Structure Note)
The existing notebooks in `tutorials/04-ml-intro/` (`01-dl-pytorch.ipynb`, `02-optuna-hyperparameter.ipynb`, `03-ml-pipeline.ipynb`) are hands-on and more advanced. These should remain as-is but are **not** part of this conceptual Part 4. They may be better repositioned into Part 5 (Deep Learning) and Part 7 (MLOps/Pipelines) once those parts are written. Flag for later restructuring.

---

## Effort Estimate

| Chapter | Estimated Writing Effort | Primary Sources |
| --- | --- | --- |
| Ch 1: What Is ML? | 3–4 days | `MLfundamentals.pdf`, `AI4Public_slide.pdf`, 2017 intro notes |
| Ch 2: Workflow & Framing | 4–5 days | `MLstrategy.pdf`, 2017 intro notes |
| Ch 3: Algorithm Panorama | 5–7 days | All PDF slides, 2017 classification notes |
| Ch 4: Bayesian Thinking | 5–6 days | Two blog posts, 2018 Bayesian notes |
| **Total** | **~3–4 weeks** | |

---

## CV-Based Additions

> Analysis of [Anthony_CV_2026_ADI.pdf](https://sambaiga.github.io/files/Anthony_CV_2026_ADI.pdf) identified five missing paradigms, two missing uncertainty techniques, four new business domains, and several forward-pointer opportunities. Changes are mapped to specific chapters and sections.

---

### A. Missing Paradigms (Add to Chapter 3)

#### A1. Graph Neural Networks — Add as §5b inside Deep Learning

The current §5 covers CNN/RNN/Transformer but omits GNNs entirely. Anthony has two IEEE publications directly on this topic (GANF for forecasting, adaptive weighted recurrence graphs for NILM), making it a natural area of authority.

**What to cover:**

- When data has relational structure that flat feature vectors cannot capture (power grids, supply chain networks, social graphs, molecular structures)
- Graph convolution intuition: nodes aggregate information from neighbours
- Graph attention networks: not all neighbours are equally informative
- Key distinction: CNNs encode spatial locality; GNNs encode *relational* structure

**Examples:**

- Primary: substation graph — each node is a substation, edges are transmission lines; GNN predicts fault propagation
- In Practice: molecular property prediction (drug discovery), fraud ring detection (finance), logistics network optimisation (supply chain)

**Source:** Anthony's own publications — GANF (2022 IEEE TSG), adaptive weighted recurrence graphs (2021 IEEE TSG). These give authentic production credibility.

**Why it belongs in the panorama:** GNNs are increasingly mainstream (used in AlphaFold, recommendation systems, chip design) and represent a distinct architectural family. Omitting them would date the book.

---

#### A2. Variational Autoencoders — Add as §3b inside Unsupervised Learning

VAEs appear in the CV as the core method for large-scale load profiling (10,000+ building profiles). They sit at the intersection of unsupervised learning and deep learning and serve as a natural bridge to §6 (LLMs/Generative AI).

**What to cover:**

- Encoder-decoder architecture: compress data into a latent distribution, reconstruct from samples
- Key idea: VAEs learn a *smooth* latent space, unlike plain autoencoders — enabling generation, interpolation, and anomaly detection
- Three uses: (1) compact representation / clustering, (2) anomaly detection (high reconstruction error = anomaly), (3) data augmentation for scarce classes

**Examples:**

- Primary: 10k building load profiles — VAE learns a 2D latent space; cluster segments emerge without labels
- In Practice: generating synthetic patient records (healthcare), augmenting rare defect images (manufacturing), learning latent user preference space (recommendation)

**Source:** CV: "variational auto-encoders and clustering to segment 10,000+ building load profiles." Transition naturally from K-means (§3a) to VAEs as "deep clustering."

---

### B. Missing Uncertainty Techniques (Add to Chapter 4)

The current plan covers Bayesian inference well but misses two important non-Bayesian approaches to uncertainty that Anthony has published on directly.

#### B1. Quantile Regression — Add as §3b in Chapter 4 (after MLE/MAP/Bayes)

Quantile regression produces prediction intervals without any distributional assumptions by training models to predict specific quantiles (e.g., 10th, 50th, 90th percentile). The FPSeq2Q architecture is built on this.

**What to cover:**

- Pinball loss as the training objective — asymmetric penalty for under- vs. over-prediction
- Produces a distribution by predicting multiple quantiles simultaneously
- No prior specification required; works with any gradient-based model
- Key limitation: quantiles can cross (10th percentile > 90th) — requires post-hoc fixes

**Examples:**

- Primary: net-load forecasting — predict P10/P50/P90 for each hour; the interval width signals how much reserve capacity to schedule
- In Practice: delivery time estimation (logistics), drug dosage ranges (clinical), salary band estimation (HR)

**Positioning within Chapter 4:** sits after MLE/MAP/Bayes (§3) as a pragmatic alternative: "If you need prediction intervals but can't specify priors, use quantile regression."

---

#### B2. Conformal Prediction — Add as §5b in Chapter 4 (after PyMC walkthrough)

Anthony has a 2024 IEEE SmartGridComm publication on conformal MLPs for probabilistic net-load forecasting. Conformal prediction gives **distribution-free, coverage-guaranteed** intervals — a fundamentally different guarantee from Bayesian credible intervals.

**What to cover:**

- Core guarantee: "the true value will fall inside the interval at least 90% of the time, regardless of model or data distribution"
- How it works: use a calibration set to compute nonconformity scores; set interval width to cover 90% of calibration errors
- Works with *any* model — wrap a fitted sklearn model, XGBoost, or neural network with conformal prediction in 10 lines
- Contrast with Bayesian: Bayesian gives calibrated distributions (requires assumptions on the likelihood and prior); conformal gives coverage guarantees (distribution-free, requires only exchangeability)

**Examples:**

- Primary: conformal MLP for low-voltage distribution network forecasting — same architecture as §5 (Deep Learning), now with guaranteed coverage
- In Practice: medical diagnosis confidence bands (FDA-regulated devices require coverage guarantees, not just calibrated probabilities), legal-risk scoring (finance)

**Source:** Anthony's 2024 IEEE SmartGridComm paper on conformal MLP.

**Why it belongs in Chapter 4:** It closes the uncertainty toolkit — Bayesian for rich prior knowledge, quantile regression for pragmatic interval training, conformal for guaranteed coverage with any model. Together they form a complete picture.

---

#### B3. Update Chapter 4 Learning Objectives

Add:
- Explain quantile regression as a distribution-free approach to prediction intervals
- Describe conformal prediction and its coverage guarantee
- Choose the right uncertainty method given the problem constraints

---

### C. Add HMMs to Chapter 4 §7 (or expand §7 into a bridge section)

Hidden Markov Models appear in the CV (CNC spindle health diagnostics). They are a classical probabilistic sequential model — predating deep learning — that connects Bayesian thinking to time series naturally.

**Brief addition to §7 (Advanced Topics):**
- HMMs as a probabilistic state-space model: hidden states (machine condition: healthy / degraded / failing) emit observable signals (vibration, temperature)
- The forward-backward algorithm as probabilistic inference
- Why HMMs still matter: interpretable, works on short sequences, widely used in manufacturing and speech
- Primary example: CNC spindle health — 3 latent states, sensor observations, transition probabilities encode wear progression
- Bridge: HMMs are to sequential data what Bayesian regression is to tabular data — a principled probabilistic model before deep learning took over

---

### D. New Business Domains (Update Running Scenario Table)

Add three new domains from CV roles to the "In Practice" rotation:

| Domain | Source in CV | Concept Fit |
| --- | --- | --- |
| **Supply chain / demand forecasting** | Current ADI role: "demand forecasting and intelligent planning across a complex global network" | Time-series forecasting, uncertainty, ranking/prioritisation |
| **Predictive maintenance / manufacturing** | CeADAR role: 30% downtime reduction, 25% OEE increase; HMM spindle diagnostics | Anomaly detection, classification, probabilistic models (HMM), RL for maintenance scheduling |
| **Precision agriculture** | UDOM role: banana disease detection computer vision, smallholder farmers | Classification (computer vision), limited-data settings (good Bayesian example), social impact framing |

**Update the multi-domain table in "Running Scenario Strategy" to include these three and add a note:**

> Supply chain is particularly valuable as a second primary example alongside energy — it is immediately relatable to engineers in any industry, appears in the author's current role, and spans regression (demand forecasting), classification (order anomaly), clustering (SKU segmentation), ranking (reorder priority), and uncertainty (safety stock under forecast error).

---

### E. Forward Pointers to Add (Chapter 3 §2 — Time-Series Forecasting)

The CV reveals a depth of published work on time-series architectures not yet reflected in the plan. Strengthen §2 with:

- **Multi-horizon forecasting** as a distinct challenge from single-step — N-HiTS and seq2seq architectures are built specifically for this
- **Uncertainty in forecasting** as a first-class concern: point forecasts are insufficient for capacity planning and reserve scheduling — cite FPSeq2Q (quantile heads) and conformal MLP as production-grade solutions
- **Forward pointer**: "In Part 5 (Deep Learning), we implement N-HiTS, FPSeq2Q, and conformal prediction heads — the architectures behind the open-source Twiga library"

This gives the book a unique identity: most ML books treat forecasting as "just regression on time." The Twiga library and the publications behind it make this chapter stand apart.

---

### F. Updated Effort Estimate

| Chapter | Original Estimate | Revised Estimate | New Content |
| --- | --- | --- | --- |
| Ch 1: What Is ML? | 3–4 days | 3–4 days | +supply chain / agriculture as In Practice domains |
| Ch 2: Workflow & Framing | 4–5 days | 4–5 days | +MLOps preview callout in §2 workflow diagram |
| Ch 3: Algorithm Panorama | 5–7 days | 6–8 days | +GNNs (§5b), +VAEs (§3b), +stronger forecasting §2 |
| Ch 4: Bayesian Thinking | 5–6 days | 7–9 days | +quantile regression (§3b), +conformal prediction (§5b), +HMMs (§7) |
| **Total** | **~3–4 weeks** | **~4–5 weeks** | |

---

### G. Summary: What the CV Adds vs. What Was Already Planned

| Element | Status Before CV | Status After |
| --- | --- | --- |
| Graph Neural Networks | Missing | Add to Ch 3 §5b |
| Variational Autoencoders | Missing | Add to Ch 3 §3b |
| Quantile regression | Missing | Add to Ch 4 §3b |
| Conformal prediction | Missing | Add to Ch 4 §5b |
| Hidden Markov Models | Missing | Add to Ch 4 §7 |
| Supply chain examples | Missing | Add to all In Practice callouts |
| Predictive maintenance examples | Implicit only | Make explicit in all In Practice callouts |
| Precision agriculture examples | Missing | Add to In Practice callouts |
| Multi-horizon forecasting depth | Shallow | Strengthen Ch 3 §2 with publications |
| Uncertainty in forecasting | Not mentioned | Add to Ch 3 §2 and Ch 4 |
| Author's publications as anchors | Not referenced | GNN, conformal, FPSeq2Q, N-HiTS referenced |

---

*Last updated: 2026-06-23*
