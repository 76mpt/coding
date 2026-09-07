def parse_label_line(line: str) -> dict:
    """把一行標註解析成 {"label": str, "box": [x1, y1, x2, y2]}。

    格式錯誤時 raise ValueError。
    """
    line_list = [item.strip() for item in line.split(',')]
    if len(line_list) != 5 or not line_list[0]:
        raise ValueError
    label = line_list[0]
    box = [int(item) for item in line_list[1:]]
    if box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError
    label = label.lower()
    result = {"label": label, "box" :box}
    return result