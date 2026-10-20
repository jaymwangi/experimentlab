# Data Dictionary — ExperimentLab

## 1. Dataset Overview

| Property | Description |
|---|---|
| Dataset file | `data/raw/ab_data.csv` |
| Original records | 294,478 |
| Number of columns | 5 |
| Unit of observation | Recorded user-level experiment exposure |
| Primary outcome | Conversion (`converted`) |
| Format | CSV |

The dataset contains records from a website A/B test comparing an
existing landing page with a new landing page.

## 2. Column Definitions

### user_id

- **Meaning:** Identifier for a user in the experiment dataset.
- **Expected type:** Integer identifier.
- **Role:** Identifies users and supports duplicate-exposure checks.
- **Validation:** Must not be missing.
- **Important:** A user ID is an identifier, not a numeric measurement.
  Repeated IDs require investigation before analysis.

### timestamp

- **Meaning:** Recorded date and time associated with the observation.
- **Expected type:** Datetime.
- **Role:** Describes when the observation occurred.
- **Validation:** Must parse successfully as a datetime.
- **Important:** The timestamp alone does not establish the user's
  assignment time or prove when the page was first displayed.

### group

- **Meaning:** Recorded experimental group.
- **Expected values:** `control`, `treatment`.
- **Role:** Defines the comparison groups.
- **Validation:** Must be non-missing and contain an allowed value.
- **Important:** Group assignment should be checked against the
  recorded landing page.

### landing_page

- **Meaning:** Landing page recorded for the observation.
- **Expected values:** `old_page`, `new_page`.
- **Role:** Describes the website experience associated with the record.
- **Validation:** Must be non-missing and contain an allowed value.
- **Expected pairing:**
  - `control` with `old_page`
  - `treatment` with `new_page`
- **Important:** Unexpected pairings must be investigated and
  documented rather than silently corrected.

### converted

- **Meaning:** Whether the recorded observation resulted in a conversion.
- **Expected values:** `0`, `1`.
- **Role:** Primary binary outcome for statistical analysis.
- **Validation:** Must be non-missing and restricted to 0 or 1.
- **Interpretation:**
  - `0`: No recorded conversion.
  - `1`: A recorded conversion.

## 3. Initial Data Quality Findings

| Check | Initial result |
|---|---:|
| Total records | 294,478 |
| Missing values | 0 |
| Fully duplicated rows | 0 |
| Excess repeated user-ID occurrences | 3,894 |
| Inconsistent group/page pairings | 3,893 |
| Consistent group/page records | 290,585 |
| Excess repeated user-ID occurrences after pairing filter | 1 |

These figures are from the initial audit. They must be revalidated
by the reproducible cleaning pipeline.

## 4. Derived Variables

### conversion_rate

- **Definition:** Number of conversions divided by the number of
  analyzed users in a group.
- **Formula:** `conversions / users_analyzed`
- **Range:** 0 to 1.
- **Presentation:** Usually expressed as a percentage.

### absolute_conversion_difference

- **Definition:** Treatment conversion rate minus control conversion rate.
- **Formula:** `p_treatment - p_control`
- **Interpretation:** Positive values favor treatment; negative values
  favor control.

### relative_conversion_change

- **Definition:** Absolute conversion-rate difference divided by the
  control conversion rate.
- **Formula:** `(p_treatment - p_control) / p_control`
- **Interpretation:** Relative change compared with control.
- **Caution:** Undefined when the control conversion rate is zero.

## 5. Analysis and Cleaning Considerations

- Preserve the original raw CSV unchanged.
- Normalize whitespace before categorical validation.
- Parse timestamps explicitly before time-based analysis.
- Investigate repeated user IDs and inconsistent group/page pairings.
- Document every exclusion and the resulting sample size.
- Do not assume that removing inconsistent records eliminates bias.
- Treat each user's outcome as the analysis unit only after the
  repeated-user issue has been addressed.
- Keep derived metrics separate from raw source columns.

## 6. Limitations

The available columns do not establish every detail of the original
experiment's randomization, exposure logging, or conversion attribution.

Conclusions must therefore acknowledge uncertainty about the original
experiment's implementation and the effect of data exclusions.
