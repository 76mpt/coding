# 021-log-sum-exp · 數值穩定的 log-sum-exp — 參考解

## 標準解

```python
import math


def log_sum_exp(values: list[float]) -> float:
    if not values:
        return float("-inf")

    m = max(values)
    if m == float("-inf"):          # 全部是 -inf，否則會算出 nan
        return float("-inf")

    return m + math.log(sum(math.exp(v - m) for v in values))
```

O(n) 時間（掃兩遍：一次 max、一次累加）、O(1) 空間。

## 恆等式的推導

```
Σᵢ eˣⁱ = Σᵢ eᵐ · e^{xᵢ − m}          提出公因式 eᵐ
       = eᵐ · Σᵢ e^{xᵢ − m}

log Σᵢ eˣⁱ = log(eᵐ · Σᵢ e^{xᵢ−m})
           = log eᵐ + log Σᵢ e^{xᵢ−m}       ← log(ab) = log a + log b
           = m + log Σᵢ e^{xᵢ−m}
```

**這個等式對任何 m 都成立**，選 `m = max` 只是為了數值穩定。
數學上等價，浮點數上天差地遠——**這就是「數值穩定」的典型樣貌：
不改變答案，只改變計算路徑。**

## 為什麼 `m = max` 是最好的選擇

取 `m = max(x)` 之後每個 `xᵢ − m ≤ 0`：

| 情況 | `e^{xᵢ−m}` | 有沒有問題 |
|---|---|---|
| `xᵢ = m`（最大項） | 1.0 | 沒有 |
| `xᵢ` 略小於 m | (0, 1) | 沒有 |
| `xᵢ ≪ m` | 下溢成 0.0 | **無害**，它本來就可以忽略 |

而且**至少有一項是 1**，所以 `Σ ≥ 1`，`log` 的參數永遠 ≥ 1，絕不可能遇到 `log(0)`。

如果選 `m = min` 呢？那所有 `xᵢ − m ≥ 0`，指數會變**更大**，溢位更嚴重。
選 `m = mean` 可以緩解但不保證安全。**只有 max 提供數學上的保證。**

## 這個技巧在哪裡出現

### 1. Softmax

```python
def softmax(x):
    m = max(x)
    exps = [math.exp(v - m) for v in x]     # 完全一樣的減 max 技巧
    total = sum(exps)
    return [e / total for e in exps]
```

`softmax(x) = softmax(x - c)` 對任何常數 c 成立（分子分母的 `e^{-c}` 抵消），
所以減 max 不改變結果。**PyTorch 的 `F.softmax` 內部就是這樣做的。**

### 2. log_softmax

```
log softmax(x)ᵢ = xᵢ − LSE(x)
```

所以 `F.log_softmax` 直接用 LSE 算，**比 `log(softmax(x))` 更穩定**。
這也是為什麼 PyTorch 建議用 `nn.CrossEntropyLoss`（內含 log_softmax）
而不是 `nn.NLLLoss(torch.log(softmax(x)))`——後者會多一次不必要的 exp/log 往返。

### 3. 機率的邊緣化

log 空間裡要算「A 或 B 的機率」時：

```
log P(A ∪ B) = LSE([log P(A), log P(B)])
```

HMM 的 forward 演算法、CRF 的配分函數、beam search 的分數合併，
全部都是在做這件事。NumPy 有 `np.logaddexp(a, b)` 專門處理兩項的情況。

## NumPy / SciPy 的現成實作

```python
from scipy.special import logsumexp
logsumexp([1000.0, 1000.0, 1000.0])     # 1001.0986122886682

import numpy as np
np.logaddexp(a, b)                       # 只有兩項時
```

實務上直接用它們。但**你要看得懂它在做什麼**——
因為當你自己寫一個新的損失函數時，同樣的問題會再出現一次，
而那時候沒有現成的函式可以呼叫。

## 常見錯誤

1. **天真實作** — `math.log(sum(math.exp(v) for v in values))`。
   `[1000]*3` 那筆直接 `OverflowError`。
2. **沒擋全 `-inf`** — `m = -inf` 時 `v - m` 是 `(-inf) - (-inf) = nan`，
   `exp(nan) = nan`，最後回傳 `nan`。**`nan` 不會報錯，只會安靜地污染後面所有計算。**
3. **忘記把 m 加回去** — 回傳 `math.log(sum(...))` 少了 `m +`，
   `[1000]*3` 會得到 1.0986 而不是 1001.0986。
4. **空 list 回傳 0.0** — 空和是 0（加法單位元），`log(0) = -inf`。
   跟上一題的空**乘**積是 1、`log(1) = 0` 剛好相反，別搞混。
5. **用 `sorted(values)[-1]` 取最大值** — 對，但是 O(n log n)。`max()` 是 O(n)。

## 延伸

`log-sum-exp` 有個漂亮的性質：它是 **max 的平滑近似**。

```
max(x) ≤ LSE(x) ≤ max(x) + log n
```

當某一項遠大於其他項時，`LSE(x) ≈ max(x)`。
所以 LSE 又叫 **softmax（軟性最大值）**——
這才是「softmax」這個名字的原始意義，
跟我們現在叫做 softmax 的那個歸一化函數其實是不同的東西（歷史遺留的命名混亂）。

LSE 是**凸函數**且處處可微，這讓它可以出現在最佳化目標裡，而 `max` 不行（不可微）。
你在 M1.1 學凸最佳化時會再看到它。
