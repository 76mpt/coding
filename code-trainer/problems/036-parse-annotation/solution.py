class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # TODO: 1) 切欄位並檢查數量 2) 轉 int（轉不動要拋 BadAnnotation）
    #       3) 檢查 x2 > x1 且 y2 > y1
    text = line.strip().split()
    if len(text) != 5:
        raise BadAnnotation
    label = text[0]
    if not label:
        raise BadAnnotation
    box = text[1:]
    try:
        x1 = int(box[0])
        y1 = int(box[1])
        x2 = int(box[2])
        y2 = int(box[3])
        if x2 <= x1 or y2 <= y1:
            raise BadAnnotation
    except:
        raise BadAnnotation
    return label, [x1, y1, x2, y2]
