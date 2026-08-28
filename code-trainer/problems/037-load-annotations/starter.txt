class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    """把一行標註解析成 (label, [x1, y1, x2, y2])。壞資料拋 BadAnnotation。"""
    # 可以把 036 的實作貼過來


def load_annotations(lines: list[str]) -> tuple[list, list]:
    """回傳 (好的標註, [(行號, 原始內容), ...])。空白行略過，壞行不拋例外。"""
    # TODO: enumerate 拿行號 → 略過空白行 → try 解析 → except 記錄
