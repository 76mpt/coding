def digital_root(n: int) -> tuple[int, int]:
    """回傳 (數位根, 相加的輪數)。"""
    res = 0
    count = 0
    while n >= 10:
        res = 0
        while n > 0:
            res += n % 10
            n = n // 10
        n = res
        count += 1
    return n, count