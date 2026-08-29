# 039-bounding-box-class · BoundingBox 類別

- 階段：基本功：語法與函式 / 1.8 class 與物件
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`make_boxes`
- 提示：共 4 階（`python trainer.py hint 039-bounding-box-class`）
- 測資：12 筆（`python trainer.py test 039-bounding-box-class`）

────────────────────────────────────────────────────────────────────

你在 031 用 tuple 表示偵測框：`(x1, y1, x2, y2)`。
那樣寫沒錯，但每次要面積就得重打一次 `(x2-x1)*(y2-y1)`，而且 `box[2]` 到底是 x2 還是 width 得靠記憶。

這題把它包成一個**類別**。

**要實作的 `BoundingBox`**

```python
b = BoundingBox(0, 0, 3, 2)

b.x1, b.y1, b.x2, b.y2   ->  0, 0, 3, 2      # 四個屬性
b.width                  ->  3               # x2 - x1
b.height                 ->  2               # y2 - y1
b.area                   ->  6               # width * height
b.center                 ->  (1.5, 1.0)      # 中心點，tuple of float
repr(b)                  ->  "BoundingBox(0, 0, 3, 2)"
```

`width`、`height`、`area`、`center` 是**算出來的**，不是存起來的——
用 `@property` 讓它們像屬性一樣存取（`b.area` 而不是 `b.area()`）。

**要實作的入口函式**

```python
make_boxes(raw)      # raw 是 [(x1,y1,x2,y2), ...]，回傳 [BoundingBox, ...]
```

**範例**

```python
boxes = make_boxes([(0, 0, 3, 2), (1, 1, 5, 5)])

boxes[0].area       ->  6
boxes[1].center     ->  (3.0, 3.0)
repr(boxes[0])      ->  "BoundingBox(0, 0, 3, 2)"
make_boxes([])      ->  []
```

**建構時要驗證**

`x2 <= x1` 或 `y2 <= y1` 時 `raise ValueError`——**在 `__init__` 裡擋**。

> 這是類別相對於 tuple 的第一個好處：**不合法的物件根本建不出來**。
> 用 tuple 的話，`(30, 20, 10, 40)` 是個完全合法的 tuple，錯誤要等到用它的時候才爆。

**`__repr__` 的格式**

```
BoundingBox(0, 0, 3, 2)
```

類別名 + 括號 + 四個座標（逗號空格分隔）。
**慣例是讓 `repr` 看起來像「能把物件建回來的那行程式碼」**——
這樣你在除錯器或 log 裡看到它，可以直接複製貼上重現。

**限制**
- 座標是 int 或 float，可以是負數。
- `raw` 可能是空 list。
- `center` 回傳 tuple，元素是 float。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 039-bounding-box-class` 驗證
3. 卡住 → `python trainer.py hint 039-bounding-box-class`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 039-bounding-box-class`
