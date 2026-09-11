def find_pair(sizes, target):
    """找兩個不同位置 i < j 使 sizes[i] + sizes[j] == target。

    多組答案時取 j 最小、再取 i 最小；找不到回傳 None。
    """
    seen = {}
    for j, x in enumerate(sizes):
        need = target - x
        if need in seen:
            return [seen[need], j]
        if x not in seen:
            seen[x] = j
    return None
        
        
