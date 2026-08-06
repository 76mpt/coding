# 019-dedupe-keep-order · 去重但保留順序

- 階段：基本功：語法與函式 / 1.4 list / tuple / dict / set
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`dedupe_keep_order`
- 提示：共 4 階（`python trainer.py hint 019-dedupe-keep-order`）
- 測資：8 筆（`python trainer.py test 019-dedupe-keep-order`）

────────────────────────────────────────────────────────────────────

實作 `dedupe_keep_order(items)`，移除重複的元素但**保留第一次出現的順序**，
回傳 `(去重後的 list, 被移除了幾個)`。

**範例**

```
dedupe_keep_order([3, 1, 3, 2, 1, 1])
->  ([3, 1, 2], 3)
```

`3` 第一次出現保留，後面的 `3` 移除；`1` 保留第一個，後面兩個 `1` 移除。
一共移除 3 個，剩下 `[3, 1, 2]`（順序是它們**第一次出現**的順序）。

```
dedupe_keep_order([])              ->  ([], 0)
dedupe_keep_order([1, 2, 3])       ->  ([1, 2, 3], 0)
dedupe_keep_order(["b","a","b","b"]) ->  (["b", "a"], 2)
dedupe_keep_order([7, 7, 7, 7, 7]) ->  ([7], 4)
```

**限制**
- 元素是可雜湊的（整數、字串、tuple），不會有 list 或 dict。
- 最多 2×10⁵ 個元素。
- 回傳 tuple 或 list 都可以。

**效能要求**：有一筆 20 萬元素的大測資並附時間上限。

**這題真正在考的**：`x in some_list` 和 `x in some_set` 的複雜度**差很多**。
如果你用 list 記錄「看過哪些」，就會是 O(n²)，必然超時。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 019-dedupe-keep-order` 驗證
3. 卡住 → `python trainer.py hint 019-dedupe-keep-order`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 019-dedupe-keep-order`
