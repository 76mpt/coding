# 051-compose-linear-maps · 合成變換就是矩陣相乘

- 階段：數學基礎（Tier 0：沒有就寸步難行） / M0.1 向量、矩陣與線性映射
- 語言：Python　難度：warmup　估時：40 分　互動方式：實作函式
- 要實作的入口：`compose_report`
- 提示：共 4 階（`python trainer.py hint 051-compose-linear-maps`）
- 測資：8 筆（`python trainer.py test 051-compose-linear-maps`）

────────────────────────────────────────────────────────────────────

## 背景

一個 2×2 矩陣 `M = [[a, b], [c, d]]` 作用在點 `p = (x, y)` 上，定義是

```
M p = (a·x + b·y,  c·x + d·y)
```

把矩陣看成「對平面做的一件事」（旋轉、縮放、剪切、投影），而不是四個數字。

這一題要你親手驗證線性代數最核心的一句話：

> **先做 B 再做 A，等於做一次 C = A·B。**

順帶驗證第二件事：**做的順序有差**，`A·B` 通常不等於 `B·A`。

## 要實作的函式

```python
def compose_report(A, B, points):
```

- `A`、`B`：2×2 矩陣，格式是「兩個列」`[[a, b], [c, d]]`
- `points`：點的串列，每個點是 `[x, y]`

回傳一個 dict：

| 鍵 | 型別 | 內容 |
|---|---|---|
| `"sequential"` | list | 每個點**先套 B、再套 A** 的結果 |
| `"combined"` | list | 先算出 `C = A·B`，每個點**只套一次 C** 的結果 |
| `"product"` | list | 矩陣 `C = A·B` 本身，一樣是 `[[?, ?], [?, ?]]` |
| `"same"` | bool | `sequential` 與 `combined` 是否逐點相等（容差 `1e-9`） |
| `"order_matters"` | bool | `A·B` 與 `B·A` 是否**不同**（不同為 `True`，容差 `1e-9`） |

所有座標與矩陣元素都回傳 `float`。

## 範例一

```python
A = [[0, -1], [1, 0]]      # 逆時針轉 90 度
B = [[2, 0], [0, 2]]       # 放大 2 倍
points = [[1, 0]]
```

先放大 `(1,0) → (2,0)`，再旋轉 `→ (0,2)`。

```python
{
  "sequential": [[0.0, 2.0]],
  "combined":   [[0.0, 2.0]],
  "product":    [[0.0, -2.0], [2.0, 0.0]],
  "same": True,
  "order_matters": False
}
```

旋轉和「等比例放大」剛好可以交換，所以 `order_matters` 是 `False`。

## 範例二（這個範例會戳破一個常見誤解）

```python
A = [[0, -1], [1, 0]]      # 逆時針轉 90 度
B = [[1, 1], [0, 1]]       # 沿 x 方向剪切
points = [[1, 0], [0, 1]]
```

```python
{
  "sequential": [[0.0, 1.0], [-1.0, 1.0]],
  "combined":   [[0.0, 1.0], [-1.0, 1.0]],
  "product":    [[0.0, -1.0], [1.0, 1.0]],
  "same": True,
  "order_matters": True
}
```

「先剪切再旋轉」和「先旋轉再剪切」是兩個不同的變換，所以 `order_matters` 是 `True`。

## 限制

- 矩陣固定 2×2，點固定二維
- `points` 可能是空串列，這時 `sequential` 與 `combined` 都是 `[]`，`same` 是 `True`
- 元素是整數或浮點數，可能有負數
- **不要用 numpy**。這一題就是要你把定義寫出來，看清楚裡面在做什麼
- 比較浮點數請用容差 `1e-9`，不要用 `==`

## 你應該親眼看到的事

`same` 永遠是 `True`——這不是巧合，而是矩陣乘法**當初就是照這樣定義出來的**。
矩陣乘法的公式長那個樣子，唯一的理由就是要讓它等於「兩個變換接起來」。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 051-compose-linear-maps` 驗證
3. 卡住 → `python trainer.py hint 051-compose-linear-maps`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 051-compose-linear-maps`
