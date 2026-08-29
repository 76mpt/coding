# 044-rotate-points · 手寫旋轉矩陣

- 階段：前置：高中數學重補（公式與計算流利度） / M00.5 三角函數、旋轉與複數
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`rotate_points`
- 提示：共 4 階（`python trainer.py hint 044-rotate-points`）
- 測資：10 筆（`python trainer.py test 044-rotate-points`）

────────────────────────────────────────────────────────────────────

二維旋轉矩陣：把平面上的點**繞原點逆時針轉 θ 弧度**。

```
        ⎡ cos θ   −sin θ ⎤
R(θ) =  ⎢                 ⎥
        ⎣ sin θ    cos θ ⎦
```

作用在點 `(x, y)` 上：

```
x' = x·cos θ − y·sin θ
y' = x·sin θ + y·cos θ
```

實作 `rotate_points(points, theta)`：把每個點轉 θ 弧度，回傳新的座標 list。

**θ 的單位是弧度**（radian），不是度數。`math.cos` / `math.sin` 吃的也是弧度。

**範例**

```python
import math

rotate_points([(1, 0)], math.pi / 2)   ->  [(0.0, 1.0)]        # 轉 90°：x 軸 → y 軸
rotate_points([(1, 0)], math.pi)       ->  [(-1.0, 0.0)]       # 轉 180°
rotate_points([(3, 4)], 0.0)           ->  [(3.0, 4.0)]        # 轉 0 度不變
rotate_points([], 1.0)                 ->  []
```

```python
rotate_points([(1, 0), (0, 1)], math.pi / 4)
->  [(0.7071067812, 0.7071067812), (-0.7071067812, 0.7071067812)]
```

## 這題要自己驗證的性質

**旋轉不改變長度。** 這是「旋轉」這件事的定義——它只轉方向，不拉不縮。

```python
p = (3, 4)                     # 長度 5
q = rotate_points([p], 1.234)[0]
math.hypot(*q)                 # 也是 5（差在 1e-15 以內）
```

寫完之後**自己驗一次**：隨便挑幾個點、隨便挑一個角度，確認長度沒變。
這比對答案更能確認你的矩陣沒寫錯——如果 `cos`/`sin` 放錯位置或符號寫反，
長度通常就會跑掉。

（背後的原因：`R` 的兩個行向量 `(cos θ, sin θ)` 和 `(−sin θ, cos θ)` 
都是單位長度而且互相垂直——那正是 `sin²θ + cos²θ = 1` 的幾何意義。）

**限制**
- `points` 是 `(x, y)` 的序列，可能是空的。
- 座標是 int 或 float。
- 回傳每個點是 tuple 或 list 都可以，元素是 float。
- 判定使用近似比較，容差 10⁻⁹。
- 最多 10⁵ 個點。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 044-rotate-points` 驗證
3. 卡住 → `python trainer.py hint 044-rotate-points`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 044-rotate-points`
