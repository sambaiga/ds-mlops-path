# Part 4: The Machine Learning Landscape — Implementation Plan

> **Role in the book:** Conceptual and practical bridge between "Dev Tools" (Parts 1–3) and the applied ML project series (Part 5+). Readers finish this part knowing *what* ML is, *how* to frame and diagnose ML problems, and *how to build* correct sklearn pipelines using the engineering habits from Parts 1–3 — before tackling real-world projects.

---

## Structure Overview

| Chapter | Title | Format | Primary Theme |
| --- | --- | --- | --- |
| 1 | The AI Landscape and What Motivates ML | QMD | AI/ML/DL hierarchy, the limits of rules |
| 2 | What Machine Learning Is | QMD | Taxonomy, paradigms, task types, when to use ML |
| 3 | The ML Workflow and Problem Framing | QMD | Formulation, evaluation, bias-variance, strategy |
| 4 | Machine Learning with scikit-learn | Notebook | sklearn API, preprocessing, evaluation in code |
| 5 | ML Pipelines, Cross-Validation, and Hyperparameter Search | Notebook | Pipeline, ColumnTransformer, Optuna |

> **Bayesian and Probabilistic Thinking** was originally planned here but moved to its own dedicated part later in the book. It is best encountered after learners have run real projects and hit the limits of point estimates.

**File layout:**
```
tutorials/04-ml-intro/
├── 01-ml-introduction.qmd        (done)
├── 02-ml-what-is-ml.qmd          (done)
├── 03-ml-workflow.qmd            (done)
├── 04-sklearn-core.ipynb         (Part 22)
└── 05-sklearn-pipeline.ipynb     (Part 23)
```

**`_quarto.yml` current state:**
```yaml
- part: "Part 4: ML Landscape"
  chapters:
    - tutorials/04-ml-intro/01-ml-introduction.qmd
    - tutorials/04-ml-intro/02-ml-what-is-ml.qmd
    - tutorials/04-ml-intro/03-ml-workflow.qmd
    - tutorials/04-ml-intro/04-sklearn-core.ipynb
    - tutorials/04-ml-intro/05-sklearn-pipeline.ipynb
```

---

## Running Scenario Strategy

**Primary dataset for notebooks: University Analytics**
2,400 student records with scores, study habits, program, and demographic features. Already familiar to learners from Parts 1–3. Using familiar data lets learners focus on the sklearn API rather than domain understanding.

Features available: `study_hours`, `attendance_pct`, `midterm_score` (numerical); `program`, `gender`, `region`, `has_internet` (categorical).

- Regression target: `final_score` (predict final exam score from early indicators)
- Classification target: `passed` (predict pass/fail from early indicators)

**Primary domain for QMD chapters: Smart Energy Analytics**
Authentic to the author's research expertise (NILM, load forecasting, smart-grid, anomaly detection).

**Supporting domains: "In Practice" callout boxes**
Each major section includes a brief multi-domain callout showing the same concept in 2–3 other contexts.

| Domain | Concept Fit |
| --- | --- |
| E-commerce / retail | Customer churn (classification), sales forecasting, recommendation |
| Healthcare / clinical | Patient readmission (classification), drug dosage (regression) |
| Finance / banking | Credit scoring (classification), fraud detection (anomaly) |
| HR / people analytics | Employee attrition (classification), salary modelling (regression) |

---

## Chapter 1: The AI Landscape and What Motivates ML

**File:** `01-ml-introduction.qmd` — **DONE**

---

## Chapter 2: What Machine Learning Is

**File:** `02-ml-what-is-ml.qmd` — **DONE**

**Pending small addition:** One section after the taxonomy (§1.2) covering the model complexity spectrum: linear → tree-based → neural. Shows interpretability–capacity tradeoff. This is the one concept not yet covered in Ch1–Ch3 that was worth keeping from the dropped panorama chapter.

---

## Chapter 3: The ML Workflow and Problem Framing

**File:** `03-ml-workflow.qmd` — **DONE**

Covers: problem framing, the 9-stage workflow, data splits (including temporal splits and distribution mismatch), evaluation metrics by task type, bias-variance diagnosis and learning curves, the decision framework for when performance is insufficient.

---

## Chapter 4: Machine Learning with scikit-learn

**File:** `04-sklearn-core.ipynb` — **Part 22**

### Purpose
Ch1–Ch3 taught the *theory*: problem framing, evaluation metrics, bias-variance diagnosis. This notebook implements every one of those concepts in code using the sklearn API. Learners leave able to build, evaluate, and persist a correct ML model with professional engineering habits (type annotations, loguru logging, pathlib).

### Learning Objectives

