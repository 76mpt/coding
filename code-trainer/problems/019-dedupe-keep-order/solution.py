def dedupe_keep_order(items: list) -> tuple[list, int]:
    """回傳 (去重後保留順序的 list, 被移除的數量)。"""
    seen = set()
    result = []
    count = 0
    for item in items:
        if item in seen:
            count += 1
        else:
            result.append(item)
            seen.add(item)
    return result, count
