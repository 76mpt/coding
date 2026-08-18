# 016-stats-varargs · 可變數量參數的統計摘要 — 參考解

## 標準解

```python
def stats(*values: float, ndigits: int = 2) -> tuple[float, float, float]:
    if not values:
        raise ValueError("至少要一個數值")
    return round(sum(values) / len(values), ndigits), max(values), min(values)
```

O(n) 時間（四個內建函式各掃一遍，常數 4）、O(1) 額外空間。

## `*args` 到底做了什麼

```python
def f(*values):
    print(type(values), values)

f(1, 2, 3)      # <class 'tuple'> (1, 2, 3)
f()             # <class 'tuple'> ()
```

`*values` **把所有位置參數打包成一個 tuple**。是 tuple 不是 list，所以不可變。

反過來，呼叫時的 `*` 是**解包**：

```python
nums = [1, 2, 3]
stats(*nums)      # 等同於 stats(1, 2, 3)
stats(nums)       # ❌ 這是傳一個 list 進去，values = ([1,2,3],)
```

同樣地 `**kwargs` 把關鍵字參數打包成 dict，呼叫時 `**d` 解包 dict。

## 為什麼 `ndigits` 自動變成 keyword-only

```python
def stats(*values, ndigits=2):
```

`*values` 會**吃掉所有位置參數**，所以 `ndigits` 之後不可能收到位置參數——
Python 因此把它視為 keyword-only，效果等同於前一題那個裸的 `*`：

```python
def f(a, *, b=1): ...      # b 是 keyword-only
def g(*args, b=1): ...     # b 也是 keyword-only
```

差別只在 `g` 還額外收集了位置參數。

## 掃四遍 vs 掃一遍

標準解呼叫了 `sum`、`len`、`max`、`min`，資料掃了四遍。想只掃一遍：

```python
def stats(*values, ndigits=2):
    if not values:
        raise ValueError("至少要一個數值")
    total = hi = lo = values[0]
    for v in values[1:]:
        total += v
        if v > hi:
            hi = v
        if v < lo:
            lo = v
    return round(total / len(values), ndigits), hi, lo
```

**但這幾乎總是更慢。** 因為 `sum`/`max`/`min` 是 C 實作，
四趟 C 迴圈比一趟 Python 迴圈快好幾倍。

**這是 Python 效能的重要直覺：「少掃幾遍」在 C/C++ 是對的，在 Python 常常是反效果。**
真正的優化方向是「把迴圈交給 C」——用內建函式、用 NumPy 向量化（節點 5.1）。

## `round` 的兩個坑

**坑一：給不給第二個參數，回傳型別不同**

```python
round(2.6)          # 3      ← int
round(2.6, 0)       # 3.0    ← float
```

**坑二：銀行家捨入（round half to even）**

```python
round(0.5)    # 0   不是 1！
round(1.5)    # 2
round(2.5)    # 2   不是 3！
round(2.675, 2)  # 2.67  不是 2.68（因為 2.675 的浮點表示其實略小於 2.675）
```

Python 對「剛好 .5」的情況會**進位到偶數**，這是 IEEE 754 的預設捨入模式，
目的是避免大量捨入時系統性偏高。

大部分情況沒差，但**金額計算要用 `decimal.Decimal`**：

```python
from decimal import Decimal, ROUND_HALF_UP
Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)   # 3
```

## 常見錯誤

1. **沒擋空輸入** — `sum(())/len(())` 拋 ZeroDivisionError，型別不是 ValueError，測資不過。
   **除法之前先檢查除數**，這是通則。
2. **對 max/min 也做 round** — 規格說只有平均要四捨五入。
   `stats(1.5, 2.5, ndigits=1)` 的 max 應該是 `2.5` 不是 `2.5` 四捨五入後的值。
3. **把簽章改成 `def stats(values, ndigits=2)`** — 那就變成傳一個 list 進來了，
   所有測資都不會過。**簽章是規格的一部分。**
4. **用 `//` 算平均** — 整數除法會把小數丟掉，`stats(1,2)` 得到 1 而不是 1.5。
5. **`ndigits` 寫成位置參數** — `def stats(ndigits=2, *values)` 是合法語法但語意完全錯了，
   `ndigits` 會吃掉第一個數值。

## 延伸

實務上算統計量會用 `statistics` 模組或 NumPy：

```python
import statistics
statistics.mean([1, 2, 3])     # 2
statistics.stdev([1, 2, 3])    # 1.0
statistics.median([1, 2, 3])   # 2

import numpy as np
np.mean(a), np.std(a), np.percentile(a, 95)
```

但**變異數有個數值陷阱**值得先知道：

```
Var(X) = E[X²] − (E[X])²        ← 數學上正確，數值上危險
```

當 `E[X²]` 和 `(E[X])²` 都很大而差很小時，相減會發生**災難性抵消**，
算出來甚至可能是負數。實務上要用 Welford 線上演算法。

你在 M00.6 會用程式親眼看到這個現象，M1.9 會正式學怎麼避免它。
