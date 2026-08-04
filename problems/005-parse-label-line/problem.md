# 005-parse-label-line · 解析標註檔的一行

- 階段：基本功：語法與函式 / 1.5 字串處理
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`parse_label_line`
- 提示：共 4 階（`python trainer.py hint 005-parse-label-line`）
- 測資：12 筆（`python trainer.py test 005-parse-label-line`）

────────────────────────────────────────────────────────────────────

物件偵測資料集的標註檔通常一行一個框，長這樣：

```
cat, 12, 30, 80, 95
```

五個欄位依序是：**類別名稱、x1、y1、x2、y2**（左上角與右下角座標）。

實作 `parse_label_line(line)`，把一行解析成 dict：

```python
{"label": "cat", "box": [12, 30, 80, 95]}
```

規則：
1. 用逗號 `,` 切分，每個欄位都要**去除頭尾空白**。
2. 類別名稱轉成**小寫**。名稱中間的空白要保留（`"Cat Dog"` → `"cat dog"`）。
3. 四個座標轉成 **int**（可能是負數）。
4. `box` 是一個長度 4 的 list：`[x1, y1, x2, y2]`。

**遇到以下情況要 `raise ValueError`**（訊息內容不限）：

| 情況 | 例子 |
|---|---|
| 欄位數不是 5 個 | `"person, 1, 2, 3"` |
| 座標不是整數 | `"cat, 1, 2, x, 4"` |
| 類別名稱是空的 | `", 1, 2, 3, 4"` |
| 框無效：`x2 <= x1` 或 `y2 <= y1` | `"cat, 10, 10, 5, 20"` |

**範例**

```
parse_label_line("cat, 12, 30, 80, 95")   ->  {"label": "cat", "box": [12, 30, 80, 95]}
parse_label_line("  DOG ,0,0,10,10  ")    ->  {"label": "dog", "box": [0, 0, 10, 10]}
parse_label_line("cat,-5,-5,5,5")         ->  {"label": "cat", "box": [-5, -5, 5, 5]}
parse_label_line("person, 1, 2, 3")       ->  raise ValueError
```

**為什麼要拋例外而不是回傳 None**：
資料集有幾萬行，如果壞掉的那行靜靜地回傳 None，你會在三小時後訓練崩潰時才發現。
**壞掉就要大聲壞掉**，而且要在最靠近問題的地方壞掉。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 005-parse-label-line` 驗證
3. 卡住 → `python trainer.py hint 005-parse-label-line`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 005-parse-label-line`
