class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # 可以把 036 的實作貼過來
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
    box = [x1, y1, x2, y2]
    return label, box

def load_annotations(lines: list[str]) -> tuple[list, list]:
    """回傳 (好的標註, [(行號, 原始內容), ...])。空白行略過，壞行不拋例外。"""
    # TODO: enumerate 拿行號 → 略過空白行 → try 解析 → except 記錄
    result = []
    bad = []
    for index, line in enumerate(lines, start = 1):
        if not line.strip():
            continue
        try:
            result.append(parse_annotation(line))
        except BadAnnotation:
            bad.append((index, line))
    return (result, bad)