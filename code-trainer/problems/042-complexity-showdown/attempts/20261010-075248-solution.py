def common_labels(a: list[str], b: list[str]) -> list[str]:
    """回傳同時在 a 和 b 裡的標籤，依 a 的首次出現順序，不重複。"""
    # TODO: 想清楚「被查的容器」該用什麼型別
    b_set = set(b)
    result = []
    seen = set()
    for label in a:
        if label in b_set and label not in seen:
            result.append(label)
            seen.add(label)
    return result