# 014-longest-run · 最長連續相同字元 — 參考解

## 標準解（單次掃描）

```python
def longest_run(s: str) -> tuple[str, int]:
    if not s:
        return "", 0

    ch, run = s[0], 1              # 目前這一段
    best_ch, best_run = s[0], 1    # 歷史最佳

    for c in s[1:]:
        if c == ch:
            run += 1
        else:
            ch, run = c, 1         # 新的一段開始
        if run > best_run:         # 用 > 才會保留先出現的
            best_ch, best_run = ch, run

    return best_ch, best_run
```

**時間 O(n)、空間 O(1)**（不算 `s[1:]` 的複製）。這是最佳解——你至少要看過每個字元一次。

## 「目前」與「最佳」要分開，這是核心

這題的結構在演算法題裡出現的頻率極高：

```
for 每個元素:
    更新「目前狀態」
    用「目前狀態」挑戰「歷史最佳」
```

同型的題目：

| 題目 | 「目前」是什麼 | 「最佳」是什麼 |
|---|---|---|
| 最大子陣列和（Kadane） | 以此結尾的最大和 | 全域最大和 |
| 股票買賣最佳時機 | 目前為止的最低價 | 最大獲利 |
| 最長不重複子字串 | 目前視窗的左界 | 最長長度 |
| 這題 | 目前這段的字元與長度 | 最長段 |

**把「目前」和「最佳」寫成兩組變數**，是避免搞混的關鍵。
很多人一開始只用一組變數，然後在邊界上錯得莫名其妙。

## 用 itertools 的一行版

```python
from itertools import groupby

def longest_run(s: str) -> tuple[str, int]:
    if not s:
        return "", 0
    ch, group = max(groupby(s), key=lambda kv: sum(1 for _ in kv[1]))
    ...
```

⚠️ **這個寫法有陷阱**：`groupby` 回傳的是**迭代器**，一旦你消耗掉它去算長度，
就不能再用了；而且 `max` 對同分會取**先出現**的（正好符合需求）但很不直觀。
正確的寫法要先物化：

```python
from itertools import groupby

def longest_run(s: str) -> tuple[str, int]:
    if not s:
        return "", 0
    runs = [(ch, len(list(g))) for ch, g in groupby(s)]
    return max(runs, key=lambda kv: kv[1])
```

短是短，但**空間變成 O(n)**（存了所有段），而且對百萬字元的輸入慢好幾倍。
`groupby` 適合「段數不多、要對每段做複雜處理」的場合；
單純找最長段的話，手寫的單次掃描更好。

**知道標準庫有什麼，但也知道什麼時候不該用它。**

## 為什麼 O(n²) 會超時

錯誤寫法通常長這樣：

```python
for i in range(len(s)):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
    # 更新最佳...
```

看起來只是兩層迴圈，但在 `"xxxx...x"`（全部相同）的情況下，
內層每次都要跑到底，總共 `n + (n-1) + ... + 1 ≈ n²/2` 次。
n = 10⁶ 時是 5×10¹¹ 次比較——大測資就是在抓這個。

## 常見錯誤

1. **用 `>=` 比較最佳值** — 會保留**最後**出現的最長段。
   `"aabb"` 會回傳 `("b", 2)` 而不是 `("a", 2)`。
2. **新段開始時長度設成 0** — 應該是 1，因為當前這個字元已經算一個了。
   `"abc"` 會得到長度 0。
3. **忘記空字串** — `s[0]` 會 IndexError。**任何用到 `s[0]` 的地方都先問「空的時候呢」。**
4. **只在 `else` 分支裡更新最佳** — 那最後一段永遠不會被檢查。
   `"aabbb"` 會回傳 `("a", 2)`。**更新最佳要放在 if/else 外面。**
5. **更新最佳時記錯字元** — 寫成 `best_ch = c`。這題碰巧一樣（因為新段開始時 `ch = c`），
   但語意上應該記「目前這段的字元」`ch`，養成正確的心智模型比較重要。

## 延伸

這題是**行程長度編碼（Run-Length Encoding, RLE）**的一半。完整的 RLE 是：

```
"aaabbccccd"  →  [("a",3), ("b",2), ("c",4), ("d",1)]
```

RLE 在影像處理裡是真的會用的東西：

- **PNG / BMP 的壓縮**：連續同色像素用 RLE 存
- **COCO 資料集的 segmentation mask**：官方格式就是 RLE 編碼的二值遮罩，
  你之後讀 COCO 標註時會直接遇到 `{"counts": [...], "size": [h, w]}` 這種欄位
- **稀疏矩陣**：連續的 0 用 RLE 表示

你在節點 4.6 資料清理時會實作一次完整的 RLE 編解碼。
