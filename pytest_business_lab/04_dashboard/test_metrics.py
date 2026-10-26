import pandas as pd
import pytest
from metrics import conversion_rate

def test_one_purchase():
    visitors = pd.DataFrame({"visitor_id": ["A", "B"]})
    orders = pd.DataFrame({"visitor_id": ["A"]})
    assert conversion_rate(visitors, orders) == pytest.approx(0.5)
