from pathlib import Path
import nbformat as nbf

PROJECT_NAME = "Enterprise-Retail-Sales-Intelligence"

# --------------------------------------------------
# Folder Structure
# --------------------------------------------------

folders = [
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks",
    "src",
    "dashboard",
    "models",
    "reports",
    "reports/figures",
]

# --------------------------------------------------
# Notebook Names
# --------------------------------------------------

notebooks = {
    "01_business_understanding.ipynb": "Business Understanding",
    "02_data_understanding.ipynb": "Data Understanding",
    "03_data_cleaning.ipynb": "Data Cleaning",
    "04_exploratory_data_analysis.ipynb": "Exploratory Data Analysis",
    "05_feature_engineering.ipynb": "Feature Engineering",
    "06_linear_regression.ipynb": "Linear Regression",
    "07_model_evaluation.ipynb": "Model Evaluation",
    "08_model_comparison.ipynb": "Model Comparison",
    "09_business_recommendations.ipynb": "Business Recommendations",
}

# --------------------------------------------------
# Python Source Files
# --------------------------------------------------

python_files = [
    "config.py",
    "data_loader.py",
    "preprocessing.py",
    "feature_engineering.py",
    "train.py",
    "evaluate.py",
    "visualization.py",
    "utils.py",
]

project = Path(PROJECT_NAME)

# --------------------------------------------------
# Create folders
# --------------------------------------------------

for folder in folders:
    path = project / folder
    path.mkdir(parents=True, exist_ok=True)

    # Git can't track empty folders
    (path / ".gitkeep").touch(exist_ok=True)

# --------------------------------------------------
# Create notebooks
# --------------------------------------------------

for filename, title in notebooks.items():

    nb = nbf.v4.new_notebook()

    markdown = f"""# {title}

## Objective

Write the objective of today's notebook.

---

## Business Question

What business question are we trying to answer today?

---

## Author

Santana Jepchumba

"""

    imports = """import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

"""

    nb.cells.append(nbf.v4.new_markdown_cell(markdown))
    nb.cells.append(nbf.v4.new_code_cell(imports))

    with open(project / "notebooks" / filename, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

# --------------------------------------------------
# Create Python files
# --------------------------------------------------

for file in python_files:
    path = project / "src" / file

    path.write_text(
f'''"""
{file}

Enterprise Retail Sales Intelligence Platform
"""

''',
        encoding="utf-8"
    )

# --------------------------------------------------
# README
# --------------------------------------------------

readme = """# Enterprise Retail Sales Intelligence Platform

## Project Overview

This project analyzes retail sales data to generate business insights,
forecast sales, and support data-driven decision making.

---

## Business Problem

Retail companies generate millions of transactions every day.

This project aims to answer questions such as:

- Which stores perform best?
- Which product families generate the most revenue?
- How do holidays affect sales?
- How can we forecast future sales?
- Which factors influence sales the most?

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Plotly
- SQL

---

## Project Structure

- Business Understanding
- Data Understanding
- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Machine Learning
- Model Evaluation
- Business Insights
- Dashboard

"""

(project / "README.md").write_text(readme, encoding="utf-8")

# --------------------------------------------------
# requirements.txt
# --------------------------------------------------

requirements = """numpy
pandas
matplotlib
seaborn
plotly
scikit-learn
jupyter
notebook
openpyxl
statsmodels
scipy
"""

(project / "requirements.txt").write_text(requirements, encoding="utf-8")

# --------------------------------------------------
# .gitignore
# --------------------------------------------------

gitignore = """__pycache__/
.ipynb_checkpoints/
*.pyc
*.pyo
*.pyd

.env
.venv
venv/

.DS_Store

models/*
!models/.gitkeep

data/processed/*
!data/processed/.gitkeep
"""

(project / ".gitignore").write_text(gitignore, encoding="utf-8")

print("=" * 60)
print(f"Project '{PROJECT_NAME}' created successfully!")
print("=" * 60)