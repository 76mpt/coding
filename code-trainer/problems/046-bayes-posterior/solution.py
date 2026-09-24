def posterior(prior: float, sensitivity: float, specificity: float) -> float:
    """回傳 P(有病 | 陽性)。分母為 0 時 raise ValueError。"""
    # TODO: 分子 = 真陽性，分母 = 真陽性 + 偽陽性
    if (sensitivity * prior) + (1 - specificity) * (1 - prior) == 0:
        raise ValueError
    return (sensitivity * prior) / ((sensitivity * prior) + (1 - specificity) * (1 - prior))