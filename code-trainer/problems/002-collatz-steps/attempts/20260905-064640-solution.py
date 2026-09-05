def collatz(n: int) -> tuple[int, int]:
    """回傳 (走到 1 的步數, 過程中出現過的最大值)。"""
    # TODO: 用一個 while 迴圈，直到 n 變成 1
    #       途中要維護兩個東西：走了幾步、看過的最大值
    steps = 0
    maxi = n
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        if n > maxi:
            maxi = n
        steps += 1
    return steps, maxi
