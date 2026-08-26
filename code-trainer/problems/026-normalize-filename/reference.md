# 026-normalize-filename · 正規化檔名 — 參考解

## 標準解

```python
def normalize_filename(name: str) -> str:
    name = name.strip()
    stem, dot, ext = name.rpartition(".")
    if not dot:                 # 沒有點：rpartition 把整串放在第三格
        stem, ext = ext, ""
    stem = stem.replace(" ", "_")                        # 空白 -> 底線
    stem = "_".join(p for p in stem.split("_") if p)     # 壓縮 + 去頭尾
    ext = ext.lower()
    return f"{stem}.{ext}" if ext else stem
```

### `rpartition` 到底回傳什麼

這題的關鍵零件，值得記清楚。它一律回傳**三個元素**：

```python
"a.b.TXT".rpartition(".")   # ('a.b', '.', 'TXT')
"README".rpartition(".")    # ('', '', 'README')      <- 找不到分隔符
```

找不到分隔符時，**原字串會放在第三格、前兩格是空的**。這是刻意設計的（`partition` 剛好相反，會放在第一格）。
所以 `if not dot:` 就是「沒有副檔名」的判斷，這時要把第三格搬回 stem。

用 `dot` 而不是 `if not ext` 來判斷比較穩：`"abc."` 這種輸入 `ext` 是空的、但點確實存在。

## 另一種寫法：split/join 換成 regex

```python
import re

def normalize_filename(name: str) -> str:
    stem, dot, ext = name.strip().rpartition(".")
    if not dot:
        stem, ext = ext, ""
    stem = re.sub(r"[ _]+", "_", stem).strip("_")
    return f"{stem}.{ext.lower()}" if ext else stem
```

`[ _]+` 一次吃掉「一段連續的空白或底線」，換成單一底線——**把 replace 和壓縮合併成一步**，
因為它不在乎那段裡面是空白還是底線。再 `.strip("_")` 去頭尾。

注意 `strip("_")` 的參數是**字元集合**不是子字串：`"__a__".strip("_")` 會把兩邊所有底線都去掉。

哪個好？**沒有 regex 的版本對新手更好讀，regex 版本更短也更好改規格**（要多支援一種分隔符只要改字元集）。
實務上兩種都常見。這題規模小，兩者效能沒有意義上的差別。

## `split(sep)` 為什麼會產生空片段

這是「split 掉再 join 回來」能運作的原因：

```python
"a__b".split("_")     # ['a', '', 'b']      中間的空字串就是「連續兩個底線」
"_a_".split("_")      # ['', 'a', '']       頭尾的空字串就是「開頭/結尾有底線」
```

所以 `if p` 濾掉空片段之後，**壓縮和去頭尾同時完成**——一個條件解決兩條規則。

順帶一提，**不給參數的 `split()` 行為完全不同**：它按任意連續空白切、而且自動丟掉空片段。
`" a  b ".split()` 直接得到 `['a', 'b']`。這是 Python 少見的「同一個方法、給不給參數行為不一樣」的設計，很容易踩到。

## 複雜度

時間 **O(n)**、空間 **O(n)**，n 是字串長度。每個步驟都掃過字串常數次。
字串在 Python 是不可變的，所以每次 `replace` / `join` 都會產生新字串——這也是空間 O(n) 的原因。

## 常見錯誤

1. **用 `split(".")` 而不是 `rsplit` / `rpartition`** —— `"a.b.TXT".split(".")` 得到三段，你會把 `a` 當主檔名。測資 `a.b.TXT` 和 `data.tar.GZ` 專門抓這個。
2. **順序寫反：先壓縮底線再換空白** —— 空白換成的那些底線就沒被壓到。測資 `_ cat  dog _.Jpeg` 專門抓這個。
3. **整串 `lower()`** —— 主檔名的大小寫也被吃掉了。隱藏測資 `MiXeD CaSe StEm.TaR` 專門抓這個。真實情境裡這會讓你對不上原始標註檔的檔名。
4. **沒處理「沒有副檔名」** —— 直接 `f"{stem}.{ext}"` 會在 `README` 後面多接一個點，變成 `"README."`。
5. **用 `strip("_ ")` 想一次去掉空白和底線** —— 方向對，但只處理頭尾，中間的連續底線還在。
6. **以為 `strip("_")` 是去掉一個底線** —— 它去掉的是頭尾**所有**屬於該字元集合的字元。

## 延伸

這題是 **S5 資料管線的縮影**。真實的資料集清理會遇到更髒的東西：Unicode 檔名、大小寫不敏感的檔案系統（macOS/Windows 上 `IMG.jpg` 和 `img.JPG` 是同一個檔）、路徑分隔符。
4.6「資料格式與資料清理」會正式練，那時候你會用 `pathlib.Path` 的 `.stem` / `.suffix` 而不是自己切字串——但自己切過一次，你才知道那些屬性在幫你處理什麼。

`split` / `join` / `strip` / `replace` 這四個是字串處理的骨幹，1.5 剩下的題會繼續用。
