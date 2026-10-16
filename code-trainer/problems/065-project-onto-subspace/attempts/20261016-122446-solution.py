def project_onto(basis, v):
    """把 v 投影到 basis 張成的子空間。

    basis: k 個長度 n 的線性獨立向量（不保證正交）
    v: 長度 n 的向量
    回傳 (p, r, dots, p2)，見題目說明。
    """
    # TODO
    pass
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))
    def norm(v):
        return sum(x * x for x in v) ** 0.5
    def orth(basis):
        qs = []
        for a in basis:
            q = [float(x) for x in a]
            for prev in qs:
                c = dot(q, prev)
                for i in range(len(q)):
                    q[i] -= c * prev[i]
            length = norm(q)
            q = [x / length for x in q]
            qs.append(q)
        return qs
    def proj(qs, v):
        p = [0.0] * len(v)
        for q in qs:
            c = dot(q, v)
            for i in range(len(v)):
                p[i] += c * q[i]
        return p
    qs = orth(basis)
    p = proj(qs, v)
    r = [float(v[i]) - p[i] for i in range(len(v))]
    dots = [dot(r, a) for a in basis]
    p2 = proj(qs, p)
    return p, r, dots, p2