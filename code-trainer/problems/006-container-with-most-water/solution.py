def max_area(heights: list[int]) -> int:
    """回傳兩線之間能盛的最大水量。"""
    # TODO: 先想清楚為什麼可以只掃一遍
    ma = 0
    i = 0
    j = len(heights) - 1
    while i < j:
        cur = (j - i) * min(heights[i], heights[j])
        if cur > ma:
            ma = cur
        if heights[j] > heights[i]:
            i += 1
        else:
            j -= 1
    return ma