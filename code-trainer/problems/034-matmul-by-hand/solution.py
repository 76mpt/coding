def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """回傳矩陣乘積 AB。維度不合就 raise ValueError。"""
    # TODO: 1) 檢查維度 2) 結果的 (i,j) = A 第 i 列 與 B 第 j 行 的內積
    n = len(A[0])
    p = len(B)
    if n != p:
        raise ValueError
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]