def nearest_imu(cam, imu):
    """對每個相機時間戳，找時間最近的 IMU 索引（同距離取較小索引）。

    cam: list[int]，非遞減
    imu: list[int]，嚴格遞增，至少一筆
    回傳 list[int]，長度同 cam。
    """
    # TODO
    pass
    cam_frame = []
    j = 0
    for target in cam:
        while j + 1 < len(imu) and imu[j + 1] < target:
            j += 1
        if j + 1 < len(imu):
            left = abs(imu[j] - target)
            right = abs(imu[j + 1] - target)
            if right < left:
                j += 1
        cam_frame.append(j)
    return cam_frame
            
