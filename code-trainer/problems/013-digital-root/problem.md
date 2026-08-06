# 013-digital-root · 數位根與迭代次數

- 階段：基本功：語法與函式 / 1.2 條件判斷與迴圈
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`digital_root`
- 提示：共 4 階（`python trainer.py hint 013-digital-root`）
- 測資：8 筆（`python trainer.py test 013-digital-root`）

────────────────────────────────────────────────────────────────────

把一個非負整數的**各位數字相加**，如果結果還是兩位數以上，就再加一次，
一直到只剩一位數為止。這個最終的一位數叫做**數位根（digital root）**。

實作 `digital_root(n)`，回傳 `(數位根, 一共加了幾輪)`。

**範例**

`n = 199` 的過程：

```
199  →  1+9+9 = 19      （第 1 輪）
 19  →  1+9   = 10      （第 2 輪）
 10  →  1+0   = 1       （第 3 輪）
```

剩下一位數 1，總共加了 3 輪，所以回傳 `(1, 3)`。

```
digital_root(0)     ->  (0, 0)    # 本來就是一位數，一輪都不用加
digital_root(9)     ->  (9, 0)
digital_root(10)    ->  (1, 1)
digital_root(38)    ->  (2, 2)    # 38 → 11 → 2
```

**限制**
- `0 <= n <= 10^18`
- 回傳 tuple 或 list 都可以。

**注意**：一位數（0–9）的答案是它自己，輪數是 **0**，不是 1。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 013-digital-root` 驗證
3. 卡住 → `python trainer.py hint 013-digital-root`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 013-digital-root`
