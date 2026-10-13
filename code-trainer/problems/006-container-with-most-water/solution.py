def max_area(heights: list[int]) -> int:
    """回傳兩線之間能盛的最大水量。"""
    # TODO: 先想清楚為什麼可以只掃一遍
    pass
    j = len(heights) - 1
    i = 0
    cur = 0
    max = 0
    while j > i:
        cur = (j - i) * min(heights[i], heights[j])
        if cur > max:
            max = cur
        if heights[i] > heights[j]:
            j -= 1
        else:
            i += 1
    return max