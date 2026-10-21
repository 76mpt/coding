def search_rotated(nums, targets):
    """回傳 (pivot, found)：旋轉點索引，以及每個 target 的索引（不存在為 -1）。"""
    # TODO
    n = len(nums)
    if n == 0:
        return -1, [-1] * len(targets)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    pivot = lo

    def lower_bound(target):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            idx = (mid + pivot) % n
            if nums[idx] < target:
                lo = mid + 1
            else:
                hi = mid
        
        if lo == n:
            return -1
        idx = (lo + pivot) % n
        if nums[idx] == target:
            return idx
        return -1
    found = [lower_bound(target) for target in targets]
    return pivot, found
