def complete_frames(filenames):
    """回傳所有相機都有拍到的幀號（由小到大）。

    filenames: list[str]，格式很髒，不合法的直接忽略
    回傳 list[int]
    """
    # TODO
    pass
    camera = {}
    for filename in filenames:
        filename = filename.strip()
        if "." not in filename:
            continue
        name, ext = filename.rsplit(".", 1)
        if ext.lower() not in ("png", "jpg", "jpeg"):
            continue
            
        name = name.lower()
        if not name.startswith("cam"):
            continue
        name = name[3:]
        if name.count("_") + name.count("-") != 1:
            continue
        if "_" in name:
            cam, frame = name.split("_")
        else:
            cam, frame = name.split("-")
        if not cam.isdigit() or not frame.isdigit():
            continue
        cam = int(cam)
        frame = int(frame)
        if cam not in camera:
            camera[cam] = set()
        camera[cam].add(frame)

    if not camera:
        return []
    result = None
    for frame in camera.values():
        if result is None:
            result = frame.copy()
        else:
            result &= frame
    return sorted(result)