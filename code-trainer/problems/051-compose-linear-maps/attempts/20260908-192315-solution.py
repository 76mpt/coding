def compose_report(A, B, points):
    """驗證：先做 B 再做 A == 做一次 A·B。

    A, B: 2x2 矩陣，格式 [[a, b], [c, d]]
    points: [[x, y], ...]
    回傳見題目說明的 dict。
    """
    eps = 1e-9
    def matmul(X, Y):
        """2x2 矩陣乘法 X @ Y"""
        return [
            [
                X[0][0] * Y[0][0] + X[0][1] * Y[1][0],
                X[0][0] * Y[0][1] + X[0][1] * Y[1][1],
            ],
            [
                X[1][0] * Y[0][0] + X[1][1] * Y[1][0],
                X[1][0] * Y[0][1] + X[1][1] * Y[1][1],
            ],
        ]
    def same_matrix(X, Y):
        return all(
            abs(X[i][j] - Y[i][j]) <= eps
            for i in range(2)
            for j in range(2)
        )
    def apply(M, p):
        """矩陣 M 作用在點 p 上"""
        x, y = p
        return [
            M[0][0] * x + M[0][1] * y,
            M[1][0] * x + M[1][1] * y,
        ]
    C_mat = matmul(A, B)
    C_mat = [[float(x), float(y)] for x, y in C_mat]
    reversed_C = matmul(B, A)
    seq = []
    com = []
    for point in points:
        seq.append(apply(A, apply(B, point)))
        com.append(apply(C_mat, point))
    same = all(abs(s[0] - c[0]) <= eps and abs(s[1] - c[1]) <= eps for s, c in zip(seq, com))
    seq = [[float(x), float(y)] for x, y in seq]
    com = [[float(x), float(y)] for x, y in com]
    
    return {"sequential": seq, "combined": com, "product": C_mat, "same": same, "order_matters": not same_matrix(C_mat, reversed_C)}
    
