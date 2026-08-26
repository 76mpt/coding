# 032-label-maps · 類別名稱與編號的對照表

- 階段：基本功：語法與函式 / 1.6 comprehension 與函式式寫法
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`label_maps`
- 提示：共 4 階（`python trainer.py hint 032-label-maps`）
- 測資：8 筆（`python trainer.py test 032-label-maps`）

────────────────────────────────────────────────────────────────────

訓練分類模型之前，要把**類別名稱**轉成**整數編號**——模型吃的是數字，人看的是名字。
所以每個資料集都需要一組雙向對照表。

實作 `label_maps(names)`，回傳 `(name_to_id, id_to_name)` 兩個 dict：

1. 依**第一次出現的順序**編號，從 **0** 開始。
2. 重複的名稱只算一次（用它第一次出現的編號）。
3. `name_to_id` 是 `{名稱: 編號}`，`id_to_name` 是 `{編號: 名稱}`——**兩個方向都要**。

**範例**

```python
label_maps(["cat", "dog", "cat", "bird"])
->  ({"cat": 0, "dog": 1, "bird": 2},
     {0: "cat", 1: "dog", 2: "bird"})
```

`cat` 第一次出現排 0，`dog` 排 1，第二個 `cat` 跳過（已經有編號了），`bird` 排 2。

```python
label_maps([])                     ->  ({}, {})
label_maps(["a"])                  ->  ({"a": 0}, {0: "a"})
label_maps(["b", "a", "b", "a"])   ->  ({"b": 0, "a": 1}, {0: "b", 1: "a"})
```

最後一個特別注意：**是出現順序，不是字母順序**。`b` 先出現所以拿 0。

**這題要用的三樣東西**

- **去重保序**：你在 `019-dedupe-keep-order` 做過。這裡不用自己寫迴圈，Python 有個一行的慣用法（提示：`dict` 的 key 天生不重複，而且從 3.7 起保證插入順序）。
- **`enumerate`**：把「第幾個」和「是什麼」一起拿到。
- **dict comprehension**：`{鍵運算式: 值運算式 for 變數 in 來源}`。

**限制**
- `names` 是字串的 list，可能是空的。
- 最多 10⁵ 個元素。
- 兩個 dict 的內容要一致（互為反函數）。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 032-label-maps` 驗證
3. 卡住 → `python trainer.py hint 032-label-maps`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 032-label-maps`
