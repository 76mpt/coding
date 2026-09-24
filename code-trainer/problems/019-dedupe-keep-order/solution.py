def dedupe_keep_order(items: list) -> tuple[list, int]:
    """回傳 (去重後保留順序的 list, 被移除的數量)。"""
    # TODO
    pass
    result = []
    seen = set()
    count = 0
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
        else:
            count += 1
    return result, count