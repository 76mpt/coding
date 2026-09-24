def shortest_window(counts, target):
    """找最短的連續區間，使區間和 >= target。

    counts: list[int]，非負
    target: int
    回傳最短長度；找不到回傳 0。
    """
    left = 0
    cur = 0
    best = len(counts) + 1
    for right in range(len(counts)):
        cur += counts[right]
        while cur >= target:
            best = min(best, right - left + 1)
            cur -= counts[left]
            left += 1
    return 0 if best == len(counts) + 1 else best
