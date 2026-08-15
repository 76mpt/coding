def gradient_descent_1d(df, x0: float, lr: float, steps: int) -> float:
    """從 x0 開始做 steps 次梯度下降，回傳最終的 x。"""
    while steps > 0:
        x0 = x0 - lr * df(x0)
        steps -= 1
    return x0