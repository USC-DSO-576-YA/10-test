"""Canonical wildfire records, filters, metrics, and chart aggregations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "outputs" / "fires_national.parquet"
MONTHLY_PATH = Path(__file__).resolve().parent / "outputs" / "monthly_wildfire.csv"
UNKNOWN_SOURCE = "Missing data/not specified/undetermined"
UNKNOWN_LABEL = "Unknown / not specified"
SIZE_CLASSES = {
    "A": "A · ≤0.25 ac",
    "B": "B · >0.25–<10 ac",
    "C": "C · 10–<100 ac",
    "D": "D · 100–<300 ac",
    "E": "E · 300–<1,000 ac",
    "F": "F · 1,000–<5,000 ac",
    "G": "G · ≥5,000 ac",
}
STATE_CODES = (
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS "
    "MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC"
).split()
STATE_NAMES = dict(zip(STATE_CODES, [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming", "District of Columbia",
]))


@dataclass(frozen=True)
class Metrics:
    fires: int
    acres: float | None
    median_size: float | None
    unknown_pct: float | None


def load_fires(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read only the dashboard fields and verify the record identifier."""
    columns = ["fod_id", "state", "fire_year", "discovery_date", "fire_size",
               "fire_size_class", "nwcg_general_cause"]
    fires = pd.read_parquet(path, columns=columns)
    if fires["fod_id"].isna().any() or fires["fod_id"].duplicated().any():
        raise ValueError("FOD_ID must identify one unique recorded fire per row")
    fires = fires.rename(columns={
        "fod_id": "fire_id", "fire_year": "year", "discovery_date": "discovery_date",
        "fire_size": "acres", "fire_size_class": "size_class",
        "nwcg_general_cause": "reported_cause",
    })
    fires["discovery_date"] = pd.to_datetime(fires["discovery_date"], errors="coerce")
    fires["year"] = pd.to_numeric(fires["year"], errors="coerce")
    fires["acres"] = pd.to_numeric(fires["acres"], errors="coerce")
    fires["state"] = fires["state"].astype("string").str.strip().str.upper()
    fires["month"] = fires["discovery_date"].dt.month
    fires["reported_cause"] = fires["reported_cause"].replace({UNKNOWN_SOURCE: UNKNOWN_LABEL}).fillna(UNKNOWN_LABEL)
    fires.loc[fires["reported_cause"].astype(str).str.strip().eq(""), "reported_cause"] = UNKNOWN_LABEL
    for field in ("state", "size_class", "reported_cause"):
        fires[field] = fires[field].astype("category")
    return fires


def filter_fires(fires: pd.DataFrame, years: tuple[int, int],
                 state: str | None = None, cause: str | None = None) -> pd.DataFrame:
    mask = fires["year"].between(*years)
    if state is not None:
        mask &= fires["state"].eq(state)
    if cause is not None:
        mask &= fires["reported_cause"].eq(cause)
    return fires.loc[mask]


def metrics(fires: pd.DataFrame) -> Metrics:
    count = int(fires["fire_id"].nunique())
    known = fires["acres"].dropna()
    return Metrics(
        fires=count,
        acres=float(known.sum()) if not known.empty else None,
        median_size=float(known.median()) if not known.empty else None,
        unknown_pct=float(fires["reported_cause"].eq(UNKNOWN_LABEL).sum() / count * 100) if count else None,
    )


def yearly(fires: pd.DataFrame, years: tuple[int, int]) -> pd.DataFrame:
    result = fires.groupby("year", observed=True).agg(
        fires=("fire_id", "nunique"), acres=("acres", "sum")
    )
    result = result.reindex(range(years[0], years[1] + 1), fill_value=0)
    result.index.name = "year"
    return result.reset_index()


def seasonality(fires: pd.DataFrame) -> pd.DataFrame:
    counts = fires.groupby("month", observed=True)["fire_id"].nunique().reindex(range(1, 13), fill_value=0)
    total = counts.sum()
    return pd.DataFrame({
        "month": range(1, 13), "fires": counts.to_numpy(),
        "percent": counts.to_numpy() / total * 100 if total else [0.0] * 12,
    })


def causes(fires: pd.DataFrame) -> pd.DataFrame:
    result = fires.groupby("reported_cause", observed=True).agg(
        fires=("fire_id", "nunique"), acres=("acres", "sum")
    ).sort_values("fires", ascending=False)
    return result.reset_index()


def cause_yearly(fires: pd.DataFrame) -> pd.DataFrame:
    counts = fires.groupby(["year", "reported_cause"], observed=True)["fire_id"].nunique().rename("fires").reset_index()
    counts["year_total"] = counts.groupby("year")["fires"].transform("sum")
    counts["percent"] = counts["fires"] / counts["year_total"] * 100
    return counts


def sizes(fires: pd.DataFrame) -> pd.DataFrame:
    frame = fires.copy()
    frame["size_class"] = frame["size_class"].astype(object).where(frame["size_class"].isin(SIZE_CLASSES), "Unknown")
    result = frame.groupby("size_class", observed=True).agg(
        fires=("fire_id", "nunique"), acres=("acres", "sum")
    ).reindex([*SIZE_CLASSES, "Unknown"], fill_value=0).reset_index()
    result["label"] = result["size_class"].map(SIZE_CLASSES).fillna("Unknown")
    return result


def state_comparison(fires: pd.DataFrame) -> pd.DataFrame:
    valid = fires.loc[fires["state"].isin(STATE_CODES)]
    result = valid.groupby("state", observed=True).agg(
        fires=("fire_id", "nunique"), acres=("acres", "sum"),
        median_size=("acres", "median"),
        unknown_count=("reported_cause", lambda s: s.eq(UNKNOWN_LABEL).sum()),
    ).reset_index()
    result["unknown_pct"] = result["unknown_count"] / result["fires"] * 100
    result["state_name"] = result["state"].map(STATE_NAMES)
    return result


def load_notebook_monthly(path: Path = MONTHLY_PATH) -> pd.DataFrame:
    monthly = pd.read_csv(path, parse_dates=["month"])
    required = {"month", "fires", "known_acres", "sizes_known", "previous", "change", "running", "average_3m"}
    missing = required.difference(monthly.columns)
    if missing:
        raise ValueError(f"Notebook monthly CSV is missing {', '.join(sorted(missing))}")
    return monthly
