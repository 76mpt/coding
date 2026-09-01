# 047-monte-carlo-bayes · 用模擬驗證貝氏 — 參考解

## 標準解

```python
import random


def simulate_posterior(prior, sensitivity, specificity, n, seed):
    rng = random.Random(seed)
    pos = 0
    tp = 0
    for _ in range(n):
        sick = rng.random() < prior
        p_positive = sensitivity if sick else 1 - specificity
        if rng.random() < p_positive:          # 兩支都會走到這行 → 亂數用量固定
            pos += 1
            if sick:
                tp += 1
    return (None if pos == 0 else tp / pos), pos
```

## `rng.random() < p` 為什麼能製造機率 p 的事件

`rng.random()` 在 `[0, 1)` 上**均勻分布**。落在 `[0, p)` 這段的機率，
就是那一段的長度——也就是 `p`。

```
0                p                    1
├────────────────┼────────────────────┤
│  < p，機率 p   │   >= p，機率 1−p    │
```

**這是所有隨機取樣的基礎**。更複雜的分布用同一個想法推廣：

| 想抽什麼 | 怎麼做 |
|---|---|
| 機率 p 的事件 | `u < p` |
| 任意離散分布 | 累積機率切段，看 `u` 落在哪一段 |
| 任意連續分布 | **反函數取樣**：`F⁻¹(u)`，F 是累積分布函數 |
| 高斯分布 | Box-Muller 變換（兩個均勻亂數 → 兩個常態亂數） |

**M0.10 分布與 MLE、M5.3 Langevin 取樣**都會回到這個主題。

## 為什麼兩支都要抽亂數

```python
# ✗ 亂數用量不固定
if sick:
    positive = rng.random() < sensitivity
else:
    positive = rng.random() < 1 - specificity
```

這樣寫其實**也是每支各抽一次**，沒問題。但如果寫成：

```python
# ✗ 真正的問題寫法
if sick and rng.random() < sensitivity:
    positive = True
elif rng.random() < 1 - specificity:      # sick 為 True 時這行不會執行
    ...
```

短路求值會讓某些路徑少抽一個亂數，**整個序列從那裡開始錯開**。

標準解用**條件運算式先算出機率、再統一抽一次**，結構上就不可能出這種問題：

```python
p_positive = sensitivity if sick else 1 - specificity
if rng.random() < p_positive:
```

> **可重現的模擬要求「亂數的消耗量與執行路徑無關」。**
> 這在除錯隨機演算法時是關鍵——不然你改一行程式，整個亂數序列就變了，
> 根本分不清結果變化是來自你的修改還是來自不同的亂數。

## `random.Random(seed)` vs `random.seed(seed)`

```python
random.seed(42)          # 設定全域產生器
random.random()          # 用全域的

rng = random.Random(42)  # 建立獨立實例
rng.random()             # 只有你在用
```

全域的問題：**你的函式會被別人影響，也會影響別人**。
如果呼叫端在你之前抽過亂數、或者你的函式跟另一個函式交錯執行，結果就不可重現。

**這是「隱藏的全域狀態」的典型危害**，跟 040 那題的類別屬性計數器是同一類問題。

實務上：

| 場景 | 做法 |
|---|---|
| 函式庫、可重複使用的元件 | **一定**用獨立實例，或接受一個 `rng` 參數 |
| 一次性腳本 | 全域也行 |
| PyTorch 訓練 | `torch.manual_seed()` + `numpy.random.seed()` + `random.seed()` **三個都要設**，而且 DataLoader 的 worker 還要另外處理 |

**5.10 訓練迴圈與資料管線**會正式處理「可重現的訓練」，比你想的複雜。

## 模擬的誤差有多大

用 n 個樣本估計一個比例 p，標準誤差是：

```
SE = √(p(1−p) / n)
```

第一筆測資：陽性約 2000 人，估計 p ≈ 0.5，所以
`SE ≈ √(0.25/2000) ≈ 0.011`。三個標準差是 0.034——測資容差設 0.06 很寬鬆。

**注意分母是「陽性人數」不是 n**——後驗機率是在陽性的人裡面算的。
盛行率 1% 時，20 萬人只有 2000 個陽性，**有效樣本數只有 1%**。
這就是為什麼罕見事件的模擬需要極大的樣本量（或者用重要性取樣之類的技巧）。

**誤差隨 `1/√n` 縮小**——要精確 10 倍，需要 100 倍的樣本。
這個 `√n` 收斂速度在 M3.2 集中不等式會正式證明（Hoeffding 界）。

## 為什麼「模擬驗證公式」值得做

公式推導可能推錯，模擬可能寫錯，**但兩者同時錯到同一個答案的機率極低**。

這跟你做過的其他驗證是同一種手法：

| 題 | 兩條獨立路徑 |
|---|---|
| 023/024 | 解析導數 vs 中央差分 |
| 030 | 投影公式 vs 殘差正交性 |
| 035 | 行列式公式 vs 叉積面積 |
| 045 | 矩陣乘法 vs 角度相加 |
| **這題** | **貝氏公式 vs 蒙地卡羅** |

**這是數學軌的核心方法論**：不要相信自己的推導，用程式逼它自證。

## 常見錯誤

1. **用全域 `random`** —— 結果不可重現，隱藏測資會抓（同 seed 跑兩次要一樣）。
2. **沒病時用 `specificity` 而不是 `1 - specificity`** —— 偽陽性機率算反，結果會偏得很誇張。
3. **`pos == 0` 時除以零** —— 要回傳 `None`。
4. **回傳 `0` 而不是 `None`** —— 「沒有陽性」和「陽性但都沒病」是不同的情況，測資用 `is None` 檢查。
5. **n 很小時期待精確結果** —— 模擬有統計誤差，1000 人的模擬不可能精確到小數點後三位。
6. **每次迴圈重建 `random.Random(seed)`** —— 那樣每個人都用同一個亂數，全部一模一樣。`rng` 要在迴圈外建立。
