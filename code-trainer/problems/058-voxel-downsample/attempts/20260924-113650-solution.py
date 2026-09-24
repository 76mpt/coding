def voxel_downsample(points, size):
    """把落在同一個體素的點合併成平均位置。

    points: list[[x, y, z]]
    size: 體素邊長
    回傳 (排序後的體素座標 list[[i, j, k]], 對應的中心點 list[[x, y, z]])
    """
    # TODO
    pass
    voxel = {}
    for x, y ,z in points:
        i = int(x // size)
        j = int(y // size)
        k = int(z // size)
        key = (i, j, k)
        if key not in voxel:
            voxel[key] = [0.0, 0.0, 0.0, 0]
        voxel[key][0] += x
        voxel[key][1] += y
        voxel[key][2] += z
        voxel[key][3] += 1
    voxel_coor = []
    center = []
    for key in sorted(voxel):
        sx, sy, sz, count = voxel[key]
        voxel_coor.append(list(key))
        center.append([sx / count, sy / count, sz / count])
    return voxel_coor, center
