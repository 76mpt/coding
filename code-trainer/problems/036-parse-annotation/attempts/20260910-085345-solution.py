class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # TODO: 1) 切欄位並檢查數量 2) 轉 int（轉不動要拋 BadAnnotation）
    #       3) 檢查 x2 > x1 且 y2 > y1
    line = line.split()
    if len(line) != 5:
        raise BadAnnotation
    label = line[0]
    try:
        box = [int(value) for value in line[1:]]
    except:
        raise BadAnnotation
    x1, y1, x2, y2 = box
    if x1 >= x2 or y1 >= y2:
        raise BadAnnotation
    return label, box
