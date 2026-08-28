# 036-parse-annotation · 標註行解析器與自訂例外

- 階段：基本功：語法與函式 / 1.7 例外處理與檔案 I/O
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`parse_annotation`
- 提示：共 4 階（`python trainer.py hint 036-parse-annotation`）
- 測資：12 筆（`python trainer.py test 036-parse-annotation`）

────────────────────────────────────────────────────────────────────

標註檔的每一行長這樣：

```
cat 10 20 30 40
```

格式是 `類別名稱 x1 y1 x2 y2`，用空白分隔，共 **5 個欄位**。

實作 `parse_annotation(line)`，回傳 `(label, [x1, y1, x2, y2])`，座標是 **int**。

**壞資料要拋自訂例外**

真實的標註檔一定有壞行——手動編輯打錯、工具版本不一致、檔案截斷。
這題要你定義一個**自訂例外類別 `BadAnnotation`**，遇到下列情況就拋它：

| 情況 | 例子 |
|---|---|
| 欄位數不是 5 | `"cat 10 20 30"` |
| 座標不是整數 | `"cat 10 20 30 abc"` |
| `x2 <= x1` 或 `y2 <= y1` | `"cat 30 20 10 40"` |

`BadAnnotation` 必須繼承 `ValueError`。

**範例**

```python
parse_annotation("cat 10 20 30 40")      ->  ("cat", [10, 20, 30, 40])
parse_annotation("  dog  1 2 3 4  ")     ->  ("dog", [1, 2, 3, 4])     # 多餘空白要容忍
parse_annotation("cat 10 20 30")         ->  BadAnnotation
parse_annotation("cat 10 20 30 abc")     ->  BadAnnotation
parse_annotation("cat 30 20 10 40")      ->  BadAnnotation             # x2 <= x1
```

**為什麼要自訂例外，不直接用 ValueError**

因為呼叫端要**分辨得出來**。用 `ValueError` 的話：

```python
try:
    label, box = parse_annotation(line)
except ValueError:        # 這裡也會接到 int() 內部拋的、其他函式拋的...
    ...
```

自訂一個類別，呼叫端就能精準地只接你的錯誤：`except BadAnnotation:`。
而讓它**繼承 `ValueError`**，是為了讓「只想粗略接住所有值錯誤」的既有程式碼也還能運作——
這是設計例外階層的標準作法。

**限制**
- `line` 是字串，可能有多餘的頭尾空白。
- 座標是十進位整數，可能是負數。
- 例外訊息的內容不限，但**類別名稱必須是 `BadAnnotation`**。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 036-parse-annotation` 驗證
3. 卡住 → `python trainer.py hint 036-parse-annotation`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 036-parse-annotation`
