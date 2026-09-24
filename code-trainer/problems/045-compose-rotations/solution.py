import math


def rotation_matrix(theta: float) -> list:
    """回傳 2x2 旋轉矩陣 [[cos, -sin], [sin, cos]]。"""
    # TODO
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, -s], [s, c]]

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def compose_rotations(alpha: float, beta: float) -> tuple:
    """回傳 (R(a)@R(b), R(a+b), e^{ia}*e^{ib}, e^{i(a+b)})。"""
    # TODO: 矩陣乘法要自己算（034 寫過），複數用 complex()
    a = rotation_matrix(alpha)
    b = rotation_matrix(beta)
    if len(a[0]) != len(b[0]):
        raise ValueError
    m1 = matmul(a, b)
    a_b = rotation_matrix(alpha + beta)
    c_alpha = complex(math.cos(alpha), math.sin(alpha))
    c_beta = complex(math.cos(beta), math.sin(beta))
    c1 = c_alpha * c_beta
    c2 = complex(math.cos(alpha + beta), math.sin(alpha + beta))
    return m1, a_b, c1, c2