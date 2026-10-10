def geometric(r: float, n: int) -> tuple:
    """回傳 (逐項累加, 閉式解, 無窮和或 None)。"""
    # TODO: 三個分別算。r == 1 時閉式解要特別處理；|r| >= 1 時無窮和是 None
    cur = 1
    ans = 0.0
    for _ in range(n):
        ans += cur
        cur *= r
    if r == 1:
        clo = n
    else:
        clo = (1 - r ** n) / (1 - r)
    return ans, clo, 1 / (1 - r) if abs(r) < 1 else None