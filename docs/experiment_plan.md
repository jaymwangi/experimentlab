# ExperimentLab: A/B Testing and Statistical Experimentation

## 1. Business Question

Does showing users a new website landing page improve the conversion
rate compared with the existing landing page?

## 2. Objective

Evaluate the difference in conversion rates between the control and
treatment groups using statistical inference.

The analysis will distinguish statistical significance from practical
business significance.

## 3. Dataset

- Source: Public E-commerce A/B Testing dataset.
- Raw file: `data/raw/ab_data.csv`
- Original records: 294,478
- Columns: user_id, timestamp, group, landing_page, converted
- Observed period: 2 January 2017 to 24 January 2017.

The raw dataset must remain unchanged.

## 4. Experimental Groups

- Control: Users assigned to the existing landing page.
- Treatment: Users assigned to the new landing page.

The group column represents recorded assignment, while landing_page
represents the page recorded for that observation.

## 5. Primary Metric

Conversion rate:

Conversion rate = Number of conversions / Number of users analyzed

The primary outcome is binary:
- 1: Converted
- 0: Did not convert

## 6. Statistical Hypotheses

Let p_control be the control-group conversion probability and
p_treatment be the treatment-group conversion probability.

Null hypothesis (H0):
p_treatment = p_control

Alternative hypothesis (H1):
p_treatment != p_control

This is a two-sided test.

## 7. Significance Level

Alpha = 0.05.

A p-value below 0.05 will be considered statistically significant,
subject to the assumptions and limitations of the analysis.

## 8. Statistical Analysis

The planned analysis includes:
- Conversion rates for both groups.
- Absolute difference in conversion rates.
- Relative change in conversion rate.
- A two-proportion statistical test.
- A 95% confidence interval for the difference.
- Practical interpretation of the effect size.

## 9. Data Quality and Cleaning

Initial audit findings:
- 294,478 original records.
- No missing values in the five columns.
- No fully duplicated rows.
- 3,894 excess occurrences of repeated user IDs.
- 3,893 records with inconsistent group and landing-page pairings.
- 290,585 records with consistent group/page pairings.
- One repeated user ID remains after filtering inconsistent assignments.

Planned handling:
1. Preserve the raw file unchanged.
2. Normalize whitespace in column names and string values.
3. Validate group, landing-page, and conversion values.
4. Investigate and document inconsistent assignments.
5. Investigate the remaining repeated user ID and define a
   deterministic, documented rule for the primary analysis.
6. Record row counts at every cleaning stage.
7. Assess the limitations introduced by exclusions.

Filtering inconsistent records may introduce selection bias if
the inconsistencies are systematic. The filtered dataset will
therefore not automatically be assumed unbiased.

## 10. Reproducibility

- Use a Python virtual environment.
- Track direct dependencies in requirements.txt.
- Separate raw data from processed data.
- Implement reusable data-cleaning functions.
- Add automated tests for data validation and statistical calculations.
- Document analysis decisions and results.

## 11. Deliverables

- Experiment plan and data dictionary.
- Reproducible data-cleaning pipeline.
- Statistical analysis and visualizations.
- Automated tests.
- Interactive Streamlit dashboard.
- Public deployment, subject to available hosting.
- Final report explaining findings, assumptions, and limitations.

## 12. Interpretation Principles

Statistical significance does not necessarily imply business value.
A non-significant result does not prove that the two conversion
rates are identical.

The final conclusion will consider effect size, uncertainty,
data quality, and the limitations of the available dataset.
