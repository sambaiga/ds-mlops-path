# Predicting Battery Capacity — Data Science End-to-End Project




## Project Overview

This project aims to predict battery capacity from charging and discharging features using the CALCE Battery Dataset. It is designed as a guided, modular learning path for transitioning  to applied data science and MLOps.

Through this project, you will:

- Build a data science project following both software engineering and data science best practices, using modular, testable, and well-structured code.

- Follow the [CRISP-DM framework](https://medium.com/@shawn.chumbar/the-crisp-dm-process-a-comprehensive-guide-4d893aecb151) to apply a systematic, end-to-end data science process from business understanding to deployment.

- Develop regression models using [scikit-learn](https://scikit-learn.org/stable/) and [XGBoost](https://xgboost.readthedocs.io/en/stable/) within reproducible machine learning pipelines.

_ Deploy the trained model using modern MLOps tools and workflows, including FastAPI, [Docker](https://www.docker.com/), [MLflow](https://mlflow.org/), [prefect](https://www.prefect.io/) to simulate real-world production environments.

## 🎓 Outcome

By the end of this project, you will have mastered:

- The end-to-end data science process — from data to deployment.

- The tools and workflows used in professional ML projects.

- How to think, structure, and deliver like a data scientist working in production environments.

Each phase will be developed in a feature branch, reviewed through a Pull Request (PR), and merged into main.

## Phase 0 Installation & Setup


1. **Clone the repository**:
   ```bash
   https://github.com/sambaiga/battery-capacity-project.git
   ```

2. **Install** [uv](https://docs.astral.sh/uv/getting-started/installation/) (if not already installed):
  ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Create and activate the virtual environment**

  ```bash
    # Create the environment in .venv
    uv venv --python 3.11
  ```
  ```bash
    # Activate the environment
    source .venv/bin/activate
```

4. **Install all dependencies **

This command reads the ``pyproject.toml`` file and installs all required packages (main, dev, test, etc.).

 ```bash
     uv sync --extra modelling  --extra dev --extra test
 ```



5. **Install the project in editable mode**.
   This is crucial for development and ensures you can import your local ark package (e.g., in Jupyter notebooks).
    ```bash
        uv pip install -e .
    ```

6. **Initialize pre-commit hooks**
This sets up hooks that automatically format and lint your code before each commit. Since pre-commit is now installed in your environment, we run it via `uv run`.
    ```bash
    uv run pre-commit install
    ```

7. **Install git-cliff (for changelog)**
   If you want to maintain an automated changelog:
  ```bash
    brew install git-cliff
  ```


### Verification

Once setup is complete:

1. Open the project in VS Code (or your preferred IDE).

2. Run the `data_exploration.ipynb` notebook from the /notebooks folder.

3. Verify imports and paths load correctly.

4. Download the dataset from [CALCE Processed Dataset on Figshare]((https://figshare.com/articles/dataset/Calce_Processed_dataset/30575315))
 and place it under: dataset folder.



If everything runs smoothly, your environment is correctly configured and ready for development.

## 🧭 Next Steps

Proceed to:

<details> <summary><b>Phase 1 — Data Loading & Exploration</b></summary>

🎯 Goal:
Understand and explore the dataset to build familiarity with its structure, content, and potential modeling features.

🧩 Tasks:

- Load and summarize data using a reusable data_loader module.

- Perform exploratory data analysis (EDA) to assess distributions, trends, and data quality.

- Visualize capacity degradation and relationships between features.

- Document insights and questions in a Jupyter notebook.

**References**
- https://github.com/sambaiga/AI4DLearning?tab=readme-ov-file
