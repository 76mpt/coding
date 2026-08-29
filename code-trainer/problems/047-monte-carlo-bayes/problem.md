# 047-monte-carlo-bayes · 用模擬驗證貝氏

- 階段：前置：高中數學重補（公式與計算流利度） / M00.6 機率、期望值與貝氏
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`simulate_posterior`
- 提示：共 4 階（`python trainer.py hint 047-monte-carlo-bayes`）
- 測資：9 筆（`python trainer.py test 047-monte-carlo-bayes`）

────────────────────────────────────────────────────────────────────

上一題你用公式算出後驗機率。這題**用模擬驗證那個公式是對的**。

做法很直白：**產生一大堆虛擬的人，數數看**。

```
對每一個人：
  1. 依 prior 決定他有沒有病
  2. 依 sensitivity / specificity 決定他驗出陽性還是陰性
  3. 記錄下來

最後：陽性的人裡面，有病的佔幾成？
```

如果模擬的結果收斂到公式算出來的值，**兩條完全獨立的路徑得到同一個答案**——
那就是你的公式沒推錯。

## 要實作的函式

```python
simulate_posterior(prior, sensitivity, specificity, n, seed)
```

- `n`：模擬幾個人
- `seed`：亂數種子（**一定要用它初始化**，這樣結果才可重現）

回傳 `(估計的後驗機率, 陽性人數)`。
**沒有任何人驗出陽性時，第一項回傳 `None`**（不能除以 0）。

## 怎麼產生隨機事件

```python
import random
rng = random.Random(seed)      # 建一個獨立的產生器，不要用全域的 random.xxx

rng.random() < p               # 以機率 p 為 True
```

`rng.random()` 回傳 `[0, 1)` 的均勻亂數。**它小於 p 的機率剛好就是 p**——
這是把「均勻亂數」變成「任意機率的事件」最基本的手法。

**每個人要用掉幾個亂數？**

這題規定：**每個人剛好抽兩次**——第一次決定有沒有病，第二次決定檢驗結果。
（順序固定，這樣才能對得上參考答案。）

```python
sick = rng.random() < prior
if sick:
    positive = rng.random() < sensitivity
else:
    positive = rng.random() < (1 - specificity)
```

注意 **`if/else` 兩支都要抽一次**——不能只在其中一支抽，否則亂數序列會錯開。

**範例**

```python
simulate_posterior(0.01, 0.99, 0.99, 200000, 42)
->  (約 0.5, 約 3960)      # 公式算出來是 0.5；陽性 = 真陽性 1980 + 偽陽性 1980

simulate_posterior(0.5, 0.9, 0.9, 100000, 0)
->  (約 0.9, 約 50000)

simulate_posterior(0.5, 0.0, 1.0, 1000, 7)
->  (None, 0)             # 沒有人陽性
```

**為什麼要用 `random.Random(seed)` 而不是 `random.seed()`**

`random.seed(42)` 會設定**全域**的產生器——如果程式其他地方也在用亂數，
就會互相干擾，結果變得不可重現。

`random.Random(seed)` 建立一個**獨立的實例**，只有你這個函式在用。
**這是可重現實驗的基本要求**，訓練模型時同樣的道理。

**限制**
- 三個機率參數在 `[0, 1]`，`n >= 0`。
- `n` 最多 2×10⁵。
- 判定容差：模擬結果只要落在理論值附近的合理範圍即可。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 047-monte-carlo-bayes` 驗證
3. 卡住 → `python trainer.py hint 047-monte-carlo-bayes`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 047-monte-carlo-bayes`
