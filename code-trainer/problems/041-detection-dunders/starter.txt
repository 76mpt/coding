class Detection:
    """一個偵測結果。相等性看 label + box，排序看 score。"""

    def __init__(self, label, box, score):
        self.label = label
        self.box = box
        self.score = score

    # TODO: __repr__ / __eq__ / __hash__ / __lt__


def rank_detections(raw: list) -> list:
    """建物件 → 去重（留第一個）→ 依分數由高到低、同分依 label 字典序。"""
    # TODO
