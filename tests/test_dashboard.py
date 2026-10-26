"""Small tests of the actual Wildfire Atlas backend, separate from wildfire.py."""
import pandas as pd
import pytest

from wildfire_dashboard.wildfire_data import UNKNOWN_LABEL, metrics, seasonality


def test_missing_size_still_counts_as_a_fire():
    fires = pd.DataFrame({
        "fire_id": ["A", "B", "C"],
        "acres": [2.0, None, 4.0],
        "reported_cause": ["Natural", UNKNOWN_LABEL, "Human"],
    })
    result = metrics(fires)
    assert result.fires == 3
    assert result.acres == pytest.approx(6)
    assert result.median_size == pytest.approx(3)
    assert result.unknown_pct == pytest.approx(100 / 3)


def test_seasonality_keeps_months_without_records():
    fires = pd.DataFrame({
        "fire_id": ["A", "B", "C"],
        "month": [1, 1, 3],
    })
    result = seasonality(fires)
    assert result["month"].tolist() == list(range(1, 13))
    assert result["fires"].tolist() == [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert result.loc[result["month"] == 1, "percent"].iloc[0] == pytest.approx(200 / 3)
    assert result["percent"].sum() == pytest.approx(100)
