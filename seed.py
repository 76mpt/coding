# -*- coding: utf-8 -*-
"""內建種子題目。

用 `python trainer.py seed` 匯入。之後的題目由 AI 教練依 curriculum.json 即時生成，
這裡只是讓系統一裝好就能開始練。

每個 spec 的欄位說明見 README.md。
"""
from __future__ import annotations

import json
from pathlib import Path

# =====================================================================
# S1 基本功
# =====================================================================

P_BMI = {
    "title": "BMI 分類報告",
    "slug": "bmi-report",
    "lang": "py",
    "node": "1.1",
    "difficulty": "warmup",
    "mode": "function",
    "entry": "bmi_report",
    "tags": ["型別轉換", "f-string", "四捨五入", "分支"],
    "statement_md": """\
實作 `bmi_report(weight_kg, height_cm)`，回傳一行 BMI 報告字串。

BMI 的定義是「體重(公斤) ÷ 身高(公尺)的平方」。注意傳進來的身高單位是**公分**。

規則：
1. 先算出 BMI，**四捨五入到小數點後一位**，之後的分類都用這個「四捨五入後的值」判斷。
2. 依這個值分類：

   | BMI 範圍 | 分類 |
   |---|---|
   | < 18.5 | 過輕 |
   | 18.5 ≤ BMI < 24 | 正常 |
   | 24 ≤ BMI < 27 | 過重 |
   | ≥ 27 | 肥胖 |

3. 回傳格式為 `"BMI {值} {分類}"`，值固定顯示一位小數（即使是整數也要顯示 `.0`）。

**範例**

```
bmi_report(70, 175)    ->  "BMI 22.9 正常"
bmi_report(50, 170)    ->  "BMI 17.3 過輕"
bmi_report(80, 172)    ->  "BMI 27.0 肥胖"
bmi_report(72.5, 168)  ->  "BMI 25.7 過重"
```

**限制**
- `weight_kg` 與 `height_cm` 都是正數，可能是整數或浮點數。
- 不需要處理非法輸入。

**特別注意邊界**：`bmi_report(60, 180)` 算出來是 18.5185…，四捨五入後是 18.5，屬於「正常」而不是「過輕」。
""",
    "starter": '''\
def bmi_report(weight_kg: float, height_cm: float) -> str:
    """回傳 "BMI 22.9 正常" 這種格式的字串。"""
    # TODO: 1) 公分換公尺 2) 算 BMI 並四捨五入到小數第一位
    #       3) 依範圍決定分類 4) 用 f-string 組出結果
    pass
''',
    "hints": [
        "先把身高換算成公尺再平方。`height_cm / 100` 會得到浮點數，"
        "而 `height_cm // 100` 是整數除法會把小數丟掉——這題要用前者。\n"
        "「平方」可以寫 `x ** 2` 或 `x * x`，兩種都可以。",

        "四捨五入到一位小數用內建的 `round(值, 1)`。\n"
        "重點是**順序**：題目要求先四捨五入，再拿四捨五入後的結果去比大小。\n"
        "如果你先用原始值分類再四捨五入顯示，`bmi_report(60, 180)` 就會分錯類。",

        "分類的四個範圍是連續且不重疊的，所以用 `if / elif / elif / else` 一路往下接即可，"
        "不需要寫 `if 18.5 <= bmi and bmi < 24` 這種雙重條件——"
        "因為能走到第二個 `elif`，就代表前面的條件都不成立，已經隱含 `bmi >= 18.5` 了。\n"
        "（Python 也支援 `18.5 <= bmi < 24` 這種連寫，之後會很常用。）",

        "格式化字串固定一位小數用 f-string 的格式規格：`f\"BMI {bmi:.1f} {category}\"`。\n"
        "`:.1f` 的意思是「當成浮點數、顯示一位小數」。\n"
        "如果直接寫 `f\"BMI {bmi} ...\"`，當 bmi 剛好是 27.0 時會印成 `27.0`（碰巧對），"
        "但 18.5 這種也可能印成 `18.5`——問題出在像 `5.6` 這種值不保證，所以還是要用 `:.1f`。",
    ],
    "tests": [
        {"args": [70, 175], "expected": "BMI 22.9 正常"},
        {"args": [50, 170], "expected": "BMI 17.3 過輕"},
        {"args": [80, 172], "expected": "BMI 27.0 肥胖"},
        {"args": [72.5, 168], "expected": "BMI 25.7 過重"},
        {"args": [60, 180], "expected": "BMI 18.5 正常"},
        {"args": [53, 170], "expected": "BMI 18.3 過輕"},
        {"args": [95, 160], "expected": "BMI 37.1 肥胖"},
        {"args": [0.5, 30], "expected": "BMI 5.6 過輕", "hidden": True,
         "note": "極端小的值，檢查你沒有寫死任何數字"},
    ],
    "verify_code": '''\
def bmi_report(weight_kg: float, height_cm: float) -> str:
    bmi = round(weight_kg / (height_cm / 100) ** 2, 1)
    if bmi < 18.5:
        category = "過輕"
    elif bmi < 24:
        category = "正常"
    elif bmi < 27:
        category = "過重"
    else:
        category = "肥胖"
    return f"BMI {bmi:.1f} {category}"
''',
    "reference_md": """\
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
""",
}

P_COLLATZ = {
    "title": "Collatz 序列的步數與峰值",
    "slug": "collatz-steps",
    "lang": "py",
    "node": "1.2",
    "difficulty": "warmup",
    "mode": "function",
    "entry": "collatz",
    "tags": ["while 迴圈", "累加器", "多回傳值", "整數運算"],
    "statement_md": """\
Collatz 猜想（又叫冰雹數列）的規則很簡單，從一個正整數 n 開始，不斷做：

- 如果 n 是**偶數**，把它變成 `n // 2`
- 如果 n 是**奇數**，把它變成 `3 * n + 1`

一直做到 n 變成 1 為止。目前數學上還沒人能證明「所有正整數都會回到 1」，但它對所有測資都成立。

實作 `collatz(n)`，回傳一個 tuple `(步數, 過程中出現過的最大值)`：

- **步數** = 從 n 走到 1 一共做了幾次變換。n 本身如果就是 1，步數是 0。
- **最大值** = 整個過程中出現過的最大數字，**包含起始的 n 本身**。

**範例**

n = 6 的完整過程是：`6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1`

一共做了 8 次變換，過程中最大的數字是 16，所以回傳 `(8, 16)`。

```
collatz(1)   ->  (0, 1)      # 一開始就是 1，沒有走任何一步，最大值就是 1
collatz(2)   ->  (1, 2)      # 2 → 1
collatz(6)   ->  (8, 16)
collatz(7)   ->  (16, 52)
```

**限制**
- `1 <= n <= 10^6`
- 回傳 tuple 或 list 都可以（比對時會轉成同一種形式）。

**提醒**：奇數變換後會**變大**（`3n+1`），所以「最大值」通常不是起點也不是終點，而是中途的某個數。
""",
    "starter": '''\
def collatz(n: int) -> tuple[int, int]:
    """回傳 (走到 1 的步數, 過程中出現過的最大值)。"""
    # TODO: 用一個 while 迴圈，直到 n 變成 1
    #       途中要維護兩個東西：走了幾步、看過的最大值
    pass
''',
    "hints": [
        "這題不能用 `for`，因為你事先不知道要跑幾次——這正是 `while` 的使用時機。\n"
        "迴圈條件就是題目的結束條件：`while n != 1:`。\n\n"
        "在迴圈開始前，你需要準備兩個變數來「累積」答案。想一想它們的初始值該是什麼？\n"
        "（提示：如果 n 一開始就是 1，迴圈一次都不會執行，這時候回傳的必須是 `(0, 1)`。"
        "反推回去，初始值就出來了。）",

        "判斷偶數用取餘數：`n % 2 == 0`。\n"
        "偶數要除以 2 時，請用 `n // 2` 而不是 `n / 2`——\n"
        "`/` 在 Python 3 永遠回傳浮點數，`10 / 2` 會得到 `5.0` 而不是 `5`。\n"
        "一旦變成浮點數，後面的 `n != 1` 比較和最大值都可能出問題（而且大數字會失去精度）。\n"
        "`//` 是整數除法，才是這題要的。",

        "「維護最大值」是很常見的模式，長這樣：\n\n"
        "```python\n"
        "biggest = 起始值\n"
        "for/while ...:\n"
        "    目前值 = 算出新的值\n"
        "    if 目前值 > biggest:\n"
        "        biggest = 目前值\n"
        "```\n\n"
        "Python 有更短的寫法：`biggest = max(biggest, 目前值)`，效果完全一樣。\n\n"
        "關鍵問題：你應該在**更新 n 之後**才去比較最大值，還是之前？\n"
        "想一下 `collatz(1)`：迴圈一次都不跑，最大值必須是 1，所以起始值就得先算進去。",

        "完整骨架（自己填空）：\n\n"
        "```python\n"
        "def collatz(n):\n"
        "    steps = 0\n"
        "    largest = n          # n 本身也算在內\n"
        "    while n != 1:\n"
        "        if n % 2 == 0:\n"
        "            n = ?\n"
        "        else:\n"
        "            n = ?\n"
        "        largest = max(largest, n)\n"
        "        steps += 1\n"
        "    return steps, largest\n"
        "```\n\n"
        "回傳多個值時，`return a, b` 就會自動打包成 tuple，不用寫 `return (a, b)`。",
    ],
    "tests": [
        {"args": [1], "expected": [0, 1]},
        {"args": [2], "expected": [1, 2]},
        {"args": [6], "expected": [8, 16]},
        {"args": [7], "expected": [16, 52]},
        {"args": [27], "expected": [111, 9232], "hidden": True,
         "note": "這是 100 以內步數最多的起點，中途會衝到 9232"},
        {"args": [97], "expected": [118, 9232], "hidden": True,
         "note": "步數比 27 更多，但峰值一樣"},
    ],
    "verify_code": '''\
def collatz(n: int) -> tuple[int, int]:
    steps = 0
    largest = n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        largest = max(largest, n)
        steps += 1
    return steps, largest
''',
    "reference_md": """\
## 標準解

```python
def collatz(n: int) -> tuple[int, int]:
    steps = 0
    largest = n              # 起點本身也要納入比較

    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        largest = max(largest, n)
        steps += 1

    return steps, largest
```

這是「累加器模式」的教科書範例：迴圈外初始化，迴圈內更新，迴圈後回傳。
`steps` 累加次數、`largest` 累積最大值，兩個各自獨立。

## 更精簡的寫法

```python
def collatz(n: int) -> tuple[int, int]:
    steps, largest = 0, n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        largest = max(largest, n)
        steps += 1
    return steps, largest
```

`n = A if 條件 else B` 是條件運算式（其他語言叫三元運算子）。
只在「兩個分支都只是給同一個變數賦值」時才用它——否則 `if/else` 更清楚。

## 位元運算版（競賽風格，看看就好）

```python
def collatz(n: int) -> tuple[int, int]:
    steps, largest = 0, n
    while n != 1:
        n = n >> 1 if n & 1 == 0 else 3 * n + 1
        if n > largest:
            largest = n
        steps += 1
    return steps, largest
```

`n & 1` 取最低位元判斷奇偶，`n >> 1` 右移一位等於除以 2。
在 C++ 競賽裡這會快一些；在 Python 裡差異很小，可讀性反而更差。
**知道有這種寫法**比**用它**重要——你之後讀別人的競賽 code 會常看到。

## 複雜度

時間 O(k)，k 是序列長度。k 沒有已知的上界公式（這正是 Collatz 猜想未解的部分），
但實務上對 n ≤ 10^6，k 最多幾百步。空間 O(1)——只用了兩個變數。

留意：**用 O(1) 空間是刻意的**。如果你為了求最大值先把整條序列存進 list 再 `max(seq)`，
答案一樣對，但空間變成 O(k)。當題目只需要「彙總結果」而不需要「完整過程」時，
邊走邊算是更好的習慣——這個直覺在處理大資料集時會救你一命。

## 常見錯誤

1. **用 `/` 而不是 `//`** — 最容易踩的坑。`n / 2` 讓 n 變成 float，
   之後 `n != 1` 比的是 `1.0 != 1`（這其實是 False，所以還會停），
   但回傳的最大值會變成 `16.0` 而不是 `16`，測資就不過。
2. **最大值初始化成 0 或 1** — 那 `collatz(1)` 會回傳 `(0, 1)` 剛好碰對，
   但如果初始化成 0 而 n 一路遞減，答案就錯了。初始值設成 `n` 最安全。
3. **在更新 n 之前才更新 largest** — 會漏掉最後一步產生的值。
   不過因為序列最後一定收在 1（最小值），這題碰巧看不出差別。
   養成習慣：**先產生新值，再拿新值去更新彙總量**。
4. **步數多算或少算一次** — 把 `steps += 1` 放在 `while` 迴圈外面或條件判斷裡。
   最可靠的檢查法：拿 `n = 2`（答案是 1 步）和 `n = 1`（答案是 0 步）手動跑一遍。

## 延伸

如果要算「1 到 10^6 之間，哪個起點的步數最多」，直接對每個 n 各跑一次是 O(n·k)，會很慢。
正確做法是**記憶化**：把算過的 n 對應的步數存起來，遇到算過的就直接查表。
這是動態規劃的雛形，你在節點 2.11 會正式學到。
""",
}

