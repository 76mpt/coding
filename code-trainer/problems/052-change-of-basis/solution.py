def change_of_basis(basis, points, matrix):
    """同一個變換，換一組基底來看。

    basis:  [[b1x, b1y], [b2x, b2y]]，保證線性獨立
    points: [[x, y], ...]，標準座標
    matrix: [[a, b], [c, d]]，標準基底下的變換
    回傳 (B-座標, 組回來的點, [T]_B, 變換後的點的 B-座標)。
    """
    # TODO
    pass
    def apply(M, p):
        return [M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1]]
    def matmul(X, Y):
        return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    def inverse_2x2(M):
        a, b = M[0]
        c, d = M[1]
        det = a * d - c * b
        return [[d / det, -b / det], [-c / det, a / det]]
    B = [[float(basis[0][0]), float(basis[1][0])], [float(basis[0][1]), float(basis[1][1])]]
    B_inv = inverse_2x2(B)
    coor = []
    for point in points:
        c = apply(B_inv, point)
        coor.append([float(c[0]), float(c[1])])
    reco = []
    for c in coor:
        p = apply(B, c)
        reco.append([float(p[0]), float(p[1])])
    M = [[float(matrix[0][0]), float(matrix[0][1])], [float(matrix[1][0]), float(matrix[1][1])]]
    BM = matmul(M, B)
    t_b = matmul(B_inv, BM)
    t_b = [[float(t_b[0][0]), float(t_b[0][1])], [float(t_b[1][0]), float(t_b[1][1])]]
    t_coor = []
    for point in points:
        tran = apply(M, point)
        c = apply(B_inv, tran)
        t_coor.append([float(c[0]), float(c[1])])
    return coor, reco, t_b, t_coor