# 069-weighted-least-squares · 加權最小平方與過定方程組 — 參考解

## 標準解

```python
def weighted_lstsq(A, b, w):
    m = len(A)
    n = len(A[0]) if m else 0

    # normal equation: (A^T W A) x = A^T W b
    # W = diag(w) 從來不建出來，wᵢ 只是乘進去的純量
    M = [[0.0] * n for _ in range(n)]
    v = [0.0] * n
    for i in range(m):
        wi, row, bi = w[i], A[i], b[i]
        for j in range(n):
            wa = wi * row[j]
            for k in range(j, n):          # M 對稱，只算上三角
                M[j][k] += wa * row[k]
            v[j] += wa * bi
    for j in range(n):
        for k in range(j):
            M[j][k] = M[k][j]

    # 高斯消去法 + 部分選軸
    aug = [M[j][:] + [v[j]] for j in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        p = aug[col][col]
        for r in range(col + 1, n):
            f = aug[r][col] / p
            if f:
                for c in range(col, n + 1):
                    aug[r][c] -= f * aug[col][c]

    x = [0.0] * n                          # 回代
    for j in range(n - 1, -1, -1):
        s = aug[j][n] - sum(aug[j][k] * x[k] for k in range(j + 1, n))
        x[j] = s / aug[j][j]

    residuals = [b[i] - sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
    dots = [sum(w[i] * A[i][j] * residuals[i] for i in range(m)) for j in range(n)]
    wrss = sum(w[i] * residuals[i] ** 2 for i in range(m))
    return (x, residuals, dots, wrss)
```

## 推導：兩條路，同一個結果

**路一：微分。** 目標函數 `f(x) = Σᵢ wᵢ (bᵢ − Σⱼ Aᵢⱼ xⱼ)²`。對 `xₖ` 偏微分：

```
∂f/∂xₖ = Σᵢ 2 wᵢ (bᵢ − (Ax)ᵢ) · (−Aᵢₖ) = −2 Σᵢ wᵢ Aᵢₖ rᵢ
```

設成 0 就得到 `Σᵢ wᵢ Aᵢₖ rᵢ = 0`，對每個 k 都成立——**這正是 `dots` 全為 0**。
把 `rᵢ = bᵢ − (Ax)ᵢ` 代回去展開，就是 `AᵀWA x = AᵀWb`。

**路二：幾何。** `⟨u, v⟩_W = Σ wᵢ uᵢ vᵢ` 是內積（`w > 0` 保證正定），
所以 `‖u‖_W = √⟨u, u⟩_W` 是個合法的範數。要最小化的 `Σ wᵢ rᵢ²` 就是 `‖b − Ax‖²_W`。
在任何內積空間裡，「點到子空間的最短距離」都發生在**垂足**，
而垂足的特徵是「殘差垂直於子空間的每一個基底向量」——在這裡就是 `A` 的 n 個行向量。

兩條路給同一組方程式。微分那條機械、不會錯；幾何那條讓你知道換了權重為什麼什麼都沒變。
**這兩種看法你都要有**：M0.8 手推反向傳播時用的是微分那套，
M0.5 的 SVD 和 M2 的三角測量用的是幾何那套。

## 另一種做法：不要碰 normal equation

`AᵀWA` 有個問題：它的條件數是 `A` 的**平方**。

```
κ(AᵀA) = κ(A)²
```

`A` 的條件數 1000（在實務資料裡很常見）會讓 `AᵀA` 變成 10⁶，
雙精度浮點數只有約 16 位有效數字，你一下就吃掉 6 位。
數值線性代數的標準做法是**完全不要建出 `AᵀA`**：

```python
import numpy as np
s = np.sqrt(w)                                   # 把權重吸收進矩陣
Aw, bw = s[:, None] * A, s * b                   # 最小化 ‖Aw x − bw‖²
Q, R = np.linalg.qr(Aw)                          # 060 你手寫過 Gram-Schmidt
x = np.linalg.solve(R, Q.T @ bw)                 # R 是上三角，回代就好
```

把權重寫成 `√wᵢ` 吸收進每一列（row），加權問題就變成普通最小平方——
這個小技巧在實務上到處都是。然後用 QR 分解解它，條件數只有 `κ(A)`，不是平方。
`np.linalg.lstsq` 內部走的是 SVD，更穩但更慢。