P_DISCOUNT = {
    "title": "滿額折扣結帳",
    "slug": "apply-discount",
    "lang": "py",
    "node": "1.3",
    "difficulty": "standard",
    "mode": "function",
    "entry": "apply_discount",
    "tags": ["預設參數", "keyword-only", "多回傳值", "sum"],
    "statement_md": """\
實作結帳函式，函式簽章**必須完全長這樣**（這是這題的重點之一）：

```python
def apply_discount(prices, *, threshold=1000, rate=0.9) -> tuple[int, bool]:
```

規則：
1. 先把 `prices`（一個數字 list）加總得到小計。
2. 如果小計 **大於或等於** `threshold`，就打折：金額變成 `小計 × rate`，**四捨五入成整數**。
3. 否則不打折，金額就是小計。
4. 回傳 `(最終金額, 是否有打折)`，第一項是整數，第二項是布林值。

**範例**

```
apply_discount([100, 200, 300])                    ->  (600, False)   # 600 < 1000，不打折
apply_discount([500, 600])                         ->  (990, True)    # 1100 * 0.9 = 990
apply_discount([100, 200, 300], threshold=500)     ->  (540, True)    # 600 >= 500，600 * 0.9 = 540
apply_discount([1000], rate=0.75)                  ->  (750, True)
apply_discount([])                                 ->  (0, False)     # 空購物車
```

**關於簽章裡的那個 `*`**

參數列中間的 `*` 代表「它後面的參數只能用關鍵字傳」。也就是說：

```python
apply_discount([1000], threshold=500)   # ✅ 可以
apply_discount([1000], 500)             # ❌ 必須拋出 TypeError
```

這是 Python 的語言特性，你**不需要自己寫檢查**——只要簽章寫對，Python 會自動幫你擋。
測資裡有一筆就是在驗證這件事。

**限制**
- `prices` 可能是空 list。
- 價格都是非負數。
- 小計剛好等於 `threshold` 時**要**打折。
""",
    "starter": '''\
def apply_discount(prices, *, threshold=1000, rate=0.9):
    """回傳 (最終金額, 是否有打折)。"""
    # TODO
    pass
''',
    "hints": [
        "加總一個 list 用內建的 `sum(prices)`，空 list 會回傳 0，剛好符合題目要的行為，"
        "所以你**不需要**特別寫 `if not prices` 來處理空購物車。\n\n"
        "先寫出「算小計 → 判斷要不要打折 → 回傳」這三步，暫時不管型別細節。",

        "「大於或等於」是 `>=`，不是 `>`。\n"
        "題目特別提到「小計剛好等於 threshold 時要打折」就是在測這個——"
        "這種**邊界條件**在規格裡出現時，通常就是測資會打的地方。\n\n"
        "回傳兩個值直接寫 `return 金額, 有沒有打折` 就好，Python 會自動打包成 tuple。",

        "四捨五入成整數用 `round(x)`（不給第二個參數就是取到整數，而且回傳的是 `int` 型別）。\n\n"
        "注意 `1100 * 0.9` 在浮點數運算下是 `990.0000000000001`，直接回傳會是 float，測資不會過。\n"
        "所以一定要包一層 `round()`。\n\n"
        "另外：不打折的那條路徑要回傳**原本的小計**，不要也去 round——"
        "如果小計本來就是整數，round 過還是整數，這裡沒差；但養成「只在需要時才轉換」的習慣。",

        "骨架：\n\n"
        "```python\n"
        "def apply_discount(prices, *, threshold=1000, rate=0.9):\n"
        "    subtotal = sum(prices)\n"
        "    if subtotal >= threshold:\n"
        "        return ?, True\n"
        "    return subtotal, False\n"
        "```\n\n"
        "簽章直接照抄題目的，一個字都不要改——`*` 也要留著。\n"
        "那個 `*` 就是 TypeError 那筆測資會過的原因，你不用寫任何額外程式碼。",
    ],
    "tests": [
        {"args": [[100, 200, 300]], "expected": [600, False]},
        {"args": [[500, 600]], "expected": [990, True]},
        {"args": [[100, 200, 300]], "kwargs": {"threshold": 500}, "expected": [540, True]},
        {"args": [[]], "expected": [0, False]},
        {"args": [[999]], "expected": [999, False], "note": "剛好差一元，不打折"},
        {"args": [[1000]], "kwargs": {"rate": 0.75}, "expected": [750, True],
         "note": "小計剛好等於門檻，要打折"},
        {"args": [[333, 333, 334]], "kwargs": {"rate": 0.85}, "expected": [850, True]},
        {"args": [[1000], 500], "raises": "TypeError", "hidden": True,
         "note": "第二個參數用位置傳，簽章裡的 * 應該讓它失敗"},
    ],
    "verify_code": '''\
def apply_discount(prices, *, threshold=1000, rate=0.9):
    subtotal = sum(prices)
    if subtotal >= threshold:
        return round(subtotal * rate), True
    return subtotal, False
''',
    "reference_md": """\
## 標準解

```python
def apply_discount(prices, *, threshold: int = 1000, rate: float = 0.9) -> tuple[int, bool]:
    subtotal = sum(prices)
    if subtotal >= threshold:
        return round(subtotal * rate), True
    return subtotal, False
```

五行，沒有更短的必要。這題考的是**函式介面設計**，不是演算法。

## `*` 到底在幹嘛

```python
def f(a, *, b=1, c=2): ...
```

`*` 之後的參數變成 **keyword-only**：呼叫時只能寫 `f(x, b=5)`，不能寫 `f(x, 5)`。

為什麼要這樣設計？看這個呼叫：

```python
apply_discount(cart, 500, 0.8)     # 500 和 0.8 分別是什麼？要翻文件才知道
apply_discount(cart, threshold=500, rate=0.8)   # 一眼看懂
```

**經驗法則**：一個函式如果有兩個以上的可選參數，而且型別相近（都是數字、都是布林），
就把它們設成 keyword-only。這能擋掉「參數順序寫反」這種最難查的 bug——
`apply_discount(cart, 0.8, 500)` 如果合法，你會得到一個完全錯誤但不會報錯的結果。

同理還有 positional-only 的 `/`（Python 3.8+），但用得少很多。

## 可變預設值的陷阱（一定要知道）

這題的預設值是數字所以安全，但如果哪天你寫：

```python
def add_item(item, cart=[]):     # ❌ 千萬不要
    cart.append(item)
    return cart
```

`cart=[]` **只會在函式定義時建立一次**，之後每次呼叫都共用同一個 list：

```python
add_item("a")   # ['a']
add_item("b")   # ['a', 'b']  ← 上一次的東西還在！
```

正確寫法：

```python
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

規則很簡單：**預設值只能用不可變物件**（數字、字串、tuple、None、布林）。
list / dict / set 一律用 `None` 當預設再在函式裡建立。
這是 Python 面試最常考的題目之一。

## 複雜度

`sum()` 是 O(n)，其餘 O(1)。空間 O(1)。

## 常見錯誤

1. **忘記 `round()`** — `1100 * 0.9` 的浮點結果是 `990.0000000000001`，
   回傳 float 而不是 int，測資 `expected: 990` 不會過。
   浮點數乘法幾乎不可能剛好是整數，只要規格說「金額是整數」就一定要 round。
2. **用 `>` 而不是 `>=`** — 小計剛好等於門檻時漏打折。規格裡出現「以上」「至少」「不小於」
   這些詞就是在講 `>=`。讀規格時把這些字圈起來。
3. **把 `*` 刪掉** — 覺得「這樣寫比較短」而改成 `def apply_discount(prices, threshold=1000, rate=0.9)`。
   功能測資會過，但 TypeError 那筆不會過。**簽章也是規格的一部分。**
4. **特別處理空 list** — 寫 `if not prices: return 0, False`。不算錯，但多餘：
   `sum([])` 本來就是 0，然後 `0 >= 1000` 是 False。
   **能靠既有語意自然成立的邊界，就不要寫特例**——每個 if 都是未來的 bug 溫床。
5. **回傳 list 而不是 tuple** — 這題兩者都會過（比對時會轉換），
   但慣例上「固定長度、各項意義不同」用 tuple，「同質、長度可變」用 list。

## 延伸

實務上這種函式很快就會長出更多需求：會員等級、優惠券疊加、稅金、四捨五入規則。
這時候參數列會爆炸，正確的重構方向是把參數收成一個設定物件：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DiscountPolicy:
    threshold: int = 1000
    rate: float = 0.9

def apply_discount(prices, policy: DiscountPolicy = DiscountPolicy()) -> tuple[int, bool]:
    ...
```

（`frozen=True` 讓它不可變，所以當預設值是安全的。）
你會在節點 1.8 和 4.1 正式練到這個。
""",
}

