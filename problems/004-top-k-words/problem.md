# 004-top-k-words · 詞頻 Top-K

- 階段：基本功：語法與函式 / 1.4 list / tuple / dict / set
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`top_k_words`
- 提示：共 4 階（`python trainer.py hint 004-top-k-words`）
- 測資：9 筆（`python trainer.py test 004-top-k-words`）

────────────────────────────────────────────────────────────────────

實作 `top_k_words(text, k)`，統計文字裡每個單字出現幾次，回傳出現最多的前 k 個。

規則：
1. 以**空白**切分單字（連續多個空白視為一個分隔）。不用處理標點符號。
2. **不分大小寫**：`"The"` 和 `"the"` 算同一個字，回傳時統一用小寫。
3. 回傳 `[(單字, 次數), ...]`，共 k 個（若相異單字不足 k 個，就回傳全部）。
4. 排序規則：**次數由多到少**；次數相同時，**依單字的字典序由小到大**。

**範例**

```
top_k_words("the quick the fox the", 2)
->  [("the", 3), ("fox", 1)]
```

`the` 出現 3 次排第一。`quick` 和 `fox` 都是 1 次，同分時比字典序，`"fox" < "quick"`，所以 fox 勝出。

```
top_k_words("A a b B c", 3)    ->  [("a", 2), ("b", 2), ("c", 1)]
top_k_words("", 3)             ->  []
top_k_words("one two three", 10)  ->  [("one", 1), ("three", 1), ("two", 1)]
top_k_words("x y z", 0)        ->  []
```

**限制**
- `text` 可能是空字串或只有空白。
- `0 <= k`，k 可能大於相異單字數。
- 文字長度最多約 10^6 個字元。

**效能要求**：有一筆 20 萬個單字的大測資並附時間上限。
每個單字都用 `text.split().count(word)` 去數是 O(n²)，會超時。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 004-top-k-words` 驗證
3. 卡住 → `python trainer.py hint 004-top-k-words`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 004-top-k-words`
