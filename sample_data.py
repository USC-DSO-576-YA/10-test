"""Small fixed tables for Module 10; each call returns a fresh table."""
import pandas as pd


def threshold_counts():
    return pd.DataFrame({
        "county": ["A", "A", "A"],
        "month": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"]),
        "fires": [2, 3, 1],
    })


def winter_counts():
    return pd.DataFrame({
        "month": pd.to_datetime([
            "2004-11-01", "2004-12-01", "2005-01-01", "2005-02-01"
        ]),
        "fires": [96, 75, 71, 97],
    })


def small_fires():
    return pd.DataFrame({
        "DISCOVERY_DATE": pd.to_datetime([
            "2025-01-05", "2025-01-17", "2025-03-02"
        ]),
        "FIRE_SIZE": [2.0, 3.0, 4.0],
    })
