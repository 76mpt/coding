def find_pair(sizes, target):
    """找兩個不同位置 i < j 使 sizes[i] + sizes[j] == target。

    多組答案時取 j 最小、再取 i 最小；找不到回傳 None。
    """
    # TODO
    pass
    seen = {}
    for j, x in enumerate(sizes):
        needs = target - x
        if needs in seen:
            return [seen[needs], j]
        if x not in seen:
            seen[x] = j
    return None