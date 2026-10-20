"""Statistical analysis for ExperimentLab A/B tests."""

from pathlib import Path

import pandas as pd
from statsmodels.stats.proportion import (
    confint_proportions_2indep,
    proportions_ztest,
)


def analyze_experiment(
    data: pd.DataFrame,
    alpha: float = 0.05,
) -> dict:
    """Compare treatment and control conversion rates."""

    required_columns = {"group", "converted"}
    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    if data.empty:
        raise ValueError("Cannot analyze an empty dataset.")

    if data["group"].isna().any() or data["converted"].isna().any():
        raise ValueError("Group and conversion values cannot be missing.")

    if not data["group"].isin(["control", "treatment"]).all():
        raise ValueError("Group must contain only control and treatment.")

    if not data["converted"].isin([0, 1]).all():
        raise ValueError("Conversion values must be 0 or 1.")

    if data["group"].nunique() != 2:
        raise ValueError("Both control and treatment groups are required.")

    control = data.loc[data["group"] == "control", "converted"]
    treatment = data.loc[data["group"] == "treatment", "converted"]

    control_users = len(control)
    treatment_users = len(treatment)

    if control_users == 0 or treatment_users == 0:
        raise ValueError("Both groups must contain at least one user.")

    control_conversions = int(control.sum())
    treatment_conversions = int(treatment.sum())

    control_rate = float(control.mean())
    treatment_rate = float(treatment.mean())

    absolute_difference = treatment_rate - control_rate
    relative_change = (
        absolute_difference / control_rate
        if control_rate > 0
        else None
    )

    z_statistic, p_value = proportions_ztest(
        count=[treatment_conversions, control_conversions],
        nobs=[treatment_users, control_users],
        alternative="two-sided",
    )

    ci_lower, ci_upper = confint_proportions_2indep(
        count1=treatment_conversions,
        nobs1=treatment_users,
        count2=control_conversions,
        nobs2=control_users,
        compare="diff",
        method="newcomb",
        alpha=alpha,
    )

    return {
        "alpha": alpha,
        "control_users": control_users,
        "control_conversions": control_conversions,
        "control_rate": control_rate,
        "treatment_users": treatment_users,
        "treatment_conversions": treatment_conversions,
        "treatment_rate": treatment_rate,
        "absolute_difference": absolute_difference,
        "relative_change": relative_change,
        "z_statistic": float(z_statistic),
        "p_value": float(p_value),
        "confidence_interval": (float(ci_lower), float(ci_upper)),
        "statistically_significant": bool(p_value < alpha),
    }


if __name__ == "__main__":
    data_path = Path("data/processed/ab_data_clean.csv")
    data = pd.read_csv(data_path)

    results = analyze_experiment(data)

    print("EXPERIMENTLAB — A/B TEST RESULTS")
    print("=" * 40)
    print(f"Significance level: {results['alpha']:.2f}")
    print(
        f"Control: {results['control_rate']:.4%} "
        f"({results['control_conversions']:,}/"
        f"{results['control_users']:,})"
    )
    print(
        f"Treatment: {results['treatment_rate']:.4%} "
        f"({results['treatment_conversions']:,}/"
        f"{results['treatment_users']:,})"
    )
    print(
        "Absolute difference: "
        f"{results['absolute_difference']:.4%}"
    )
    print(
        "Relative change: "
        f"{results['relative_change']:.2%}"
    )
    print(f"Z-statistic: {results['z_statistic']:.4f}")
    print(f"P-value: {results['p_value']:.6g}")
    print(
        "95% confidence interval: "
        f"[{results['confidence_interval'][0]:.4%}, "
        f"{results['confidence_interval'][1]:.4%}]"
    )
    print(
        "Statistically significant: "
        f"{results['statistically_significant']}"
    )
