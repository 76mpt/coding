class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # 可以把 036 的實作貼過來
    parts = line.split()
    if len(parts) != 5:
        raise BadAnnotation(f"需要 5 個欄位，得到 {len(parts)}：{line!r}")

    label = parts[0]
    try:
        coords = [int(v) for v in parts[1:]]
    except ValueError:
        raise BadAnnotation(f"座標必須是整數：{line!r}") from None

    x1, y1, x2, y2 = coords
    if x2 <= x1 or y2 <= y1:
        raise BadAnnotation(f"框的寬高必須為正：{line!r}")

    return label, coords

def load_annotations(lines: list[str]) -> tuple[list, list]:
    """回傳 (好的標註, [(行號, 原始內容), ...])。空白行略過，壞行不拋例外。"""
    # TODO: enumerate 拿行號 → 略過空白行 → try 解析 → except 記錄
    good, bad = [], []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            good.append(parse_annotation(line))
        except BadAnnotation:
            bad.append((index, line))
    return good, bad