這題要你手寫 normal equation，是因為**你得先知道它在算什麼**，
才有資格嫌它數值不好。條件數本身是 M0.6 的主題。

## 複雜度

- 建 `M`、`v`：**O(m n²)**。m 可以很大（2000），n 很小（≤ 6），這一項是主要成本
- 高斯消去：**O(n³)**，n ≤ 6 所以可以忽略
- 空間：**O(n² + m)**。真的建出 `W` 會變成 O(m²)，m = 2000 就是 400 萬個元素，那是這題要你避開的坑

## 常見錯誤

1. **`wᵢ` 只乘一次** — 寫成 `M[j][k] += w[i] * A[i][j] * A[i][k]` 是對的，
   但如果你先把 `A` 的每一列乘上 `wᵢ` 再做 `AᵀA`，權重就被乘了兩次（變成 `wᵢ²`）。
   正確的「吸收進矩陣」要用 `√wᵢ`，不是 `wᵢ`。第三筆測資（`w = [1, 1, 100]`）會抓到：
   你會得到 `w = [1, 1, 10000]` 的答案。
2. **`residuals` 乘了權重** — 題目明說 `residuals` 是**不加權**的 `bᵢ − (Ax)ᵢ`。
   權重只出現在 `dots` 和 `wrss` 裡。
3. **真的建出 `W`** — `[[w[i] if i == j else 0 for j in range(m)] for i in range(m)]`。
   建出來本身只要 80 毫秒左右，不痛；痛的是接著老實算 `AᵀW`——
   那是 `n·m²` 次乘法，`m = 2000` 時實測 750 毫秒，直接撞上限。
   小測資完全看不出來，大測資那筆才會現形。
4. **回代寫錯方向** — 從 `j = 0` 往下算，但 `x[0]` 需要 `x[1]`、`x[2]`…
   回代一定是從最後一個未知數往前。n = 1 那筆測資過了但 n = 3 那筆錯，就是這個。
5. **沒有選軸，又剛好遇到 0 樞紐** — 這題保證 `AᵀWA` 可逆，所以數學上不會真的除以 0，
   但消去過程中某一列的首項可能變成很小的數，答案的精度會掉到 `1e-6` 以下。
6. **`n` 從 `A` 的列數去推** — `len(A)` 是 m 不是 n，要用 `len(A[0])`。
   第七筆測資是方陣（m = n），這個錯誤在那裡不會現形，其他筆會。

## 延伸

**這一節到這裡結束了。** 065 的投影矩陣、066 的直線擬合、這題的加權一般化，
是同一個東西的三個版本：把 `b` 投影到 `A` 的行空間，殘差垂直。

接下來這個概念會一直回來：

- **M0.5 SVD 與偽逆**：當 `A` 的行向量**不**獨立時（`AᵀA` 不可逆），normal equation 就死了。
  偽逆 `A⁺` 是那時候的答案，而它是用 SVD 定義的。這題的「保證可逆」那條限制，
  到 M0.5 會被拆掉。
- **M0.6 條件數**：為什麼 `AᵀA` 是個數值上的壞主意，以及該怎麼量化「壞」。
- **M1 最佳化**：非線性最小平方（Gauss-Newton、Levenberg-Marquardt）
  每一步都在解一個這題這樣的加權線性最小平方——雅可比矩陣當 `A`，殘差當 `b`。

**跟你的方向的關係**：這題的 `w` 在 SLAM 裡有名字，叫**資訊矩陣**（information matrix），
是量測共變異數的反矩陣 `Σ⁻¹`。`Σᵢ wᵢ rᵢ²` 就是**馬氏距離**（Mahalanobis distance）的平方，
而 bundle adjustment 的目標函數正是一大堆這種項加起來。
你今天寫的 `M = AᵀWA` 在那裡叫 Hessian 的近似，`v = AᵀWb` 叫梯度。

再往前一步：真實資料有離群點（誤匹配的特徵點），平方誤差會被它們拉爛。
解法是 **IRLS**（iteratively reweighted least squares）——
每一輪根據上一輪的殘差重算 `wᵢ`（殘差大的點權重壓低，例如 Huber loss），
然後再解一次這題。所以 `w` 不是給定的，是算出來的，而**內層那個解就是你剛寫的函式**。
