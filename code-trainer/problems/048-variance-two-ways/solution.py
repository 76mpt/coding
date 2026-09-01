def variance_two_ways(xs: list) -> tuple:
    """回傳 (用定義式算的變異數, 用展開式算的變異數)。空 list 要 raise ValueError。"""
    # TODO: 兩個都要照各自的公式算，不要互相抄
    if not xs:
        raise ValueError
    n = len(xs)
    mean_u = sum(xs) / n
    return (sum((x - mean_u) ** 2 for x in xs) / n, sum(x ** 2  for x in xs) / n - mean_u ** 2)