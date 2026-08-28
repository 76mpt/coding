def find_images(text: str) -> list[str]:
    """回傳文字裡的影像檔名，依首次出現順序，不分大小寫去重。"""
    # TODO: 1) 切詞 2) 判斷是不是影像檔名（不分大小寫）
    #       3) 不分大小寫去重，但回傳原始大小寫
    name_list = text.split()
    result = []
    seen = set()
    for name in name_list:
        name_low = name.lower()
        if (name_low.endswith((".png", ".jpg", ".jpeg"))) and name_low[0] != ".":
            if name_low not in seen:
                seen.add(name.lower())
                result.append(name)
    return result