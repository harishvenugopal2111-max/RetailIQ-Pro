import pandas as pd

def load_data():
    df = pd.read_csv("data/clean_superstore.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Safe date conversion
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

    # Remove invalid dates
    if "Order Date" in df.columns:
        df = df.dropna(subset=["Order Date"])

    return df