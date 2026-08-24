def longest_run(s: str) -> tuple[str, int]:
    """回傳 (最長連續段的字元, 長度)。"""
    char, res_char = "", ""
    char_len, res_len = 1, 0
    for c in s:
        if char == c:
            char_len += 1
        else:
            char_len = 1
            char = c
        if char_len > res_len:
            res_char = char
            res_len = char_len
    return res_char, res_len
