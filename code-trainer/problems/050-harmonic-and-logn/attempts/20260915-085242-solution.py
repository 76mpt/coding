import math

GAMMA = 0.5772156649015329


def series_facts(n: int) -> tuple:
    """回傳 (H_n, H_n - (ln n + γ), 砍半次數)。n = 0 時第二項是 None。"""
    # TODO: 三個分別算
    H_n = 0
    for i in range(n):
        H_n += 1 / (i + 1)
    if n == 0:
        dif = None
    else:
        dif = H_n - (math.log(n) + GAMMA)
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return H_n, dif, count
    