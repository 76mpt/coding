# 061-rank-and-null-space · 秩、零空間與它們的垂直關係 — 參考解

## 標準解

```python
def rank_and_null_space(A):
    m, n = len(A), len(A[0])
    R = [[float(x) for x in row] for row in A]      # 複本；A 留著算 dots
    pivots = []
    r = 0                                           # 下一個 pivot 要放的列
    for c in range(n):
        if r == m:
            break
        p = max(range(r, m), key=lambda i: abs(R[i][c]))   # partial pivoting
        if abs(R[p][c]) < 1e-9:
            continue                                # 這一行是自由變數，r 不動
        R[r], R[p] = R[p], R[r]
        piv = R[r][c]
        R[r] = [x / piv for x in R[r]]              # pivot 變成 1
        for i in range(m):                          # 上下都消成 0
            if i != r:
                f = R[i][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[r])]
        pivots.append(c)
        r += 1

    basis = []
    for f in [c for c in range(n) if c not in pivots]:
        v = [0.0] * n
        v[f] = 1.0
        for row, pc in enumerate(pivots):
            v[pc] = -R[row][f]                      # 移項來的負號
        basis.append(v)

    dots = [[sum(a * b for a, b in zip(row, v)) for v in basis] for row in A]
    return len(pivots), basis, dots
```

時間 O(m · n · min(m, n))：每個 pivot 要消 m 列、每列 n 個數。

## 推導一：列運算不改變零空間

三種列運算都對應左乘一個**可逆**矩陣 E（交換、縮放、加倍數各有一種 E）。所以

```
A x = 0   ⟺   E A x = 0      （往右推：兩邊乘 E；往左推：兩邊乘 E⁻¹）
```

把所有列運算合起來，`RREF = E_k … E_1 A`，所以 `RREF x = 0` 和 `A x = 0` 的解完全相同。

## 推導二：基底真的是基底

**它們是解**：RREF 第 row 列（pivot 在行 pc）寫成方程式是

```
x_pc + Σ_{自由行 f} R[row][f] · x_f = 0
```

（其他 pivot 行在這一列都是 0，這正是「pivot 上下都要消成 0」的用處。）
把 `x_f = 1`、其他自由變數 = 0 代進去，得到 `x_pc = −R[row][f]`，就是我們造的向量。

**它們線性獨立**：第 j 個基底向量在第 j 個自由行是 1，其他基底向量在那一行都是 0，
所以任何非零線性組合都不可能是零向量。

**它們張成整個零空間**：任何解 x 由它的自由變數值唯一決定，
而 `x = Σ_f x_f · (第 f 個基底向量)` 在自由行上跟 x 一致，pivot 行也被同一組方程式決定，所以相等。

基底向量個數 = 自由變數個數 = `n − rank`。這就是**秩—零化度定理**。

## 為什麼 dots 全為 0 證明了什麼

`A v = 0` 的第 i 個分量就是 `A[i] · v`。所以 `dots` 全為 0 等於直接驗證了「每個基底向量都是解」。

這個檢查**用原始的 A** 而不是 RREF，所以它能抓到你 RREF 過程中的任何錯誤——
不管是消錯、換錯列還是漏消 pivot 上方的數，最後 `A v` 都不會是 0。

## 四個基本子空間

這題碰到了其中兩個。完整的圖是這樣（A 是 m×n、秩 r）：

| 子空間 | 住在 | 維度 | 跟誰垂直 |
|---|---|---|---|
| 列空間 row(A)（列的所有線性組合） | ℝⁿ | r | 零空間 |
| 零空間 null(A)（`A x = 0` 的解） | ℝⁿ | n − r | 列空間 |
| 行空間 col(A)（行的所有線性組合） | ℝᵐ | r | 左零空間 |
| 左零空間 null(Aᵀ)（`Aᵀ y = 0` 的解） | ℝᵐ | m − r | 行空間 |

ℝⁿ 被切成列空間和零空間兩塊，ℝᵐ 被切成行空間和左零空間兩塊，每一對都互相垂直、維度加起來剛好填滿。
**列空間和行空間的維度都是 r**——這件事一點都不顯然（列和行根本住在不同的空間），
但 RREF 看得出來：pivot 的個數既是獨立列數，也是獨立行數。

這張表是 Gilbert Strang 整門 MIT 18.06 的骨架，蘇柏青第 7 講「矩陣相關子空間的維度」講的就是它。

## 另一種寫法：SVD

```python
import numpy as np
U, S, Vt = np.linalg.svd(np.asarray(A, dtype=float))
rank = int((S > 1e-9).sum())
null_basis = Vt[rank:]          # 正交單位的零空間基底
```

`np.linalg.matrix_rank` 和 `scipy.linalg.null_space` 都是這樣做的。SVD 的好處是：

- **數值上穩健得多**：RREF 靠「這個數是不是 0」做判斷，浮點誤差下這個判斷很脆弱；
  SVD 看奇異值的大小，可以清楚看到「幾乎相依」的程度
- **給出的基底是正交單位的**——等於幫你把 RREF 的基底再做一次 060 的 Gram-Schmidt

代價是看不出 pivot 結構，也比較慢。M0.5 SVD 會正式處理。

## 常見錯誤

1. **只消 pivot 下方的數（列梯形，不是簡化列梯形）**——pivot 上方留著非零數，
   basis 公式就錯了，`dots` 不會是 0。隱藏測資 `[[1,2,1,1],[2,4,0,6],[1,2,-1,5]]` 專門抓這個。

2. **自由變數那一行也讓 `r` 前進**——之後的 pivot 會放錯列，秩算多或算少。
   `[[0,0,1],[0,0,2]]` 會抓到。

3. **用 `== 0` 判斷**——除法之後的 `1e-17` 不等於 0，會被當成 pivot。

4. **忘了負號**——`v[pc] = R[row][f]`。`dots` 會變成 `2 × A[i][f]` 之類的東西，而不是 0。

5. **直接修改 A 而不是複本**——`dots` 算出來會用到 RREF 的列，而 RREF 的列跟 basis 的內積**也是 0**，
   所以檢查形同虛設，錯誤的 RREF 也抓不到。

6. **沒處理換列**——假設第一列的第一個數一定不是 0。`[[0,1],[1,0]]` 會在第 0 行找不到 pivot，
   把一個滿秩矩陣算成秩 1。

## 延伸

零空間是 3D 視覺裡最常解的問題之一：

- **M2.3 Homography（DLT）**：4 組對應點排成 8×9 的矩陣 A，要找的單應矩陣 h 就是 `A h = 0` 的解——
  A 的零空間。有雜訊時零空間不存在，改用 SVD 取最小奇異值對應的向量。
- **M2.4 基礎矩陣（八點法）**：同樣是 `A f = 0`，f 是 9 維向量。
- **Bundle Adjustment 的規範自由度（gauge freedom）**：單目 SLAM 的 Jacobian 有一個 7 維零空間
  （3 平移 + 3 旋轉 + 1 尺度）——整個場景一起平移、旋轉、縮放，觀測完全不變。
  不處理這個零空間，最佳化器會在那 7 個方向上亂漂。

這題做完 M0.2 就收完了。下一步 M0.3 投影與最小平方，會把「列空間和零空間垂直」這件事
變成「殘差和行空間垂直」——你在 030 已經看過它的一維版本。
