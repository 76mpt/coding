def first_bad_bracket(s):
    """回傳第一個壞掉的括號索引；全部正確回傳 -1。

    s: str，含 ()[]{} 與其他可忽略的字元
    回傳 int
    """
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for i, text in enumerate(s):
        if text in '([{':
            stack.append((text, i))
        elif text in ')}]':
            if not stack:
                return i
            
            left, left_i = stack[-1]
            if left != pairs[text]:
                return i
            
            stack.pop()
    if stack:
        return stack[0][1]
    return -1

