def voxel_downsample(points, size):
    """把落在同一個體素的點合併成平均位置。

    points: list[[x, y, z]]
    size: 體素邊長
    回傳 (排序後的體素座標 list[[i, j, k]], 對應的中心點 list[[x, y, z]])
    """
    voxels = {}
    for x, y, z in points:
        i = int(x // size)
        j = int(y // size)
        k = int(z // size)
        key = (i, j, k)
        if key not in voxels:
            voxels[key] = [0.0, 0.0, 0.0, 0]
        voxels[key][0] += x
        voxels[key][1] += y
        voxels[key][2] += z
        voxels[key][3] += 1
    voxel_coor = []
    centers = []
    for key in sorted(voxels):
        sx, sy, sz, count = voxels[key]
        voxel_coor.append(list(key))
        centers.append([sx / count, sy / count, sz / count])
    return voxel_coor, centers