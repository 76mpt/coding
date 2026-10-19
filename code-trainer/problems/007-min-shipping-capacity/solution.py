def min_capacity(weights: list[int], days: int) -> int:
    """回傳能在 days 天內運完所有包裹的最小載重上限。"""
    # TODO
    pass
    left = max(weights)
    right = sum(weights)
    while left < right:
        cap = (left + right) // 2
        used = 1
        cur = 0
        for w in weights:
            if cur + w > cap:
                used += 1
                cur = 0
            cur += w
        if used <= days:
            right = cap
        else:
            left = cap + 1
    return left