import math


def rotation_matrix(theta: float) -> list:
    """回傳 2x2 旋轉矩陣 [[cos, -sin], [sin, cos]]。"""
    # TODO
    c = math.cos(theta)
    s = math.sin(theta)
    answer = [[c, -s], [s, c]]
    return answer

def _mul2(A,B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2) for i in range(2)]]

def _euler(theta):
    return complex(math.cos(theta), math.sin(theta))

def compose_rotations(alpha: float, beta: float) -> tuple:
    """回傳 (R(a)@R(b), R(a+b), e^{ia}*e^{ib}, e^{i(a+b)})。"""
    # TODO: 矩陣乘法要自己算（034 寫過），複數用 complex()
    m1 = _mul2(rotation_matrix(alpha), rotation_matrix(beta))
    m2 = rotation_matrix(alpha + beta)
    c1 = _euler(alpha) * _euler(beta)
    c2 = _euler(alpha + beta)
    return m1, m2, c1, c2
