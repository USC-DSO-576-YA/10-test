import pandas as pd
import pytest
from wildfire_dashboard.drought_data import monthly_drought, join_monthly


def weekly():
    return pd.DataFrame({"StateAbbreviation": ["CA", "CA", "NV"], "MapDate": [20000104, 20000111, 20000104], "D1": [20., 40., 90.], "D2": [5., 15., 80.]})


def fires():
    return pd.DataFrame({"state": ["CA", "CA", "NV"], "fire_id": [1, 2, 3], "discovery_date": pd.to_datetime(["2000-01-05", "2000-01-12", "2000-01-05"])})


def test_monthly_average_does_not_add_overlapping_categories():
    row = monthly_drought(weekly()).query("state == 'CA'").iloc[0]
    assert row.drought_pct == 30
    assert row.severe_pct == 10
    assert row.observations == 2


def test_join_does_not_multiply_fire_counts_or_mix_states():
    result = join_monthly(fires(), monthly_drought(weekly()), (2000, 2000))
    assert len(result) == 12
    assert result.fires.sum() == 2
    assert result.iloc[0].drought_pct == 30
    assert result.iloc[1].fires == 0
    assert pd.isna(result.iloc[1].drought_pct)


def test_unavailable_drought_is_not_zero():
    result = join_monthly(fires(), monthly_drought(weekly()), (1999, 1999))
    assert result.drought_pct.isna().all()


def test_duplicate_monthly_keys_are_rejected():
    drought = monthly_drought(weekly())
    with pytest.raises(pd.errors.MergeError):
        join_monthly(fires(), pd.concat([drought, drought]), (2000, 2000))


def test_duplicate_weekly_observations_are_rejected():
    with pytest.raises(ValueError, match="one drought observation"):
        monthly_drought(pd.concat([weekly(), weekly()]))
