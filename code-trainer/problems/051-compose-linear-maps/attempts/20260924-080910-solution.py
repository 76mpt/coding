def compose_maps(A, B, points):
    """驗證：先做 B 再做 A == 做一次 A·B。

    A, B: 2x2 矩陣，格式 [[a, b], [c, d]]
    points: [[x, y], ...]
    回傳 (先B再A的點, 只套C的點, A·B, B·A)。
    """
    def apply(M, p):
        return [M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1]]
    def matmul(X, Y):
        return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    
    res = [apply(A, apply(B, point)) for point in points]
    mat = matmul(A, B)
    res_C = [apply(mat, point) for point in points]
    return res, res_C, mat, matmul(B, A)

