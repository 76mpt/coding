# 053-compact-detections · 就地過濾偵測框

- 階段：資料結構與演算法（LeetCode 風格） / 2.1 陣列與雙指標
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`compact`
- 提示：共 4 階（`python trainer.py hint 053-compact-detections`）
- 測資：10 筆（`python trainer.py test 053-compact-detections`）

────────────────────────────────────────────────────────────────────

物件偵測模型吐出一堆偵測框，每個框有一個信心分數。後處理的第一步是**丟掉分數太低的框**。

給一個整數陣列 `scores` 和一個門檻 `threshold`，把所有 `scores[i] < threshold` 的元素移掉，
**保留下來的元素要維持原本的相對順序**。

實作 `compact(scores, threshold)`，回傳 `(保留了幾個, 保留下來的那幾個元素)`。

**範例**

```python
compact([9, 2, 7, 1, 8, 3], 5)   ->  (3, [9, 7, 8])
compact([1, 2, 3], 5)            ->  (0, [])
compact([5, 5, 5], 5)            ->  (3, [5, 5, 5])      # >= 門檻要留下
compact([], 5)                   ->  (0, [])
```

**限制**
- `0 <= n <= 2 * 10^5`
- `-10^9 <= scores[i], threshold <= 10^9`
- 判斷是 `>= threshold` 保留，`< threshold` 丟掉。
- 回傳的 list 就是保留下來的元素，長度等於第一個回傳值。

**效能與記憶體要求**：測資裡有一筆 n = 200,000 的大測資與時間上限。
更重要的是**做法**——這題要你用**快慢指標就地覆寫** `scores`，
而不是 `[x for x in scores if x >= threshold]` 開一個新 list。

兩種寫法都是 O(n) 時間，測資分不出來。但差別在**空間**：
就地覆寫是 O(1) 額外空間，開新 list 是 O(n)。
偵測後處理常常在記憶體吃緊的裝置上跑，這個差別是真的。

> 寫完之後回頭看一眼：你的 `scores` 前 `k` 個元素，是不是就是答案？
> 如果是，你就寫對了；如果 `scores` 原封不動，你開了新 list。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 053-compact-detections` 驗證
3. 卡住 → `python trainer.py hint 053-compact-detections`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 053-compact-detections`
