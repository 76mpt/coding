import numpy as np


def iou_matrix(boxes_a, boxes_b):
    """回傳 (Na, Nb) 的 IoU 矩陣。boxes 格式為 [x1, y1, x2, y2]。"""
    a = np.asarray(boxes_a, dtype=np.float64)
    b = np.asarray(boxes_b, dtype=np.float64)
    # TODO: 不要用 for 迴圈
    pass
