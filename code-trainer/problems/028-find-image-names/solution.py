def find_images(text: str) -> list[str]:
    """回傳文字裡的影像檔名，依首次出現順序，不分大小寫去重。"""
    # TODO: 1) 切詞 2) 判斷是不是影像檔名（不分大小寫）
    #       3) 不分大小寫去重，但回傳原始大小寫
    files = text.split()
    seen = set()
    result = []
    for file in files:
        if not "." in file:
            continue
        stem, dot, ext = file.rpartition(".")
        if not stem:
            continue
        if ext.lower() == "jpg" or ext.lower() == "jpeg" or ext.lower() == "png":
            if (stem + dot + ext).lower() not in seen:
                result.append(stem + dot + ext)
                seen.add((stem + dot + ext).lower())
    return result