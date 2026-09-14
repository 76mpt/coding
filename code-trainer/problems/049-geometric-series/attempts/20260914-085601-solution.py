def geometric(r: float, n: int) -> tuple:
    """回傳 (逐項累加, 閉式解, 無窮和或 None)。"""
    # TODO: 三個分別算。r == 1 時閉式解要特別處理；|r| >= 1 時無窮和是 None
    result = 0
    cur = 1
    for _ in range(n):
        result += cur
        cur *= r
    if r != 1:
        set_n = (1 - cur) / (1 - r)
    else:
        set_n = n
    if abs(r) >= 1:
        closed = None
    else:
        closed = 1 / (1 - r)
    return result, set_n, closed