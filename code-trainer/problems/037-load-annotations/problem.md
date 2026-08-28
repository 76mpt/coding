# 037-load-annotations · 壞行跳過，好行保留

- 階段：基本功：語法與函式 / 1.7 例外處理與檔案 I/O
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`load_annotations`
- 提示：共 4 階（`python trainer.py hint 037-load-annotations`）
- 測資：10 筆（`python trainer.py test 037-load-annotations`）

────────────────────────────────────────────────────────────────────

上一題（036）的 `parse_annotation` 遇到壞行就拋例外。
但真實情況是：**一萬行的標註檔裡有三行壞掉，你不能因此整個訓練不跑**。

實作 `load_annotations(lines)`，逐行處理，回傳 `(好的標註, 壞行的報告)`：

```
( [(label, [x1,y1,x2,y2]), ...],      ← 解析成功的，依原順序
  [(行號, 原始內容), ...] )            ← 失敗的，行號從 1 開始
```

**規則**

1. **空白行**（完全空的、或只有空白字元）**直接略過**，不算好也不算壞。
2. 其他行用 036 的規格解析：`label x1 y1 x2 y2`，五個欄位，座標是整數，且 `x2 > x1`、`y2 > y1`。
3. 解析失敗的行進「壞行報告」，記 `(行號, 原始內容)`——**行號用原本的行號**（含被略過的空白行一起數），**內容保留原樣不要 strip**。
4. **不管有幾行壞掉，函式都不該拋例外。**

**範例**

```python
lines = [
    "cat 10 20 30 40",
    "",
    "dog 1 2 x 4",
    "bus 0 0 5 5",
]

load_annotations(lines)
->  ( [("cat", [10,20,30,40]), ("bus", [0,0,5,5])],
      [(3, "dog 1 2 x 4")] )
```

`"dog 1 2 x 4"` 在第 **3** 行——空白行雖然被略過，**但它還是佔一個行號**。

```python
load_annotations([])            ->  ([], [])
load_annotations(["   ", ""])   ->  ([], [])      # 全是空白行
load_annotations(["bad"])       ->  ([], [(1, "bad")])
```

**這題在練什麼**

> **拋出例外的層級 ≠ 處理例外的層級。**

`parse_annotation` 只負責說「這行壞了」，**它不知道也不該知道**呼叫端想怎麼辦。
這個函式才是決定「跳過並記錄」的人。換一個呼叫端，可能決定「一壞就中止」——
那也是它的自由，解析函式不用改。

你要在這裡**自己實作 `parse_annotation`**（或把 036 的貼過來），
然後用 `try/except` 把它包起來。

**限制**
- `lines` 是字串 list，可能是空的。
- 最多 10⁵ 行。
- 兩個回傳值都是 list，順序都依原本的行順序。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 037-load-annotations` 驗證
3. 卡住 → `python trainer.py hint 037-load-annotations`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 037-load-annotations`
