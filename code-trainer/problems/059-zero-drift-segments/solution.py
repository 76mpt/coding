def count_segments(deltas, k):
    """計算和剛好等於 k 的連續片段個數。

    deltas: list[int]，可正可負
    k: int
    回傳 int
    """
    count = 0
    cur = 0
    seen = {0: 1}
    for x in deltas:
        cur += x
        target = cur - k
        if target in seen:
            count += seen[target]
        seen[cur] = seen.get(cur, 0) + 1
    return count