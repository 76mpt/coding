def next_stronger(scores):
    """對每個索引，找右邊第一個分數嚴格更大的索引；沒有則 -1。

    scores: list[int]
    回傳 list[int]，長度同 scores
    """
    n = len(scores)
    answer = [-1] * n
    stack = []
    for index, score in enumerate(scores):
        while stack and scores[stack[-1]] < score:
            j = stack.pop()
            answer[j] = index
        stack.append(index)
    return answer