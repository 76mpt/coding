# 023-numerical-derivative · 數值微分：中央差分

- 階段：前置：高中數學重補（公式與計算流利度） / M00.4 微分與鏈鎖律
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`numerical_derivative`
- 提示：共 4 階（`python trainer.py hint 023-numerical-derivative`）
- 測資：9 筆（`python trainer.py test 023-numerical-derivative`）

────────────────────────────────────────────────────────────────────

導數的定義是：

```
f'(x) = lim_{h→0}  ( f(x+h) − f(x) ) / h
```

實作 `numerical_derivative(f, x, h=1e-5)`，用數值方法近似 `f'(x)`。
`f` 是一個吃一個浮點數、回傳一個浮點數的函式。

**範例**

```python
numerical_derivative(lambda t: t ** 2, 3.0)   ->  6.0        # (x²)' = 2x，x=3 → 6
numerical_derivative(math.sin, 0.0)           ->  1.0        # (sin)' = cos，cos(0) = 1
numerical_derivative(math.exp, 1.0)           ->  2.718...   # (eˣ)' = eˣ
numerical_derivative(lambda t: 5.0, 1.0)      ->  0.0        # 常數的導數是 0
```

**這題的關鍵：不能直接照抄定義**

把定義直接寫成程式叫做**前向差分**：

```python
(f(x + h) - f(x)) / h          # ❌ 精度不夠
```

它的誤差是 **O(h)**。`h = 1e-5` 時誤差約 10⁻⁵，
測資的容差比這個嚴格，所以**前向差分不會過**。

你要用的是**中央差分**，它的誤差是 **O(h²)**：

```
f'(x) ≈ ( f(x+h) − f(x−h) ) / (2h)
```

同樣的 `h = 1e-5`，誤差只有 10⁻¹⁰——**精度好一億倍，成本只多一次函式呼叫**。

**限制**
- `f` 在 `x` 附近是平滑的。
- 判定使用近似比較，容差約 10⁻⁷。
- `h` 可能由呼叫者指定。

**為什麼要學這個**：這個函式就是 **gradient check**——
你之後手推反向傳播、實作新的損失函數時，都要靠它驗證解析梯度有沒有推錯。
它是研究工作最常用的除錯工具之一。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 023-numerical-derivative` 驗證
3. 卡住 → `python trainer.py hint 023-numerical-derivative`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 023-numerical-derivative`
