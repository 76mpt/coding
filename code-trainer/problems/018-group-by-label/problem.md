# 018-group-by-label · 依類別分組標註

- 階段：基本功：語法與函式 / 1.4 list / tuple / dict / set
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`group_by_label`
- 提示：共 4 階（`python trainer.py hint 018-group-by-label`）
- 測資：6 筆（`python trainer.py test 018-group-by-label`）

────────────────────────────────────────────────────────────────────

物件偵測的標註通常是一串記錄，每筆長這樣：

```python
{"label": "cat", "box": [0, 0, 1, 1]}
```

實作 `group_by_label(records)`，把這串記錄**依 label 分組**，
回傳 `{label: [該類別的所有 box]}`。

每個類別底下的 box **要維持原本在 `records` 裡出現的順序**。

**範例**

```python
records = [
    {"label": "cat", "box": [0, 0, 1, 1]},
    {"label": "dog", "box": [2, 2, 3, 3]},
    {"label": "cat", "box": [4, 4, 5, 5]},
]

group_by_label(records)
->  {
      "cat": [[0, 0, 1, 1], [4, 4, 5, 5]],
      "dog": [[2, 2, 3, 3]],
    }
```

```
group_by_label([])   ->  {}
```

**限制**
- `records` 可能是空 list。
- `label` 是字串，`box` 是 list。
- 同一個 label 可能出現很多次，也可能只出現一次。
- 記錄最多 10⁵ 筆。

**效能要求**：有一筆 10 萬筆記錄的大測資。
「先收集所有不重複的 label，再對每個 label 掃一遍 records」是 O(類別數 × 筆數)，會超時。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 018-group-by-label` 驗證
3. 卡住 → `python trainer.py hint 018-group-by-label`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 018-group-by-label`
