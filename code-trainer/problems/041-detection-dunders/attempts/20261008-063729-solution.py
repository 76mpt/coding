class Detection:
    """一個偵測結果。相等性看 label + box，排序看 score。"""

    def __init__(self, label, box, score):
        self.label = label
        self.box = tuple(box)
        self.score = score

    # TODO: __repr__ / __eq__ / __hash__ / __lt__
    def __repr__(self):
        return f"Detection({self.label!r}, {self.box}, {self.score})"
    def __eq__(self, other):
        if not isinstance(other, Detection):
            return NotImplemented
        return self.label == other.label and self.box == other.box
    def __hash__(self):
        return hash((self.label, self.box))
    def __lt__(self, other):
        if not isinstance(other, Detection):
            return NotImplemented
        return self.score < other.score

def rank_detections(raw: list) -> list:
    """建物件 → 去重（留第一個）→ 依分數由高到低、同分依 label 字典序。"""
    seen = set()
    unique = []
    for label, box, score in raw:
        det = Detection(label, box, score)
        if det not in seen:
            seen.add(det)
            unique.append(det)
    return sorted(unique, key = lambda x: (-x.score, x.label))