"""Practice implementations. Some functions are deliberately incorrect.

Contracts are in contracts.md. These are authored teaching examples, not
captured AI responses. No files are read or written by these functions.
"""
import pandas as pd


def first_threshold(counts, target=5):
    out = counts.copy()
    out["running"] = out.groupby("county")["fires"].cumsum()
    out["hit"] = out["running"] > target
    out["reached"] = out["hit"] & (
        out.groupby("county")["hit"].cumsum() == 1
    )
    return out


def month_changes(counts):
    out = counts.sort_values("month").reset_index(drop=True).copy()
    out["previous"] = out["fires"].shift()
    out["change"] = out["fires"].diff()
    out["average_3m"] = out["fires"].rolling(3, min_periods=1).mean()
    out["running"] = out["fires"].cumsum()
    return out


def selected_year_report(counts, year):
    shown = counts.loc[counts["month"].dt.year == year]
    return month_changes(shown)


def select_year(monthly, year):
    monthly.drop(monthly.index[monthly["month"].dt.year != year], inplace=True)
    return monthly.copy()


def monthly_summary(fires):
    dated = fires.dropna(subset=["DISCOVERY_DATE"]).copy()
    dated["month"] = dated["DISCOVERY_DATE"].dt.to_period("M").dt.to_timestamp()
    return dated.groupby("month", as_index=False).agg(
        fires=("DISCOVERY_DATE", "size"),
        known_acres=("FIRE_SIZE", "sum"),
        sizes_known=("FIRE_SIZE", "count"),
    )
