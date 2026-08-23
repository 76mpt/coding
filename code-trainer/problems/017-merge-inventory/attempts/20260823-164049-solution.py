def merge_inventory(a: dict, b: dict) -> dict:
    """合併兩份庫存，數量相加，移除 <= 0 的項目。不可修改 a 和 b。"""
    new_dict = {}
    for item in a:
        new_dict.update({item:a[item]})
    for item in b:
        if item in new_dict:
            new_dict.update({item:b[item] + new_dict[item]})
        else:
            new_dict.update({item:b[item]})
    for item in list(new_dict.keys()):
        if new_dict[item] <= 0:
            del new_dict[item]
    return new_dict

    #new_dict = dict(a)
    #for key, value in b.items():
    #   new_dict[key] = new_dict.get(key, 0) + value
    #return {key: value for key, value in new_dict.items() if value > 0}

    #OR
    #return {key:value for key, value in (Counter(a) + Counter(b)).items() if value > 0}
    