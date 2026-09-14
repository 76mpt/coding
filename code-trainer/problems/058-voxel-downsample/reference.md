# 058-voxel-downsample · 點雲體素降採樣 — 參考解

## 標準解

```python
import math

def voxel_downsample(points, size):
    groups = {}                                   # (i, j, k) → [sx, sy, sz, count]
    for x, y, z in points:
        key = (math.floor(x / size), math.floor(y / size), math.floor(z / size))
        g = groups.setdefault(key, [0.0, 0.0, 0.0, 0])
        g[0] += x
        g[1] += y
        g[2] += z
        g[3] += 1

    keys = sorted(groups)                         # tuple 逐元素比較，剛好是題目要的順序
    voxels = [list(k) for k in keys]
    centroids = [[groups[k][0] / groups[k][3],
                  groups[k][1] / groups[k][3],
                  groups[k][2] / groups[k][3]] for k in keys]
    return voxels, centroids
```

時間 O(n + V log V)，V 是非空體素數（最後排序）。空間 O(V)——**跟點數無關**。

## 三種取整，差在負數

| 寫法 | `2.7` | `-0.4` | `-2.0` | 行為 |
|---|---|---|---|---|
| `int(x)` | 2 | **0** | -2 | 往 0 截斷 |
| `math.floor(x)` | 2 | -1 | -2 | 往下取整，回傳 int |
| `x // 1` | 2.0 | -1.0 | -2.0 | 往下取整，**回傳 float** |

這題要往下取整。`int()` 在負數時會讓 `(-1, 0)` 這段區間跟 `[0, 1)` 合併成同一格——
**原點附近的體素是別的體素的兩倍大**。點雲通常以感測器為原點，
這個 bug 會剛好出現在感測器正前方最密集的區域。

`x // size` 也是往下取整，但結果是 float。當 dict key 時 `-1.0` 和 `-1` 會被當成同一個 key
（`hash(-1.0) == hash(-1)`），所以功能上可以用，但輸出前要記得轉 int。

## 為什麼 value 存總和而不是點

如果寫成 `groups.setdefault(key, []).append([x, y, z])`，最後再平均，功能完全正確。
但記憶體是 O(n)——你把所有點複製了一份，只為了最後算一個平均。

存 `[sx, sy, sz, count]` 是 O(V)。對一個 100 萬點、降採樣到 1 萬個體素的點雲，
記憶體差 100 倍。這個「**只存算最終答案需要的統計量**」的想法叫**串流統計（streaming statistics）**，
平均、變異數、最大最小值都可以這樣做（048 的變異數也有對應的串流版本）。

## 另一種寫法：numpy 向量化

```python
import numpy as np

def voxel_downsample(points, size):
    if not points:
        return [], []
    P = np.asarray(points, dtype=float)
    keys = np.floor(P / size).astype(np.int64)
    uniq, inverse = np.unique(keys, axis=0, return_inverse=True)
    counts = np.bincount(inverse)
    sums = np.zeros((len(uniq), 3))
    np.add.at(sums, inverse, P)
    return uniq.tolist(), (sums / counts[:, None]).tolist()
```

實際點雲處理會寫這個版本，快幾十倍。`np.unique(..., axis=0)` 做的是排序而不是雜湊，
但剛好一次解決了「分組」和「排序」兩件事。這在 S5 的 CV 實作節點會正式練到。

## 常見錯誤

1. **用 `int()` 取整**——負數座標落錯格。範例最後一點、隱藏測資的全負數點都會抓到。

2. **用 list 當 key**——`groups[[i, j, k]]` 直接 `TypeError: unhashable type: 'list'`。

3. **忘了排序**——dict 保留插入順序，輸出會是「第一次遇到的順序」而不是座標順序。

4. **key 忘了取整**——`key = (x / size, y / size, z / size)`，每個點都是自己一格，完全沒有降採樣。

5. **size 不是 2 的次方時的浮點陷阱**——`0.3 / 0.1` 在 Python 是 `2.9999999999999996`，
   往下取整得到 2 而不是 3。這題刻意限制 size 避開它，但實務上這是真實存在的 bug：
   PCL 和 Open3D 都有人回報過邊界點被分到錯的體素。常見的處理是除完之後加一個極小的 epsilon，
   或直接把座標量化成整數（例如轉成公釐）再做。

## 延伸

- **PCL 的 `VoxelGrid`、Open3D 的 `voxel_down_sample`** 做的就是這件事，你剛寫的是它們的核心。
- **佔據網格（occupancy grid）**：不存平均位置，改存「這格有沒有東西」，就是機器人導航用的地圖。
- **Voxel hashing**（Nießner 2013）：KinectFusion 之類的即時 3D 重建，
  用雜湊表只存「表面附近」的體素，讓重建範圍從一個房間擴展到一整棟樓。key 就是這題的 `(i, j, k)` tuple，
  只是用一個專門設計過的 hash 函數把三個整數混成一個數。
- **近鄰搜尋的空間雜湊**：要找某個點附近的點，只要查它的體素和相鄰 26 個體素，
  不用掃整個點雲——ICP 點雲配準的第一步常常這樣做。

下一題是 2.2 最難的一題：**前綴和 + 雜湊**，把 054 的滑動視窗推廣到有負數的情況。
