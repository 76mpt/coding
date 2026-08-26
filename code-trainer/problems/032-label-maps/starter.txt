def label_maps(names: list[str]) -> tuple[dict, dict]:
    """回傳 (名稱->編號, 編號->名稱) 兩個 dict，依首次出現順序編號。"""
    # TODO: 1) 去重保序 2) 用 enumerate 配編號 3) 兩個 dict comprehension
