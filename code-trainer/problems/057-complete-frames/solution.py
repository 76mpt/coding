def complete_frames(filenames):
    """回傳所有相機都有拍到的幀號（由小到大）。

    filenames: list[str]，格式很髒，不合法的直接忽略
    回傳 list[int]
    """
    cameras = {}
    for file in filenames:
        file = file.strip()
        if not "." in file:
            continue
        cam, ext = file.rsplit(".", 1)
        if ext.lower() not in ("png", "jpg", "jpeg"):
            continue
        cam = cam.lower()
        if not cam.startswith("cam"):
            continue
        cam = cam[3:]
        if cam.count("_") + cam.count("-") != 1:
            continue
        if "_" in cam:
            camera, frame = cam.split("_")
        if "-" in cam:
            camera, frame = cam.split("-")
        if not camera.isdigit() or not frame.isdigit():
            continue
        camera = int(camera)
        frame = int(frame)
        if camera not in cameras:
            cameras[camera] = set()
        cameras[camera].add(frame)

    if not cameras:
        return []
    result = None
    for frame in cameras.values():
        if result is None:
            result = frame.copy()
        else:
            result &= frame
    return sorted(result)