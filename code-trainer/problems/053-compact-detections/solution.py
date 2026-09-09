def compact(scores, threshold):
    """就地丟掉低於門檻的分數，保留原順序。

    scores: list[int]
    threshold: int
    回傳 (保留了幾個, 保留下來的那幾個元素)。
    """
    write = 0
    for score in scores:
        if score >= threshold:
            scores[write] = score
            write += 1
    return write, scores[:write]

    #O(n) T, O(1) space