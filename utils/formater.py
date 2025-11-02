

def formatter(total_S: int, amount: int, total: int):
    total_F = format(total, ",").replace(",", ".")
    total_SF = format(total_S, ",").replace(",", ".")
    amount_F = format(amount, ",").replace(",", ".")
    return total_F, total_SF, amount_F