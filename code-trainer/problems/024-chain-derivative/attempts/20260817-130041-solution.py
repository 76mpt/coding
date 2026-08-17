def chain_derivative(layers, x: float) -> tuple[float, float]:
    """layers = [(f1, df1), (f2, df2), ...] 代表 f1(f2(...fn(x)))。

    回傳 (合成函數的值, 導數)。
    """
    values = [x]
    for f, _ in reversed(layers):
        values.append(f(values[-1]))
    grad = 1.0
    for i, (f, df) in enumerate(reversed(layers)):
        grad *= df(values[i])
    
    return values[-1], grad
