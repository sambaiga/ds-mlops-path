# Dataset research: high-impact free datasets for business ML

Research into Hugging Face, Kaggle, and Nature (*Scientific Data*) datasets that
demonstrate the business value of data analytics and ML across regression,
classification, ranking/recommendation, clustering/segmentation, forecasting,
and anomaly detection, while being recent and high-value. No single free
dataset natively aces all six paradigms, but one comes close.

## Top pick: "Open e-commerce 1.0" (Nature *Scientific Data*, 2024)

[Berke et al., MIT Media Lab](https://www.nature.com/articles/s41597-024-03329-6)
5,027 U.S. Amazon consumers, **1.8M real purchases spanning 2018-2022**, each
linked via informed-consent survey to demographics, lifestyle, and health
variables. Hosted on
[Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YGLYDY),
open access, peer-reviewed.

This is rare: individual-level purchase behavior *linked to who the person is*
almost never gets released openly (privacy). That linkage is what makes it
"high-value" rather than just another transactions table, and the 2018-2022
window includes the COVID demand shock, which is a strong
forecasting/anomaly narrative for free.

| Task | How it maps |
|---|---|
| Regression | Predict spend (total or per-category) from demographics/lifestyle |
| Classification | Predict a demographic trait (e.g., presence of children, income band) from purchase mix; category-adoption prediction |
| Clustering/segmentation | Consumer personas from RFM + category mix + demographics |
| Forecasting | Per-household or per-category monthly spend, 5 real years including COVID shock |
| Recommendation/ranking | Next-category / co-purchase recommendation from purchase sequences |
| Anomaly detection | Spending-pattern breaks per household (life events, panic-buying spikes) |

Caveat: only 5,027 people (fine for row-level models, thin for per-user ones),
and no rich product text/images.

## Complements, if splitting by strength instead of one flagship

- **Recommendation/ranking at scale**:
  [Amazon Reviews 2023 (McAuley Lab, Hugging Face)](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
  571M+ reviews, 48M+ products, 33 categories, includes bought-together
  graphs and images. Actively used in 2024-2025 recsys research; sample one
  category (e.g. `All_Beauty`, ~700K reviews) to keep it teachable. No native
  license restriction beyond Amazon's ToS on redistribution/commercial
  scraping reuse, fine for education.
- **Easiest to teach, most existing tutorials**:
  [Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
  7 relational tables (orders, items, payments, reviews, products, sellers,
  geolocation), 100K orders. Weakest on "recent" (2016-2018) and license is
  CC BY-NC-SA (non-commercial), but if the goal is a clean teaching path with
  abundant reference notebooks, this is the path of least resistance.

## Open question

Whether to prototype loading and profiling the Nature dataset (or one of the
alternates) in the repo to see it against real notebook constraints before
committing to it as a running dataset for the ML landscape / MLOps / value-
driven-AI parts.
