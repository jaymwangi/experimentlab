"""Data validation and cleaning pipeline for ExperimentLab."""

from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = {
    "user_id",
    "timestamp",
    "group",
    "landing_page",
    "converted",
}

EXPECTED_PAGE = {
    "control": "old_page",
    "treatment": "new_page",
}


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Load raw CSV data and normalize column names."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize string values and parse timestamps."""
    df = df.copy()

    for column in ["group", "landing_page"]:
        df[column] = df[column].astype("string").str.strip()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

    return df


def validate_data(df: pd.DataFrame) -> None:
    """Validate essential values before cleaning."""
    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Missing values found in required columns.")

    if not df["group"].isin(EXPECTED_PAGE).all():
        raise ValueError("Unexpected experimental group.")

    if not df["landing_page"].isin(
        EXPECTED_PAGE.values()
    ).all():
        raise ValueError("Unexpected landing-page value.")

    if not df["converted"].isin([0, 1]).all():
        raise ValueError("Conversion values must be 0 or 1.")


def prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Prepare assignment-consistent, one-row-per-user data.

    Excludes group/page mismatches. For the remaining repeated user,
    retains the earliest timestamp deterministically.

    Returns the processed dataframe and an audit summary.
    """
    df = normalize_data(df)
    validate_data(df)

    summary: dict[str, Any] = {
        "input_rows": len(df),
        "input_unique_users": int(df["user_id"].nunique()),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    expected_pages = df["group"].map(EXPECTED_PAGE)
    valid_assignment = df["landing_page"].eq(expected_pages)

    summary["mismatched_assignments_excluded"] = int(
        (~valid_assignment).sum()
    )

    df = df.loc[valid_assignment].copy()

    # Retain the earliest record for each user, using a stable sort.
    df = df.sort_values(
        ["timestamp", "user_id"], kind="mergesort"
    )
    duplicate_mask = df.duplicated("user_id", keep="first")

    summary["repeated_user_rows_excluded"] = int(
        duplicate_mask.sum()
    )

    df = df.loc[~duplicate_mask].copy()

    summary["output_rows"] = len(df)
    summary["output_unique_users"] = int(df["user_id"].nunique())

    if df["user_id"].duplicated().any():
        raise AssertionError("Processed data contains repeated user IDs.")

    conversion_summary = (
        df.groupby("group")["converted"]
        .agg(
            users="size",
            conversions="sum",
            conversion_rate="mean",
        )
    )

    summary["conversion_summary"] = {
        group: {
            "users": int(row["users"]),
            "conversions": int(row["conversions"]),
            "conversion_rate": float(row["conversion_rate"]),
        }
        for group, row in conversion_summary.iterrows()
    }

    return df.reset_index(drop=True), summary


def run_pipeline(
    input_path: str | Path,
    output_path: str | Path,
) -> dict:
    """Run the pipeline and save the processed dataset."""
    raw = load_raw_data(input_path)
    processed, summary = prepare_data(raw)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(output_path, index=False)

    summary["output_path"] = str(output_path)
    return summary


if __name__ == "__main__":
    results = run_pipeline(
        "data/raw/ab_data.csv",
        "data/processed/ab_data_clean.csv",
    )

    print("EXPERIMENTLAB — CLEANING REPORT")
    print("=" * 45)

    for key, value in results.items():
        print(f"{key}: {value}")
