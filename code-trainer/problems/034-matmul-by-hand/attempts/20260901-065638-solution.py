def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """回傳矩陣乘積 AB。維度不合就 raise ValueError。"""
    # TODO: 1) 檢查維度 2) 結果的 (i,j) = A 第 i 列 與 B 第 j 行 的內積
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    if n != len(B):
        raise ValueError("A不等於B的維度")
    result = [[0.0] * p for _ in range(m)]
    for i in range(m):          
        for j in range(p):    
            dot_product = 0.0
            for k in range(n):
                dot_product += A[i][k] * B[k][j]
                result[i][j] = dot_product
    return result