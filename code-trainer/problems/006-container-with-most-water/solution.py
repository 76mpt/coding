def max_area(heights: list[int]) -> int:
    """回傳兩線之間能盛的最大水量。"""
    # TODO: 先想清楚為什麼可以只掃一遍
    max_vol = 0
    i, j = 0, len(heights) - 1
    while i < j:
        vol = (j - i) * min(heights[i], heights[j])
        max_vol = max(vol, max_vol)
        if heights[i] < heights[j]:
            i += 1
        else:
            j -= 1
    return max_vol
