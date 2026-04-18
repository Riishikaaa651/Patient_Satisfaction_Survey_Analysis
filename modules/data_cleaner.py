import pandas as pd
import numpy as np
import streamlit as st
from utils.logger import get_logger

logger = get_logger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fix types, handle nulls."""
    initial_rows = len(df)

    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace(r"[^\w_]", "", regex=True))

    # Detect and parse date columns
    for col in df.columns:
        if "date" in col or "time" in col:
            try:
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
            except Exception:
                pass

    # Convert rating columns to numeric
    rating_keywords = ["rating", "score", "satisfaction"]
    for col in df.columns:
        if any(kw in col for kw in rating_keywords):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill numeric nulls with median, categorical with mode
    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64]:
            df[col] = df[col].fillna(df[col].median())
        elif df[col].dtype == object:
            if df[col].isnull().sum() > 0:
                mode_val = df[col].mode()
                df[col] = df[col].fillna(mode_val[0] if len(mode_val) else "Unknown")

    # Clip rating columns to valid range
    for col in df.columns:
        if "rating" in col and df[col].dtype in [np.float64, np.int64]:
            df[col] = df[col].clip(1, 5)

    removed = initial_rows - len(df)
    st.info(f"🧹 Cleaning: removed {removed} duplicates, {initial_rows} → {len(df)} rows")
    logger.info("Cleaning complete: %d rows removed, %d remaining", removed, len(df))
    return df
