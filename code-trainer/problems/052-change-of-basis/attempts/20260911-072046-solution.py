def change_of_basis(basis, points, matrix):
    """同一個變換，換一組基底來看。

    basis:  [[b1x, b1y], [b2x, b2y]]，保證線性獨立
    points: [[x, y], ...]，標準座標
    matrix: [[a, b], [c, d]]，標準基底下的變換
    回傳 (B-座標, 組回來的點, [T]_B, 變換後的點的 B-座標)。
    """
    def matmul(A, B):
        """2x2 矩陣乘法"""
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1],
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1],
            ],
        ]

    def apply(M, p):
        """矩陣 M 作用在點 p 上"""
        x, y = p
        return [
            M[0][0] * x + M[0][1] * y,
            M[1][0] * x + M[1][1] * y,
        ]

    def inverse_2X2(M):
        a, b = M[0]
        c, d = M[1]
        det = a * d - b * c
        return [[d / det, -b / det], [-c / det, a / det]]

    B = [[float(basis[0][0]), float(basis[1][0])], [float(basis[0][1]), float(basis[1][1])]]
    B_inv = inverse_2X2(B)
    coor = []
    for point in points:
        c = apply(B_inv, point)
        coor.append([float(c[0]), float(c[1])])

    reco = []
    for c in coor:
        c1, c2 = c
        x = c1 * B[0][0] + c2 * B[0][1]
        y = c1 * B[1][0] + c2 * B[1][1]
        reco.append([float(x), float(y)])
    
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