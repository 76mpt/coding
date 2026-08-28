def chain_derivative(layers, x: float) -> tuple[float, float]:
    """layers = [(f1, df1), (f2, df2), ...] 代表 f1(f2(...fn(x)))。

    回傳 (合成函數的值, 導數)。
    """
    x0 = x
    values = []
    result = 1.0
    for layer, _ in reversed(layers):
        values.append(x0)
        x0 = layer(x0)
    for i, (_, df) in enumerate(reversed(layers)):
        result *= df(values[i])
    return x0, result
