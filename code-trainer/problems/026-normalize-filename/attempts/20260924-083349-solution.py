def normalize_filename(name: str) -> str:
    """把檔名正規化：副檔名轉小寫、空白換底線、壓縮重複底線。"""
    # TODO: 1) 去頭尾空白 2) 切出主檔名與副檔名
    #       3) 主檔名：空白換底線、壓縮、去頭尾底線 4) 組回去
    text = name.strip()
    stem, dot, typ = text.rpartition('.')
    if not dot:
        stem = typ
        typ = ""
    typ = typ.lower()
    stem = stem.replace(" ", "_")
    stem = "_".join(text for text in stem.split("_") if text)
    return stem + dot + typ if typ else stem
