def digital_root(n: int) -> tuple[int, int]:
    """回傳 (數位根, 相加的輪數)。"""
    steps = 0
    while n >= 10:
        cur = 0
        while n > 0:
            cur += n % 10
            n = n // 10
        n = cur
        steps += 1
    return n, steps