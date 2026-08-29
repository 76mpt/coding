class BoundingBox:
    """一個偵測框。width/height/area/center 都是算出來的。"""

    def __init__(self, x1, y1, x2, y2):
        # TODO: 驗證 + 存四個座標
        ...

    # TODO: width / height / area / center 用 @property
    # TODO: __repr__


def make_boxes(raw: list) -> list:
    """把 [(x1,y1,x2,y2), ...] 變成 [BoundingBox, ...]。"""
    # TODO
