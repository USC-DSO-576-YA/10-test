def conversion_rate(visitors, orders):
    return len(orders) / visitors["visitor_id"].nunique()
