import math


def dot_and_angle(a: list[float], b: list[float]) -> tuple[float, float]:
    """回傳 (內積, 夾角弧度)。夾角用 arccos((a·b)/(|a||b|)) 算。"""
    # TODO: 1) 檢查長度與零向量 2) 座標式算內積
    #       3) 算兩個長度 4) 算 cos 並夾回 [-1, 1] 5) arccos
    if not a or not b or not len(a) == len(b):
        raise ValueError
    dot_prod = sum(x * y for x, y in zip(a,b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(y**2 for y in b))
    if mag_a == 0 or mag_b == 0:
        raise ValueError
    cos_theta = dot_prod / (mag_a * mag_b)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    angle_acos = math.acos(cos_theta)
    return dot_prod, angle_acos