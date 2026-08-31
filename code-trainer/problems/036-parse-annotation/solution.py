class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # TODO: 1) 切欄位並檢查數量 2) 轉 int（轉不動要拋 BadAnnotation）
    #       3) 檢查 x2 > x1 且 y2 > y1
    line_list = [item.strip() for item in line.split()]
    if len(line_list) != 5 or not line_list[0]:
        raise BadAnnotation("need 5 slots")
    label = line_list[0]
    try:
        box = [int(item) for item in line_list[1:]]
    except ValueError:
        raise BadAnnotation("must be int for coordinates")
    x1, y1, x2, y2 = box
    if x2 <= x1 or y2 <= y1:
        raise BadAnnotation("window size should > 0")
    label = label.lower()
    
    return label, box