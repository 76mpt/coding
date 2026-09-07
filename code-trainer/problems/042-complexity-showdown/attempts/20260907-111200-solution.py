def common_labels(a: list[str], b: list[str]) -> list[str]:
    """回傳同時在 a 和 b 裡的標籤，依 a 的首次出現順序，不重複。"""
    # TODO: 想清楚「被查的容器」該用什麼型別
    seen = set()
    b_set = set(b)
    result = []
    for item in a:
        if item not in seen and item in b_set:
            result.append(item)
            seen.add(item)
    return result