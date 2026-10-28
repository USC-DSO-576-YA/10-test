def net_price(eligible_subtotal, discount_rate):
    discounted = eligible_subtotal * (1 - discount_rate)
    return discounted * (1 - discount_rate)
