# 001-bmi-report · BMI 分類報告 — 參考解

## 標準解

```python
def bmi_report(weight_kg: float, height_cm: float) -> str:
    height_m = height_cm / 100
    bmi = round(weight_kg / height_m ** 2, 1)

    if bmi < 18.5:
        category = "過輕"
    elif bmi < 24:
        category = "正常"
    elif bmi < 27:
        category = "過重"
    else:
        category = "肥胖"

    return f"BMI {bmi:.1f} {category}"
```

這就是最佳解——沒有更快的寫法，O(1) 時間 O(1) 空間。這題真正在考的是**把規格翻成程式的精確度**。

## 另一種寫法：查表

當分類從 4 種變成 20 種時，一長串 `elif` 會很難維護。專業的寫法是把「規則」變成資料：

```python
import bisect

THRESHOLDS = [18.5, 24, 27]
CATEGORIES = ["過輕", "正常", "過重", "肥胖"]

def bmi_report(weight_kg: float, height_cm: float) -> str:
    bmi = round(weight_kg / (height_cm / 100) ** 2, 1)
    category = CATEGORIES[bisect.bisect_right(THRESHOLDS, bmi)]
    return f"BMI {bmi:.1f} {category}"
```

`bisect_right` 會回傳「bmi 應該插在 THRESHOLDS 的哪個位置」，剛好就是分類的索引。
規則變動時只要改那兩個 list，不用動邏輯——這種「資料驅動」的想法在工程上很常見。
（`bisect` 就是二分搜尋，你在節點 2.5 會正式學到。）

## 複雜度

O(1) 時間、O(1) 空間。

## 常見錯誤

1. **忘記公分換公尺** — 直接 `weight / height_cm ** 2` 會得到 0.0023 這種值。
   養成習慣：算式寫下去之前先確認每個變數的單位。
2. **分類用原始值、顯示用四捨五入值** — `bmi_report(60, 180)` 原始值是 18.5185，
   兩種順序都會得到「正常」所以看不出來；但如果原始值是 18.4999，
   先四捨五入是 18.5（正常），後四捨五入是 18.4999（過輕），答案就不一樣了。
   規格說「先四捨五入再分類」時，順序就是需求的一部分。
3. **用 `if` 而不是 `elif`** — 四個獨立的 `if` 會讓 BMI=30 同時通過多個分支，
   最後 `category` 被覆寫成最後一個成立的值。
4. **浮點數比較** — 這題安全，但要知道 `0.1 + 0.2 == 0.3` 在 Python 裡是 `False`。
   之後處理浮點數相等時要用 `abs(a - b) < 1e-9` 這種容差比較。

## 延伸思考

`round()` 在 Python 用的是「銀行家捨入」：`round(2.5)` 是 2 而不是 3，`round(3.5)` 才是 4。
這題因為是 `round(x, 1)` 且輸入是實數運算結果，碰到剛好 .x5 的機率極低所以沒事。
但如果哪天你的金額計算對不上一分錢，通常就是這裡。金融計算要用 `decimal.Decimal`。
