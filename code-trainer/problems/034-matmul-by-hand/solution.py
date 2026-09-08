def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """回傳矩陣乘積 AB。維度不合就 raise ValueError。"""
    # TODO: 1) 檢查維度 2) 結果的 (i,j) = A 第 i 列 與 B 第 j 行 的內積
    if len(A[0]) != len(B):
        raise ValueError
    result = [[0.0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result