class BoundingBox:
    """一個偵測框。width/height/area/center 都是算出來的。"""

    def __init__(self, x1, y1, x2, y2):
        if x2 <= x1 or y2 <= y1:
            raise ValueError
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    # TODO: width / height / area / center 用 @property
    @property
    def width(self):
        return self.x2 - self.x1
    @property
    def height(self):
        return self.y2 - self.y1
    @property
    def area(self):
        return self.width * self.height
    @property
    def center(self) -> tuple:
        cx = self.x1 + self.width / 2 
        cy = self.y1 + self.height / 2
        return (float(cx), float(cy))
    # TODO: __repr__
    def __repr__(self) -> str:
        return f"BoundingBox({self.x1}, {self.y1}, {self.x2}, {self.y2})"


def make_boxes(raw: list) -> list:
    """把 [(x1,y1,x2,y2), ...] 變成 [BoundingBox, ...]。"""
    return [BoundingBox(x1, y1, x2, y2) for x1, y1, x2, y2 in raw]
