import pytest
from retention import retained_fraction

def test_no_one_returns():
    assert retained_fraction(["A", "B"], ["C"]) == pytest.approx(0)
