"""Decorator examples using small, made-up inputs and the real dashboard code.

Run from the repository folder:
    uv run python -m pytest tests/test_wildfire_parametrize.py -v --tb=short

A decorator is the @ line above a function. Here, parametrize asks pytest to
run the same test once for each row of inputs. The ids label those runs.
"""
import pandas as pd
import pytest

from wildfire_dashboard.wildfire_data import filter_fires, metrics, seasonality


# Each tuple supplies acres, expected_count, and expected_acres, in that order.
# Missing size does not erase a fire. An entirely unknown size total stays missing.
@pytest.mark.parametrize(
    "acres, expected_count, expected_acres",
    [
        ([2, 4], 2, 6),
        ([2, None, 4], 3, 6),
        ([None, None], 2, None),
        ([0, None], 2, 0),
    ],
    ids=["known-sizes", "one-missing-size", "all-sizes-missing", "recorded-zero"],
)
def test_fire_count_and_known_acres(acres, expected_count, expected_acres):
    fires = pd.DataFrame({
        "fire_id": range(len(acres)),  # One distinct ID per recorded fire.
        "acres": acres,
        "reported_cause": ["Natural"] * len(acres),
    })
    result = metrics(fires)

    assert result.fires == expected_count
    if expected_acres is None:
        # Do not compare NaN with ==. isna accepts None and pandas missing values.
        assert pd.isna(result.acres)
    else:
        # approx allows tiny floating-point differences, not a wrong total.
        assert result.acres == pytest.approx(expected_acres)


# Assume these records cover all 12 months: no event records means zero events.
# This is NOT a rule for months whose source data was never collected.
@pytest.mark.parametrize(
    "months, month_to_check, expected_count, expected_percent",
    [
        ([1, 1, 3], 1, 2, 200 / 3),
        ([1, 1, 3], 2, 0, 0),
        ([12, 12], 12, 2, 100),
    ],
    ids=["january-share", "february-no-records", "december-only"],
)
def test_monthly_counts_and_shares(months, month_to_check, expected_count, expected_percent):
    fires = pd.DataFrame({"fire_id": range(len(months)), "month": months})
    result = seasonality(fires)

    assert result["month"].tolist() == list(range(1, 13))
    # Select the month named in this parameter row, then retrieve its one row.
    row = result.loc[result["month"] == month_to_check].iloc[0]
    assert row["fires"] == expected_count
    assert row["percent"] == pytest.approx(expected_percent)
    assert result["percent"].sum() == pytest.approx(100)


# A dashboard year range includes BOTH endpoints. State selection must also work.
@pytest.mark.parametrize(
    "years, state, expected_ids",
    [
        ((2020, 2021), "CA", ["B", "C"]),
        ((2021, 2021), "CA", ["C"]),
        ((2020, 2021), "NV", ["D"]),
    ],
    ids=["both-year-boundaries", "single-year", "different-state"],
)
def test_year_and_state_filters(years, state, expected_ids):
    fires = pd.DataFrame({
        "fire_id": ["A", "B", "C", "D", "E"],
        "year": [2019, 2020, 2021, 2021, 2022],
        "state": ["CA", "CA", "CA", "NV", "CA"],
    })
    result = filter_fires(fires, years, state=state)

    # Checking the actual IDs catches selecting the wrong fires with the right count.
    assert result["fire_id"].tolist() == expected_ids
