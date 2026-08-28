def box_areas(boxes, min_area=0):
    """回傳面積 >= min_area 的框的面積，依原順序。"""
    # TODO: 用一個 list comprehension 完成「算面積 + 過濾」
    result = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in boxes if (x2 - x1) * (y2 - y1) >= min_area]
    return result 