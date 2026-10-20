import pandas as pd
import pytest

from src.statistical_analysis import analyze_experiment


@pytest.fixture
def experiment_data():
    return pd.DataFrame(
        {
            "group": (
                ["control"] * 100
                + ["treatment"] * 100
            ),
            "converted": (
                [1] * 10 + [0] * 90
                + [1] * 15 + [0] * 85
            ),
        }
    )


def test_analysis_calculates_group_conversion_rates(experiment_data):
    results = analyze_experiment(experiment_data)

    assert results["control_users"] == 100
    assert results["control_conversions"] == 10
    assert results["control_rate"] == pytest.approx(0.10)

    assert results["treatment_users"] == 100
    assert results["treatment_conversions"] == 15
    assert results["treatment_rate"] == pytest.approx(0.15)


def test_analysis_calculates_effect_in_correct_direction(experiment_data):
    results = analyze_experiment(experiment_data)

    assert results["absolute_difference"] == pytest.approx(0.05)
    assert results["relative_change"] == pytest.approx(0.50)


def test_analysis_returns_valid_inference_results(experiment_data):
    results = analyze_experiment(experiment_data)

    lower, upper = results["confidence_interval"]

    assert 0 <= results["p_value"] <= 1
    assert lower < upper
    assert lower <= results["absolute_difference"] <= upper
    assert results["statistically_significant"] == (
        results["p_value"] < results["alpha"]
    )


def test_analysis_rejects_invalid_alpha(experiment_data):
    with pytest.raises(ValueError, match="alpha"):
        analyze_experiment(experiment_data, alpha=1.0)


def test_analysis_requires_both_groups():
    data = pd.DataFrame(
        {"group": ["control"], "converted": [1]}
    )

    with pytest.raises(ValueError, match="Both control and treatment"):
        analyze_experiment(data)
