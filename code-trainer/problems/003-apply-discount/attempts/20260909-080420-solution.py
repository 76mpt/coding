def apply_discount(prices, *, threshold=1000, rate=0.9):
    """回傳 (最終金額, 是否有打折)。"""
    total = sum(prices)
    if total >= threshold:
        return round(total * rate), True
    return total, False
