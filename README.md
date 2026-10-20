# ExperimentLab — A/B Testing & Statistical Decision Support

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Open%20App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://experimentlab-ab-testing.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-181717?style=flat&logo=github&logoColor=white)](https://github.com/jaymwangi/experimentlab)

**Technologies used**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat&logo=scipy&logoColor=white)
![statsmodels](https://img.shields.io/badge/statsmodels-4051B5?style=flat)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)

ExperimentLab is a statistics-focused data science portfolio project that evaluates whether a new e-commerce landing page changes user conversion rates. It combines data validation, reproducible cleaning, hypothesis testing, confidence intervals, automated tests, and an interactive Streamlit dashboard.

## Business Problem

An e-commerce team is considering replacing its existing landing page with a new design. The objective is to determine whether the new page produces a measurable change in conversion rate before making a business decision.

**Research question:** Does the new landing page change the conversion rate compared with the existing page?

## Key Findings

The analysis uses assignment-consistent records and retains one record per user.

| Metric | Control | Treatment |
|---|---:|---:|
| Users | 145,274 | 145,310 |
| Conversions | 17,489 | 17,264 |
| Conversion rate | 12.04% | 11.88% |

- **Absolute difference:** −0.158 percentage points (treatment minus control).
- **Relative change:** −1.31%.
- **Two-sided p-value:** 0.1899.
- **95% confidence interval at α = 0.05:** approximately −0.394 to +0.078 percentage points.
- **Decision at α = 0.05:** Fail to reject the null hypothesis.

The treatment group had a slightly lower observed conversion rate, but the evidence is insufficient to conclude that the conversion rates differ statistically. This does not prove that the two pages are equivalent.

## Statistical Methodology

- **Primary metric:** Conversion rate, calculated as conversions divided by users.
- **Null hypothesis (H₀):** The control and treatment conversion rates are equal.
- **Alternative hypothesis (H₁):** The conversion rates differ.
- **Statistical test:** Two-sided, two-proportion z-test.
- **Uncertainty estimate:** Newcombe confidence interval for the difference between two independent proportions.
- **Significance level:** Configurable in the dashboard (0.01, 0.05, or 0.10).

Statistical significance is not the same as business significance. The size of the estimated effect, uncertainty, implementation costs, and business context should also inform the decision.

## Data and Quality Controls

The project uses the public e-commerce A/B testing dataset containing user IDs, timestamps, experimental groups, landing-page assignments, and conversion outcomes.

The pipeline:
1. Loads the raw CSV and validates required columns.
2. Normalizes text values and parses timestamps.
3. Checks missing values, allowed categories, and binary conversion outcomes.
4. Excludes records whose landing-page assignment does not match the experimental group.
5. Retains one assignment-consistent record per user, using the earliest timestamp when a user appears more than once.
6. Saves the processed dataset separately from the original data.

The source contains 294,478 rows. The cleaning process excludes 3,893 assignment-mismatched records and one additional repeated-user row, resulting in 290,584 unique users.

These exclusions are documented decisions, not proof that all data-quality or experimental-design problems have been eliminated.

## Project Structure

```text
experimentlab/
├── app.py
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── data_dictionary.md
│   └── experiment_plan.md
├── src/
│   ├── data_audit.py
│   ├── data_pipeline.py
│   ├── statistical_analysis.py
│   └── generate_report.py
├── tests/
│   ├── test_data_pipeline.py
│   └── test_statistical_analysis.py
├── requirements.txt
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd experimentlab
```

### 2. Create and activate a virtual environment

On Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare the dataset

Place the source CSV at `data/raw/ab_data.csv`, then run:

```bash
python -m src.data_pipeline
```

### 5. Run the statistical analysis

```bash
python -m src.statistical_analysis
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

### 7. Run the tests

```bash
python -m pytest -v
```

## Limitations

- The dataset is historical; results do not establish how a landing page would perform in a future experiment.
- The original randomization process and exact exposure history cannot be independently verified from the available fields.
- Filtering assignment mismatches and repeated users may introduce selection bias.
- The analysis relies on assumptions appropriate to comparing two proportions, including independent user-level observations.
- Statistical significance alone does not establish practical or commercial value.

## Technologies

Python, pandas, NumPy, SciPy, statsmodels, Matplotlib, Streamlit, and pytest.

## Data Source

Public dataset: [Analyze A/B Test Results — `ab_data.csv`](https://raw.githubusercontent.com/beery4010/Analyze-AB-Test-Results/master/ab_data.csv).

---

*ExperimentLab is an educational portfolio project demonstrating statistical reasoning, data-quality practices, reproducible analysis, and decision-focused communication.*