P_TOPK = {
    "title": "詞頻 Top-K",
    "slug": "top-k-words",
    "lang": "py",
    "node": "1.4",
    "difficulty": "standard",
    "mode": "function",
    "entry": "top_k_words",
    "timeout": 8,
    "tags": ["dict 計數", "sorted key", "同分排序", "tuple"],
    "statement_md": """\
實作 `top_k_words(text, k)`，統計文字裡每個單字出現幾次，回傳出現最多的前 k 個。

規則：
1. 以**空白**切分單字（連續多個空白視為一個分隔）。不用處理標點符號。
2. **不分大小寫**：`"The"` 和 `"the"` 算同一個字，回傳時統一用小寫。
3. 回傳 `[(單字, 次數), ...]`，共 k 個（若相異單字不足 k 個，就回傳全部）。
4. 排序規則：**次數由多到少**；次數相同時，**依單字的字典序由小到大**。

**範例**

```
top_k_words("the quick the fox the", 2)
->  [("the", 3), ("fox", 1)]
```

`the` 出現 3 次排第一。`quick` 和 `fox` 都是 1 次，同分時比字典序，`"fox" < "quick"`，所以 fox 勝出。

```
top_k_words("A a b B c", 3)    ->  [("a", 2), ("b", 2), ("c", 1)]
top_k_words("", 3)             ->  []
top_k_words("one two three", 10)  ->  [("one", 1), ("three", 1), ("two", 1)]
top_k_words("x y z", 0)        ->  []
```

**限制**
- `text` 可能是空字串或只有空白。
- `0 <= k`，k 可能大於相異單字數。
- 文字長度最多約 10^6 個字元。

**效能要求**：有一筆 20 萬個單字的大測資並附時間上限。
每個單字都用 `text.split().count(word)` 去數是 O(n²)，會超時。
""",
    "starter": '''\
def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """回傳出現次數前 k 名的 (單字, 次數)。"""
    # TODO
    pass
''',
    "hints": [
        "分三步做，每一步都很單純：\n"
        "1. 把文字切成單字 list\n"
        "2. 數每個單字出現幾次\n"
        "3. 排序後取前 k 個\n\n"
        "切分用 `text.lower().split()`。**不要傳參數給 split()**——\n"
        "`split()` 不給參數時會自動處理連續空白、換行、tab，而且開頭結尾的空白也不會產生空字串。\n"
        "`split(' ')` 反而會在連續空白處產生一堆 `''`。這是 Python 一個很貼心的設計。",

        "數次數的標準做法是用 dict 當計數器：\n\n"
        "```python\n"
        "counts = {}\n"
        "for word in words:\n"
        "    counts[word] = counts.get(word, 0) + 1\n"
        "```\n\n"
        "`counts.get(word, 0)` 的意思是「拿 word 的值，沒有的話就當作 0」。\n"
        "如果直接寫 `counts[word] + 1`，第一次遇到某個字時會 KeyError。\n\n"
        "為什麼一定要用 dict？因為 dict 的查找是 **O(1)**。\n"
        "如果你對每個單字都跑一次 `words.count(word)`，每次都要掃過整個 list，"
        "總共就是 O(n²)——20 萬個字就是 400 億次比較。",

        "排序的關鍵在 `sorted()` 的 `key` 參數：它接受一個函式，"
        "對每個元素算出一個「排序用的值」，然後照那個值排。\n\n"
        "這題要**兩個層次**的排序：次數由大到小，同分時單字由小到大。\n"
        "Python 排序 tuple 時是逐項比較的（先比第 0 項，一樣才比第 1 項），\n"
        "所以你只要讓 key 回傳一個 tuple 就能一次搞定兩個層次。\n\n"
        "剩下的問題是「次數要由大到小、單字要由小到大」，方向相反。\n"
        "整個 `sorted(reverse=True)` 會把兩個層次都反過來，不是你要的。\n"
        "有個小技巧可以只把數字那一項反向——想想看負號能做什麼。",

        "```python\n"
        "def top_k_words(text, k):\n"
        "    counts = {}\n"
        "    for word in text.lower().split():\n"
        "        counts[word] = counts.get(word, 0) + 1\n"
        "\n"
        "    ordered = sorted(counts.items(), key=lambda kv: (?, ?))\n"
        "    return ordered[:k]\n"
        "```\n\n"
        "- `counts.items()` 會給你 `[(單字, 次數), ...]`，剛好就是要回傳的形狀。\n"
        "- `lambda kv: ...` 裡的 `kv` 就是每一個 `(單字, 次數)`，"
        "所以 `kv[0]` 是單字、`kv[1]` 是次數。\n"
        "- 把次數變成 `-kv[1]`，大的次數就變成小的負數，排在前面——這樣就達成「次數由大到小」了。\n"
        "- 切片 `ordered[:k]` 在 k 大於長度時**不會報錯**，會自動回傳全部；k=0 時回傳空 list。"
        "所以你不需要寫任何 if 去處理這兩種情況。",
    ],
    "tests": [
        {"args": ["the quick the fox the", 2], "expected": [["the", 3], ["fox", 1]]},
        {"args": ["A a b B c", 3], "expected": [["a", 2], ["b", 2], ["c", 1]]},
        {"args": ["", 3], "expected": []},
        {"args": ["   \n\t  ", 3], "expected": [], "note": "只有空白字元"},
        {"args": ["one two three", 10], "expected": [["one", 1], ["three", 1], ["two", 1]],
         "note": "k 大於相異單字數"},
        {"args": ["x y z", 0], "expected": []},
        {"args": ["  多   空白   多 ", 2], "expected": [["多", 2], ["空白", 1]],
         "note": "連續空白"},
        {"args": ["b b a a c", 2], "expected": [["a", 2], ["b", 2]],
         "note": "同分時 a 要排在 b 前面，即使 b 先出現"},
        {"args_expr": "[' '.join(['w' + str(i % 5000) for i in range(200000)]), 5]",
         "expected": [["w0", 40], ["w1", 40], ["w10", 40], ["w100", 40], ["w1000", 40]],
         "hidden": True, "max_ms": 1200,
         "note": "20 萬個單字、5000 個相異字，每個都是 40 次，全靠字典序決勝"},
    ],
    "verify_code": '''\
def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]
''',
    "reference_md": """\
## 標準解

```python
def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1

    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]
```

**O(n + m log m)**，n 是單字總數、m 是相異單字數。

## Pythonic 版本（實務上就這樣寫）

```python
from collections import Counter

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
```

`Counter` 就是專門做計數的 dict 子類別，C 實作，比手寫迴圈快 2–3 倍。

⚠️ **但不要用 `Counter.most_common(k)`**：它同分時的順序是「插入順序」而不是字典序，
這題會錯。`most_common` 只在你不在乎同分順序時才能用——這是很多人踩過的坑。

## 最佳解：k 很小時用 heap

當 m（相異單字數）是百萬等級、而 k 只有 10 時，把全部排序是浪費：

```python
import heapq
from collections import Counter

def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    return heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
```

**O(n + m log k)** 而不是 O(n + m log m)。m = 10^6、k = 10 時大約快 5 倍。

用 `nsmallest` 配上 `(-次數, 單字)` 這個 key，語意剛好等同「次數最多、同分取字典序最小」。

實務判斷：**k ≥ m/10 左右就直接 sort**，heap 的常數項比較大反而不划算。
沒實測就別為了 heap 而 heap。

## 那個 `(-kv[1], kv[0])` 為什麼能一次排好兩個層次

Python 比較 tuple 是**逐項字典序比較**：先比第 0 項，相等才比第 1 項。
所以 `key` 回傳 tuple 就等於「多重排序鍵」。

方向相反的問題用負號解決：次數 3 變成 -3，次數 1 變成 -1，而 `-3 < -1`，
所以次數多的排前面。

字串沒有負號可用。如果需要「字串降序 + 數字升序」，就得靠**穩定排序**分兩趟：

```python
items.sort(key=lambda kv: kv[0])                  # 先排次要鍵（升序）
items.sort(key=lambda kv: kv[1], reverse=True)    # 再排主要鍵
```

Python 的 sort 保證**穩定**（相等元素維持原有相對順序），所以第二趟不會打亂第一趟的結果。
順序是**先排次要鍵、後排主要鍵**，很反直覺，記住它。

## 常見錯誤

1. **用 `words.count(word)` 數次數** — O(n²)。20 萬字時是 400 億次比較，跑不完。
   這是新手最常見的效能地雷：**看到 `.count()` 在迴圈裡就要警覺**。
2. **用 `most_common(k)`** — 同分順序錯，見上。
3. **`split(' ')` 而不是 `split()`** — `"a  b".split(' ')` 得到 `['a', '', 'b']`，
   那個空字串會被當成一個「單字」計數。
4. **忘記 `.lower()`，或只對部分做** — 要在切分**之前**（或之後統一）轉小寫，
   不能一半用原字一半用小寫。
5. **手寫 if 處理 k=0 或 k > 長度** — 不必要，切片本來就正確處理這兩種情況。
   `[1,2,3][:0]` 是 `[]`，`[1,2,3][:99]` 是 `[1,2,3]`。
6. **先取前 k 再排序** — 順序反了，會拿到錯的 k 個。

## 延伸

這題的骨架（計數 → 排序 → 取前 k）之後會一直出現：

- **NLP**：詞彙表建立、TF-IDF 的第一步就是這個
- **CV**：資料集類別分布統計、找出長尾類別
- **除錯**：log 裡哪個錯誤最常出現
- **LeetCode 347** Top K Frequent Elements 是同一題

在 CV 訓練前先跑一次類別計數，是發現「資料集不平衡」的最快方法——
很多訓練不起來的模型，問題根本在這裡。
""",
}

