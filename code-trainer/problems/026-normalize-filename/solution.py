def normalize_filename(name: str) -> str:
    """把檔名正規化：副檔名轉小寫、空白換底線、壓縮重複底線。"""
    # TODO: 1) 去頭尾空白 2) 切出主檔名與副檔名
    #       3) 主檔名：空白換底線、壓縮、去頭尾底線 4) 組回去
    name = name.strip()
    file, dot, ext = name.rpartition('.')
    if not dot:
        file = ext
        ext = ""
    file = file.replace(" ", "_")
    ext = ext.lower()
    
    file = "_".join(text for text in file.split("_") if text)
    return file + dot + ext
    