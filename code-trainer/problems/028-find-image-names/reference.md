# 028-find-image-names · 從文字中挑出影像檔名 — 參考解

## 標準解

```python
EXTS = (".jpg", ".jpeg", ".png")


def find_images(text: str) -> list[str]:
    out, seen = [], set()
    for word in text.split():
        low = word.lower()
        if not low.endswith(EXTS):
            continue
        if not any(low.endswith(e) and len(word) > len(e) for e in EXTS):
            continue
        if low in seen:
            continue
        seen.add(low)
        out.append(word)          # 原始大小寫
    return out
```

把長度檢查寫得更直白一點也完全可以：

```python
        stem, dot, ext = low.rpartition(".")
        if not stem or f".{ext}" not in EXTS:
            continue
```

這版讀起來更接近規格的原文（「副檔名前面至少有一個字元」→ `if not stem`），而且不用算長度。
兩種都對，**選你三個月後看得懂的那個**。

## 三個 Python 細節

### 1. `str.endswith` 吃 tuple

```python
low.endswith((".jpg", ".jpeg", ".png"))     # 一次比對三個
low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")   # 等價但囉嗦
```

`startswith` 也一樣。**注意一定要是 tuple 不能是 list**，給 list 會拋 `TypeError`。
這是 Python 標準函式庫少見的「只收 tuple」的介面。

### 2. 不給參數的 `split()` 是另一個函式

```python
"  a \n\t b  ".split()        # ['a', 'b']        按任意連續空白切、自動丟空片段
"  a \n\t b  ".split(" ")     # ['', '', 'a', '\n\t', 'b', '', '']
```

這題規格說「可能有多個空白、換行、tab」——不給參數的版本**一行就全部處理掉了**，
包括空字串輸入（`"".split()` 回傳 `[]`）。給了參數反而要自己收拾空片段。

### 3. `set` 的 `in` 是 O(1)，`list` 的 `in` 是 O(n)

```python
seen = set()      # in 走雜湊，平均 O(1)
seen = []         # in 從頭掃到尾，O(n)
```

大測資有 10⁵ 個詞、5×10⁴ 個相異檔名。用 list 的話總成本是 O(n²) ≈ 2.5×10⁹ 次比較——會直接超時。
**這是 1.4「list vs set 查找」和 1.9「複雜度直覺」的實戰版**：同一份邏輯、換一個容器，能跑與不能跑的差別。

## 另一種寫法：regex

```python
import re

PATTERN = re.compile(r"\S*[^\s.](?:\.jpg|\.jpeg|\.png)$", re.IGNORECASE)


def find_images(text: str) -> list[str]:
    out, seen = [], set()
    for word in text.split():
        if not PATTERN.fullmatch(word):
            continue
        low = word.lower()
        if low not in seen:
            seen.add(low)
            out.append(word)
    return out
```

`re.IGNORECASE` 一個旗標就處理掉大小寫，`[^\s.]` 保證副檔名前面至少一個非點字元。

**但這裡 regex 不見得比較好**：`endswith` 版本更快（沒有 regex 引擎的開銷）、也更好懂。
regex 的優勢要在規則變複雜時才顯現——例如「主檔名只能是字母數字」「要支援 20 種副檔名」。
**規則簡單就用字串方法，規則複雜才上 regex**，這是實務上的判準。

## 為什麼不能先 `text.lower()` 再處理

很多人第一直覺是「整段轉小寫就不用煩惱大小寫了」。問題是**題目要你回傳原始大小寫**——
轉小寫是不可逆的，資訊丟了就回不來。

所以正確的模式是：**用衍生形式做判斷，用原始形式當資料**。

```python
low = word.lower()      # 衍生形式：只用來比對
out.append(word)        # 原始形式：這才是要保留的
```

這個模式在資料處理裡無所不在——正規化只是為了比對，永遠不要拿正規化的結果覆蓋原始資料。
之後做資料集去重、標註對齊時你會一直用到。

## 複雜度

- 時間 **O(n)**，n 是 `text` 的總字元數。切詞 O(n)、每個詞的 `lower`/`endswith`/雜湊查詢都與詞長成正比，加總還是 O(n)。
- 空間 **O(n)**，`seen` 和 `out` 最壞情況存下所有詞。

**這是最佳解**——你至少要讀過每個字元一次才知道有哪些檔名，所以 O(n) 是下界。

## 常見錯誤

1. **`append(low)` 而不是 `append(word)`** —— 回傳的全變小寫。範例 2 和隱藏測資 `A.PNG a.png ...` 專門抓這個。
2. **用 list 當 `seen`** —— 小測資全過，大測資超時。這是最惡劣的一種 bug：功能正確但規模上不去，而且本機小資料測不出來。
3. **忘記排除 `".png"`** —— `endswith` 對它回傳 True。測資 `.png x.png` 和 `.jpeg .png .jpg` 專門抓這個。
4. **用 `".jpg" in word` 而不是 `endswith`** —— `"a.jpgx"` 會被誤判成影像。測資 `a.jpgx b.pngy c.jpg` 專門抓這個。「包含」和「結尾是」是兩件事。
5. **先 `text.lower()` 再切詞** —— 原始大小寫救不回來了（見上一節）。
6. **用 `split(" ")`** —— 換行和 tab 分隔的詞會黏在一起，而且會產生一堆空字串。測資 7 用了 `\n` 和 `\t`。
7. **每次迴圈重算 `word.lower()` 三、四次** —— 不會錯，但白做工。算一次存起來是免費的。

## 延伸

「切詞 → 過濾 → 不分大小寫去重、保留順序」這個組合是**資料清理的標準流程**，
之後 4.6「資料格式與資料清理」會用在真實的 CSV 和標註檔上。

去重保序這件事還有一個 Python 慣用法值得知道：

```python
list(dict.fromkeys(items))       # 保序去重，一行
```

`dict` 從 3.7 起保證插入順序，所以拿它當「有序的 set」用。
**但這題用不上**——因為你的去重鍵（小寫）和要保留的值（原始）不是同一個東西。
真要用得寫成 `list({w.lower(): w for w in words}.values())`，而那個會保留**最後**一個而不是第一個。想想為什麼。

1.6 comprehension 那節會讓你把這類迴圈改寫成一行；1.9 複雜度那節會回來算這題 list vs set 的實際差距。
