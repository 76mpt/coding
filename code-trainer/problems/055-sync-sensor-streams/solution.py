def nearest_imu(cam, imu):
    """對每個相機時間戳，找時間最近的 IMU 索引（同距離取較小索引）。

    cam: list[int]，非遞減
    imu: list[int]，嚴格遞增，至少一筆
    回傳 list[int]，長度同 cam。
    """
    result = []
    j = 0
    for frame in cam:
        while j + 1 < len(imu) and imu[j + 1] < frame:
            j += 1
        if j + 1 < len(imu):
            left = abs(imu[j] - frame)
            right = abs(imu[j + 1] - frame)
            if right < left:
                j += 1
        result.append(j)
    return result