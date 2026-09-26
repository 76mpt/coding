class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # TODO: 1) 切欄位並檢查數量 2) 轉 int（轉不動要拋 BadAnnotation）
    #       3) 檢查 x2 > x1 且 y2 > y1
    anno = line.strip().split()
    if len(anno) != 5:
        raise BadAnnotation
    label = anno[0]
    try:
        x1 = int(anno[1])
        y1 = int(anno[2])
        x2 = int(anno[3])
        y2 = int(anno[4])
        box = [x1, y1, x2, y2]
        if x2 <= x1 or y2 <= y1:
            raise BadAnnotation
    except:
        raise BadAnnotation
    return label, box
