# 025-gradient-descent-1d · 一維梯度下降（看見學習率的威力與災難）

- 階段：前置：高中數學重補（公式與計算流利度） / M00.4 微分與鏈鎖律
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`gradient_descent_1d`
- 提示：共 4 階（`python trainer.py hint 025-gradient-descent-1d`）
- 測資：8 筆（`python trainer.py test 025-gradient-descent-1d`）

────────────────────────────────────────────────────────────────────

導數告訴你「往哪個方向走函數會變大」。所以要**最小化**一個函數，
就往導數的**反方向**走一小步，反覆進行：

```
x ← x − lr · f'(x)
```

`lr`（learning rate，學習率）決定每步走多遠。

實作 `gradient_descent_1d(df, x0, lr, steps)`：

- `df` 是目標函數的**導函式**
- `x0` 是起始位置
- `lr` 是學習率
- `steps` 是迭代次數
- 回傳迭代 `steps` 次之後的 `x`

**範例**

最小化 `f(x) = x²`，導數是 `f'(x) = 2x`，最小值在 `x = 0`：

```python
gradient_descent_1d(lambda t: 2*t, x0=10.0, lr=0.1, steps=100)
->  2.037e-09        # 幾乎收斂到 0
```

```python
gradient_descent_1d(lambda t: 2*t, x0=10.0, lr=0.5, steps=1)
->  0.0              # lr=0.5 時一步就到！ 10 - 0.5*20 = 0
```

```python
gradient_descent_1d(lambda t: 2*t, x0=10.0, lr=1.0, steps=100)
->  10.0             # ⚠️ 完全沒有前進
```

最後那個例子值得停下來想：`lr=1.0` 時 `x ← x − 1·2x = −x`，
每一步都跳到對稱的另一邊，**永遠在 ±10 之間震盪**。100 步（偶數）之後回到 10.0。

而 `lr=1.1` 會**發散**——每一步都跳得更遠，最後爆炸。

**限制**
- `steps >= 0`（為 0 時直接回傳 `x0`）。
- 判定使用近似比較。
- 不需要判斷收斂或提前停止，就老實跑滿 `steps` 次。

**這題就是所有深度學習優化器的最小核心。** Adam、SGD with momentum
都是在這條式子上加東西，但骨架就是這一行。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 025-gradient-descent-1d` 驗證
3. 卡住 → `python trainer.py hint 025-gradient-descent-1d`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 025-gradient-descent-1d`
