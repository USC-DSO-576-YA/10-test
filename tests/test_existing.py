from sample_data import small_fires, threshold_counts, winter_counts
from wildfire import first_threshold, monthly_summary, selected_year_report


def test_threshold_above_target():
    result = first_threshold(threshold_counts(), target=4)
    assert result["reached"].tolist() == [False, True, False]


def test_selected_year_totals():
    result = selected_year_report(winter_counts(), 2005)
    assert len(result) == 2
    assert result["fires"].sum() == 168


def test_summary_totals():
    result = monthly_summary(small_fires())
    assert result["fires"].sum() == 3
    assert result["known_acres"].sum() == 9
