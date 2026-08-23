def merge_inventory(a: dict, b: dict) -> dict:
    """合併兩份庫存，數量相加，移除 <= 0 的項目。不可修改 a 和 b。"""
    merged = dict(a)
    for key, value in b.items():
        merged[key] = merged.get(key, 0) + value
    merged = {k: v for k, v in merged.items() if v != 0}
    return merged
