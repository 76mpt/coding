# 033-label-stats · 標籤合法性檢查

- 階段：基本功：語法與函式 / 1.6 comprehension 與函式式寫法
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`label_stats`
- 提示：共 4 階（`python trainer.py hint 033-label-stats`）
- 測資：10 筆（`python trainer.py test 033-label-stats`）

────────────────────────────────────────────────────────────────────

訓練分類模型時，標籤必須落在 `[0, num_classes)` 這個範圍。
超出範圍的標籤會讓 `CrossEntropyLoss` 直接崩潰（或更糟——安靜地算出垃圾），所以**餵進模型之前一定要檢查**。

實作 `label_stats(labels, num_classes)`，回傳三個東西：

```
(全部合法嗎, 合法的有幾個, 出現過哪些合法標籤)
     bool          int              set
```

「合法」的定義是 `0 <= label < num_classes`（左閉右開，跟 `range` 一樣）。

**範例**

```python
label_stats([0, 1, 2, 1], 3)  ->  (True,  4, {0, 1, 2})
label_stats([0, 3, 1], 3)     ->  (False, 2, {0, 1})      # 3 不合法（要 < 3）
label_stats([-1, -2], 3)      ->  (False, 0, set())       # 負數也不合法
label_stats([2, 2, 2], 3)     ->  (True,  3, {2})         # 相異只有一個
label_stats([], 5)            ->  (True,  0, set())       # 空的算全部合法
```

**空 list 為什麼是 `True`**

這不是特例，是 `all()` 的定義。「所有元素都滿足條件」在沒有元素時**自動成立**——
這叫**空真（vacuous truth）**：你找不到任何一個反例。

```python
all([])   # True
any([])   # False
```

記法：`all` 找的是「有沒有反例」，沒東西就沒反例；`any` 找的是「有沒有例子」，沒東西就沒例子。

**這題要用的三個工具**

| 工具 | 這題拿來做什麼 |
|---|---|
| `all(...)` | 判斷是否全部合法 |
| `sum(...)` | 數出合法的有幾個 |
| `{... for ...}` | set comprehension，收集相異的合法標籤 |

三個都吃 **generator expression**，不要先建中間的 list。

**限制**
- `labels` 是整數 list，可能是空的，可能有負數。
- `num_classes >= 1`。
- 最多 10⁶ 個元素——**有一筆大測資的第一個元素就不合法**，`all()` 的短路特性會讓你瞬間得到答案。
- 回傳的第三項必須是 `set`。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 033-label-stats` 驗證
3. 卡住 → `python trainer.py hint 033-label-stats`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 033-label-stats`
