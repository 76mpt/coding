def voxel_downsample(points, size):
    """把落在同一個體素的點合併成平均位置。

    points: list[[x, y, z]]
    size: 體素邊長
    回傳 (排序後的體素座標 list[[i, j, k]], 對應的中心點 list[[x, y, z]])
    """
    # TODO
    pass
    vox = {}
    for x, y, z in points:
        i = int(x // size)
        j = int(y // size)
        k = int(z // size)
        key = (i, j, k)
        if key not in vox:
            vox[key] = [0.0, 0.0, 0.0, 0]
        vox[key][0] += x
        vox[key][1] += y
        vox[key][2] += z
        vox[key][3] += 1

    vox_coor = []
    center = []
    for key in sorted(vox):
        sx, sy, sz, count = vox[key]
        vox_coor.append(list(key))
        center.append([sx / count, sy / count, sz / count])
    return vox_coor, center