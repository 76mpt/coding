class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # 可以把 036 的實作貼過來
    anno = line.strip().split()
    if len(anno) != 5:
        raise BadAnnotation
    label = anno[0]
    if not label:
        raise BadAnnotation
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


def load_annotations(lines: list[str]) -> tuple[list, list]:
    """回傳 (好的標註, [(行號, 原始內容), ...])。空白行略過，壞行不拋例外。"""
    # TODO: enumerate 拿行號 → 略過空白行 → try 解析 → except 記錄
    result = []
    bad = []
    for i, line in enumerate(lines, start = 1):
        if not line.strip():
            continue
        try:
            result.append(parse_annotation(line))
        except:
            bad.append((i, line))
    return (result, bad)