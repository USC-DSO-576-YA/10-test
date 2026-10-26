def shipping_fee(post_discount_subtotal):
    return 0 if post_discount_subtotal > 50 else 5