| # | Skill | Covered in |
| --- | --- | --- |
| 1 | Describe the sklearn API contract (fit/predict/transform/score) and apply it to any estimator | Sec. 1 |
| 2 | Load and explore a real dataset, separating numerical and categorical features | Sec. 2 |
| 3 | Apply StandardScaler and MinMaxScaler correctly, fitting only on training data | Sec. 3 |
| 4 | Split data with train_test_split, using stratification for classification | Sec. 4 |
| 5 | Establish a DummyRegressor / DummyClassifier baseline before training any model | Sec. 5 |
| 6 | Train LinearRegression and LogisticRegression and evaluate with the metrics from Ch3 | Sec. 6 |
| 7 | Use cross_val_score and StratifiedKFold for reliable model assessment | Sec. 7 |
| 8 | Compute and interpret learning curves, connecting back to Ch3 §5 diagnosis | Sec. 8 |
| 9 | Persist a trained model with joblib and reload it for inference | Sec. 9 |
| 10 | Build a type-annotated, logged end-to-end training function | Capstone |

### Section Outline

**§0 Setup**
Imports with type annotations (from Part 16), loguru logger configuration (from Part 21). Brief: this notebook is Ch3 in code.

**§1 The sklearn API contract**
Three object types: Transformers (fit + transform), Predictors (fit + predict), Pipelines (both). The single rule: fit on training data only, then transform/predict on anything. Diagram showing the flow. Key Concept callout.

**§2 The dataset: University Analytics**
Load `university_analytics.csv` from the existing data directory. Show the connection: "you've been computing grades manually in Parts 1–3; now you'll predict them." Select three numerical features (`study_hours`, `attendance_pct`, `midterm_score`) and two targets (`final_score` for regression, `passed` for classification). Note that categorical features (`program`, `gender`, `region`) are intentionally left for the Pipeline notebook.

**§3 Preprocessing: StandardScaler and MinMaxScaler**
StandardScaler: zero mean, unit variance — the default for most sklearn models (linear models, SVM, KNN, neural nets). MinMaxScaler: bounded [0,1] — prefer when the algorithm requires bounded features or the scale itself is interpretable. The critical rule: `fit` only on training data, then `transform` both train and test. Show the leakage mistake: fitting the scaler on all data first. Common Mistake callout.

**§4 Splitting data (Ch3 §3 in code)**
`train_test_split` for regression. Stratified split for classification (`stratify=y`) — show why it matters on imbalanced `passed` column. Connecting explicitly to Ch3 §3 temporal split note.

**§5 Baseline first (Ch3 §5 in code)**
`DummyRegressor(strategy="mean")` and `DummyClassifier(strategy="most_frequent")`. These are the baselines from Ch3: any model that doesn't beat a dummy is not learning. Log baseline metrics with loguru. Key Concept callout.

**§6 Simple models and evaluation (Ch3 §4 in code)**
Regression: `LinearRegression` with MAE, RMSE, R² — connecting each metric to Ch3 §4 descriptions. Classification: `LogisticRegression` with `classification_report` and `ConfusionMatrixDisplay` — connecting precision/recall tradeoff to Ch3 §4. Use type-annotated `evaluate_regressor()` and `evaluate_classifier()` helper functions. Log results with loguru.

**§7 Cross-validation**
Why single train/val split is unreliable (high variance estimate). `cross_val_score` with `KFold` and `StratifiedKFold`. Connecting to Ch3: cross-validation gives a distribution of scores, not a point estimate — this is what "model assessment" really means.

**§8 Learning curves (Ch3 §5 in code)**
`sklearn.model_selection.learning_curve`. Plot training error and validation error against training set size — the exact plot from Ch3 §5 diagrams. Read the four patterns: underfitting (both high), overfitting (large gap), good fit (both low), data-limited (val still decreasing at max size). Pro Tip: plot learning curves for every model before reporting results.

**§9 Model persistence**
`joblib.dump()` to save, `joblib.load()` to restore. Use `pathlib.Path` for the save location. Show that the loaded model produces identical predictions. Connect to Ch3 §2 workflow: "Deployment" step requires a serialized model object.

**Capstone: end-to-end training function**
Type-annotated `train_and_evaluate()` function that accepts a dataset path, target column, and model, then runs: load → select features → split → scale → fit → evaluate → learning curve → save. Uses loguru at each stage. Activity: run it for both regression and classification targets, compare performance to the dummy baseline.

### Markers

| Type | Content |
| --- | --- |
| Key Concept | sklearn API contract: fit on train, transform/predict on any split |
| Key Concept | Baseline first: DummyRegressor/Classifier sets the floor |
| Common Mistake | Fitting the scaler on all data before splitting (data leakage) |
| Common Mistake | Reporting accuracy on imbalanced classes (use classification_report) |
| Activity | Verify: does StandardScaler on a StandardScaler-transformed test set produce zero-mean output? Why or why not? |
| Activity | Add Ridge regression to the comparison and plot all three learning curves on the same axes |
| Pro Tip | Plot learning curves before reporting any model result |

### Source Assets

| Asset | Description |
| --- | --- |
| `tutorials/01-python-basics/data/university_analytics.csv` | 2,400 student records, mixed numerical + categorical features |
| Ch3 §3 (data splits), §4 (evaluation metrics), §5 (learning curves) | Theory implemented in code here |
| Parts 16 + 21 (type annotations, loguru) | Dev-tools practices applied directly |

---

## Chapter 5: ML Pipelines, Cross-Validation, and Hyperparameter Search

