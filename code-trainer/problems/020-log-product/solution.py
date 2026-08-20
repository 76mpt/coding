import math


def log_product(values: list[float]) -> float:
    """回傳 log(所有元素的乘積)，用連加而不是連乘。"""
    if any(value == 0.0 for value in values):
        return -math.inf
    return sum(math.log(value) for value in values)
