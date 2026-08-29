# 042-complexity-showdown · 同一件事的四種寫法

- 階段：基本功：語法與函式 / 1.9 複雜度直覺
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`common_labels`
- 提示：共 4 階（`python trainer.py hint 042-complexity-showdown`）
- 測資：9 筆（`python trainer.py test 042-complexity-showdown`）

────────────────────────────────────────────────────────────────────

這題的答案很簡單，**難的是讓它夠快**。

實作 `common_labels(a, b)`：回傳同時出現在 `a` 和 `b` 裡的標籤，
**依它們在 `a` 裡第一次出現的順序**，而且**不重複**。

**範例**

```python
common_labels(["cat", "dog", "bus", "cat"], ["bus", "cat"])   ->  ["cat", "bus"]
common_labels(["a", "b"], ["c"])                              ->  []
common_labels([], ["x"])                                      ->  []
common_labels(["x", "x", "x"], ["x"])                         ->  ["x"]
```

第一個範例：`cat` 在 a 的第 0 位、`bus` 在第 2 位，所以順序是 `["cat", "bus"]`。
第二個 `cat` 重複，丟掉。`dog` 不在 b 裡面，丟掉。

## 效能要求

有一筆測資是 **`a` 和 `b` 各 10 萬個元素**，時限 1.5 秒。

最直觀的寫法會超時：

```python
[x for x in a if x in b]          # b 是 list → 每次 in 都是 O(n) → 總共 O(n²)
```

10⁵ × 10⁵ = **10¹⁰ 次比較**，跑幾十分鐘。

**關鍵是 `x in 某容器` 的成本跟容器的型別有關**：

| 容器 | `in` 的複雜度 | 為什麼 |
|---|---|---|
| `list` / `tuple` | **O(n)** | 從頭掃到尾 |
| `set` / `dict` | **O(1)** 平均 | 算 hash 直接跳到位置 |
| 排序過的 list + `bisect` | O(log n) | 二分搜尋 |

**同一份邏輯，只要把「被查的那個容器」換成 `set`，複雜度就從 O(n²) 掉到 O(n)。**

## 兩個順序陷阱

1. **順序依 `a`**，不是依 b、也不是字典序。
2. **`set` 不保證順序**——所以 `list(set(a) & set(b))` 雖然一行就寫完，
   但順序是不確定的（同一份程式跑兩次可能不一樣）。**這題不能用。**

**限制**
- `a`、`b` 是字串 list，可能是空的。
- 各最多 10⁵ 個元素。
- 回傳 list。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 042-complexity-showdown` 驗證
3. 卡住 → `python trainer.py hint 042-complexity-showdown`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 042-complexity-showdown`
