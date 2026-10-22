def sort_detections(dets):
    """先依 cls 遞增、再依 score 遞減排序，平手時保持原順序。

    回傳 (order, sorted_dets)。
    """
    order = sorted(range(len(dets)), key=lambda i: (dets[i][0], -dets[i][1], i))
    sorted_det = [dets[i] for i in order]
    return order, sorted_det
