import math


def entropy(probs: list[float], base: float = 2) -> float:
    """回傳 -sum(p * log_base(p))，p=0 的項當作 0。"""
    return -sum(p * math.log(p, base) for p in probs if p != 0)
