"""Generate a reproducible JSON report for ExperimentLab."""

import json
from pathlib import Path

import pandas as pd

from src.statistical_analysis import analyze_experiment


DATA_PATH = Path("data/processed/ab_data_clean.csv")
REPORT_PATH = Path("reports/ab_test_results.json")


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    results = analyze_experiment(data)

    report = {
        "project": "ExperimentLab",
        "experiment": "New landing page vs existing landing page",
        "hypothesis": "Two-sided difference in conversion rates",
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2, allow_nan=False),
        encoding="utf-8",
    )

    print(f"Report saved to: {REPORT_PATH}")
    print(f"P-value: {results['p_value']:.6f}")
    print(
        "Statistically significant: "
        f"{results['statistically_significant']}"
    )


if __name__ == "__main__":
    main()
