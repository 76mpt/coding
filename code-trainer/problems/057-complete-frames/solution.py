def complete_frames(filenames):
    """回傳所有相機都有拍到的幀號（由小到大）。

    filenames: list[str]，格式很髒，不合法的直接忽略
    回傳 list[int]
    """
    cameras = {}

    for filename in filenames:
        filename = filename.strip()

        # 副檔名
        if "." not in filename:
            continue

        name, ext = filename.rsplit(".", 1)

        if ext.lower() not in ("png", "jpg", "jpeg"):
            continue

        # cam 開頭，不分大小寫
        name = name.lower()

        if not name.startswith("cam"):
            continue

        name = name[3:]

        # 分隔符必須剛好一個
        if name.count("_") + name.count("-") != 1:
            continue

        if "_" in name:
            cam, frame = name.split("_")
        else:
            cam, frame = name.split("-")

        # 必須是數字
        if not cam.isdigit() or not frame.isdigit():
            continue

        # 重點：轉成 int，消除前導零
        cam = int(cam)
        frame = int(frame)

        if cam not in cameras:
            cameras[cam] = set()

        cameras[cam].add(frame)

    if not cameras:
        return []

    # 第一台相機的 frames
    result = None

    for frames in cameras.values():
        if result is None:
            result = frames.copy()
        else:
            result &= frames

    return sorted(result)
