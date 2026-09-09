def longest_run(s: str) -> tuple[str, int]:
    """回傳 (最長連續段的字元, 長度)。"""
    # TODO: 只掃一遍
    cur, ma = "", ""
    cur_len, ma_len = 0, 0
    if not s:
        return "", 0
    for text in s:
        if text != cur:
            cur = text
            cur_len = 1
        else:
            cur_len += 1
        if cur_len > ma_len:
            ma = cur
            ma_len = cur_len
    return ma, ma_len
        
