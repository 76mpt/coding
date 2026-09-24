import math


def dot_and_angle(a: list[float], b: list[float]) -> tuple[float, float]:
    """回傳 (內積, 夾角弧度)。夾角用 arccos((a·b)/(|a||b|)) 算。"""
    # TODO: 1) 檢查長度與零向量 2) 座標式算內積
    #       3) 算兩個長度 4) 算 cos 並夾回 [-1, 1] 5) arccos
    if len(a) != len(b):
        raise ValueError
    coor = 0.0
    for i in range(len(a)):
        coor += a[i] * b[i]
    dot_a = math.sqrt(sum(x * x for x in a))
    dot_b = math.sqrt(sum(x * x for x in b))
    if dot_a == 0.0 or dot_b == 0.0:
        raise ValueError
    theta = math.acos(max(-1.0, min(1.0, coor / (dot_a * dot_b))))
    return coor, theta
    