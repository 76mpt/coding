def longest_run(s: str) -> tuple[str, int]:
    """回傳 (最長連續段的字元, 長度)。"""
    if not s:
        return "", 0
    char, max_char = s[0], s[0]
    count, max_count = 1, 1
    for c in s[1:]:
        if c == char:
            count += 1
        else:
            count = 1
            char = c
        if count > max_count:
            max_char = char
            max_count = count
    return max_char, max_count
