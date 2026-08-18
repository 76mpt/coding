def stats(*values, ndigits=2):
    """回傳 (平均, 最大, 最小)。沒有數值時 raise ValueError。"""
    if not values:
        raise ValueError
    return round(sum(values) / len(values), ndigits), max(values), min(values)
        
