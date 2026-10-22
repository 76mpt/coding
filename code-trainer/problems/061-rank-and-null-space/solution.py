def rank_and_null_space(A):
    """用 RREF 求秩與零空間基底，並驗證零空間垂直於列空間。

    A: m×n 整數矩陣（list of rows）
    回傳 (rank, basis, dots)，見題目說明。
    """
    m = len(A)
    n = len(A[0])
    R = [list(map(float, r))for r in A]
    pivots = []
    row = 0
    for col in range(n):
        p = next((i for i in range(row, m) if abs(R[i][col]) > 1e-9), None)
        if p is None:
            continue
        R[row], R[p] = R[p], R[row]
        x = R[row][col]
        R[row] = [v / x for v in R[row]]

        for i in range(m):
            if i != row:
                x = R[i][col]
                R[i] = [a - x * b for a, b in zip(R[i], R[row])]
        pivots.append(col)
        row += 1
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        v = [0.0] * n
        v[f] = 1.0
        for i, p in enumerate(pivots):
            v[p] = -R[i][f]
        basis.append(v)
    dots = [[sum(a * b for a, b in zip(r, v))for v in basis] for r in A]
    return len(pivots), basis, dots