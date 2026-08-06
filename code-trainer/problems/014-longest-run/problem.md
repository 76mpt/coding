# 014-longest-run · 最長連續相同字元

- 階段：基本功：語法與函式 / 1.2 條件判斷與迴圈
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`longest_run`
- 提示：共 4 階（`python trainer.py hint 014-longest-run`）
- 測資：9 筆（`python trainer.py test 014-longest-run`）

────────────────────────────────────────────────────────────────────

實作 `longest_run(s)`，找出字串裡**最長的一段連續相同字元**，
回傳 `(那個字元, 長度)`。

如果有多段一樣長，回傳**最先出現**的那一段。
空字串回傳 `("", 0)`。

**範例**

```
longest_run("aaabbccccd")
```

各段是：`aaa`(3)、`bb`(2)、`cccc`(4)、`d`(1)。最長是 `cccc`，所以回傳 `("c", 4)`。

```
longest_run("")          ->  ("", 0)
longest_run("a")         ->  ("a", 1)
longest_run("abc")       ->  ("a", 1)    # 三段都是 1，取最先的
longest_run("aabb")      ->  ("a", 2)    # 兩段都是 2，取最先的
longest_run("aabbbcc")   ->  ("b", 3)
```

**限制**
- `len(s) <= 10^6`
- 字元可以是任何字元，包含空白（`"  a  "` 的答案是 `(" ", 2)`）。
- 回傳 tuple 或 list 都可以。

**效能要求**：只能掃過字串**一次**。對每個位置都往後數一遍是 O(n²)，字串長時會超時。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 014-longest-run` 驗證
3. 卡住 → `python trainer.py hint 014-longest-run`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 014-longest-run`
