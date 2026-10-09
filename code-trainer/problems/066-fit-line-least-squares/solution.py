def fit_line(xs, ys):
    """最小平方擬合 y = a x + b。

    xs, ys: 等長的數字 list，xs 至少有兩個不同值
    回傳 ([a, b], residuals, dots, sse)，見題目說明。
    """
    # TODO
    pass
    m = len(xs)
    sx = sum(float(x) for x in xs)
    sy = sum(float(y) for y in ys)
    sxx = sum(float(x) * float(x) for x in xs)
    sxy = sum(float(x) * float(y) for x, y in zip(xs, ys))

    det = sxx * m - sx * sx
    a = (m * sxy - sx * sy) / det
    b = (sxx * sy - sx * sxy) / det
    a = float(a)
    b = float(b)

    residual = [float(y) - (a * float(x) + b) for x, y in zip(xs, ys)]
    dot = [sum(r * float(x) for r, x in zip(residual, xs)), sum(residual)]
    sse = sum(r * r for r in residual)
    return [a, b], residual, dot, sse