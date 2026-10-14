# 007-min-shipping-capacity · 貨船運送能力下限 — 參考解

## 標準解（二分答案）

```python
def min_capacity(weights: list[int], days: int) -> int:
    def days_needed(cap: int) -> int:
        # 載重為 cap 時，貪心裝載需要幾天
        count, current = 1, 0
        for w in weights:
            if current + w > cap:
                count += 1
                current = 0
            current += w
        return count

    lo, hi = max(weights), sum(weights)     # 答案的可能範圍
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid            # 可行 → 答案是 mid 或更小
        else:
            lo = mid + 1        # 不可行 → 答案一定更大
    return lo
```

**時間 O(n log S)**，S = sum(weights)。n = 10^5、S ≈ 5×10^7 時約 26 輪 × 10^5 = 2.6×10^6 次運算。
**空間 O(1)。**

## 「二分答案」這個套路

一般的二分搜尋是「在有序陣列裡找一個值」。二分答案不一樣：

> 當答案本身具有單調性——**「x 可行 ⟹ 所有 > x 都可行」**——
> 就可以二分猜答案，把「求最佳解」變成「重複驗證」。

辨認訊號：題目問**「最小的最大值」**或**「最大的最小值」**。
中文很拗口，但只要看到這種句型，八成就是二分答案。

三個步驟，缺一不可：

1. **確定答案的範圍** `[lo, hi]`，且要保證 `hi` 一定可行（否則二分會回傳一個假答案）。
2. **寫出 `check(x)`**，判斷 x 是否可行。這通常是個貪心或模擬，是全題最需要動腦的部分。
3. **證明單調性**：x 可行 ⟹ x+1 也可行。沒有單調性就不能二分。

這題的單調性證明：載重從 cap 提高到 cap+1，原本的分法**仍然合法**（每天的總重沒變、上限變寬），
所以需要的天數不會變多。因此 `days_needed` 對 cap 單調不增。∎

## 邊界為什麼是 `max(weights)` 而不是 1 或 0

如果 `lo` 從 1 開始，答案雖然還是對的（因為小於 max 的 cap 都會被判為不可行），
但 `days_needed` 會遇到「單一包裹就超過 cap」的情況：

```python
if current + w > cap:   # current 歸零後仍然 0 + w > cap
    count += 1
    current = 0
current += w            # 硬塞進去，這一天超載了
```

程式不會爆炸，但 `days_needed` 回傳的天數在語意上是錯的（那天裝了超過上限的貨）。
剛好因為它回傳的天數偏大會被判不可行，答案沒錯——**靠運氣對的程式碼**。

從 `max(weights)` 起步就沒有這個模糊地帶，而且少跑幾輪。
**二分答案的下界要設在「語意上有意義的最小值」**，這是好習慣。

## 二分模板：兩種寫法別混用

```python
# 找「第一個滿足條件的位置」——這題用的
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):
        hi = mid            # 注意不是 mid - 1
    else:
        lo = mid + 1
return lo                   # 迴圈結束時 lo == hi

# 找「最後一個滿足條件的位置」
while lo < hi:
    mid = (lo + hi + 1) // 2    # 注意 +1，避免無窮迴圈
    if check(mid):
        lo = mid
    else:
        hi = mid - 1
return lo
```

第二種一定要 `+1` 讓 mid 偏右，否則 `lo=3, hi=4` 時 `mid=3`，
若 check 通過則 `lo=3`，區間不變 → **無窮迴圈**。

**建議只背第一種**，遇到「找最後一個」時改成「找第一個不滿足的，再減一」，
可以少記一半的細節，也少一半出錯機會。

## 常見錯誤

1. **`days_needed` 的 count 從 0 開始** — 會少算一天。用 `[10], 1` 這種單元素測資馬上抓到。
2. **可行時寫 `hi = mid - 1`** — 會把正確答案跳過。這個模板裡「可行的 mid 本身可能就是答案」，
   不能排除它。
3. **上界設成 `max(weights) * len(weights)`** — 不算錯（比 sum 大），但白跑好幾輪。
4. **`for cap in range(max(w), sum(w)+1)` 線性掃** — 邏輯完全正確，但 O(n × S)，
   這題是 5×10^12 次運算。**正確但太慢也是不及格**，這是演算法題和寫程式的差別。
5. **忘記包裹順序不能改** — 如果可以排序，這題就變成完全不同的（更難的）裝箱問題。
   **題目說「按順序」時，那個限制往往就是解法的關鍵**。

## 同型題（練會這個套路，這些就都會了）

| 題目 | check(x) 是什麼 |
|---|---|
| LC 875 愛吃香蕉的珂珂 | 速度 x 時要吃幾小時 |
| LC 410 分割陣列的最大值 | 每段和 ≤ x 時要分幾段 |
| LC 1482 製作花束所需最少天數 | 第 x 天時能做幾束 |
| LC 4 兩個排序陣列的中位數 | （進階）分割點是否合法 |

## 和 CV 的關聯

二分答案在研究裡出現得比想像中多：

- **調閾值**：找「讓 recall ≥ 0.95 的最大 confidence 閾值」，
  因為 recall 對閾值單調，可以二分而不是掃 1000 個值。
- **找最大 batch size**：不斷試「這個 batch size 會不會 OOM」，
  是否 OOM 對 batch size 單調 → 二分幾次就能逼出上限。
- **NMS 的 IoU 閾值調參**、**學習率的 LR range test**，思路都類似。
