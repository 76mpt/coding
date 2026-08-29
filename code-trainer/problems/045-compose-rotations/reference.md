# 045-compose-rotations · 旋轉相加與歐拉公式 — 參考解

## 標準解

```python
import math


def rotation_matrix(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]


def _mul2(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def _euler(theta):
    return complex(math.cos(theta), math.sin(theta))


def compose_rotations(alpha, beta):
    m1 = _mul2(rotation_matrix(alpha), rotation_matrix(beta))
    m2 = rotation_matrix(alpha + beta)
    c1 = _euler(alpha) * _euler(beta)
    c2 = _euler(alpha + beta)
    return m1, m2, c1, c2
```

## 把矩陣乘法展開，和角公式就掉出來了

```
⎡cosα  −sinα⎤ ⎡cosβ  −sinβ⎤
⎣sinα   cosα⎦ ⎣sinβ   cosβ⎦
```

左上角 = `cosα·cosβ + (−sinα)·sinβ` = **`cosα cosβ − sinα sinβ`**

左下角 = `sinα·cosβ + cosα·sinβ` = **`sinα cosβ + cosα sinβ`**

而 `R(α+β)` 的左上角是 `cos(α+β)`、左下角是 `sin(α+β)`。兩邊要相等，就必須：

```
cos(α+β) = cos α cos β − sin α sin β
sin(α+β) = sin α cos β + cos α sin β
```

**那就是和角公式。**

> 高中背和角公式是死記，這裡它是**「旋轉兩次等於轉總角度」這個幾何事實的代數形式**。
> 記不起來的時候，把兩個旋轉矩陣乘開就有了——**這比背誦可靠得多**。

## 複數在做完全相同的事

```
(a + bi)(c + di) = (ac − bd) + (ad + bc)i
                     ↑            ↑
                  跟矩陣左上角一樣  跟矩陣左下角一樣
```

把 `a = cosα, b = sinα, c = cosβ, d = sinβ` 代進去，**兩邊逐字相同**。

這不是巧合——**複數 `cos θ + i sin θ` 和旋轉矩陣 `[[cos,−sin],[sin,cos]]` 是同一個東西的兩種寫法**。
（正式的說法：複數體同構於這類 2×2 實矩陣構成的環。）

所以：

| 複數 | 旋轉矩陣 |
|---|---|
| `e^{iα} · e^{iβ} = e^{i(α+β)}` | `R(α)R(β) = R(α+β)` |
| `\|e^{iθ}\| = 1` | `det(R) = 1`、保長度 |
| `1/e^{iθ} = e^{−iθ}` | `R(θ)⁻¹ = R(−θ) = Rᵀ` |

**複數版本簡單太多**——一次乘法 vs 八次。這就是為什麼訊號處理全部用複數表示旋轉，
而不是矩陣。

## 歐拉公式為什麼成立

把三個泰勒展開排在一起：

```
e^x    = 1 + x + x²/2! + x³/3! + x⁴/4! + …
cos x  = 1     − x²/2!         + x⁴/4! − …
sin x  =     x        − x³/3!         + x⁵/5! − …
```

把 `x = iθ` 代進 `e^x`。因為 `i² = −1`、`i³ = −i`、`i⁴ = 1` 循環，
**實部剛好湊成 `cos θ` 的展開，虛部剛好湊成 `sin θ`**。

```
e^{iθ} = cos θ + i sin θ
```

這條式子把**指數、三角、複數**三個看似無關的東西綁在一起，
是數學裡最有生產力的等式之一。

**它在你的路線圖上出現在哪：**

| 節點 | 用途 |
|---|---|
| **M1.5** 傅立葉 | `e^{-2πikn/N}` 就是 DFT 的核心，整個頻域分析建立在它上面 |
| **M1.6** 卷積定理 | 「時域卷積 = 頻域相乘」，因為 `e^{iθ}` 把卷積對角化了 |
| **M2.7** 四元數 | 複數的三維推廣，用來表示 3D 旋轉 |

## 為什麼 `m1` 不能直接寫成 `R(α+β)`

測資會抓。有一筆隱藏測資檢查 `m1[0][0]` 必須等於 `cos2·cos3 − sin2·sin3`（**分別算再組合**）。

數學上兩者相等，但**浮點運算下差在 1e-16 左右**——而且更重要的是，
**這題的目的就是讓你親眼看到兩條路徑撞出同一個答案**。直接寫 `R(α+β)` 等於沒驗證。

這跟 030 不准寫 `area = abs(det)`、035 不准偷懶是同一種要求。

## 常見錯誤

1. **`m1` 直接用 `rotation_matrix(alpha + beta)`** —— 沒驗證到任何東西，隱藏測資抓。
2. **矩陣乘法的索引寫錯** —— `B[j][k]` 而不是 `B[k][j]`，算出的是 `A·Bᵀ`。034 的常見錯誤第 2 條。
3. **複數寫成 `complex(sin, cos)`** —— 實部虛部反了。實部是 cos。
4. **自己實作複數乘法** —— Python 內建就支援 `*`，不用重寫（重寫也不算錯，但沒必要）。
5. **回傳 numpy 陣列** —— 題目要 list of list。
6. **用 `math.e ** (1j*theta)`** —— `math` 不支援複數，會 TypeError。要用 `cmath.exp(1j*theta)` 或直接 `complex(cos, sin)`。

（順帶：`cmath` 模組是 `math` 的複數版本。`cmath.exp(1j*theta)` 和 `complex(cos θ, sin θ)` 結果相同，
用哪個都可以——但**手寫 `complex(cos, sin)` 更能看出歐拉公式在做什麼**。）
