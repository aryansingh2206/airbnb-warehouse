import pandas as pd
from pathlib import Path
import numpy as np

RAW = Path("data/raw/listings.csv")
OUT = Path("data/staged/listings_clean.parquet")

def parse_price(x):
    if pd.isna(x):
        return np.nan
    return float(str(x).replace("$","").replace(",","").strip())

def clean():
    df = pd.read_csv(RAW, low_memory=False)

    # Price
    if "price" in df.columns:
        df["price"] = df["price"].apply(parse_price)

    # last_review → date
    if "last_review" in df.columns:
        df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    # Numeric columns
    num_cols = [
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "availability_365",
        "number_of_reviews_ltm",
        "calculated_host_listings_count"
    ]

    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    df.to_parquet(OUT, index=False)
    print(f"Cleaned → {OUT}")

if __name__ == "__main__":
    clean()
