from pathlib import Path


class BadAnnotation(ValueError):
    """標註行格式不合法。"""

def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # 可以把 036 的實作貼過來
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

def read_label_file(path) -> tuple[dict, int]:
    """讀標註檔，回傳 ({label: 次數}, 壞行數)。檔案問題要讓例外往上拋。"""
    # TODO: with open(..., encoding="utf-8") 讀檔 → 逐行解析 → 統計
    if not path:
        raise FileNotFoundError
    result = {}
    count = 0
    with open(path, encoding="utf-8") as f:
        if not f:
            return result, count
        for line in f:
            if not line.strip():
                continue
            try:
                label, _ = parse_annotation(line)
                result[label] = result.get(label, 0) + 1
            except BadAnnotation:
                count += 1
    return result, count