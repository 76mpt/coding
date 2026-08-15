# 024-chain-derivative · 鏈鎖律：多層合成函數的導數 — 參考解

## 標準解

```python
def chain_derivative(layers, x: float) -> tuple[float, float]:
    # 前向：由內而外，記錄每一層的輸入
    values = [x]
    for f, _ in reversed(layers):
        values.append(f(values[-1]))

    # 反向：把每層的導數連乘
    grad = 1.0
    n = len(layers)
    for i, (_, df) in enumerate(layers):
        grad *= df(values[n - 1 - i])      # layers[i] 的輸入是 values[n-1-i]

    return values[-1], grad
```

O(n) 時間、**O(n) 空間**（要存中間值）。

## 為什麼一定要存中間值

鏈鎖律的每一項 `fₖ'(uₖ)` 都要在**該層自己的輸入** `uₖ` 上求值：

```
d/dx f₁(f₂(f₃(x))) = f₁'(f₂(f₃(x))) · f₂'(f₃(x)) · f₃'(x)
                        └─ u₂ ─┘        └ u₃ ┘      └ x ┘
```

這些 `uₖ` 只有在前向計算時才算得出來。所以流程**必然是兩趟**：

```
前向（forward）：算值，順便把中間結果存起來
反向（backward）：用存下來的中間結果算梯度
```

**這就是 PyTorch 訓練時記憶體會爆的根本原因。** 網路越深、batch 越大，
要存的 activation 越多。相關的工程手段：

- **`torch.no_grad()`** — 推論時不存中間值，記憶體省一大半
- **gradient checkpointing** — 只存部分層，其餘在 backward 時重算（時間換空間）
- **就地操作（in-place）** — `relu_()` 覆寫輸入，但如果那個值 backward 還要用就會報錯

你現在寫的這 12 行，就是這一切的最小模型。

## 反向傳播 = 這題的多變數版本

單變數的鏈鎖律是**純量連乘**：

```
dy/dx = (dy/du₁)(du₁/du₂)…(duₙ/dx)
```

多變數版本裡，每個「導數」變成 **Jacobian 矩陣**，連乘變成**矩陣連乘**：

```
∂L/∂x = J₁ J₂ … Jₙ
```

而反向傳播的關鍵洞察是：**乘法的結合律讓你可以選擇計算順序**。

```
(((J₁ J₂) J₃) J₄)     ← 從左到右 = 反向模式（backprop）
(J₁ (J₂ (J₃ J₄)))     ← 從右到左 = 前向模式
```

損失函數的輸出是**純量**（1 維），輸入是**百萬維**的參數。
從左到右算的話，每一步都是「1×n 的向量」乘「n×m 的矩陣」，永遠不用具體化整個 Jacobian；
從右到左則要處理巨大的矩陣乘矩陣。

**這就是為什麼深度學習用反向模式自動微分，而不是前向模式。**
你在節點 5.9 手寫 tiny autograd 時會親手實作這個選擇。

## 驗證你的實作對不對

用上一題的數值微分交叉檢查：

```python
def composed(layers):
    def g(t):
        for f, _ in reversed(layers):
            t = f(t)
        return t
    return g

layers = [(math.sin, math.cos), (lambda t: t**2, lambda t: 2*t)]
value, grad = chain_derivative(layers, 1.0)
numeric = numerical_derivative(composed(layers), 1.0)
print(abs(grad - numeric))      # 應該在 1e-10 量級
```

**這就是 gradient check。** 解析梯度（鏈鎖律）跟數值梯度（有限差分）
是兩條完全獨立的路徑，兩者吻合幾乎可以確定你推對了。

## 常見錯誤

1. **所有導函式都在 x 上求值** — 寫成 `df(x)`。
   對 `[sq, sq], x=2` 會得到 `2·2 × 2·2 = 16` 而不是 32。
   **每一層的導函式要在它自己的輸入上求值。**
2. **索引搞反** — `values[i]` 而不是 `values[n-1-i]`。
   兩層對稱的情況（如 `[sq, sq]`）碰巧會對，三層測資就會抓到。
3. **`grad` 初始值設 0** — 乘法的單位元是 1。全部會變成 0。
4. **前向的方向搞反** — `for f, _ in layers` 而不是 `reversed(layers)`。
   `layers[0]` 是最外層，要**最後**才算。
5. **只回傳導數** — 題目要 `(值, 導數)` 兩個。
6. **用遞迴但沒處理空 list** — 遞迴版要記得 base case 回傳 `(x, 1.0)`。

## 延伸：遞迴版本

```python
def chain_derivative(layers, x):
    if not layers:
        return x, 1.0
    inner_value, inner_grad = chain_derivative(layers[1:], x)
    f, df = layers[0]
    return f(inner_value), df(inner_value) * inner_grad
```

更短、更貼近數學定義，而且「先算內層再算外層」的結構一目了然。
缺點是 `layers[1:]` 每次都複製一份（O(n²) 空間），而且深層網路會爆 recursion limit。

**遞迴適合表達，迭代適合執行。** 兩種都要會寫。

## 這條規則之後會出現在哪

| 場合 | 鏈鎖律的樣貌 |
|---|---|
| 反向傳播 | 逐層把梯度往回傳 |
| 重參數化技巧（VAE） | `z = μ + σ·ε`，梯度穿過取樣 |
| Diffusion 的訓練 | 損失對噪聲預測的梯度 |
| 相機標定 | 重投影誤差對相機參數的 Jacobian（M2.2） |
| **SE(3) 上的最佳化** | 李代數擾動的鏈鎖律（M2.8） |

最後一項是你主方向的核心：SLAM 的 bundle adjustment 就是在算
「重投影誤差對位姿的 Jacobian」，而那條 Jacobian 是用鏈鎖律一層層推出來的。
