from pathlib import Path


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

def read_label_file(path) -> tuple[dict, int]:
    """讀標註檔，回傳 ({label: 次數}, 壞行數)。檔案問題要讓例外往上拋。"""
    # TODO: with open(..., encoding="utf-8") 讀檔 → 逐行解析 → 統計
    error = 0
    result = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.split():
                continue
            try:
                label, _ = parse_annotation(line)
            except BadAnnotation:
                error += 1
                continue
            result[label] = result.get(label, 0) + 1
        return result, error