P_PARSE = {
    "title": "解析標註檔的一行",
    "slug": "parse-label-line",
    "lang": "py",
    "node": "1.5",
    "difficulty": "standard",
    "mode": "function",
    "entry": "parse_label_line",
    "tags": ["字串處理", "split/strip", "型別轉換", "ValueError"],
    "statement_md": """\
物件偵測資料集的標註檔通常一行一個框，長這樣：

```
cat, 12, 30, 80, 95
```

五個欄位依序是：**類別名稱、x1、y1、x2、y2**（左上角與右下角座標）。

實作 `parse_label_line(line)`，把一行解析成 dict：

```python
{"label": "cat", "box": [12, 30, 80, 95]}
```

規則：
1. 用逗號 `,` 切分，每個欄位都要**去除頭尾空白**。
2. 類別名稱轉成**小寫**。名稱中間的空白要保留（`"Cat Dog"` → `"cat dog"`）。
3. 四個座標轉成 **int**（可能是負數）。
4. `box` 是一個長度 4 的 list：`[x1, y1, x2, y2]`。

**遇到以下情況要 `raise ValueError`**（訊息內容不限）：

| 情況 | 例子 |
|---|---|
| 欄位數不是 5 個 | `"person, 1, 2, 3"` |
| 座標不是整數 | `"cat, 1, 2, x, 4"` |
| 類別名稱是空的 | `", 1, 2, 3, 4"` |
| 框無效：`x2 <= x1` 或 `y2 <= y1` | `"cat, 10, 10, 5, 20"` |

**範例**

```
parse_label_line("cat, 12, 30, 80, 95")   ->  {"label": "cat", "box": [12, 30, 80, 95]}
parse_label_line("  DOG ,0,0,10,10  ")    ->  {"label": "dog", "box": [0, 0, 10, 10]}
parse_label_line("cat,-5,-5,5,5")         ->  {"label": "cat", "box": [-5, -5, 5, 5]}
parse_label_line("person, 1, 2, 3")       ->  raise ValueError
```

**為什麼要拋例外而不是回傳 None**：
資料集有幾萬行，如果壞掉的那行靜靜地回傳 None，你會在三小時後訓練崩潰時才發現。
**壞掉就要大聲壞掉**，而且要在最靠近問題的地方壞掉。
""",
    "starter": '''\
def parse_label_line(line: str) -> dict:
    """把一行標註解析成 {"label": str, "box": [x1, y1, x2, y2]}。

    格式錯誤時 raise ValueError。
    """
    # TODO
    pass
''',
    "hints": [
        "先做「快樂路徑」（一切正常的情況），再回頭補錯誤處理。\n\n"
        "第一步：`line.split(',')` 會得到一個字串 list。\n"
        "第二步：每個欄位都要 `.strip()` 去掉頭尾空白。\n\n"
        "有個很好用的寫法可以一次做完：\n"
        "```python\n"
        "parts = [p.strip() for p in line.split(',')]\n"
        "```\n"
        "這叫 list comprehension，意思是「對 split 出來的每個 p，取 p.strip()，組成新 list」。\n"
        "（節點 1.6 會專門練這個。）",

        "「欄位數不是 5」的檢查放在最前面，因為後面所有步驟都假設有 5 個欄位。\n\n"
        "```python\n"
        "if len(parts) != 5:\n"
        "    raise ValueError(f\"需要 5 個欄位，得到 {len(parts)} 個：{line!r}\")\n"
        "```\n\n"
        "這種「先擋掉不合法的情況再往下做」的寫法叫 **early return / guard clause**，"
        "比把主邏輯包在一層層 if 裡面好讀很多。\n\n"
        "錯誤訊息裡把原始資料帶上（`{line!r}` 的 `!r` 是用 repr 顯示，"
        "會保留引號和跳脫字元，看得出有沒有隱藏的空白），"
        "這樣真的壞掉時你能一眼知道是哪一行。",

        "座標轉整數用 `int(欄位)`。好消息是：**`int(\"x\")` 本來就會拋 ValueError**，\n"
        "所以「座標不是整數」這條規則你完全不用自己檢查，讓 `int()` 自然失敗就好。\n\n"
        "這是很重要的思維：**不要重複實作語言已經提供的驗證**。\n\n"
        "剩下兩條需要自己寫：\n"
        "- 類別名稱空字串：`if not label:` （空字串在 Python 是 falsy）\n"
        "- 框無效：`if x2 <= x1 or y2 <= y1:`\n\n"
        "四個座標一次轉換可以寫 `x1, y1, x2, y2 = [int(p) for p in parts[1:]]`——\n"
        "右邊是 4 個元素的 list，左邊 4 個變數，Python 會自動拆包。",

        "骨架：\n\n"
        "```python\n"
        "def parse_label_line(line):\n"
        "    parts = [p.strip() for p in line.split(',')]\n"
        "    if len(parts) != 5:\n"
        "        raise ValueError(...)\n"
        "\n"
        "    label = parts[0].?          # 記得轉小寫\n"
        "    if not label:\n"
        "        raise ValueError(...)\n"
        "\n"
        "    x1, y1, x2, y2 = [int(p) for p in parts[1:]]   # int() 會自己擋非數字\n"
        "    if ? :\n"
        "        raise ValueError(...)\n"
        "\n"
        "    return {\"label\": label, \"box\": [x1, y1, x2, y2]}\n"
        "```\n\n"
        "注意 `parts[1:]` 是切片，取索引 1 到最後，也就是四個座標。",
    ],
    "tests": [
        {"args": ["cat, 12, 30, 80, 95"], "expected": {"label": "cat", "box": [12, 30, 80, 95]}},
        {"args": ["  DOG ,0,0,10,10  "], "expected": {"label": "dog", "box": [0, 0, 10, 10]}},
        {"args": ["cat,-5,-5,5,5"], "expected": {"label": "cat", "box": [-5, -5, 5, 5]},
         "note": "負座標是合法的"},
        {"args": ["Cat Dog, 1, 2, 3, 4"], "expected": {"label": "cat dog", "box": [1, 2, 3, 4]},
         "note": "名稱中間的空白要保留"},
        {"args": ["person, 1, 2, 3"], "raises": "ValueError"},
        {"args": ["a, 1, 2, 3, 4, 5"], "raises": "ValueError", "note": "欄位太多"},
        {"args": ["cat, 1, 2, x, 4"], "raises": "ValueError"},
        {"args": [", 1, 2, 3, 4"], "raises": "ValueError"},
        {"args": ["   , 1, 2, 3, 4"], "raises": "ValueError",
         "note": "strip 之後才是空字串"},
        {"args": ["cat, 10, 10, 5, 20"], "raises": "ValueError"},
        {"args": ["cat, 0, 0, 0, 10"], "raises": "ValueError", "hidden": True,
         "note": "寬度為 0 的退化框，x2 <= x1"},
        {"args": ["cat, 0, 10, 10, 10"], "raises": "ValueError", "hidden": True,
         "note": "高度為 0"},
    ],
    "verify_code": '''\
def parse_label_line(line: str) -> dict:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise ValueError(f"需要 5 個欄位，得到 {len(parts)} 個：{line!r}")

    label = parts[0].lower()
    if not label:
        raise ValueError(f"類別名稱不可為空：{line!r}")

    x1, y1, x2, y2 = [int(p) for p in parts[1:]]
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"框無效 ({x1},{y1},{x2},{y2})：{line!r}")

    return {"label": label, "box": [x1, y1, x2, y2]}
''',
    "reference_md": """\
## 標準解

```python
def parse_label_line(line: str) -> dict:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise ValueError(f"需要 5 個欄位，得到 {len(parts)} 個：{line!r}")

    label = parts[0].lower()
    if not label:
        raise ValueError(f"類別名稱不可為空：{line!r}")

    x1, y1, x2, y2 = [int(p) for p in parts[1:]]   # int() 自己會擋非整數
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"框無效 ({x1},{y1},{x2},{y2})：{line!r}")

    return {"label": label, "box": [x1, y1, x2, y2]}
```

O(len(line)) 時間、O(1) 額外空間。

結構就是三段 **guard clause** 之後回傳——所有驗證都在前面擋掉，主邏輯不用巢狀。

## 為什麼不自己檢查「是不是整數」

新手常寫：

```python
if not parts[1].isdigit():            # ❌ 三個問題
    raise ValueError(...)
```

1. `"-5".isdigit()` 是 **False**，負座標會被誤判成錯誤。
2. `"１２３".isdigit()` 是 **True**（全形數字），但 `int()` 也能處理，白檢查了。
3. 你重複實作了 `int()` 已經做對的事，而且做得比較差。

**讓專門的函式自己拋錯**，這是 Python 的 EAFP 風格
（Easier to Ask Forgiveness than Permission，先做再說、錯了再處理），
對照的是 LBYL（Look Before You Leap，先檢查再做）。

只有在需要**更好的錯誤訊息**時，才值得包一層：

```python
try:
    x1, y1, x2, y2 = [int(p) for p in parts[1:]]
except ValueError as e:
    raise ValueError(f"座標必須是整數：{line!r}") from e
```

`from e` 會保留原始例外的 traceback（顯示成「The above exception was the direct cause of...」），
除錯時能同時看到「我的訊息」和「真正壞在哪」。**包裝例外時一定要加 `from e`**。

## 實務版：一次處理整個檔案

單行解析只是零件，真實情境長這樣：

```python
from pathlib import Path

def load_labels(path: Path) -> tuple[list[dict], list[tuple[int, str]]]:
    boxes, errors = [], []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.strip()
            if not raw or raw.startswith("#"):     # 跳過空行與註解
                continue
            try:
                boxes.append(parse_label_line(raw))
            except ValueError as e:
                errors.append((lineno, str(e)))
    return boxes, errors
```

三個實務重點：

1. **行號**（`enumerate(f, start=1)`）— 沒有行號的錯誤訊息在幾萬行的檔案裡沒有用。
2. **收集錯誤而不是第一個就中斷** — 一次跑完看到全部 37 個壞行，
   比修一個跑一次修 37 次快得多。
3. **`encoding="utf-8"`** — Windows 上不指定會用系統預設編碼（cp950），
   遇到中文標註直接爆炸。**開檔一律明寫 encoding**。

## 常見錯誤

1. **忘記 `.strip()`** — `"cat, 12".split(",")` 得到 `["cat", " 12"]`，
   注意前面那個空格。`int(" 12")` 剛好可以（int 會自己忽略空白），
   但 `label` 就會變成 `" dog"` 而不是 `"dog"`，測資不會過。
2. **用 `isdigit()` 檢查** — 見上，負數會壞。
3. **先取 `parts[0]` 再檢查長度** — 如果 `line` 是空字串，`split` 得到 `[""]`，
   長度 1，但你已經先摸了 `parts[1]` 就會 IndexError（型別是 IndexError 不是 ValueError，測資不過）。
   **順序很重要：先檢查長度，再存取元素。**
4. **回傳 None 或印訊息取代 raise** — 呼叫端無法區分「解析失敗」和「這行沒有框」。
   拋例外才能強迫呼叫端做決定。
5. **框無效用 `<` 而不是 `<=`** — 寬度為 0 的框（`x1 == x2`）在後續計算 IoU 時
   面積是 0，會產生 0/0。這種退化框必須擋掉，這也是隱藏測資在測的。

## 延伸

真實的標註格式還有幾種，之後會遇到：

- **YOLO**：`class_id cx cy w h`，而且座標是**正規化到 0–1** 的相對值
- **COCO**：JSON，box 是 `[x, y, width, height]`（左上角 + 寬高，不是兩個角）
- **Pascal VOC**：XML，`xmin/ymin/xmax/ymax`

**格式轉換時最常見的 bug 就是搞混 `[x1,y1,x2,y2]` 和 `[x,y,w,h]`**——
兩者的前兩項一樣，所以錯了不會爆炸，只會讓框畫在奇怪的位置、mAP 莫名其妙很低。
養成習慣：函式名或變數名裡就標明格式，例如 `box_xyxy`、`box_xywh`。

節點 4.6 會練完整的資料清理管線，節點 5.8 會用這裡解析出來的框去算 IoU 和 mAP。
""",
}

# =====================================================================
# S2 資料結構與演算法
# =====================================================================

P_MAX_AREA = {
    "title": "盛最多水的容器",
    "slug": "container-with-most-water",
    "lang": "py",
    "node": "2.1",
    "difficulty": "standard",
    "mode": "function",
    "entry": "max_area",
    "timeout": 5,
    "tags": ["雙指標", "對撞指標", "貪心", "LeetCode 11"],
    "statement_md": """\
給一個長度為 n 的整數陣列 `heights`，`heights[i]` 代表第 i 條垂直線的高度，
第 i 條線的兩個端點是 `(i, 0)` 和 `(i, heights[i])`。

從中選**兩條**線，與 x 軸一起圍成一個容器。求這個容器最多能裝多少水。

容器的容量 = **寬 × 高**，其中
- 寬 = 兩條線的索引差
- 高 = 兩條線之中**比較矮**的那一條（水會從矮的那邊溢出去）

回傳最大容量。容器本身不能傾斜。

**範例**

```
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
```

選 index 1（高 8）和 index 8（高 7）：寬 = 8 - 1 = 7，高 = min(8, 7) = 7，容量 = 49。
這是最大值，所以回傳 `49`。

```
max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  ->  49
max_area([1, 1])                       ->  1
max_area([4, 3, 2, 1, 4])              ->  16
max_area([1, 2, 1])                    ->  2
```

**限制**
- `2 <= n <= 2 * 10^5`
- `0 <= heights[i] <= 10^4`

**效能要求**：測資裡有一筆 n = 200,000 的大測資，並且有時間上限。
兩層迴圈枚舉所有配對是 O(n²) ≈ 2×10^10 次運算，會直接超時。
這題的重點就是**想出 O(n) 的做法**。
""",
    "starter": '''\
def max_area(heights: list[int]) -> int:
    """回傳兩線之間能盛的最大水量。"""
    # TODO: 先想清楚為什麼可以只掃一遍
    pass
''',
    "hints": [
        "先確定你能寫出**暴力解**（就算會超時）：兩層迴圈枚舉所有 (i, j) 配對，\n"
        "容量是 `(j - i) * min(heights[i], heights[j])`，取最大。\n\n"
        "先把暴力解寫出來跑過小測資，確認你對題目的理解沒錯。\n"
        "然後再問自己：這 O(n²) 種配對裡，有沒有一大堆是**根本不可能是答案**、可以整批跳過的？",

        "考慮把兩個指標放在**陣列的最左端和最右端**（`lo = 0`, `hi = n - 1`）。\n\n"
        "這組配對有一個特別的性質：它的**寬度是所有配對裡最大的**。\n"
        "任何其他配對的寬度都比它小。\n\n"
        "現在的問題變成：接下來該把哪個指標往內移？移動之後會失去什麼、可能得到什麼？",

        "關鍵推論（這是這題的靈魂，請先自己想過再往下看）：\n\n"
        "假設現在 `heights[lo] < heights[hi]`，也就是**左邊比較矮**。\n"
        "此時容量受限於左邊那條矮線。\n\n"
        "現在考慮所有「包含 lo 這條線」的配對：`(lo, hi)`、`(lo, hi-1)`、`(lo, hi-2)`…\n"
        "它們的高度都不會超過 `heights[lo]`（因為高度取 min，而 lo 已經是矮的那邊，\n"
        "另一邊再高也沒用），而寬度全都**比現在的 `(lo, hi)` 更小**。\n\n"
        "所以：**`(lo, hi)` 已經是所有包含 lo 的配對裡最好的那一個**。\n"
        "記下它的容量之後，lo 這條線就再也沒有用了，可以永久排除 → `lo += 1`。\n\n"
        "反之若右邊比較矮，就 `hi -= 1`。這樣每一步排除一條線，n 步就掃完了。",

        "程式骨架：\n\n"
        "```python\n"
        "def max_area(heights):\n"
        "    lo, hi = 0, len(heights) - 1\n"
        "    best = 0\n"
        "    while lo < hi:\n"
        "        h = min(heights[lo], heights[hi])\n"
        "        best = max(best, (hi - lo) * h)\n"
        "        if heights[lo] < heights[hi]:\n"
        "            lo += 1\n"
        "        else:\n"
        "            hi -= 1\n"
        "    return best\n"
        "```\n\n"
        "兩個細節：\n"
        "- 迴圈條件是 `lo < hi` 而不是 `lo <= hi`（同一條線不能跟自己組成容器）。\n"
        "- 兩邊**等高**時往哪邊移都可以，因為兩條線同時被排除也不會漏掉答案。",
    ],
    "tests": [
        {"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expected": 49},
        {"args": [[1, 1]], "expected": 1},
        {"args": [[4, 3, 2, 1, 4]], "expected": 16},
        {"args": [[1, 2, 1]], "expected": 2},
        {"args": [[2, 3, 4, 5, 18, 17, 6]], "expected": 17},
        {"args": [[0, 0, 5, 0, 0]], "expected": 0,
         "note": "全部配對都至少有一邊是 0"},
        {"args": [[100, 1, 1, 1, 1, 1, 1, 100]], "expected": 700,
         "note": "兩端最高，中間全矮"},
        {"args_expr": "[[(i * i * 37) % 1000 for i in range(200000)]]",
         "expected": 199382054, "hidden": True, "max_ms": 1500,
         "note": "n = 200,000。O(n^2) 在這裡是 2*10^10 次運算，必然超時"},
    ],
    "verify_code": '''\
def max_area(heights: list[int]) -> int:
    lo, hi = 0, len(heights) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(heights[lo], heights[hi]))
        if heights[lo] < heights[hi]:
            lo += 1
        else:
            hi -= 1
    return best
''',
    "reference_md": """\
## 標準解（對撞雙指標，O(n)）

```python
def max_area(heights: list[int]) -> int:
    lo, hi = 0, len(heights) - 1
    best = 0

    while lo < hi:
        height = min(heights[lo], heights[hi])
        best = max(best, (hi - lo) * height)

        # 移動比較矮的那一邊：它已經不可能參與更好的答案了
        if heights[lo] < heights[hi]:
            lo += 1
        else:
            hi -= 1

    return best
```

**時間 O(n)，空間 O(1)。** 這已經是最佳解——你至少得看過每個元素一次，所以 O(n) 是下界。

## 為什麼這樣是對的（正確性證明）

這是本題的核心，面試官八成會追問。用**排除法**論證：

設當前指標為 `lo`、`hi`，且 `heights[lo] < heights[hi]`（左邊矮）。
考慮任何一個「包含 lo」但還沒被檢查過的配對 `(lo, j)`，其中 `lo < j < hi`：

- 它的**寬度** `j - lo < hi - lo`，嚴格小於當前寬度。
- 它的**高度** `min(heights[lo], heights[j]) ≤ heights[lo] = min(heights[lo], heights[hi])`，
  不超過當前高度。（因為 min 的結果不會超過其中任何一項。）

寬和高都不超過當前配對，所以 `容量(lo, j) ≤ 容量(lo, hi)`。
換句話說，**`(lo, hi)` 已經是所有含 lo 的配對中最好的**，記錄完就可以安全地丟掉 lo。

每次迴圈排除一條線，最多 n 次就結束。因為每次排除的都是「已經取到最佳值」的線，
所以真正的最佳解永遠留在剩下的區間裡，不會被漏掉。

## 對照：暴力解（會超時，但你該先寫得出來）

```python
def max_area_brute(heights):
    n = len(heights)
    return max(
        (j - i) * min(heights[i], heights[j])
        for i in range(n) for j in range(i + 1, n)
    )
```

O(n²)。n = 200,000 時是 2×10^10 次運算，Python 大約要跑好幾個小時。
**能寫出暴力解再優化，比一開始就想最佳解實際得多**——面試時也是先講暴力解再優化。

## 常見錯誤

1. **迴圈條件寫成 `lo <= hi`** — 當 `lo == hi` 時寬度為 0，雖然不影響答案（多算一個 0），
   但邏輯上表示「一條線和自己組成容器」，是錯的。
2. **移動高的那一邊** — 直覺上「留下高的線比較好」，但這樣會漏掉答案。
   反例：`[100, 1, 1, 1, 1, 1, 1, 100]`，正確答案 700（兩端）。
   若每次移動高的那邊，第一步就會把某個 100 丟掉。
3. **只更新一次 best 就 break** — 容量不是單調的，不能提早結束。
4. **兩邊等高時只移一邊還想繼續比較另一邊** — 等高時移哪邊都對，
   因為兩條線的最佳配對都已經是當前這個了。不用特別處理。

## 這個技巧之後會用在哪

「對撞雙指標」是 O(n²) → O(n) 最常見的手法之一，同型的題目有：

- **Two Sum II（已排序陣列）** — 和太小往右移、太大往左移。
- **三數之和 / 四數之和** — 固定一個數，剩下的用對撞指標。
- **接雨水（Trapping Rain Water）** — 這題的近親，同樣是「移動矮的那邊」。強烈建議接著練這題。
- **驗證迴文** — 最單純的對撞指標。

判斷「能不能用對撞指標」的訊號：
**問題定義在一個區間的兩端，而且你能證明移動某一端不會遺失最佳解。**

在 CV 裡，NMS（非極大值抑制）排序後的處理、以及 1D 訊號的區間搜尋，
用的都是同一種「單調性 + 排除」的思路。
""",
}


