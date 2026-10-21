import math


def log_product(values: list[float]) -> float:
    """回傳 log(所有元素的乘積)，用連加而不是連乘。"""
    if not values:
        return 0.0
    if 0 in values:
        return float(-math.inf)
    return sum(math.log(value) for value in values)
