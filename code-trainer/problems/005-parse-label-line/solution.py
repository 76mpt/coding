def parse_label_line(line: str) -> dict:
    """把一行標註解析成 {"label": str, "box": [x1, y1, x2, y2]}。

    格式錯誤時 raise ValueError。
    """
    line = line.strip().split(',')
    if len(line) != 5:
        raise ValueError
    label = line[0]
    if not label:
        raise ValueError
    try:
        x1, y1, x2, y2 = [int(num) for num in line[1:]]
    except:
        raise ValueError
    if x2 <= x1 or y2 <= y1:
        raise ValueError
    label = label.strip().lower()
    box = [x1, y1, x2 , y2]
    result = {"label": label, "box": box}
    return result
