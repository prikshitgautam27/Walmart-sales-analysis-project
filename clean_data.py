"""
Walmart Sales Data - Cleaning Script
-------------------------------------
Reads the raw Walmart.csv, cleans it, and writes a clean CSV
ready to be loaded into a database.

Run this from the project root:
    python scripts/clean_data.py
"""

import pandas as pd

RAW_PATH = "data/Walmart.csv"
CLEAN_PATH = "data/walmart_clean_data.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding_errors="ignore")
    print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names to lowercase for consistency across SQL engines
    df.columns = [c.strip().lower() for c in df.columns]

    # Drop exact duplicate rows
    before = len(df)
    df = df.drop_duplicates().copy()
    print(f"Dropped {before - len(df)} duplicate rows")

    # unit_price comes in as a string like "$74.69" - strip the $ and convert to float
    df["unit_price"] = (
        df["unit_price"].astype(str).str.replace("$", "", regex=False).astype(float)
    )

    # Drop rows where essential numeric fields are missing (unit_price, quantity)
    before = len(df)
    df = df.dropna(subset=["unit_price", "quantity"]).copy()
    print(f"Dropped {before - len(df)} rows with missing unit_price/quantity")

    # Ensure correct dtypes
    df["quantity"] = df["quantity"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["profit_margin"] = df["profit_margin"].astype(float)

    # Feature engineering: total sale amount per transaction
    df["total"] = (df["unit_price"] * df["quantity"]).round(2)

    # Feature engineering: profit per transaction
    df["profit"] = (df["total"] * df["profit_margin"]).round(2)

    return df


def main():
    df = load_data(RAW_PATH)
    df = clean_data(df)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned data to {CLEAN_PATH} -> {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.head())


if __name__ == "__main__":
    main()
