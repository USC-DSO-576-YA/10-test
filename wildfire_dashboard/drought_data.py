"""Join complementary data at one row per calendar month."""
from pathlib import Path
import pandas as pd

OUTPUTS = Path(__file__).resolve().parent / "outputs"


def monthly_drought(weekly):
    """Mean of weekly map observations dated in each month (not a daily mean)."""
    frame = weekly.copy()
    frame["date"] = pd.to_datetime(frame["MapDate"].astype(str), format="%Y%m%d")
    if frame.duplicated(["StateAbbreviation", "date"]).any():
        raise ValueError("Expected one drought observation per state and map date")
    frame["month"] = frame["date"].dt.to_period("M").dt.to_timestamp()
    # Traditional D1 already includes D2–D4: never sum these columns.
    return frame.groupby(["StateAbbreviation", "month"], as_index=False).agg(
        drought_pct=("D1", "mean"), severe_pct=("D2", "mean"),
        observations=("D1", "count"),
    ).rename(columns={"StateAbbreviation": "state"})


def join_monthly(fires, drought, years, state="CA"):
    """Keep all selected months; missing drought remains missing."""
    months = pd.date_range(f"{years[0]}-01-01", f"{years[1]}-12-01", freq="MS")
    selected = fires.loc[fires["state"].eq(state)].copy()
    selected["month"] = selected["discovery_date"].dt.to_period("M").dt.to_timestamp()
    counts = selected.groupby("month")["fire_id"].nunique()
    result = pd.DataFrame({"month": months, "state": state})
    result["fires"] = result["month"].map(counts).fillna(0).astype(int)
    return result.merge(drought, on=["state", "month"], how="left", validate="one_to_one")


def load_drought():
    return monthly_drought(pd.read_csv(OUTPUTS / "drought_ca_weekly.csv"))
