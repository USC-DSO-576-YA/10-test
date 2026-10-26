from shipping import shipping_fee

def test_common_orders():
    assert shipping_fee(20) == 5
    assert shipping_fee(100) == 0
