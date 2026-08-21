# 004-top-k-words · 詞頻 Top-K — 參考解

## 標準解

```python
def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1

    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]
```

**O(n + m log m)**，n 是單字總數、m 是相異單字數。

## Pythonic 版本（實務上就這樣寫）

```python
from collections import Counter

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
```

`Counter` 就是專門做計數的 dict 子類別，C 實作，比手寫迴圈快 2–3 倍。

⚠️ **但不要用 `Counter.most_common(k)`**：它同分時的順序是「插入順序」而不是字典序，
這題會錯。`most_common` 只在你不在乎同分順序時才能用——這是很多人踩過的坑。

## 最佳解：k 很小時用 heap

當 m（相異單字數）是百萬等級、而 k 只有 10 時，把全部排序是浪費：

```python
import heapq
from collections import Counter

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    return heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
```

**O(n + m log k)** 而不是 O(n + m log m)。m = 10^6、k = 10 時大約快 5 倍。

用 `nsmallest` 配上 `(-次數, 單字)` 這個 key，語意剛好等同「次數最多、同分取字典序最小」。

實務判斷：**k ≥ m/10 左右就直接 sort**，heap 的常數項比較大反而不划算。
沒實測就別為了 heap 而 heap。

## 那個 `(-kv[1], kv[0])` 為什麼能一次排好兩個層次

Python 比較 tuple 是**逐項字典序比較**：先比第 0 項，相等才比第 1 項。
所以 `key` 回傳 tuple 就等於「多重排序鍵」。

方向相反的問題用負號解決：次數 3 變成 -3，次數 1 變成 -1，而 `-3 < -1`，
所以次數多的排前面。

字串沒有負號可用。如果需要「字串降序 + 數字升序」，就得靠**穩定排序**分兩趟：

```python
items.sort(key=lambda kv: kv[0])                  # 先排次要鍵（升序）
items.sort(key=lambda kv: kv[1], reverse=True)    # 再排主要鍵
```

Python 的 sort 保證**穩定**（相等元素維持原有相對順序），所以第二趟不會打亂第一趟的結果。
順序是**先排次要鍵、後排主要鍵**，很反直覺，記住它。

## 常見錯誤

1. **用 `words.count(word)` 數次數** — O(n²)。20 萬字時是 400 億次比較，跑不完。
   這是新手最常見的效能地雷：**看到 `.count()` 在迴圈裡就要警覺**。
2. **用 `most_common(k)`** — 同分順序錯，見上。
3. **`split(' ')` 而不是 `split()`** — `"a  b".split(' ')` 得到 `['a', '', 'b']`，
   那個空字串會被當成一個「單字」計數。
4. **忘記 `.lower()`，或只對部分做** — 要在切分**之前**（或之後統一）轉小寫，
   不能一半用原字一半用小寫。
5. **手寫 if 處理 k=0 或 k > 長度** — 不必要，切片本來就正確處理這兩種情況。
   `[1,2,3][:0]` 是 `[]`，`[1,2,3][:99]` 是 `[1,2,3]`。
6. **先取前 k 再排序** — 順序反了，會拿到錯的 k 個。

## 延伸

這題的骨架（計數 → 排序 → 取前 k）之後會一直出現：

- **NLP**：詞彙表建立、TF-IDF 的第一步就是這個
- **CV**：資料集類別分布統計、找出長尾類別
- **除錯**：log 裡哪個錯誤最常出現
- **LeetCode 347** Top K Frequent Elements 是同一題

在 CV 訓練前先跑一次類別計數，是發現「資料集不平衡」的最快方法——
很多訓練不起來的模型，問題根本在這裡。
