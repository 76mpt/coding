def compose_maps(A, B, points):
    """驗證：先做 B 再做 A == 做一次 A·B。

    A, B: 2x2 矩陣，格式 [[a, b], [c, d]]
    points: [[x, y], ...]
    回傳 (先B再A的點, 只套C的點, A·B, B·A)。
    """
    # TODO
    pass
    def matmul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B))] for i in range(len(A))]
    def apply(A, point):
        return [A[0][0] * point[0] + A[0][1] * point[1], A[1][0] * point[0] + A[1][1] * point[1]]
    res = [apply(A, apply(B, point)) for point in points]
    mat = matmul(A, B)
    res_C = [apply(mat, point) for point in points]
    return res, res_C, mat, matmul(B, A)
