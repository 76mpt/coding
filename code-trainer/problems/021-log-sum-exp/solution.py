import math


def log_sum_exp(values: list[float]) -> float:
    """回傳 log(sum(exp(v) for v in values))，但不能真的算 exp(v)。"""
    if not values:
        return -math.inf
    m = max(values)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(value - m) for value in values)) 
