def det_and_area(M: list[list[float]]) -> tuple[float, float]:
    """回傳 (det(M), 單位正方形變換後的面積)。面積要用叉積算，不要用 abs(det)。"""
    # TODO: 1) det = ad - bc
    #       2) 兩個基底向量的像：(a,c) 和 (b,d)
    #       3) 面積 = |叉積|
