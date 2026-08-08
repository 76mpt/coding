# 020-log-product · 連乘機率的對數（親眼看見下溢） — 參考解

## 標準解

```python
import math


def log_product(values: list[float]) -> float:
    total = 0.0                     # 空乘積是 1，log(1) = 0
    for v in values:
        if v == 0:
            return float("-inf")    # 乘積是 0，log(0) = -∞
        total += math.log(v)
    return total
```

O(n) 時間、O(1) 空間。

## 更 pythonic 的寫法

```python
import math


def log_product(values: list[float]) -> float:
    if any(v == 0 for v in values):
        return float("-inf")
    return sum(math.log(v) for v in values)
```

`sum(...)` 對空的 generator 回傳 `0`（int），會被自動當成 0.0 使用。
要嚴謹一點可以寫 `sum(..., 0.0)` 指定起始值。

`math.fsum` 是更精確的版本（使用 Shewchuk 演算法，消除累加誤差）：

```python
return math.fsum(math.log(v) for v in values)
```

對 10⁵ 個項的累加，普通 `sum` 的誤差大約在 10⁻¹¹ 量級，`fsum` 是 0。
**當你在累加很多項、而且結果要拿去做減法時，`fsum` 值得用。**

## 為什麼一定要用 log —— 這是本節的核心

浮點數（float64）能表示的正數範圍大約是 `10⁻³⁰⁸ ~ 10³⁰⁸`。

```python
import math
math.prod([0.01] * 1000)     # 0.0
```

真值是 10⁻²⁰⁰⁰，遠低於下限，於是被**無聲地**壓成 0.0。
可怕的地方在於：**它不報錯**。你的程式會繼續跑，只是所有結果都變成垃圾。

取 log 之後：

```
log(10⁻²⁰⁰⁰) = -2000 × log(10) ≈ -4605
```

一個再普通不過的數字。

### 這件事在 ML 裡的具體樣貌

**最大概似估計**要最大化

```
L(θ) = Π p(xᵢ | θ)
```

n = 1000 筆資料時直接下溢。所以實務上一律最大化 **log-likelihood**：

```
ℓ(θ) = Σ log p(xᵢ | θ)
```

這樣做有三個好處，缺一不可：

1. **數值穩定** — 連乘變連加，不會下溢
2. **微分變簡單** — 連乘要套 n 次乘積律，連加只要各項分別微分
3. **不改變答案** — `log` 是**嚴格單調遞增**的，所以
   `argmax L(θ) = argmax log L(θ)`。這是「可以隨便取 log」的理論依據。

第 3 點很關鍵：如果 log 不是單調的，取 log 就會改變最優解，那就不能這樣做了。

## 交叉熵從哪來

分類問題假設標籤服從 Categorical 分布，第 i 筆資料的機率是 `p_{y_i}`（正確類別的預測機率）。
最大化概似：

```
maximize  Π p_{yᵢ}
⟺ maximize  Σ log p_{yᵢ}
⟺ minimize  −Σ log p_{yᵢ}      ← 這就是 cross-entropy loss
```

**你每天在用的 `nn.CrossEntropyLoss()` 就是這條式子。**
那個負號只是把「最大化」換成「最小化」（因為最佳化器習慣往下走）。

## 常見錯誤

1. **先乘再取 log** — 這題的主角。`[0.01]*1000` 那筆會拋 ValueError。
2. **初始值設成 1.0** — 那是**乘法**的單位元。取 log 之後應該用**加法**的單位元 0.0。
   空 list 會回傳 1.0 而不是 0.0。
3. **用 `math.log(v, 10)` 或 `math.log2`** — 題目要自然對數。
   底數不同答案會差一個常數倍（`log₁₀ x = ln x / ln 10`）。
4. **沒處理 0** — `math.log(0)` 拋 `ValueError: math domain error`，
   不會回傳 `-inf`。（NumPy 的 `np.log(0)` 才會給 `-inf` 加一個警告。）
5. **用 `v < 1e-300` 判斷 0** — 不要自作聰明。規格說的是「等於 0」，
   而 `1e-300` 是合法的正數，它的 log 是 -690，不是 -inf。

## 延伸

同一個「換到 log 空間運算」的思路貫穿整個機率程式設計：

| 原本 | log 空間 |
|---|---|
| `a × b` | `log a + log b` |
| `a / b` | `log a − log b` |
| `aⁿ` | `n × log a` |
| **`a + b`** | **`logaddexp(log a, log b)`** ← 這個不簡單 |

最後一列是麻煩的地方：**log 空間裡的「加法」需要特殊處理**，
因為 `log(a+b)` 沒辦法拆成 `log a` 和 `log b` 的簡單組合。
解法是 **log-sum-exp**，也就是下一題。

HMM 的 forward-backward、CRF、beam search、softmax 的分母——
全部都需要 log-sum-exp。
