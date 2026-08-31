def parse_label_line(line: str) -> dict:
    """把一行標註解析成 {"label": str, "box": [x1, y1, x2, y2]}。

    格式錯誤時 raise ValueError。
    """
    line_list = [item.strip() for item in line.split(",")]
    if len(line_list) != 5:
        raise ValueError("長度不正確")
    label = line_list[0].lower()
    if not label:
        raise ValueError("名稱不存在")
    x1, y1, x2, y2 = [int(num) for num in line_list[1:]]
    if x2 <= x1 or y2 <= y1:
        raise ValueError("無效邊界座標框")
    return {"label": label, "box": [x1, y1, x2, y2]}
