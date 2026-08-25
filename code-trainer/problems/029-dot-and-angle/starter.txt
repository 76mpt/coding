import math


def dot_and_angle(a: list[float], b: list[float]) -> tuple[float, float]:
    """回傳 (內積, 夾角弧度)。夾角用 arccos((a·b)/(|a||b|)) 算。"""
    # TODO: 1) 檢查長度與零向量 2) 座標式算內積
    #       3) 算兩個長度 4) 算 cos 並夾回 [-1, 1] 5) arccos
