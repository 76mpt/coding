import math

GAMMA = 0.5772156649015329


def series_facts(n: int) -> tuple:
    """回傳 (H_n, H_n - (ln n + γ), 砍半次數)。n = 0 時第二項是 None。"""
    # TODO: 三個分別算
    h_n = 0
    for i in range(n):
        h_n += (1 / (i + 1))
    dif = h_n - (math.log(n) + GAMMA) if n != 0 else None
    count = 0
    m = n
    while m > 1:
        m //= 2
        count += 1
    return h_n, dif, count

    