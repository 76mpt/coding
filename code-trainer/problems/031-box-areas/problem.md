# 031-box-areas · 篩選偵測框的面積

- 階段：基本功：語法與函式 / 1.6 comprehension 與函式式寫法
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`box_areas`
- 提示：共 4 階（`python trainer.py hint 031-box-areas`）
- 測資：9 筆（`python trainer.py test 031-box-areas`）

────────────────────────────────────────────────────────────────────

物件偵測的輸出是一堆**邊界框（bounding box）**，每個框用四個數字表示：

```
(x1, y1, x2, y2)     左上角 (x1, y1)、右下角 (x2, y2)
面積 = (x2 - x1) × (y2 - y1)
```

實作 `box_areas(boxes, min_area=0)`：算出每個框的面積，**只保留面積 ≥ `min_area` 的**，依原本的順序回傳 list。

**範例**

```python
boxes = [(0, 0, 2, 3), (1, 1, 1, 1), (0, 0, 10, 10)]

box_areas(boxes, 1)   ->  [6, 100]        # 中間那個面積 0，被濾掉
box_areas(boxes)      ->  [6, 0, 100]     # 預設 min_area=0，全部保留
box_areas([], 0)      ->  []
box_areas([(2, 3, 5, 7)])       ->  [12]        # 3 × 4
box_areas([(-2, -2, 0, 0)])     ->  [4]         # 座標可以是負的
```

**這題要用 comprehension 寫**

這是節點 1.6 的第一題，重點是把「走訪 → 轉換 → 過濾」壓成一行：

```python
[ 要放進去的東西  for 變數 in 來源  if 保留的條件 ]
       ↑              ↑                ↑
     轉換           走訪            過濾
```

順序跟你腦中想的相反——**先寫「要什麼」，再寫「從哪來」，最後寫「留哪些」**。

每個框是四個數字的 tuple，comprehension 的 `for` 可以**直接解包**成四個名字，不用寫 `box[0]`、`box[1]`。

**限制**
- `boxes` 是 tuple 或 list 的序列，每個有 4 個數字（int 或 float）。
- 保證 `x2 >= x1` 且 `y2 >= y1`，所以面積不會是負的。
- `boxes` 可能是空的。
- 最多 10⁵ 個框。
- **面積 0 的框在 `min_area=0` 時要保留**（`0 >= 0` 成立）。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 031-box-areas` 驗證
3. 卡住 → `python trainer.py hint 031-box-areas`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 031-box-areas`
