# 017-merge-inventory · 合併庫存

- 階段：基本功：語法與函式 / 1.4 list / tuple / dict / set
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`merge_inventory`
- 提示：共 4 階（`python trainer.py hint 017-merge-inventory`）
- 測資：9 筆（`python trainer.py test 017-merge-inventory`）

────────────────────────────────────────────────────────────────────

兩間分店各有一份庫存清單，用 dict 表示「商品名 → 數量」。
實作 `merge_inventory(a, b)`，把兩份合併成一份。

規則：
1. 兩邊都有的商品，數量**相加**。
2. 只有一邊有的商品，直接帶過去。
3. 合併後數量 **小於或等於 0** 的商品要**從結果中移除**（可能是退貨造成負數）。
4. **不可以修改傳入的 `a` 和 `b`**——呼叫者還要用它們。

**範例**

```
merge_inventory({"apple": 3, "pear": 1}, {"apple": 2, "kiwi": 5})
->  {"apple": 5, "pear": 1, "kiwi": 5}
```

```
merge_inventory({}, {})              ->  {}
merge_inventory({"a": 1}, {"a": -1}) ->  {}          # 相加為 0，移除
merge_inventory({"a": 5}, {"a": -2}) ->  {"a": 3}
merge_inventory({"a": 0}, {})        ->  {}          # 本來就是 0，也要移除
```

**限制**
- 數量是整數，可以是負數或 0。
- key 是字串。
- 回傳的 dict 順序不影響判定。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 017-merge-inventory` 驗證
3. 卡住 → `python trainer.py hint 017-merge-inventory`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 017-merge-inventory`
