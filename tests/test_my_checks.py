"""Add the tests you write in class below these imports."""
import pandas as pd
import pytest

from sample_data import small_fires, threshold_counts, winter_counts
from wildfire import (
    first_threshold, month_changes, monthly_summary,
    select_year, selected_year_report,
)
