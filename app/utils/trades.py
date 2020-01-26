import decimal

def calculate_trade(shares, price, fee):
    cost = decimal.Decimal(shares*price)
    cost += fee
    return float(round(cost, 2))