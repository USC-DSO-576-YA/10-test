import pytest
from promotion import net_price

def test_no_discount():
    assert net_price(100, 0) == pytest.approx(100)
