import math


def rotation_matrix(theta: float) -> list:
    """回傳 2x2 旋轉矩陣 [[cos, -sin], [sin, cos]]。"""
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, -s], [s, c]]


def compose_rotations(alpha: float, beta: float) -> tuple:
    """回傳 (R(a)@R(b), R(a+b), e^{ia}*e^{ib}, e^{i(a+b)})。"""
    # TODO: 矩陣乘法要自己算（034 寫過），複數用 complex()
    a = rotation_matrix(alpha)
    b = rotation_matrix(beta)
    if len(a[0]) != len(b):
        raise ValueError
    m1 = [[0.0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                m1[i][j] += a[i][k] * b[k][j]
    m2 = rotation_matrix(alpha + beta)
    c_alpha = complex(math.cos(alpha), math.sin(alpha))
    c_beta = complex(math.cos(beta), math.sin(beta))
    c1 = c_alpha * c_beta
    c2 = complex(math.cos(alpha + beta), math.sin(alpha + beta))
    return m1, m2, c1, c2
    