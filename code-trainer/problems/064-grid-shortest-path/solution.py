from collections import deque


def shortest_path(grid):
    """佔據網格上從左上到右下的最短步數；走不到回傳 -1。

    grid: list[list[int]]，0 可通行、1 障礙
    回傳 int
    """
    # TODO
    pass
    m = len(grid)
    n = len(grid[0])
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return -1
    if m == 1 and n == 1:
        return 0
    que = deque([(0, 0, 0)])
    grid[0][0] = 1
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while que:
        r, c, steps = que.popleft()
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if not (0 <= nr < m and 0 <= nc < n):
                continue
            if grid[nr][nc] == 1:
                continue
            if nr == m - 1 and nc == n - 1:
                return steps + 1
            grid[nr][nc] = 1
            que.append((nr, nc, steps + 1))
    return -1