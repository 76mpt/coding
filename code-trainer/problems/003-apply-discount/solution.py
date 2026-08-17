def apply_discount(prices, *, threshold=1000, rate=0.9):
    """回傳 (最終金額, 是否有打折)。"""
    total = 0
    for price in prices:
        total += price
    if total >= threshold:
        total = int(total * rate)
        return total, True
    return total, False
