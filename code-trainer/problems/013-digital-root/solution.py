def digital_root(n: int) -> tuple[int, int]:
    """回傳 (數位根, 相加的輪數)。"""
    # TODO
    step = 0
    while n >= 10:
        result = 0
        while n > 0:
            result += n % 10
            n //= 10
        n = result
        step += 1
    return n, step