P_MIN_CAPACITY = {
    "title": "貨船運送能力下限",
    "slug": "min-shipping-capacity",
    "lang": "py",
    "node": "2.5",
    "difficulty": "standard",
    "mode": "function",
    "entry": "min_capacity",
    "timeout": 20,
    "tags": ["二分答案", "貪心檢驗", "單調性", "LeetCode 1011"],
    "statement_md": """\
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
""",
    "starter": '''\
def min_capacity(weights: list[int], days: int) -> int:
    """回傳能在 days 天內運完所有包裹的最小載重上限。"""
    # TODO
    pass
''',
    "hints": [
        "先解決一個比較簡單的子問題：\n\n"
        "**給定一個載重上限 `cap`，需要幾天才能運完？**\n\n"
        "這個子問題有唯一的貪心解：每天盡量多裝，裝不下了就換下一天。\n"
        "為什麼貪心是對的？因為包裹順序固定，今天少裝一個並不會讓明天裝得更多，\n"
        "所以「盡量多裝」不會比任何其他分法差。\n\n"
        "先把這個 `days_needed(cap)` 函式寫出來，它是整題的基礎。",

        "有了 `days_needed(cap)` 之後，觀察它的**單調性**：\n\n"
        "```\n"
        "cap 很小  →  需要很多天\n"
        "cap 很大  →  需要很少天\n"
        "```\n\n"
        "`cap` 越大，需要的天數**單調不增**。所以如果把每個 cap 標記成「可行 / 不可行」，\n"
        "整條數線會長這樣：\n\n"
        "```\n"
        "cap:     1   2   3  ...  14  15  16  17 ...\n"
        "可行?    ✗   ✗   ✗       ✗   ✓   ✓   ✓\n"
        "                             ↑ 你要找的就是這個分界點\n"
        "```\n\n"
        "**在一條「前面全 ✗、後面全 ✓」的數線上找分界點** —— 這就是二分搜尋。\n"
        "這個套路叫「二分答案」：不直接算答案，而是二分猜答案 + 驗證。",

        "二分的**搜尋範圍**要想清楚，這是二分答案最容易錯的地方：\n\n"
        "- **下界**：載重至少要能裝下最重的那個包裹，否則它永遠上不了船 → `max(weights)`\n"
        "- **上界**：載重大到能一天裝完全部 → `sum(weights)`\n\n"
        "答案一定落在 `[max(weights), sum(weights)]` 之間，而且這個區間的左端點**保證存在可行解**。\n\n"
        "接著用「找第一個可行的位置」這種二分模板：\n\n"
        "```python\n"
        "lo, hi = max(weights), sum(weights)\n"
        "while lo < hi:\n"
        "    mid = (lo + hi) // 2\n"
        "    if days_needed(mid) <= days:\n"
        "        hi = mid        # mid 可行，答案可能就是它，所以保留 mid\n"
        "    else:\n"
        "        lo = mid + 1    # mid 不可行，答案一定在右邊\n"
        "return lo\n"
        "```\n\n"
        "注意兩個不對稱：可行時是 `hi = mid`（不是 mid-1），不可行時是 `lo = mid + 1`。\n"
        "這個不對稱就是「找第一個 ✓」的關鍵。",

        "`days_needed` 的完整寫法：\n\n"
        "```python\n"
        "def days_needed(cap):\n"
        "    count, current = 1, 0     # 從第 1 天開始，今天已裝 0\n"
        "    for w in weights:\n"
        "        if current + w > cap:  # 今天裝不下了\n"
        "            count += 1         # 換一天\n"
        "            current = 0\n"
        "        current += w\n"
        "    return count\n"
        "```\n\n"
        "注意 `count` 從 **1** 開始（第一天一開始就存在），不是 0。\n"
        "用 `weights=[10], days=1` 驗證：迴圈裡 `0+10 > 10` 是 False，所以不換天，\n"
        "回傳 1 ✓。\n\n"
        "為什麼迴圈條件是 `while lo < hi` 而不是 `lo <= hi`？\n"
        "因為這個模板在 `lo == hi` 時就代表區間只剩一個候選，那就是答案，不需要再檢查。",
    ],
    "tests": [
        {"args": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5], "expected": 15},
        {"args": [[3, 2, 2, 4, 1, 4], 3], "expected": 6},
        {"args": [[1, 2, 3, 1, 1], 4], "expected": 3},
        {"args": [[10], 1], "expected": 10, "note": "只有一個包裹"},
        {"args": [[1, 2, 3, 4, 5], 1], "expected": 15, "note": "一天運完，答案是總和"},
        {"args": [[1, 2, 3, 4, 5], 5], "expected": 5, "note": "每天一個，答案是最大值"},
        {"args": [[5, 5, 5, 5], 2], "expected": 10},
        {"args": [[500] * 100, 10], "expected": 5000, "note": "全部等重"},
        {"args_expr": "[[(i * i * 7919) % 1000 + 1 for i in range(100000)], 3000]",
         "expected": 17935, "hidden": True, "max_ms": 8000,
         "note": "10 萬個包裹。逐一嘗試每個 cap 是 O(值域 × n)，必然超時"},
    ],
    "verify_code": '''\
def min_capacity(weights: list[int], days: int) -> int:
    def days_needed(cap: int) -> int:
        count, current = 1, 0
        for w in weights:
            if current + w > cap:
                count += 1
                current = 0
            current += w
        return count

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
''',
    "reference_md": """\
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
""",
}

