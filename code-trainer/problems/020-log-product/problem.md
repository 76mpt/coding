# 020-log-product · 連乘機率的對數（親眼看見下溢）

- 階段：前置：高中數學重補（公式與計算流利度） / M00.1 對數與指數（重點中的重點）
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`log_product`
- 提示：共 4 階（`python trainer.py hint 020-log-product`）
- 測資：9 筆（`python trainer.py test 020-log-product`）

────────────────────────────────────────────────────────────────────

機器學習裡的**概似（likelihood）**是一大串機率連乘：

```
L = p₁ × p₂ × … × pₙ
```

實作 `log_product(values)`，回傳 **`log(L)`**（自然對數），
其中 `values` 是那串機率。

**但你不能真的先乘起來再取 log。** 原因看範例。

**範例**

```
log_product([0.5] * 10)     ->  -6.931471805599453     # = 10 × ln(0.5)
log_product([0.01] * 1000)  ->  -4605.17018598815      # = 1000 × ln(0.01)
log_product([])             ->  0.0                    # 空乘積是 1，ln(1) = 0
log_product([2.0, 4.0])     ->  2.0794415416798357     # = ln(8)
```

**為什麼不能先乘**

```python
math.prod([0.01] * 1000)     # 0.0   ← 下溢了！
math.log(0.0)                # ValueError: math domain error
```

1000 個 0.01 相乘的真值是 10⁻²⁰⁰⁰。
`float` 能表示的最小正數大約是 10⁻³⁰⁸，所以結果被無聲地壓成 **0.0**，
接著 `log(0)` 直接爆炸。

**這就是為什麼所有損失函數都寫成 `-Σ log(...)` 而不是 `-log(Π...)`。**

**規則**
- 用 `log(ab) = log a + log b`，把連乘變成**連加**。
- 如果 `values` 裡有 **0**，數學上乘積是 0，`log(0) = -∞`，
  請回傳 `float("-inf")`（不要拋例外）。
- 空 list 回傳 `0.0`。

**限制**
- `0 <= values[i]`，可能大於 1。
- 最多 10⁵ 個元素。
- 判定使用近似比較，浮點誤差不影響。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 020-log-product` 驗證
3. 卡住 → `python trainer.py hint 020-log-product`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 020-log-product`
