def parse_label_line(line: str) -> dict:
    """把一行標註解析成 {"label": str, "box": [x1, y1, x2, y2]}。

    格式錯誤時 raise ValueError。
    """
    new = line.strip().split(",")
    if len(new) != 5 or new[0] == "":
        raise ValueError
    label = new[0]
    label = label.strip().lower()
    try:
        x1, y1, x2, y2 = [int(num) for num in new[1:]]
    except:
        raise ValueError
    if x2 <= x1 or y2 <= y1:
        raise ValueError
    box = [x1, y1, x2, y2]
    result = {"label" : label, "box" : box}
    return result