P_CPP_DISTINCT = {
    "title": "去重排序（C++ STL 入門）",
    "slug": "cpp-unique-sorted",
    "lang": "cpp",
    "node": "2.12",
    "difficulty": "warmup",
    "mode": "io",
    "timeout": 10,
    "tags": ["vector", "sort", "unique", "快速 I/O"],
    "statement_md": """\
這是你的第一題 C++。跟 Python 題不同，C++ 題用**標準輸入輸出**（競賽的標準形式）：
從 `stdin` 讀資料，把答案印到 `stdout`。

**題目**

讀入 n 個整數，把它們**去除重複**並**由小到大排序**後輸出。

**輸入格式**

```
第一行：一個整數 n
第二行：n 個以空白分隔的整數
```

**輸出格式**

```
第一行：去重後的數量 k
第二行：k 個由小到大排列的整數，以單一空白分隔
```

**範例**

輸入：
```
5
3 1 2 3 1
```

輸出：
```
3
1 2 3
```

**限制**
- `1 <= n <= 2 * 10^5`
- `1 <= a_i <= 10^9`（注意上限，想想該用什麼型別）

**效能要求**：有一筆 n = 200,000 的大測資並附時間上限。
用 `cin >> x` 逐個讀入時，記得關掉 C++ 與 C 的 I/O 同步，否則光是讀入就可能超時。

**這題要練的**：`vector` 的使用、`sort`、`unique` + `erase` 這個慣用組合、以及快速 I/O。
""",
    "starter": """\
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    // TODO: 讀入、排序、去重、輸出

    return 0;
}
""",
    "hints": [
        "先確認 C++ 的基本 I/O 骨架能跑：\n\n"
        "```cpp\n"
        "int n;\n"
        "cin >> n;\n"
        "vector<int> a(n);            // 直接開好 n 個位置\n"
        "for (int i = 0; i < n; i++) cin >> a[i];\n"
        "```\n\n"
        "`vector<int> a(n)` 會建立 n 個元素、全部初始化為 0。\n"
        "這比 `vector<int> a;` 再一直 `push_back` 更好——它一次配置好記憶體，不用反覆重新配置。\n\n"
        "`a_i` 最大 10^9，還在 `int` 的範圍內（約 2.1×10^9），所以 `int` 就夠，不需要 `long long`。",

        "C++ 的去重慣用法是**先排序，再去重**。原因是 `unique` 只會移除**相鄰**的重複元素，\n"
        "所以必須先讓相同的值排在一起。\n\n"
        "排序用 `<algorithm>` 的 `sort`：\n"
        "```cpp\n"
        "sort(a.begin(), a.end());\n"
        "```\n\n"
        "C++ 的區間都是 **[begin, end)**（左閉右開），`end()` 指向「最後一個元素的後一格」，\n"
        "不是最後一個元素。這個慣例整個 STL 都通用。",

        "`unique` 有個新手一定會踩的坑：**它不會真的刪掉元素、也不會改變 vector 的大小**。\n\n"
        "它做的是把不重複的元素往前搬，然後回傳一個迭代器，指向「有效資料的結尾」。\n"
        "後面那段是垃圾值，還留在 vector 裡。\n\n"
        "所以標準寫法是 `unique` 之後緊接著 `erase`，把尾巴真的砍掉：\n\n"
        "```cpp\n"
        "a.erase(unique(a.begin(), a.end()), a.end());\n"
        "```\n\n"
        "這行叫做 **erase-remove idiom**，是 C++ 最常見的慣用句之一，背下來。\n"
        "執行完之後 `a.size()` 就是去重後的數量。",

        "輸出時注意兩件事：\n\n"
        "1. **不要用 `endl`**。`endl` 每次都會強制 flush 緩衝區，在大量輸出時非常慢。\n"
        "   用 `\"\\n\"` 就好。\n"
        "2. 分隔用單一空白，行末有沒有多餘空白都沒關係（比對時會去掉行尾空白）。\n\n"
        "```cpp\n"
        "cout << a.size() << \"\\n\";\n"
        "for (size_t i = 0; i < a.size(); i++) {\n"
        "    cout << a[i] << \" \\n\"[i + 1 == a.size()];   // 競賽常見的小技巧\n"
        "}\n"
        "```\n\n"
        "最後那個 `\" \\n\"[條件]` 是在「空白」和「換行」之間選一個——\n"
        "看得懂就好，寫成普通的 if 也完全可以。\n\n"
        "還有 `main` 開頭那兩行一定要留著：\n"
        "```cpp\n"
        "ios::sync_with_stdio(false);   // 關掉與 C stdio 的同步，cin/cout 快好幾倍\n"
        "cin.tie(nullptr);              // 解除 cin 與 cout 的綁定，不再每次輸入前 flush\n"
        "```",
    ],
    "tests": [
        {"stdin": "5\n3 1 2 3 1\n", "stdout": "3\n1 2 3"},
        {"stdin": "1\n42\n", "stdout": "1\n42", "note": "單一元素"},
        {"stdin": "6\n5 5 5 5 5 5\n", "stdout": "1\n5", "note": "全部相同"},
        {"stdin": "4\n1000000000 1 1000000000 2\n", "stdout": "3\n1 2 1000000000",
         "note": "接近 int 上限"},
        {"stdin": "5\n5 4 3 2 1\n", "stdout": "5\n1 2 3 4 5", "note": "完全逆序"},
        {"stdin_expr": "'200000\\n' + ' '.join([str((i * i * 37) % 50 + 1) "
                       "for i in range(200000)]) + '\\n'",
         "stdout": "22\n1 3 4 8 9 13 14 18 19 23 24 26 28 29 33 34 38 39 43 44 48 49",
         "hidden": True, "max_ms": 6000,
         "note": "20 萬筆輸入，考驗 I/O 速度"},
    ],
    "verify_code": """\
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());

    cout << a.size() << "\\n";
    for (size_t i = 0; i < a.size(); i++) {
        cout << a[i] << (i + 1 == a.size() ? '\\n' : ' ');
    }
    return 0;
}
""",
    "reference_md": """\
## 標準解

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());

    cout << a.size() << "\\n";
    for (size_t i = 0; i < a.size(); i++) {
        cout << a[i] << (i + 1 == a.size() ? '\\n' : ' ');
    }
    return 0;
}
```

**時間 O(n log n)**（瓶頸在 sort），**空間 O(n)**。

## erase-remove idiom

```cpp
a.erase(unique(a.begin(), a.end()), a.end());
```

拆開來看：

```cpp
auto last = unique(a.begin(), a.end());   // 把相異元素往前搬，回傳有效區間的結尾
a.erase(last, a.end());                   // 把後面的垃圾真的砍掉
```

`unique` 只是**搬動**，不會改 size——這是 STL 「algorithm 不能改變容器大小」的通則。
所有 `remove` / `remove_if` / `unique` 都是這樣，都需要搭配 `erase`。

`unique` 只移除**相鄰**重複，所以一定要先 `sort`。
（如果不想排序也要去重，就得用 `unordered_set`，見下。）

C++20 之後有更簡潔的寫法：

```cpp
#include <ranges>
ranges::sort(a);
auto [first, last] = ranges::unique(a);
a.erase(first, last);
```

## 另一種寫法：用 set

```cpp
int n; cin >> n;
set<int> s;
for (int i = 0, x; i < n; i++) { cin >> x; s.insert(x); }

cout << s.size() << "\\n";
for (int x : s) cout << x << ' ';
```

`set` 自動排序又自動去重，程式碼短很多。**但實務上比較慢**：

| 做法 | 複雜度 | 實測（n=2×10^5） | 原因 |
|---|---|---|---|
| `vector` + sort + unique | O(n log n) | 快 | 連續記憶體，cache 友善 |
| `set` | O(n log n) | 慢 2–4 倍 | 紅黑樹，每個節點各自配置、指標跳來跳去 |
| `unordered_set` + sort | O(n) 平均 | 中間 | 雜湊，但仍要配置節點 |

**同樣的複雜度，常數項可以差好幾倍。**
競賽的通則是：**能用 vector 就用 vector**，只有在需要「邊插入邊維持有序」時才用 set。

## 快速 I/O

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

- 第一行：預設 `cin`/`cout` 會和 C 的 `scanf`/`printf` 保持同步，
  代價是每次操作都有額外開銷。關掉之後快 3–5 倍。
  **代價**：關掉後就不能再混用 `scanf`/`printf`。
- 第二行：預設每次 `cin >>` 之前會自動 flush `cout`（為了讓提示訊息先出現）。
  解除綁定就省掉這個。
  **代價**：互動題（需要即時看到輸出）不能這樣做。

還有一個：**永遠不要在迴圈裡用 `endl`**。
`endl` = `'\\n'` + `flush`，20 萬次 flush 可以讓 0.1 秒的程式變成 2 秒。

## 常見錯誤

1. **忘記 `erase`** — 只呼叫 `unique` 就直接輸出 `a.size()`，size 完全沒變，
   輸出會多出一堆垃圾值。這是第一次用 `unique` 的人 100% 會犯的錯。
2. **忘記先 `sort`** — `unique` 只處理相鄰重複，`3 1 2 3 1` 不排序的話一個都去不掉。
3. **用 `int` 存超過 2×10^9 的值** — 這題上限 10^9 安全，
   但如果題目是 `1 <= a_i <= 10^18` 就必須用 `long long`。
   **每次看到數值上限，先在心裡跟 2.1×10^9 比一下**。
4. **用 `endl`** — 大量輸出時的隱形殺手。
5. **`for (size_t i...)` 與 `for (int i...)` 混用比較** — `a.size()` 回傳的是無號的 `size_t`，
   跟 `int` 比較時編譯器會警告（這個專案開了 `-Wall -Wextra`，你會看到）。
   要嘛用 `size_t`，要嘛存成 `int m = a.size();`。
6. **`bits/stdc++.h`** — 這是 GCC 專屬的「全部標頭一次引入」，
   競賽很方便，**但正式專案不要用**（編譯慢、不可攜）。工作上要老實寫 `#include <vector>` 等等。

## 之後會怎麼用

「排序 + 去重」在競賽裡的正式名稱是**離散化**：
當數值範圍很大（10^9）但相異值很少（10^5）時，把每個值映射成它的排名，
就能用陣列當作查找表。這是線段樹、掃描線的必要前處理，你會在節點 3.8 用到。

```cpp
// 離散化的完整慣用寫法
vector<int> vals = a;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());
// 查 x 的排名（0-based）
int rank_of_x = lower_bound(vals.begin(), vals.end(), x) - vals.begin();
```
""",
}

# =====================================================================
# S3 競賽演算法
# =====================================================================

