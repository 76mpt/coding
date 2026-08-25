def project(a: list[float], b: list[float]) -> tuple[list[float], list[float]]:
    """回傳 (a 在 b 上的投影向量, 殘差向量 a - 投影)。"""
    # TODO: 1) 檢查長度與 b 是否為零向量
    #       2) 算係數 (a·b)/(b·b)  3) 乘回 b 得到 p  4) r = a - p
