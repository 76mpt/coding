import math


def rotate_points(points: list, theta: float) -> list:
    """把每個點繞原點逆時針轉 theta 弧度。"""
    # TODO: cos/sin 只要算一次，然後對每個點套用旋轉公式
    c = math.cos(theta)
    s = math.sin(theta)
    result = [(x * c - y * s, x * s + y * c) for x, y in points]
    return result

