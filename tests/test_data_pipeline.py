import pandas as pd
import pytest

from src.data_pipeline import normalize_data, prepare_data, validate_data


@pytest.fixture
def sample_data():
    """Small dataset containing valid rows and known data-quality issues."""
    return pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4, 4],
            "timestamp": [
                "2026-01-01 10:00:00",
                "2026-01-01 10:05:00",
                "2026-01-01 10:10:00",
                "2026-01-01 10:15:00",
                "2026-01-01 10:20:00",
            ],
            "group": [
                " control ",
                "treatment",
                "control",
                "treatment",
                "treatment",
            ],
            "landing_page": [
                " old_page ",
                "new_page",
                "new_page",
                "new_page",
                "new_page",
            ],
            "converted": [0, 1, 1, 0, 0],
        }
    )


def test_normalize_data_strips_whitespace_and_parses_timestamp(sample_data):
    result = normalize_data(sample_data)

    assert result.loc[0, "group"] == "control"
    assert result.loc[0, "landing_page"] == "old_page"
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_validate_data_rejects_invalid_conversion(sample_data):
    sample_data.loc[0, "converted"] = 2
    normalized = normalize_data(sample_data)

    with pytest.raises(ValueError, match="Conversion values must be 0 or 1"):
        validate_data(normalized)


def test_prepare_data_excludes_mismatches_and_repeated_users(sample_data):
    cleaned, summary = prepare_data(sample_data)

    assert len(cleaned) == 3
    assert cleaned["user_id"].is_unique
    assert set(cleaned["user_id"]) == {1, 2, 4}
    assert summary["mismatched_assignments_excluded"] == 1
    assert summary["repeated_user_rows_excluded"] == 1
    assert summary["output_rows"] == 3


def test_prepare_data_keeps_earliest_record_for_repeated_user(sample_data):
    cleaned, _ = prepare_data(sample_data)

    repeated_user = cleaned.loc[cleaned["user_id"] == 4]

    assert len(repeated_user) == 1
    assert repeated_user.iloc[0]["timestamp"] == pd.Timestamp(
        "2026-01-01 10:15:00"
    )


def test_load_raw_data_rejects_missing_required_column(tmp_path):
    from src.data_pipeline import load_raw_data

    csv_path = tmp_path / "incomplete.csv"
    pd.DataFrame(
        {
            "user_id": [1],
            "timestamp": ["2026-01-01 10:00:00"],
            "group": ["control"],
            "landing_page": ["old_page"],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_raw_data(csv_path)


def test_validate_data_rejects_missing_values(sample_data):
    sample_data.loc[0, "converted"] = float("nan")
    normalized = normalize_data(sample_data)

    with pytest.raises(ValueError, match="Missing values"):
        validate_data(normalized)
