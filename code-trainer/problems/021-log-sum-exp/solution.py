import math


def log_sum_exp(values: list[float]) -> float:
    """回傳 log(sum(exp(v) for v in values))，但不能真的算 exp(v)。"""
    # TODO
    pass
    if not values:
        return -math.inf
    m = max(values)
    if m == -math.inf:
        return -math.inf
    exp = m + math.log(sum(math.exp(v - m) for v in values))
    return exp