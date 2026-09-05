def geometric(r: float, n: int) -> tuple:
    """回傳 (逐項累加, 閉式解, 無窮和或 None)。"""
    # TODO: 三個分別算。r == 1 時閉式解要特別處理；|r| >= 1 時無窮和是 None
    if n == 0:
        return 0.0, 0.0, 2.0
    res = 1
    result = 0
    for _ in range(n):
        result += res
        res *= r
    set_n = (1 - r ** n) / (1 - r) if r != 1 else float(n)
    set_inf = 1 / (1 - r) if abs(r) < 1 else None
    return result, set_n, set_inf