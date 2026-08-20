def collatz(n: int) -> tuple[int, int]:
    """回傳 (走到 1 的步數, 過程中出現過的最大值)。"""
    # TODO: 用一個 while 迴圈，直到 n 變成 1
    #       途中要維護兩個東西：走了幾步、看過的最大值
    count, max = 0, n
    while n > 1:
        n = n // 2 if n % 2 == 0 else n * 3 + 1
        count += 1
        if n > max:
            max = n
    return count, max