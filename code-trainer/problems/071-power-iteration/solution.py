import math
def power_iteration(A, v0, iters):
    """冪迭代：跑 iters 輪，回傳 (lam, v, lams, resid)。"""
    # TODO
    n = len(A)
    def norm(v):
        return math.sqrt(sum(x * x for x in v))
    def mat_vec(A, v):
        return [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
    v = [x / norm(v0) for x in v0]
    lams = []

    for _ in range(iters):
        Av = mat_vec(A, v)
        v = [x / norm(Av) for x in Av]
        Av = mat_vec(A, v)
        lam = sum(v[i] * Av[i] for i in range(n))
        lams.append(lam)
    
    Av = mat_vec(A, v)
    residual = norm([Av[i] - lams[-1] * v[i] for i in range(n)])
    idx = max(range(n), key=lambda i:abs(v[i]))
    if v[idx] < 0:
        v = [-x for x in v]
    return lams[-1], v, lams, residual
