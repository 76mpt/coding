def search_bounds(nums, targets):
    """對每個 target 回傳 [lower_bound, upper_bound]。不要用 bisect 模組。"""
    # TODO
    n = len(nums)
    result = []
    for t in targets:
        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < t:
                left = mid + 1
            else:
                right = mid
        lower = left

        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if nums[mid] <= t:
                left = mid + 1
            else:
                right = mid
        upper = left

        result.append([lower, upper])
    return result
