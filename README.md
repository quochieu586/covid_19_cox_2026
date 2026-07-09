# Globally modeling the duration of reaching the risk tipping point in the Covid-19 outbreaks

### Authors

<div style="text-align: center;">
P. T. Huong<sup>[1,2,<span style="font-family: FontAwesome;">&#xf0e0;</span>]</sup>,
T. Q. Hieu<sup>[1,2]</sup>,  
T. Q. Trung<sup>[1,2]</sup>,  
N. T. Dung<sup>[1,2]</sup>
</div>

---

<sup>1</sup> Ho Chi Minh City University of Technology, 268 Ly Thuong Kiet Street, District 10, Ho Chi Minh City, Vietnam  
<sup>2</sup> Vietnam National University Ho Chi Minh City, Linh Trung Ward, Thu Duc City, Ho Chi Minh City, Vietnam
<sup><span style="font-family: FontAwesome;">&#xf0e0;</span></sup> Corresponding authors (huongphan@hcmut.edu.vn)

---

## 1. Overview

This repository accompanies the manuscript **"Globally Modeling the Duration of Reaching the Risk Tipping Point in COVID-19 Outbreaks."** It contains:

- 📊 Processed datasets used in the study
- 🧹 Source code for data preprocessing and survival modeling
- 📒 Jupyter notebooks to reproduce the experimental results
- 🚨 An example implementation of the proposed early warning system

The repository reproduces the computational workflow presented in the manuscript, beginning with the curated OWID COVID-19 dataset containing missing values, followed by missing-value imputation, fitting the time-varying Cox survival model, and demonstrating its application as an early warning system.

---

## 2. Repository Structure

```text
covid-19-Cox-2026/
│
├── data/
│   ├── owid.csv
│   ├── time-dependent-variables-MissForest.csv
│   └── time-independent-variables-MissForest.csv
│
├── notebooks/
│   ├── missing_imputation.ipynb
│   ├── fitting_cox_model.ipynb
│   └── early_warning_system.ipynb
│
├── src/
│   ├── preprocess.py
│   ├── model.py
│   └── metric.py
│
└── README.md
```

### Folder Description

| Folder | Description |
|---------|-------------|
| **data/** | Original and processed datasets used throughout the study. |
| **notebooks/** | Jupyter notebooks reproducing the experiments and figures in the manuscript. |
| **src/** | Python implementation of preprocessing, modeling, and evaluation. |

---

## 3. Dataset

| File | Description |
|------|-------------|
| [`owid.csv`](data/owid.csv) | Raw OWID dataset after manual preprocessing (column selection, corrections from external sources, etc.). |
| [`time-dependent-variables-MissForest.csv`](data/time-dependent-variables-MissForest.csv) | Final time-dependent covariates after missing-value imputation. |
| [`time-independent-variables-MissForest.csv`](data/time-independent-variables-MissForest.csv) | Final time-independent (country-level) covariates after missing-value imputation. |

---

## 4. Workflow

```text
OWID Dataset
      │
      ▼
Manual Preprocessing
      │
      ▼
Missing Value Imputation
      │
      ▼
Processed Datasets
      │
      ▼
Time-varying Cox Model
      │
      ▼
Risk Prediction
      │
      ▼
Early Warning System
```

---

## 5. Notebooks

| Notebook | Description |
|----------|-------------|
| [`missing_imputation.ipynb`](notebooks/missing_imputation.ipynb) | Demonstrates the complete missing-value imputation pipeline from the raw OWID dataset to the final modeling datasets. |
| [`fitting_cox_model.ipynb`](notebooks/fitting_cox_model.ipynb) | Fits the proposed time-varying Cox model and reproduces the experimental results reported in the manuscript. |
| [`early_warning_system.ipynb`](notebooks/early_warning_system.ipynb) | Demonstrates the deployment of the proposed survival model as an early warning system. |

---

## 6. Source Code

| Module | Description |
|--------|-------------|
| [`preprocess.py`](src/preprocess.py) | Data preprocessing, feature engineering, and dataset preparation. |
| [`model.py`](src/model.py) | Implementation of the time-varying Cox survival model. |
| [`metric.py`](src/metric.py) | Evaluation metrics and utility functions. |

---

## 7. Reproducing the Results

1. Clone the repository.

   ```bash
   git clone https://github.com/<username>/covid-19-Cox-2026.git
   cd covid-19-Cox-2026
   ```

2. Install the required Python dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Execute the notebooks in the following order:

   1. `missing_imputation.ipynb`
   2. `fitting_cox_model.ipynb`
   3. `early_warning_system.ipynb`

---

## 8. Citation

If you find this repository useful in your research, please consider citing our manuscript.

```bibtex
@article{...}
```