P_DIFF = {
    "title": "區間加值後的最大值",
    "slug": "range-add-max",
    "lang": "cpp",
    "node": "3.2",
    "difficulty": "standard",
    "mode": "io",
    "timeout": 15,
    "tags": ["差分陣列", "前綴和", "離線處理"],
    "statement_md": """\
有一個長度為 n 的陣列，**一開始全部是 0**。

接著有 q 次操作，每次操作給三個整數 `l r v`，表示把區間 `[l, r]`（含兩端）
裡的每個位置都**加上** v。

所有操作做完後，請輸出陣列的**最大值**，以及**最先**達到這個最大值的位置（1-based）。

**輸入格式**

```
第一行：n q
接下來 q 行：每行三個整數 l r v
```

**輸出格式**

```
一行兩個整數：最大值 位置
```

**範例**

輸入：
```
5 2
1 3 2
2 5 1
```

輸出：
```
3 2
```

推導過程：
```
初始       [0, 0, 0, 0, 0]
1 3 2  →  [2, 2, 2, 0, 0]
2 5 1  →  [2, 3, 3, 1, 1]
```
最大值 3，最先出現在位置 2。

**限制**
- `1 <= n <= 2 * 10^5`
- `0 <= q <= 2 * 10^5`（q 可能是 0，此時整個陣列都是 0，答案是 `0 1`）
- `1 <= l <= r <= n`
- `1 <= v <= 100`

**效能要求**：n 和 q 都是 20 萬的大測資，並附時間上限。
每次操作老實地跑一遍 `for (i = l; i <= r; i++) a[i] += v;` 是 O(n·q) = 4×10^10，必然超時。

**提示方向**：你不需要在每次操作時就知道陣列長什麼樣子，只需要**最後**知道。
""",
    "starter": """\
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    // TODO

    return 0;
}
""",
    "hints": [
        "先想清楚為什麼暴力會慢：每次操作要走過 (r - l + 1) 個位置，\n"
        "最壞情況每次都是整個陣列，總共 O(n·q)。\n\n"
        "關鍵洞察是題目給的那句話：**你只需要知道最後的結果**。\n"
        "中間過程長什麼樣子完全沒人問。\n\n"
        "所以問題變成：有沒有辦法讓每次操作只花 **O(1)**，最後再一次性地把整個陣列「算出來」？",

        "考慮記錄「**變化量**」而不是「值」。\n\n"
        "定義一個輔助陣列 `d`，其中 `d[i]` 代表「位置 i 比位置 i-1 多了多少」。\n"
        "換句話說，原陣列 `a[i] = d[1] + d[2] + ... + d[i]`，也就是 d 的**前綴和**。\n\n"
        "現在問自己：如果要讓 `a` 在區間 `[l, r]` 全部加 v，`d` 需要改哪幾個位置？\n\n"
        "- 位置 l 相對於 l-1，多了 v → `d[l]` 要 +v\n"
        "- 位置 l+1 到 r 之間，相鄰差值都沒變（大家都加了 v）→ 不用動\n"
        "- 位置 r+1 相對於 r，少了 v（因為 r+1 沒加）→ `d[r+1]` 要 -v\n\n"
        "**只要改兩個位置**，每次操作就變成 O(1) 了。",

        "這個技巧叫**差分陣列**，是前綴和的反向操作：\n\n"
        "```\n"
        "前綴和：從 差分 還原成 原陣列      （區間查詢 O(1)）\n"
        "差分  ：從 原陣列 記錄成 差分      （區間更新 O(1)）\n"
        "```\n\n"
        "流程是：\n"
        "1. 開一個大小 **n + 2** 的差分陣列（全 0）\n"
        "2. 每次操作：`d[l] += v; d[r+1] -= v;`\n"
        "3. 全部操作做完後，跑一次前綴和，邊算邊記錄最大值與位置\n\n"
        "為什麼是 n + 2 不是 n + 1？因為 `r` 最大是 n，`r + 1` 就會是 n + 1，\n"
        "而陣列用 1-based 索引，所以需要索引 0..n+1，共 n + 2 格。\n"
        "少開這一格就是 buffer overflow——**這是差分陣列最經典的 bug**。",

        "骨架：\n\n"
        "```cpp\n"
        "int n, q;\n"
        "cin >> n >> q;\n"
        "vector<long long> d(n + 2, 0);\n"
        "\n"
        "for (int i = 0; i < q; i++) {\n"
        "    int l, r, v;\n"
        "    cin >> l >> r >> v;\n"
        "    d[l] += v;\n"
        "    d[r + 1] -= v;\n"
        "}\n"
        "\n"
        "long long best = ?, cur = 0;\n"
        "int pos = ?;\n"
        "for (int i = 1; i <= n; i++) {\n"
        "    cur += d[i];              // 前綴和，cur 就是 a[i]\n"
        "    if (cur > best) { best = cur; pos = i; }   // 嚴格大於 → 保留最先出現的\n"
        "}\n"
        "cout << best << ' ' << pos << \"\\n\";\n"
        "```\n\n"
        "兩個細節：\n"
        "- `best` 的初始值：q 可能是 0，這時整個陣列都是 0，答案要是 `0 1`。\n"
        "  想想 best 初始化成什麼才不會出錯（設成 0 也行，但 pos 要一起想清楚）。\n"
        "- 用 `>` 而不是 `>=`，才會保留**最先**達到最大值的位置。\n\n"
        "型別：q 次操作 × v 最大 100 = 2×10^7，`int` 其實夠用。\n"
        "但養成「累加量先想會不會爆」的習慣，不確定就用 `long long`，成本很低。",
    ],
    "tests": [
        {"stdin": "5 2\n1 3 2\n2 5 1\n", "stdout": "3 2"},
        {"stdin": "1 1\n1 1 7\n", "stdout": "7 1", "note": "單一元素"},
        {"stdin": "4 3\n1 4 1\n2 3 5\n3 3 2\n", "stdout": "8 3"},
        {"stdin": "3 0\n", "stdout": "0 1", "note": "沒有任何操作，全部是 0"},
        {"stdin": "5 1\n1 5 3\n", "stdout": "3 1", "note": "全部相同，取最先的位置"},
        {"stdin": "5 2\n5 5 4\n1 1 4\n", "stdout": "4 1",
         "note": "兩處同為最大值，要輸出比較前面的"},
        {"stdin_expr": "'\\n'.join(['200000 200000'] + "
                       "['%d %d %d' % ((i * i * 7919) % 200000 + 1, "
                       "min((i * i * 7919) % 200000 + 1 + (i * 37) % 1000, 200000), "
                       "i % 100 + 1) for i in range(200000)]) + '\\n'",
         "stdout": "47176 97601", "hidden": True, "max_ms": 4000,
         "note": "n = q = 200,000。暴力是 4*10^10 次運算"},
    ],
    "verify_code": """\
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<long long> d(n + 2, 0);

    for (int i = 0; i < q; i++) {
        int l, r, v;
        cin >> l >> r >> v;
        d[l] += v;
        d[r + 1] -= v;
    }

    long long best = LLONG_MIN, cur = 0;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        cur += d[i];
        if (cur > best) { best = cur; pos = i; }
    }
    cout << best << ' ' << pos << "\\n";
    return 0;
}
""",
    "reference_md": """\
## 標準解（差分陣列）

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<long long> d(n + 2, 0);       // 注意是 n + 2

    for (int i = 0; i < q; i++) {
        int l, r, v;
        cin >> l >> r >> v;
        d[l] += v;
        d[r + 1] -= v;                   // r 最大是 n，所以會碰到索引 n+1
    }

    long long best = LLONG_MIN, cur = 0;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        cur += d[i];                     // cur 就是 a[i]
        if (cur > best) { best = cur; pos = i; }   // 嚴格大於，保留最先出現的
    }

    cout << best << ' ' << pos << "\\n";
    return 0;
}
```

**時間 O(n + q)**，**空間 O(n)**。這是最佳解——你至少要讀完 q 筆輸入、掃過 n 個位置。

## 差分與前綴和是一對逆運算

```
        差分 d[i] = a[i] - a[i-1]
a  ─────────────────────────────►  d
   ◄─────────────────────────────
        前綴和 a[i] = Σ d[1..i]
```

它們的用途剛好對稱：

| | 單點更新 | 區間更新 | 單點查詢 | 區間查詢 |
|---|---|---|---|---|
| **原陣列** | O(1) | O(n) | O(1) | O(n) |
| **前綴和** | O(n) | O(n) | O(1) | **O(1)** |
| **差分** | O(1) | **O(1)** | O(n) | O(n) |

所以選擇很清楚：

- **只有區間查詢，沒有更新** → 前綴和
- **只有區間更新，最後才查詢**（這題）→ 差分
- **更新和查詢交錯出現** → 差分救不了你，要用**樹狀陣列 (BIT)** 或**線段樹**，
  兩者都能做到 O(log n)。你會在節點 3.8 學到。

**這題能用差分的關鍵，是所有更新都在所有查詢之前**——這叫「離線處理」。
如果題目改成「每次操作後立刻問最大值」，差分就沒用了。

## 二維版本（CV 會用到）

同樣的想法可以推廣到二維。要對子矩形 `(r1,c1)-(r2,c2)` 全部加 v：

```cpp
d[r1][c1]     += v;
d[r1][c2 + 1] -= v;
d[r2 + 1][c1] -= v;
d[r2 + 1][c2 + 1] += v;
```

最後對每一列做前綴和、再對每一行做前綴和，就還原出整個矩陣。四個角落的加加減減是容斥原理。

二維前綴和在 CV 裡有個專有名詞叫 **integral image（積分圖）**，
Viola-Jones 人臉偵測靠它在 O(1) 時間算出任意矩形區域的像素和，
這是它能在 2001 年就做到即時偵測的關鍵。你在節點 5.4 會實作一次。

## 常見錯誤

1. **陣列開 n + 1 而不是 n + 2** — `r = n` 時 `d[r+1] = d[n+1]` 就越界了。
   在 C++ 這是 undefined behavior：可能沒事、可能答案錯、可能 segfault，
   而且**小測資通常看不出來**。這是差分陣列的頭號 bug。
2. **用 `>=` 比較最大值** — 會記錄成最後一個達到最大值的位置，題目要最先的。
3. **`best` 初始化成 0** — 這題所有 v 都是正的所以碰巧沒事。
   但如果 v 可以是負的，全陣列都是負值時就會錯誤地回傳 0。
   **初始化成 `LLONG_MIN`，或用「第一個元素」當初始值**，才是通用寫法。
4. **忘記 q 可能是 0** — 迴圈一次都不跑，要保證輸出 `0 1` 而不是垃圾值。
   `pos` 初始化成 1 就是為了這個。
5. **邊算前綴和邊存回陣列** — 沒錯，但沒必要。這題只要最大值，
   用一個 `cur` 變數滾動即可，省下 O(n) 空間。

## 同型題

| 題目 | 變化 |
|---|---|
| LC 1109 航班預訂統計 | 完全一樣的差分 |
| LC 1094 拼車 | 差分 + 檢查是否超載 |
| LC 370 區間加法 | 這題的原型 |
| 掃描線求最大重疊區間 | 差分的變形（把區間端點排序後掃過去） |

最後那個「掃描線」值得特別記住：把 `(l, +v)` 和 `(r+1, -v)` 當成事件排序後掃過去，
就能處理**座標範圍很大但事件很少**的情況（例如 l, r 可以到 10^9）。
這正是 **NMS 的區間版本**，也是計算幾何裡「矩形面積聯集」的標準解法。
""",
}

# =====================================================================
# S5 AI / Computer Vision 研究基本功
# =====================================================================

