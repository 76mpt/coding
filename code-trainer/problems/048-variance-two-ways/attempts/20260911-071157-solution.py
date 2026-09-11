def variance_two_ways(xs: list) -> tuple:
    """回傳 (用定義式算的變異數, 用展開式算的變異數)。空 list 要 raise ValueError。"""
    # TODO: 兩個都要照各自的公式算，不要互相抄
    if not xs:
        raise ValueError
    vari_det = 0.0
    vari = 0.0
    n = len(xs)
    miu = sum(xs) / n
    vari_det = sum((x - miu) ** 2 for x in xs) / n
    vari = sum(x ** 2 for x in xs) / n - miu ** 2 
    return vari_det, vari