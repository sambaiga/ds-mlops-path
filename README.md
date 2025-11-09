# Predicting Battery Capacity — Data Science End-to-End Project

## Project Overview

This project aims to predict battery capacity from charging and discharging features using the CALCE Battery Dataset. It is designed as a guided, modular learning path for transitioning  to applied data science and MLOps.

Through this project, you will:

- Build a data science project following software engineering best practices.

- Learn to package your code into reusable components.

- Apply machine learning pipelines for regression using scikit-learn and XGBoost.

- Deploy a model locally as an API using FastAPI + Docker.

- Simulate MLOps principles (versioning, CI/CD, reproducibility).

Each phase will be developed in a feature branch, reviewed through a Pull Request (PR), and merged into main.

## Phase 0 Installation & Setup


1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
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
  ```bash
    brew install git-cliff
  ```
Once you've completed these steps, you are ready to open the project in VS Code and test your setup by running the test notebook.

### Key Development Workflow Commands

| Task                                | Command                                      | Purpose |
|-------------------------------------|----------------------------------------------|---------|
| **Code Formatting (Apply)**         | `uv run ruff format .`                       | Applies automatic code formatting across the entire project. Run this frequently to maintain style consistency. |
| Linting & Fixing                | `uv run ruff check . --fix`                  | Runs the linter to detect issues and attempts to automatically fix simple violations (like unused imports). |
| Formatting (Check)              | `uv run ruff format . --check`               | Checks if any files require formatting. It fails (exits non-zero) if changes are needed, making it perfect for CI/pre-commit checks. |
| Test Run (Full)                | `uv run pytest`                              | Executes your entire test suite. This automatically includes coverage reports as configured in your `pyproject.toml`. |
| Run Hooks Manually              | `uv run pre-commit run --all-files`          | Executes all pre-commit checks (formatting, linting, lock file check) on every file. Use this for a full project cleanup before pushing. |
