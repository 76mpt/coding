# 007-min-shipping-capacity · 貨船運送能力下限

- 階段：資料結構與演算法（LeetCode 風格） / 2.5 二分搜尋
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`min_capacity`
- 提示：共 4 階（`python trainer.py hint 007-min-shipping-capacity`）
- 測資：9 筆（`python trainer.py test 007-min-shipping-capacity`）

────────────────────────────────────────────────────────────────────

碼頭上有一排包裹，第 i 個包裹重 `weights[i]`。船每天出航一次，
**必須按照順序**把包裹裝上船（不能跳過、不能重排），每天裝的總重不能超過船的載重上限。

給定 `weights` 和天數 `days`，求「能在 `days` 天內把所有包裹運完」的**最小載重上限**。

**範例**

```
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5
```

答案是 `15`。載重 15 時的分法是：

```
第 1 天：1, 2, 3, 4, 5   (15)
第 2 天：6, 7            (13)
第 3 天：8               (8)
第 4 天：9               (9)
第 5 天：10              (10)
```

載重 14 就不可能在 5 天內運完，所以 15 是最小值。

```
min_capacity([1,2,3,4,5,6,7,8,9,10], 5)  ->  15
min_capacity([3,2,2,4,1,4], 3)           ->  6
min_capacity([1,2,3,1,1], 4)             ->  3
min_capacity([10], 1)                    ->  10
```

**限制**
- `1 <= len(weights) <= 10^5`
- `1 <= weights[i] <= 500`
- `1 <= days <= len(weights)`

**效能要求**：有一筆 10 萬個包裹的大測資並附時間上限。
從最小可能載重開始一個一個試（`for cap in range(...)`）會超時。

**提示方向**：這題不是「算出」答案，而是「找出」答案。想想看你能不能**驗證**一個給定的載重行不行。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 007-min-shipping-capacity` 驗證
3. 卡住 → `python trainer.py hint 007-min-shipping-capacity`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 007-min-shipping-capacity`
