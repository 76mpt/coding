def label_maps(names: list[str]) -> tuple[dict, dict]:
    """回傳 (名稱->編號, 編號->名稱) 兩個 dict，依首次出現順序編號。"""
    # TODO: 1) 去重保序 2) 用 enumerate 配編號 3) 兩個 dict comprehension
    result = dict.fromkeys(names)
    name_to_id = {name: i for i, name in enumerate(result)}
    id_to_name = {i: name for i, name in enumerate(result)}
    return name_to_id, id_to_name