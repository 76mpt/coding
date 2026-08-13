def longest_run(s: str) -> tuple[str, int]:
    """回傳 (最長連續段的字元, 長度)。"""
    cur_char, best_char, pre_char = str(""), str(""), str("")
    cur_len, best_len = 0, 0
    for char in s:
        if char == pre_char:
            cur_len += 1
        else:
            cur_char = char
            cur_len = 1
        if cur_len > best_len:
            best_char = cur_char
            best_len = cur_len
        pre_char = char
    return best_char, best_len

    # if not s:
    #     return "", 0
    # char, run = s[0], 1
    # best_char, best_run = s[0], 1
    # for cha in s[1:]:
    #     if cha == char:
    #         run += 1
    #     else:
    #         char, run = cha, 1
    #     if run > best_run:
    #         best_char, best_run = char, run
    # return best_char, best_run