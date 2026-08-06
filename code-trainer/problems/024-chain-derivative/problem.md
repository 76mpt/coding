# 024-chain-derivative · 鏈鎖律：多層合成函數的導數

- 階段：前置：高中數學重補（公式與計算流利度） / M00.4 微分與鏈鎖律
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`chain_derivative`
- 提示：共 4 階（`python trainer.py hint 024-chain-derivative`）
- 測資：7 筆（`python trainer.py test 024-chain-derivative`）

────────────────────────────────────────────────────────────────────

**鏈鎖律**是微積分裡對深度學習最重要的一條規則：

```
d/dx  f(g(x))  =  f'(g(x)) · g'(x)
```

「外層在內層的值上的導數」乘以「內層的導數」。

推廣到 n 層：

```
d/dx  f₁(f₂(…fₙ(x)))  =  f₁'(u₁) · f₂'(u₂) · … · fₙ'(x)
```

其中 `uₖ` 是**第 k 層的輸入**（也就是它下面那些層算完的結果）。

實作 `chain_derivative(layers, x)`：

- `layers` 是一個 list，每個元素是 `(函式, 該函式的導函式)` 的 tuple。
- 順序是**由外到內**：`layers[0]` 是最外層，`layers[-1]` 是最內層。
- 回傳 `(合成函數在 x 的值, 合成函數在 x 的導數)`。

**範例**

```python
sq  = (lambda t: t**2, lambda t: 2*t)      # f(t)=t², f'(t)=2t
sn  = (math.sin, math.cos)                 # f(t)=sin t, f'(t)=cos t

chain_derivative([sn, sq], 1.0)
->  (0.8414709848078965, 1.0806046117362795)
```

這代表 `f(x) = sin(x²)`，在 x=1 時：
- 值 = `sin(1) = 0.8415`
- 導數 = `cos(x²) · 2x = cos(1) · 2 = 1.0806`

```
chain_derivative([], 7.0)   ->  (7.0, 1.0)     # 沒有層 = 恆等函數，導數是 1
```

**限制**
- `layers` 可能是空 list。
- 判定使用近似比較。
- 回傳 tuple 或 list 都可以。

**這題就是反向傳播的骨架**：先「前向」算出每一層的輸入，再「反向」把導數連乘起來。
你在節點 5.9 手寫 autograd 時，做的是同一件事，只是換成多變數版本。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 024-chain-derivative` 驗證
3. 卡住 → `python trainer.py hint 024-chain-derivative`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 024-chain-derivative`
