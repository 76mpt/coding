def gradient_descent_1d(df, x0: float, lr: float, steps: int) -> float:
    """從 x0 開始做 steps 次梯度下降，回傳最終的 x。"""
    x = x0
    for _ in range(steps):
        x = x - lr * df(x)
    return x
