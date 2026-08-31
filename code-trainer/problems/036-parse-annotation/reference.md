# 036-parse-annotation · 標註行解析器與自訂例外 — 參考解

## 標準解

```python
class BadAnnotation(ValueError):
    """標註行格式不合法。"""


def parse_annotation(line: str) -> tuple[str, list[int]]:
    parts = line.split()
    if len(parts) != 5:
        raise BadAnnotation(f"需要 5 個欄位，得到 {len(parts)}：{line!r}")

    label = parts[0]
    try:
        coords = [int(v) for v in parts[1:]]
    except ValueError:
        raise BadAnnotation(f"座標必須是整數：{line!r}") from None

    x1, y1, x2, y2 = coords
    if x2 <= x1 or y2 <= y1:
        raise BadAnnotation(f"框的寬高必須為正：{line!r}")

    return label, coords
```

## 三個檢查的順序不能換

```
1. 欄位數      ← 沒有 5 個就沒得談，而且後面的解包會先炸
2. 型別        ← 先確定是數字，才能比大小
3. 語意        ← x2 > x1 是「這個值合不合理」，不是「格式對不對」
```

**由外而內、由粗到細。** 這個順序在任何驗證函式裡都適用：先確認結構、再確認型別、最後確認語意。
順序反了的話，你會在解包不存在的欄位時拿到 `ValueError: not enough values to unpack`——
那個錯誤訊息對使用者毫無幫助。

## 為什麼要 `from None`

不加的話錯誤訊息會變成兩層：

```
ValueError: invalid literal for int() with base 10: 'abc'

During handling of the above exception, another exception occurred:

BadAnnotation: 座標必須是整數：'cat 10 20 30 abc'
```

**對呼叫端來說 `int()` 的內部細節是雜訊**——他只需要知道「這行標註壞了」。
`from None` 把原始例外藏起來，只留下你的。

反過來，如果原始例外**有診斷價值**（例如網路逾時包成 `FetchError`），就該用 `from e` 保留它。
**兩種都是刻意的選擇，不要讓它預設發生。**

## 為什麼繼承 `ValueError` 而不是 `Exception`

例外階層的設計原則：**繼承「語意上最接近的既有例外」**。

- 呼叫端想精準處理 → `except BadAnnotation:`
- 呼叫端只想粗略接住所有「值不對」的錯 → `except ValueError:` **也接得到**

繼承 `Exception` 的話，第二種呼叫端就漏接了。這在你把函式加進既有系統時特別重要——
**你不能要求所有既有的 `except ValueError` 都改寫。**

（真的沒有合適的父類別時才繼承 `Exception`。大專案常見的作法是先定一個模組級基底
`class AnnotationError(ValueError)` 再往下細分。）

## 例外訊息要放什麼

```python
raise BadAnnotation(f"需要 5 個欄位，得到 {len(parts)}：{line!r}")
                     └─ 期望 ─┘ └─ 實際 ─┘ └─ 哪一筆 ─┘
```

三件事缺一不可。想像你在跑一萬行的標註檔，只看到 `BadAnnotation` 這五個字——
**沒有 `line` 的話你根本不知道要去改哪一行。**

`{line!r}` 用 `repr` 而不是 `str`，是為了讓空白和不可見字元現形：
`'cat 10 20 30 '` 一眼看得出結尾多一個空格，`cat 10 20 30 ` 看不出來。

## 常見錯誤

1. **用 `split(' ')`** —— 給了參數就不會合併連續空白，`"  dog  1 2 3 4  "` 會切出一堆空字串，欄位數變成 9。測資第二筆專門抓。
2. **忘記攔 `int()` 的 ValueError** —— `"cat 10 20 30 abc"` 會直接拋原始的 `ValueError`。測資檢查的是類別名稱，父類別不算通過。
3. **`x2 < x1` 寫成小於** —— 題目要求嚴格大於，寬度 0 的框不合法。測資 `"cat 10 20 10 40"` 抓這個。
4. **檢查順序反了** —— 先解包再檢查數量，錯誤訊息會變成 Python 內部的解包錯誤。
5. **以為 `int('4.5')` 會回傳 4** —— 它會拋 ValueError，不會自動截斷。要截斷得先 `float()` 再 `int()`。
6. **例外訊息是空的** —— `raise BadAnnotation()`。測資會過，但實務上等於沒說。

## 延伸

這題是 **4.2「錯誤處理與防禦性設計」的預習**。那一節會正式教例外階層、重試、超時、logging。

真實的資料管線裡，這個函式會被包在一個「**逐行處理、壞行跳過並記錄**」的迴圈裡——
那正是這個節點下一題要做的事。關鍵在於：**解析函式自己不決定「壞行該怎麼辦」**，
它只負責明確地說「這行壞了、壞在哪」，決定權留給呼叫端。

這個分工叫「**拋出的層級 ≠ 處理的層級**」，是例外機制存在的理由。
