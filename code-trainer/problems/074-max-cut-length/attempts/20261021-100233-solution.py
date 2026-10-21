def max_cut_length(lengths, k):
    """求能切出 k 段等長片段的最大片段長度。回傳 float。"""
    # TODO
    lo = 0.0
    hi = max(lengths)
    for _ in range(100):
        mid = (lo + hi) / 2
        count = 0
        for length in lengths:
            count += int(length / mid)
            if count >= k:
                break
        if count >= k:
            lo = mid
        else:
            hi = mid
    return lo
