def merge_inventory(a: dict, b: dict) -> dict:
    """合併兩份庫存，數量相加，移除 <= 0 的項目。不可修改 a 和 b。"""
    result = a.copy()
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    result = {key:value for key, value in result.items() if value != 0}
    return result