"""ExperimentLab: Statistical A/B testing dashboard."""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from src.statistical_analysis import analyze_experiment


st.set_page_config(
    page_title="ExperimentLab | A/B Testing",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = "data/processed/ab_data_clean.csv"

st.title("ExperimentLab")
st.subheader("A/B Testing & Statistical Decision Support")
st.write(
    "Evaluate whether a new landing page changes conversion rates "
    "using statistical evidence, uncertainty estimates, and "
    "practical interpretation."
)

with st.sidebar:
    st.header("Experiment settings")
    alpha = st.selectbox(
        "Significance level (α)",
        options=[0.01, 0.05, 0.10],
        index=1,
        help="The threshold used to assess statistical significance.",
    )

    st.divider()
    st.caption("Experiment design")
    st.write("**Control:** Existing landing page")
    st.write("**Treatment:** New landing page")
    st.write("**Test:** Two-sided, two-proportion z-test")

try:
    data = pd.read_csv(DATA_PATH)
    results = analyze_experiment(data, alpha=alpha)
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Unable to load or analyze the experiment data: {exc}")
    st.stop()

control_rate = results["control_rate"]
treatment_rate = results["treatment_rate"]
difference = results["absolute_difference"]
relative_change = results["relative_change"]
ci_lower, ci_upper = results["confidence_interval"]
p_value = results["p_value"]

st.divider()
st.header("Experiment results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Control conversion rate",
        f"{control_rate:.2%}",
        help="Conversions divided by users in the control group.",
    )
    st.caption(
        f"{results['control_conversions']:,} conversions / "
        f"{results['control_users']:,} users"
    )

with col2:
    st.metric(
        "Treatment conversion rate",
        f"{treatment_rate:.2%}",
        delta=f"{difference * 100:+.3f} percentage points",
        delta_color="normal",
        help="Difference is treatment minus control.",
    )
    st.caption(
        f"{results['treatment_conversions']:,} conversions / "
        f"{results['treatment_users']:,} users"
    )

with col3:
    st.metric("P-value", f"{p_value:.4f}")
    st.caption(f"Significance threshold: α = {alpha:.2f}")

st.divider()
st.header("Estimated treatment effect")

effect_col, interpretation_col = st.columns([1, 1])

with effect_col:
    st.metric(
        "Absolute difference",
        f"{difference * 100:+.3f} pp",
    )

    if relative_change is not None:
        st.metric(
            "Relative change",
            f"{relative_change:+.2%}",
        )

    confidence_level = (1 - alpha) * 100

    st.write(
        f"**{confidence_level:.0f}% confidence interval "
        "for the absolute difference**"
    )
    st.write(
        f"{ci_lower * 100:+.3f} to "
        f"{ci_upper * 100:+.3f} percentage points"
    )

    st.caption("Conversion rates by experiment group")

    chart_data = pd.DataFrame(
        {
            "Group": ["Control", "Treatment"],
            "Conversion rate": [control_rate, treatment_rate],
        }
    ).set_index("Group")

    st.bar_chart(chart_data)
    
    fig, ax = plt.subplots(figsize=(8, 2.5))

    ax.errorbar(
        x=difference * 100,
        y=0,
        xerr=[
            [difference * 100 - ci_lower * 100],
            [ci_upper * 100 - difference * 100],
        ],
        fmt="o",
        capsize=6,
    )

    ax.axvline(0, linestyle="--")
    ax.set_yticks([])
    ax.set_xlabel("Treatment effect (percentage points)")
    ax.set_title(
        f"Treatment effect with {(1 - alpha) * 100:.0f}% confidence interval"
    )
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    st.pyplot(fig)
    plt.close(fig)

with interpretation_col:
    st.subheader("Statistical conclusion")

    if results["statistically_significant"]:
        st.success(
            f"The result is statistically significant at α = {alpha:.2f}. "
            "Reject the null hypothesis of equal conversion rates."
        )
    else:
        st.info(
            f"The result is not statistically significant at α = {alpha:.2f}. "
            "Fail to reject the null hypothesis of equal conversion rates."
        )

    st.write(
        "The confidence interval estimates a range of plausible values "
        "for the treatment effect under the method's assumptions."
    )

    if ci_lower <= 0 <= ci_upper:
        st.write(
            f"The {confidence_level:.0f}% confidence interval includes "
            "zero, so no difference is compatible with the data "
            "at this confidence level."
        )
st.divider()
st.header("Methodology")

with st.expander("How the experiment is analyzed"):
    st.markdown(
        """
        **Primary metric:** Conversion rate = conversions / users.

        **Null hypothesis (H₀):** The control and treatment conversion
        rates are equal.

        **Alternative hypothesis (H₁):** The conversion rates differ.

        **Statistical test:** Two-sided, two-proportion z-test.

        **Confidence interval:** 95% Newcombe interval for the absolute
        difference between two independent proportions.

        **Decision rule:** Reject H₀ when the p-value is below the
        selected significance level.

        Statistical significance alone does not establish business
        importance or prove that the new page caused the observed effect.
        """
    )

with st.expander("Data quality and cleaning"):
    st.markdown(
        """
        The dashboard uses the processed dataset produced by the
        ExperimentLab cleaning pipeline.

        - Group and landing-page values are normalized.
        - Records with mismatched group/page assignments are excluded.
        - Repeated users are reduced to one record, retaining the earliest
          timestamp among assignment-consistent records.
        - The raw CSV remains unchanged.

        These cleaning decisions may introduce selection bias. The results
        should be interpreted alongside the dataset's experimental-design
        limitations.
        """
    )

st.caption(
    "ExperimentLab | Educational portfolio project | "
    "Statistical evidence supports decisions; it does not replace them."
)