P_IOU = {
    "title": "IoU 矩陣（向量化）",
    "slug": "iou-matrix",
    "lang": "py",
    "node": "5.1",
    "difficulty": "standard",
    "mode": "function",
    "entry": "iou_matrix",
    "timeout": 20,
    "tags": ["numpy", "broadcasting", "IoU", "物件偵測"],
    "statement_md": """\
**IoU（Intersection over Union，交並比）** 是物件偵測最核心的指標：
兩個框重疊的面積 ÷ 兩個框聯集的面積。值域是 0（完全不重疊）到 1（完全重合）。

```
IoU = 交集面積 / (面積A + 面積B - 交集面積)
```

實作 `iou_matrix(boxes_a, boxes_b)`：

- `boxes_a`：形狀 (Na, 4) 的框，每個框是 `[x1, y1, x2, y2]`（左上角、右下角）
- `boxes_b`：形狀 (Nb, 4)
- 回傳形狀 **(Na, Nb)** 的矩陣，`result[i][j]` 是 `boxes_a[i]` 與 `boxes_b[j]` 的 IoU

回傳 numpy array 或巢狀 list 都可以。

**交集的算法**

兩個矩形的交集也是矩形，它的座標是：

```
交集 x1 = max(a.x1, b.x1)      交集 x2 = min(a.x2, b.x2)
交集 y1 = max(a.y1, b.y1)      交集 y2 = min(a.y2, b.y2)
交集寬  = max(0, 交集x2 - 交集x1)      ← 這個 max(0, ...) 很重要
交集高  = max(0, 交集y2 - 交集y1)
```

如果兩個框根本不重疊，算出來的寬或高會是**負的**，這時候要當成 0。

**範例**

```python
a = [[0, 0, 10, 10], [5, 5, 15, 15]]
b = [[0, 0, 10, 10], [20, 20, 30, 30], [5, 5, 10, 10]]

iou_matrix(a, b)
->  [[1.0,        0.0, 0.25],
     [0.14285714, 0.0, 0.25]]
```

驗算 `result[1][0]`：a[1] = [5,5,15,15]（面積 100），b[0] = [0,0,10,10]（面積 100）。
交集是 [5,5,10,10]，面積 25。聯集 = 100 + 100 - 25 = 175。IoU = 25/175 ≈ 0.142857。

**限制**
- `1 <= Na, Nb <= 1000`
- 座標是浮點數，可能是負的
- **退化框**（寬或高為 0）的面積是 0。若聯集也是 0，IoU 定義為 **0.0**（不要除以零）

**效能要求（這題的重點）**

有一筆 600×600 的大測資，時間上限 **400 毫秒**。
兩層 Python 迴圈跑 36 萬次配對會超時——**必須用 numpy 向量化**。

這正是這個節點要練的：把「對每一對做同樣的事」變成「對整個陣列一次做完」。
""",
    "starter": '''\
import numpy as np


def iou_matrix(boxes_a, boxes_b):
    """回傳 (Na, Nb) 的 IoU 矩陣。boxes 格式為 [x1, y1, x2, y2]。"""
    a = np.asarray(boxes_a, dtype=np.float64)
    b = np.asarray(boxes_b, dtype=np.float64)
    # TODO: 不要用 for 迴圈
    pass
''',
    "hints": [
        "先用兩層 for 迴圈寫出正確答案（會超時，但這是你的**正確性基準**）。\n"
        "之後向量化版本寫好，可以拿小測資跟它對答案。\n\n"
        "研究工作的標準流程就是這樣：**先寫慢但明顯正確的版本，再優化，然後比對兩者結果**。\n"
        "直接寫向量化版本而沒有基準可比，錯了你不會知道。\n\n"
        "接著看形狀：輸入是 (Na,4) 和 (Nb,4)，輸出是 (Na,Nb)。\n"
        "**沒有 4 這個維度了**——它被「消化」掉了。而 Na 和 Nb 這兩個維度要湊在一起。\n"
        "這個形狀變化本身就在暗示做法。",

        "numpy 的 **broadcasting（廣播）** 規則：兩個陣列運算時，\n"
        "從**最後一個維度**開始往前對齊，每個維度必須「相等」或「其中一個是 1」。\n"
        "是 1 的那個維度會被自動「複製」到另一個的大小。\n\n"
        "```python\n"
        "x = np.array([1, 2, 3])          # 形狀 (3,)\n"
        "y = np.array([10, 20])           # 形狀 (2,)\n"
        "\n"
        "x[:, None]      # 形狀 (3, 1)   ← None 插入一個新的維度\n"
        "y[None, :]      # 形狀 (1, 2)\n"
        "\n"
        "x[:, None] + y[None, :]          # 形狀 (3, 2) ← 所有配對的和！\n"
        "# [[11, 21],\n"
        "#  [12, 22],\n"
        "#  [13, 23]]\n"
        "```\n\n"
        "**這就是「所有配對」的做法**：一個變成直的 (Na, 1)，一個變成橫的 (1, Nb)，\n"
        "運算後自動得到 (Na, Nb)。這題從頭到尾就是這一招。",

        "把每個座標分量取出來（`a[:, 0]` 是所有 a 框的 x1，形狀 (Na,)），\n"
        "然後用 `[:, None]` 和 `[None, :]` 讓它們配對：\n\n"
        "```python\n"
        "inter_x1 = np.maximum(a[:, 0][:, None], b[:, 0][None, :])   # 形狀 (Na, Nb)\n"
        "```\n\n"
        "可以更簡潔地寫成 `np.maximum(a[:, None, 0], b[None, :, 0])`。\n\n"
        "⚠️ **一定要用 `np.maximum` 而不是 `max`**：\n"
        "- `max(x, y)` 是 Python 內建，比較兩個**整體**，對陣列會報錯或給錯誤結果\n"
        "- `np.maximum(x, y)` 是**逐元素**取大者，這才是你要的\n\n"
        "同理，「負數變 0」要用 `np.clip(w, 0, None)` 或 `np.maximum(w, 0)`，\n"
        "不能用 `if w < 0`——陣列不能直接放進 if。",

        "完整結構：\n\n"
        "```python\n"
        "def iou_matrix(boxes_a, boxes_b):\n"
        "    a = np.asarray(boxes_a, dtype=np.float64)\n"
        "    b = np.asarray(boxes_b, dtype=np.float64)\n"
        "\n"
        "    area_a = ?      # 形狀 (Na,)，記得寬高也要 clip 到 >= 0\n"
        "    area_b = ?      # 形狀 (Nb,)\n"
        "\n"
        "    x1 = np.maximum(a[:, None, 0], b[None, :, 0])   # (Na, Nb)\n"
        "    y1 = np.maximum(a[:, None, 1], b[None, :, 1])\n"
        "    x2 = np.minimum(a[:, None, 2], b[None, :, 2])\n"
        "    y2 = np.minimum(a[:, None, 3], b[None, :, 3])\n"
        "\n"
        "    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)\n"
        "    union = area_a[:, None] + area_b[None, :] - inter\n"
        "\n"
        "    return np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)\n"
        "```\n\n"
        "最後那行處理除以零。注意**不能**只寫 `np.where(union > 0, inter / union, 0.0)`——\n"
        "`np.where` 的兩個分支都會被**完整計算**，所以 `inter / union` 還是會執行、\n"
        "還是會噴 RuntimeWarning。用 `np.maximum(union, 1e-12)` 讓分母永遠不是 0，\n"
        "再靠 `np.where` 選出正確的值。這是 numpy 條件運算的固定套路。",
    ],
    "tests": [
        {"args": [[[0, 0, 10, 10], [5, 5, 15, 15]],
                  [[0, 0, 10, 10], [20, 20, 30, 30], [5, 5, 10, 10]]],
         "expected": [[1.0, 0.0, 0.25], [0.14285714285714285, 0.0, 0.25]],
         "cmp": "approx"},
        {"args": [[[0, 0, 2, 2]], [[1, 1, 3, 3]]],
         "expected": [[0.14285714285714285]], "cmp": "approx",
         "note": "交集 1，聯集 7"},
        {"args": [[[0, 0, 1, 1]], [[1, 1, 2, 2]]],
         "expected": [[0.0]], "cmp": "approx", "note": "只碰到角落，交集為 0"},
        {"args": [[[0, 0, 10, 10]], [[100, 100, 110, 110]]],
         "expected": [[0.0]], "cmp": "approx", "note": "完全不重疊，寬高都是負的"},
        {"args": [[[0, 0, 0, 0]], [[0, 0, 10, 10]]],
         "expected": [[0.0]], "cmp": "approx", "note": "退化框，面積 0"},
        {"args": [[[0, 0, 0, 0]], [[0, 0, 0, 0]]],
         "expected": [[0.0]], "cmp": "approx", "hidden": True,
         "note": "聯集也是 0，不可以除以零或回傳 nan"},
        {"args": [[[-5, -5, 5, 5]], [[0, 0, 10, 10]]],
         "expected": [[0.14285714285714285]], "cmp": "approx", "note": "負座標"},
        {"args": [[[0, 0, 4, 4]], [[1, 1, 3, 3]]],
         "expected": [[0.25]], "cmp": "approx", "note": "一個框完全包住另一個：4/16"},
        {"args_expr": "[[[i, i, i + 10, i + 10] for i in range(600)], "
                      "[[j * 0.5, j * 0.5, j * 0.5 + 8.0, j * 0.5 + 8.0] for j in range(600)]]",
         "validator": "np.asarray(got).shape == (600, 600) and "
                      "abs(float(np.asarray(got).sum()) - 2422.076905128353) < 1e-3",
         "hidden": True, "max_ms": 400,
         "note": "600x600 = 36 萬個配對。Python 雙層迴圈必然超時，只有向量化能過"},
    ],
    "verify_code": '''\
import numpy as np


def iou_matrix(boxes_a, boxes_b):
    a = np.asarray(boxes_a, dtype=np.float64)
    b = np.asarray(boxes_b, dtype=np.float64)

    area_a = np.clip(a[:, 2] - a[:, 0], 0, None) * np.clip(a[:, 3] - a[:, 1], 0, None)
    area_b = np.clip(b[:, 2] - b[:, 0], 0, None) * np.clip(b[:, 3] - b[:, 1], 0, None)

    x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    y2 = np.minimum(a[:, None, 3], b[None, :, 3])

    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    union = area_a[:, None] + area_b[None, :] - inter
    return np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)
''',
    "reference_md": """\
## 標準解（完全向量化）

```python
import numpy as np


def iou_matrix(boxes_a, boxes_b):
    a = np.asarray(boxes_a, dtype=np.float64)
    b = np.asarray(boxes_b, dtype=np.float64)

    # 各自的面積，形狀 (Na,) 和 (Nb,)。clip 是為了處理退化框
    area_a = np.clip(a[:, 2] - a[:, 0], 0, None) * np.clip(a[:, 3] - a[:, 1], 0, None)
    area_b = np.clip(b[:, 2] - b[:, 0], 0, None) * np.clip(b[:, 3] - b[:, 1], 0, None)

    # 交集矩形的四個座標，形狀都是 (Na, Nb)
    x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    y2 = np.minimum(a[:, None, 3], b[None, :, 3])

    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    union = area_a[:, None] + area_b[None, :] - inter

    # union 為 0 時（兩個都是退化框）定義 IoU = 0，且避免除以零的 warning
    return np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)
```

**時間 O(Na·Nb)**（無法更好，輸出本身就有 Na·Nb 個數），
但常數項差很多：600×600 大約 **10–30 ms**，純 Python 迴圈要 **2–4 秒**，差 100 倍以上。

## broadcasting 的心智模型

`a[:, None, 0]` 這種寫法看起來很怪，拆開來就清楚了：

```python
a[:, 0]            # 形狀 (Na,)      所有 a 框的 x1
a[:, 0][:, None]   # 形狀 (Na, 1)    變成一「直行」
b[:, 0][None, :]   # 形狀 (1, Nb)    變成一「橫列」

np.maximum(直行, 橫列)   # 形狀 (Na, Nb)   自動配對出所有組合
```

`a[:, None, 0]` 只是 `a[:, 0][:, None]` 的簡寫（在取索引時就插入新軸）。

**通用配方**：要對兩組東西做「所有配對」的運算，
就把一組變成 `(N, 1, ...)`、另一組變成 `(1, M, ...)`，然後直接運算。
形狀 (N, M, ...) 的結果會自動出現，不需要任何迴圈。

這個配方在研究 code 裡到處都是：
兩兩距離矩陣、attention 的 QKᵀ、對比學習的相似度矩陣、k-NN 搜尋，全都是同一招。

## 記憶體代價（實務上會咬你的地方）

向量化的代價是**記憶體**。這個實作會產生 6 個 (Na, Nb) 的中間陣列：

```
Na = Nb = 10000 → 每個中間陣列 10^8 × 8 bytes = 800 MB
6 個 → 約 5 GB → MemoryError
```

框數量很大時要**分塊處理**：

```python
def iou_matrix_chunked(boxes_a, boxes_b, chunk=2000):
    a = np.asarray(boxes_a, dtype=np.float64)
    b = np.asarray(boxes_b, dtype=np.float64)
    out = np.empty((len(a), len(b)), dtype=np.float64)
    for start in range(0, len(a), chunk):
        end = min(start + chunk, len(a))
        out[start:end] = iou_matrix(a[start:end], b)
    return out
```

**「向量化」不等於「全部一次算完」**。真正的技巧是找到記憶體與速度的平衡點——
分塊之後仍然是向量化的，只是每塊小一點。在 GPU 上這叫 chunked attention，是同一個道理。

## 為什麼那個 `np.where` 要那樣寫

```python
np.where(union > 0, inter / union, 0.0)              # ❌ 仍會 RuntimeWarning
np.where(union > 0, inter / np.maximum(union, 1e-12), 0.0)   # ✅
```

`np.where(cond, x, y)` 是**先把 x 和 y 都完整算出來，再逐元素挑選**。
它不像 Python 的 `if` 會短路。所以 `inter / union` 還是會對 union=0 的位置做除法，
產生 `nan` 和一個 RuntimeWarning，只是結果最後被丟掉。

在研究 code 裡這特別危險：**nan 會在後續計算裡無聲地擴散**，
loss 突然變 nan 卻找不到源頭，通常就是這種除零。

其他做法：

```python
with np.errstate(divide="ignore", invalid="ignore"):    # 只是關掉警告，nan 還在
    iou = np.where(union > 0, inter / union, 0.0)

iou = np.divide(inter, union, out=np.zeros_like(inter), where=union > 0)   # 最乾淨
```

最後一種用 `where=` 參數，真正**跳過**不該算的位置，不會產生 nan。

## PyTorch 版本（幾乎一模一樣）

```python
import torch

def iou_matrix(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    area_a = (a[:, 2] - a[:, 0]).clamp(min=0) * (a[:, 3] - a[:, 1]).clamp(min=0)
    area_b = (b[:, 2] - b[:, 0]).clamp(min=0) * (b[:, 3] - b[:, 1]).clamp(min=0)

    lt = torch.max(a[:, None, :2], b[None, :, :2])      # 左上角
    rb = torch.min(a[:, None, 2:], b[None, :, 2:])      # 右下角
    wh = (rb - lt).clamp(min=0)
    inter = wh[..., 0] * wh[..., 1]

    union = area_a[:, None] + area_b[None, :] - inter
    return inter / union.clamp(min=1e-12)
```

`clamp` = numpy 的 `clip`，`...` = 前面所有維度。
注意這裡用 `a[:, None, :2]` 一次處理 x1,y1 兩個分量，比分開寫更精簡。

實務上直接用 `torchvision.ops.box_iou` 就好，但**你要看得懂它在做什麼**——
自己寫過一次，之後 debug 才有能力判斷是不是這裡出問題。

## 常見錯誤

1. **用 Python 的 `max` 而不是 `np.maximum`** — 對陣列會拋
   `ValueError: truth value of an array is ambiguous`，或在某些情況給出完全錯誤的結果。
   **`max`/`min` 是比較整體，`np.maximum`/`np.minimum` 是逐元素。**
2. **忘記 clip 負數** — 不重疊的框算出來寬高是負的，兩個負數相乘變成**正的面積**，
   IoU 會出現大於 1 甚至離譜的值。`[[0,0,10,10]]` vs `[[100,100,110,110]]` 這筆測資就是在抓這個。
3. **除以零** — 退化框（寬或高為 0）讓聯集變成 0。結果是 `nan`，
   而 `nan` 的可怕之處是它**不會報錯**，只會讓後面的 mAP 變成 nan。
4. **搞混 xyxy 和 xywh** — COCO 格式是 `[x, y, w, h]`，
   直接餵進這個函式不會報錯，只會得到錯誤的 IoU。
   **在函式名或參數名標明格式**（`boxes_xyxy`）能省下很多小時。
5. **輸出形狀轉置** — 回傳 (Nb, Na) 而不是 (Na, Nb)。
   Na == Nb 時完全看不出來，直到某天用不同數量的框才爆炸。
   養成習慣：**寫完先 `assert result.shape == (len(a), len(b))`**。
6. **用 `np.array` 而不是 `np.asarray`** — `np.array` 一定複製，
   `np.asarray` 只在必要時複製。輸入已經是 array 時 `asarray` 零成本。

## 接下來

這個函式是後面好幾題的零件：

- **NMS（非極大值抑制）** — 按信心度排序後，反覆刪掉與已選框 IoU > 閾值的框（節點 5.8）
- **mAP** — 用 IoU ≥ 0.5 判定 TP/FP，再算 precision-recall 曲線下面積（節點 5.8）
- **anchor 匹配** — 訓練時把每個 ground truth 指派給 IoU 最大的 anchor
- **GIoU / DIoU / CIoU loss** — IoU 的可微分改良版，現代偵測器的迴歸損失

「IoU 矩陣算出來之後 `argmax(axis=1)`」就是最基本的框匹配，
你會在寫任何偵測評估腳本時用到它。
""",
}


SPECS = [
    P_BMI, P_COLLATZ, P_DISCOUNT, P_TOPK, P_PARSE,
    P_MAX_AREA, P_MIN_CAPACITY, P_CPP_DISTINCT,
    P_DIFF,
    P_IOU,
]


def run(create, force: bool = False) -> int:
    """把種子題目寫進 problems/。已存在的（依標題判斷）預設會略過。"""
    root = Path(__file__).resolve().parent / "problems"
    existing = set()
    for meta in root.glob("*/meta.json"):
        existing.add(json.loads(meta.read_text(encoding="utf-8"))["title"])

    created = 0
    for spec in SPECS:
        if spec["title"] in existing and not force:
            print(f"–  已存在，略過：{spec['title']}")
            continue
        pid = create(spec)
        print(f"✓  {pid}   [{spec['node']}] {spec['title']}")
        created += 1
    return created
