# 016-stats-varargs · 可變數量參數的統計摘要

- 階段：基本功：語法與函式 / 1.3 函式：參數與回傳
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`stats`
- 提示：共 4 階（`python trainer.py hint 016-stats-varargs`）
- 測資：9 筆（`python trainer.py test 016-stats-varargs`）

────────────────────────────────────────────────────────────────────

實作 `stats`，接受**任意多個數值**，回傳它們的 `(平均, 最大, 最小)`。

函式簽章**必須是**：

```python
def stats(*values, ndigits=2) -> tuple[float, float, float]:
```

規則：
1. 平均值要**四捨五入到 `ndigits` 位小數**，預設 2 位。
2. 最大值與最小值**原封不動**回傳，不做四捨五入。
3. 一個數值都沒傳的話，`raise ValueError`。

**範例**

```
stats(1, 2, 3)              ->  (2.0, 3, 1)
stats(1, 2, 3, 4)           ->  (2.5, 4, 1)
stats(10, -5, 3)            ->  (2.67, 10, -5)      # 平均 2.666... 進位到 2 位
stats(1, 2, 4, ndigits=3)   ->  (2.333, 4, 1)
stats(5)                    ->  (5.0, 5, 5)
stats()                     ->  raise ValueError
```

**關於 `*values` 和 `ndigits`**

- `*values` 會把**所有位置參數收集成一個 tuple**。呼叫 `stats(1, 2, 3)` 時 `values` 就是 `(1, 2, 3)`。
- 因為 `*values` 會吃掉所有位置參數，**`ndigits` 自動變成 keyword-only**——
  你不可能用位置的方式傳它。所以 `stats(1, 2, 3)` 裡的 `3` 是數值，不是 `ndigits`。

**限制**
- 數值可能是 int 或 float，可能是負數。
- 不需要處理非數值型別。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 016-stats-varargs` 驗證
3. 卡住 → `python trainer.py hint 016-stats-varargs`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 016-stats-varargs`
