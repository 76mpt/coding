# 006-container-with-most-water · 盛最多水的容器

- 階段：資料結構與演算法（LeetCode 風格） / 2.1 陣列與雙指標
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`max_area`
- 提示：共 4 階（`python trainer.py hint 006-container-with-most-water`）
- 測資：8 筆（`python trainer.py test 006-container-with-most-water`）

────────────────────────────────────────────────────────────────────

給一個長度為 n 的整數陣列 `heights`，`heights[i]` 代表第 i 條垂直線的高度，
第 i 條線的兩個端點是 `(i, 0)` 和 `(i, heights[i])`。

從中選**兩條**線，與 x 軸一起圍成一個容器。求這個容器最多能裝多少水。

容器的容量 = **寬 × 高**，其中
- 寬 = 兩條線的索引差
- 高 = 兩條線之中**比較矮**的那一條（水會從矮的那邊溢出去）

回傳最大容量。容器本身不能傾斜。

**範例**

```
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
```

選 index 1（高 8）和 index 8（高 7）：寬 = 8 - 1 = 7，高 = min(8, 7) = 7，容量 = 49。
這是最大值，所以回傳 `49`。

```
max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  ->  49
max_area([1, 1])                       ->  1
max_area([4, 3, 2, 1, 4])              ->  16
max_area([1, 2, 1])                    ->  2
```

**限制**
- `2 <= n <= 2 * 10^5`
- `0 <= heights[i] <= 10^4`

**效能要求**：測資裡有一筆 n = 200,000 的大測資，並且有時間上限。
兩層迴圈枚舉所有配對是 O(n²) ≈ 2×10^10 次運算，會直接超時。
這題的重點就是**想出 O(n) 的做法**。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 006-container-with-most-water` 驗證
3. 卡住 → `python trainer.py hint 006-container-with-most-water`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 006-container-with-most-water`
