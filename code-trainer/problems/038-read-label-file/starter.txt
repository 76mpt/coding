from pathlib import Path


class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def read_label_file(path) -> tuple[dict, int]:
    """讀標註檔，回傳 ({label: 次數}, 壞行數)。檔案問題要讓例外往上拋。"""
    # TODO: with open(..., encoding="utf-8") 讀檔 → 逐行解析 → 統計
