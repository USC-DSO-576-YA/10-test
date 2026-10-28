def retained_fraction(january_customers, february_customers):
    return len(set(january_customers) & set(february_customers)) / len(january_customers)
