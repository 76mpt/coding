def min_capacity(weights: list[int], days: int) -> int:
    """回傳能在 days 天內運完所有包裹的最小載重上限。"""
    # TODO
    pass
    left = max(weights)
    right = sum(weights)

    while left < right:
        cap = (left + right) // 2
        used_day = 1
        current_load = 0

        for w in weights:
            if current_load + w > cap:
                used_day += 1
                current_load = 0
            current_load += w

        if used_day <= days:
            right = cap
        else:
            left = cap + 1
    return left