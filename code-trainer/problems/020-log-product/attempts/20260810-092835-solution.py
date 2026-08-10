import math


def log_product(values: list[float]) -> float:
    """回傳 log(所有元素的乘積)，用連加而不是連乘。"""
    # TODO
    result = 0.0
    for value in values:
        if value == 0:
            return float("-inf")
        result += math.log(value)
    return result
    pass
