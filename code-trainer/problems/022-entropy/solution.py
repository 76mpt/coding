import math


def entropy(probs: list[float], base: float = 2) -> float:
    """回傳 -sum(p * log_base(p))，p=0 的項當作 0。"""
    return -sum(prob * math.log(prob, base)for prob in probs if prob != 0)
