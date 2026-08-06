# 021-log-sum-exp · 數值穩定的 log-sum-exp

- 階段：前置：高中數學重補（公式與計算流利度） / M00.1 對數與指數（重點中的重點）
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`log_sum_exp`
- 提示：共 4 階（`python trainer.py hint 021-log-sum-exp`）
- 測資：10 筆（`python trainer.py test 021-log-sum-exp`）

────────────────────────────────────────────────────────────────────

上一題把「連乘」搬到了 log 空間。這題處理更麻煩的：**log 空間裡的「相加」**。

給你一串已經取過 log 的數值 `x₁, …, xₙ`，
要算出它們**還原後相加、再取 log** 的結果：

```
LSE(x) = log( e^{x₁} + e^{x₂} + … + e^{xₙ} )
```

實作 `log_sum_exp(values)`。

**天真寫法會爆炸**

```python
math.log(sum(math.exp(v) for v in values))
```

`math.exp(710)` 會拋 `OverflowError`（float 上限約 10³⁰⁸ ≈ e⁷¹⁰）。
而 `math.exp(-800)` 會下溢成 0.0，一整串都下溢的話 `log(0)` 又爆炸。

**範例**

```
log_sum_exp([1000.0, 1000.0, 1000.0])  ->  1001.0986122886682
```

驗算：三個相同的數相加是 `3 × e¹⁰⁰⁰`，取 log 得 `1000 + log 3 ≈ 1001.0986`。
但 `e¹⁰⁰⁰` 本身根本算不出來。

```
log_sum_exp([0.0, 0.0, 0.0])   ->  1.0986122886681098    # = log 3
log_sum_exp([5.0])             ->  5.0
log_sum_exp([1.0, 2.0, 3.0])   ->  3.4076059644443806
log_sum_exp([])                ->  float("-inf")         # 空和是 0，log 0 = -∞
```

**關鍵恆等式**（想不出來就看提示，但先自己推一次）

```
log Σ e^{xᵢ}  =  m + log Σ e^{xᵢ − m}      對任何常數 m 都成立
```

取 `m = max(x)` 之後，所有指數都 ≤ 0，`e^{xᵢ−m}` 落在 `(0, 1]`，**永遠不會溢位**。

**限制**
- `values[i]` 是浮點數，可能非常大或非常小，可能是 `-inf`。
- 全部都是 `-inf` 時回傳 `-inf`。
- 最多 10⁵ 個元素。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 021-log-sum-exp` 驗證
3. 卡住 → `python trainer.py hint 021-log-sum-exp`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 021-log-sum-exp`
