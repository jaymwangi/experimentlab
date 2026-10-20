from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/raw/ab_data.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    print("=" * 60)
    print("EXPERIMENTLAB — DATA AUDIT")
    print("=" * 60)

    print(f"\nDataset shape: {df.shape}")

    print("\nColumn data types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:", df.duplicated().sum())
    print("Duplicate user IDs:", df["user_id"].duplicated().sum())

    print("\nGroup counts:")
    print(df["group"].value_counts(dropna=False))

    print("\nLanding-page counts:")
    print(df["landing_page"].value_counts(dropna=False))

    print("\nGroup vs. landing page:")
    print(pd.crosstab(df["group"], df["landing_page"]))

    print("\nConversion outcomes:")
    print(df["converted"].value_counts(dropna=False))

    print("\nConversion summary by group:")
    print(
        df.groupby("group")["converted"]
        .agg(users="count", conversions="sum", conversion_rate="mean")
    )

    print("\nTimestamp range:")
    print(df["timestamp"].min(), "to", df["timestamp"].max())

    print("\nAudit complete.")

if __name__ == "__main__":
    main()
