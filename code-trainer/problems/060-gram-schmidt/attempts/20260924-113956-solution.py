def gram_schmidt(vectors):
    """把線性獨立的向量組正交化。

    vectors: k 個長度 n 的向量
    回傳 (Q, G, rebuilt)，見題目說明。
    """
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))
    Q = []
    for vector in vectors:
        w = [float(x) for x in vector]
        for q in Q:
            coeff = dot(q, vector)
            w = [wi - coeff * qi for wi, qi in zip(w, q)]
        length = dot(w, w) ** 0.5
        Q.append([wi / length for wi in w])
    G = [[dot(a, b) for b in Q] for a in Q]
    rebuild = [[sum(dot(q, vector) * q[i] for q in Q) for i in range(len(vector))] for vector in vectors]
    return Q, G, rebuild