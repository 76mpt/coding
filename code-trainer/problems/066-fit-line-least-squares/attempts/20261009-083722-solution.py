def fit_line(xs, ys):
    """最小平方擬合 y = a x + b。

    xs, ys: 等長的數字 list，xs 至少有兩個不同值
    回傳 ([a, b], residuals, dots, sse)，見題目說明。
    """
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

    residuals = [float(y) - (a * float(x) + b) for x, y in zip(xs, ys)]
    dots = [sum(r * float(x) for r, x in zip(residuals, xs)), sum(residuals)]
    sse = sum(r * r for r in residuals)
    return ([a, b], residuals, dots, float(sse))
