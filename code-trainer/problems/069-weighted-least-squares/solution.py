def weighted_lstsq(A, b, w):
    """加權最小平方：最小化 sum_i w[i] * (b[i] - (A @ x)[i]) ** 2。

    回傳 (x, residuals, dots, wrss)。
    """
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))
    def mat_vec(A, x):
        return [dot(row, x) for row in A]
    def solve(M, rhs):
        n = len(rhs)
        aug = [[float(v) for v in M[i]] + [float(rhs[i])]for i in range(n)]
        for col in range(n):
            pivot = max(range(col, n), key=lambda i: abs(aug[i][col]))
            aug[col], aug[pivot] = aug[pivot], aug[col]
            p = aug[col][col]
            for j in range(col, n + 1):
                aug[col][j] /= p
            for i in range(n):
                if i == col:
                    continue
                factor = aug[i][col]
                for j in range(col, n + 1):
                    aug[i][j] -= factor * aug[col][j]
        return [float(aug[i][n]) for i in range(n)]
    
    m = len(A)
    n = len(A[0])
    M = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for i in range(m):
        for j in range(n):
            rhs[j] += w[i] * A[i][j] * b[i]
            for k in range(n):
                M[j][k] += w[i] * A[i][j] * A[i][k]
    x = solve(M, rhs)
    Ax = mat_vec(A, x)
    residual = [float(b[i] - Ax[i]) for i in range(m)]
    dots = [float(sum(w[i] * A[i][j] * residual[i] for i in range(m))) for j in range(n)]
    wrss = float(sum(w[i] * residual[i] ** 2 for i in range(m)))
    return x, residual, dots, wrss