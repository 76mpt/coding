def build_report(records: list) -> str:
    """回傳每行 'label:score'（三位小數）的字串，由後往前，結尾不換行。"""
    # TODO: 避開字串累加與 list.insert(0, ...) 這兩個 O(n) 陷阱
    result = []
    for label, score in reversed(records):
        result.append(f"{label}:{score:.3f}")
    result = "\n".join(result)
    return result