# 041-detection-dunders · 讓物件能比較、排序、去重

- 階段：基本功：語法與函式 / 1.8 class 與物件
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`rank_detections`
- 提示：共 4 階（`python trainer.py hint 041-detection-dunders`）
- 測資：10 筆（`python trainer.py test 041-detection-dunders`）

────────────────────────────────────────────────────────────────────

偵測模型吐出來的每個結果有 **框、類別、信心分數**。
實務上你要做三件事：**依分數排序**、**去掉重複的**、**判斷兩個結果是不是同一個**。

Python 的做法不是寫 `d.compare_to(other)`，而是實作 **dunder 方法**，
讓內建的 `sorted()`、`set()`、`==` 直接吃你的物件。

**要實作的 `Detection`**

```python
d = Detection("cat", (0, 0, 3, 2), 0.9)

d.label      ->  "cat"
d.box        ->  (0, 0, 3, 2)
d.score      ->  0.9

repr(d)      ->  "Detection('cat', (0, 0, 3, 2), 0.9)"
```

| dunder | 用來支援 | 語意 |
|---|---|---|
| `__repr__` | `repr(d)`、除錯輸出 | 格式見上面 |
| `__eq__` | `d1 == d2`、`in`、去重 | **label 和 box 都相同就算相等**（**分數不算**） |
| `__hash__` | 放進 `set`、當 dict 的 key | 跟 `__eq__` 用同一組欄位 |
| `__lt__` | `sorted()`、`min`/`max` | **依分數比大小** |

**為什麼 `__eq__` 不看分數**

同一個物體被模型偵測兩次，框和類別一樣但分數可能是 0.91 和 0.90——
**那是重複，該去掉一個**。所以「是不是同一個偵測」由 label + box 決定，不看分數。

**要實作的入口函式**

```python
rank_detections(raw)
```

`raw` 是 `[(label, box, score), ...]`。要做三步：

1. 建成 `Detection` 物件
2. **去重**——label + box 相同的只留**第一個出現的**
3. **依分數由高到低排序**，分數相同時**依 label 字典序由小到大**

回傳排好的 list。

**範例**

```python
raw = [
    ("cat", (0, 0, 3, 2), 0.9),
    ("dog", (5, 5, 9, 9), 0.7),
    ("cat", (0, 0, 3, 2), 0.5),   # 跟第一個重複（框和類別一樣），丟掉
]

rank_detections(raw)
->  [Detection('cat', (0, 0, 3, 2), 0.9), Detection('dog', (5, 5, 9, 9), 0.7)]
```

**`__eq__` 和 `__hash__` 必須成對**

Python 的規則：**相等的物件必須有相同的 hash**。
只寫 `__eq__` 不寫 `__hash__` 的話，Python 會把你的類別標成 unhashable，
**放進 `set` 會直接 TypeError**。

最簡單的做法是讓 `__hash__` 回傳「那組決定相等性的欄位」的 tuple 的 hash。

**限制**
- `box` 是 4 個數字的 tuple。
- `score` 是 0 到 1 的 float。
- `raw` 可能是空 list。
- 最多 10⁵ 筆。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 041-detection-dunders` 驗證
3. 卡住 → `python trainer.py hint 041-detection-dunders`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 041-detection-dunders`