**File:** `05-sklearn-pipeline.ipynb` — **Part 23**

### Purpose
Chapter 4 builds models on pre-cleaned numerical features. This notebook adds the full production-grade sklearn idiom: Pipeline + ColumnTransformer for mixed-type data, proper cross-validated hyperparameter search with Optuna, and a model card to document the result.

### Learning Objectives

| # | Skill | Covered in |
| --- | --- | --- |
| 1 | Build a Pipeline that chains preprocessing and a model into one object | Sec. 1 |
| 2 | Use ColumnTransformer to apply different transformers to different feature types | Sec. 2 |
| 3 | Explain why a Pipeline prevents data leakage inside cross-validation | Sec. 3 |
| 4 | Search hyperparameters with GridSearchCV and RandomizedSearchCV | Sec. 4 |
| 5 | Run an Optuna study to optimize pipeline hyperparameters efficiently | Sec. 5 |
| 6 | Interpret feature importance and SHAP values for a fitted pipeline | Sec. 6 |
| 7 | Document a trained model with a brief model card | Sec. 7 |

### Section Outline

**§1 The Pipeline object**
Chain: ColumnTransformer → model. One call to `fit(X_train, y_train)` runs the whole chain. One call to `predict(X_test)` preprocesses and predicts. Why this matters: without a Pipeline, manually applying preprocessing inside a cross-validation loop re-fits transformers on the validation fold — data leakage.

**§2 ColumnTransformer: mixed feature types**
Numerical columns → StandardScaler. Categorical columns → OneHotEncoder. The `remainder="drop"` option. Show why the university analytics data needs this: `program` and `region` must be one-hot encoded, not ignored.

**§3 Why Pipeline prevents leakage**
Compare: manual preprocessing before cross_val_score (wrong) vs. Pipeline inside cross_val_score (correct). Demonstrate the numeric difference in reported score. Connect to Ch3 §3.4 (feature leakage).

**§4 Hyperparameter search: GridSearchCV and RandomizedSearchCV**
`param_grid` with double-underscore syntax for pipeline steps (`model__C`, `preprocessor__num__with_mean`). When to use grid vs. random search.

**§5 Optuna: production-grade hyperparameter search**
Why Optuna: pruning (stop bad trials early), distributed search, richer search spaces (log-uniform, integer, categorical). Show a minimal Optuna study for the sklearn pipeline. Connect to `pyproject.toml`: Optuna is already in the `modelling` extra.

**§6 Feature importance and SHAP values (brief)**
For linear models: `coef_` after inverse-transforming. For tree-based models: `feature_importances_`. SHAP as a model-agnostic alternative — 3 lines of code. Forward pointer to Part 5 projects where SHAP appears in every project.

**§7 Model card**
Brief documentation: problem statement, features used, model type, evaluation scores (train/val), known limitations. Print as a structured dict. Connect to Ch3 §1 ML spec card: the model card is the completed version of the spec card.

### Markers

| Type | Content |
| --- | --- |
| Key Concept | Pipeline = preprocessing + model as a single, leak-free object |
| Common Mistake | Fitting preprocessing outside the Pipeline (guaranteed leakage inside cross-validation) |
| Common Mistake | Using GridSearchCV on a large search space (exponential cost) |
| Activity | Replace LogisticRegression with a GradientBoostingClassifier and rerun the Optuna study |
| Pro Tip | Always use a Pipeline in production; a model that requires manual preprocessing before calling predict will break |

---

## Part 5: Classical ML Projects — Implementation Plan

> **Role in the book:** Applies everything from Part 4 to five end-to-end projects using real datasets. No new theory is introduced. Each project follows the same spine from Ch3, using the sklearn Pipeline from Ch5.

**Project spine (applied in every notebook):**

1. Problem spec card (Ch3 §1)
2. Data loading and EDA
3. Feature engineering + ColumnTransformer pipeline
4. Model selection: baseline → simple model → boosting model
5. Evaluation with metrics from Ch3 §4
6. Learning curve diagnosis (Ch3 §5)
7. Decision framework if performance is insufficient (Ch3 §6)
8. Key findings and recommendations

### Proposed Projects

| # | Problem | Dataset | Algorithm family |
| --- | --- | --- | --- |
| 5.1 | Predict hourly bike demand (regression) | Seoul Bike Sharing Demand (UCI, 8,760 rows) | Linear → Ridge → LightGBM |
| 5.2 | Predict customer churn (classification) | IBM Telco Customer Churn (7,043 rows) | Logistic → Random Forest → XGBoost |
| 5.3 | Detect energy theft (anomaly detection) | Synthetic + real smart meter features | Isolation Forest → Autoencoder baseline |
| 5.4 | Segment customers (clustering) | Customer Personality Analysis (Kaggle, 2,240 rows) | K-Means → DBSCAN |
| 5.5 | Recommend movies (collaborative filtering) | MovieLens 25M | Item-based CF → matrix factorisation baseline |

> Dataset choices, exact file names, and boosting model details are confirmed before each project notebook is written.
