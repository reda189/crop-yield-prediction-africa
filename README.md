# 🌾 Predicting Crop Yield for Resilient Agri-Food Systems in Africa

An end-to-end data analytics and machine learning project that predicts crop yield across **53 African countries (2000–2022)** from environmental and agricultural data, including rainfall, temperature, fertilizer usage and cultivated land area.

> **Final model:** CatBoost, with a **test R² of 0.947**, a test MAE of 481.8 and a test RMSE of 742.1.

*Course project for CSC 4351 at Al Akhawayn University, by Ahmed Reda Benyaich and Amine Amar.*

---

## 📌 Research Question

> *To what extent can crop yield be predicted from rainfall, temperature, fertilizer usage, cultivated land area, time, and country context?*

The problem is formulated as a **supervised regression task**. The goal is to explain variation in crop yield and to predict it for unseen country-year observations, as a basis for a data-driven **decision-support tool** for agricultural planning.

---

## 🗂️ Repository Structure

```
├── cleaning codes/                 # Scripts that clean each raw source file
│   ├── AAA_clean_crop_yield.py
│   ├── AAA_clean_fertilizer.py
│   ├── AAA_clean_land_area.py
│   ├── AAA_clean_rainfall.py
│   └── AAA_clean_temperature.py
├── data/                           # Cleaned datasets (one per variable)
│   ├── M2C1_cleaned_crop_yield.csv
│   ├── M2C1_cleaned_fertilizer.csv
│   ├── M2C1_cleaned_land_area.csv
│   ├── M2C1_cleaned_rainfall.csv
│   └── M2C1_cleaned_temperature.csv
├── ProjectCodes.ipynb              # Main notebook: EDA, statistics, modeling, evaluation
├── FinalReportAhmedRedaBenyaich.pdf
└── Predicting Crop Yield for Resilient Agri-Food Systems ... .pdf   # Presentation
```

---

## 📊 Data

| Variable | Description | Source |
|---|---|---|
| `Crop_Yield` | Crop yield, the **target variable** | FAOSTAT |
| `Rainfall` | Average annual precipitation (mm) | World Bank |
| `Temperature` | Average annual temperature (°C) | World Bank |
| `Fertilizer_Usage` | Fertilizer consumption per area (kg/ha) | World Bank |
| `Land_Area` | Agricultural land area | World Bank |
| `Country`, `Year` | Contextual identifiers | — |

- Each raw CSV is cleaned by its own script: column selection, renaming, filtering to African countries and standardization.
- The cleaned files are merged on **Country + Year** into a final dataset of **1,172 observations × 7 variables** with **no missing values**.
- The data is public, aggregated at national level and contains no personal information.

---

## 🔬 Methodology

### 1. Exploratory Data Analysis
- Computed summary statistics and a missing-value analysis, and plotted the distributions and outliers (boxplots, raw and log-scale).
- **Crop yield is right-skewed.** Fertilizer usage and land area are also strongly skewed, so both were log-transformed with `log(1+x)`.
- **Average yield rose over time,** from about 6,500 in 2000 to about 7,800 in 2022.
- **Yield differs strongly from one country to another,** so `Country` was kept as a predictor.
- **Fertilizer usage has the strongest correlation with yield** (r = 0.50).

### 2. Statistical Foundations
- **Sampling comparison** (n ≈ 30% of the data): random, stratified (by country) and cluster sampling. **Stratified sampling gave the most stable estimates.**
- **Hypothesis test:** a one-sample t-test compared the sample mean with the population mean (t = −0.65, p = 0.51). The difference is not significant, so the sample is representative.
- **Power analysis:** the test cannot detect a mean shift of 2 units, because crop yield varies too much (power = 0.05).
- **Bootstrapping:** 10,000 resamples. The bootstrap 95% CI [6658.9, 7336.7] closely matches the analytical CI [6648.5, 7336.0].

### 3. Predictive Modeling
- 80/20 train/test split (937 / 235 rows) with a fixed seed, plus K-fold cross-validation.
- One-hot encoding of `Country`, and log transforms of the skewed predictors.
- Benchmarked **5 models:** Multiple Linear Regression (OLS with HC3 robust errors), Random Forest, LightGBM, XGBoost and CatBoost.

---

## 🏆 Results

**Cross-validation comparison** (used for model selection):

| Model | CV R² (mean ± std) | CV MAE | CV RMSE |
|---|---|---|---|
| **CatBoost** | **0.937 ± 0.027** | 503.7 | **806.2** |
| XGBoost | 0.934 ± 0.034 | 472.5 | 814.9 |
| LightGBM | 0.931 ± 0.049 | 436.1 | 820.8 |
| Random Forest | 0.921 ± 0.060 | 349.7 | 859.2 |
| Linear Regression | 0.900 ± 0.032 | 598.8 | 1022.0 |

**CatBoost was selected:** it had the highest CV R², the lowest CV RMSE and the most stable results across folds.

**Final CatBoost performance:**

| | R² | MAE | RMSE |
|---|---|---|---|
| Train | 0.975 | 378.8 | 519.7 |
| **Test** | **0.947** | **481.8** | **742.1** |

The gap between train and test scores is small, so the model is not severely overfitting.

### What drives the predictions? (permutation importance)

| Feature | Mean R² decrease | 95% CI |
|---|---|---|
| Rainfall | 0.547 | [0.457, 0.636] |
| log(Fertilizer_Usage) | 0.325 | [0.252, 0.397] |
| Country | 0.182 | [0.159, 0.206] |
| log(Land_Area) | 0.130 | [0.105, 0.156] |
| Year | 0.112 | [0.024, 0.199] |
| Temperature | 0.076 | [0.059, 0.093] |

All confidence intervals are above zero, so every predictor contributes useful information. These are **predictive** effects, not causal ones.

### Error analysis
- Most residuals fall between −1,000 and +1,000 and are centered on zero.
- The largest errors occur on unusual country-years. The worst is **Botswana 2015**, underpredicted by about 6,700. The cause is probably local factors that are not in the data (irrigation, soil, crop type, climate shocks).

---

## ⚠️ Limitations

- **The data is aggregated at national level,** which hides regional and farm-level variation.
- **Important variables are missing,** such as irrigation, soil quality, crop type and drought events.
- **Validation is not time-aware,** and the models give point predictions only, without prediction intervals.
- **The results are predictive, not causal.**

## 🚀 Future Work

- Time-aware validation (train on earlier years, test on later years) and leave-one-country-out validation.
- Prediction intervals using conformal prediction or quantile regression.
- New features: rainfall anomalies, lagged variables, interaction terms and climate-zone groupings.
- Hyperparameter tuning and stacked ensembles (CatBoost + XGBoost + LightGBM).
- A **Streamlit dashboard** and an early-warning system for low-yield risk.

---

## ▶️ How to Run

```bash
git clone https://github.com/reda189/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
jupyter notebook ProjectCodes.ipynb
```

> **Note:** the notebook reads the cleaned datasets from the `data/` folder, so run it from the repository root.

---

## 🛠️ Tech Stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `CatBoost` · `XGBoost` · `LightGBM` · `statsmodels` · `SciPy` · `Matplotlib` · `Seaborn` · `Jupyter`

## 👤 Authors

- **Ahmed Reda Benyaich**: [LinkedIn](https://www.linkedin.com/in/reda-benyaich-3583ba32a/) · [GitHub](https://github.com/reda189)
- **Amine Amar**

*Data sources: [FAOSTAT](https://www.fao.org/faostat/) and [World Bank Open Data](https://data.worldbank.org/).*
