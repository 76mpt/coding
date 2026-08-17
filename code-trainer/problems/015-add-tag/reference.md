# 015-add-tag · 標籤累加器（可變預設值陷阱） — 參考解

## 標準解

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

## 為什麼 `tags=[]` 是錯的

**函式的預設值在「定義時」求值一次，之後永遠共用同一個物件。**

```python
def bad(tag, tags=[]):
    tags.append(tag)
    return tags

print(bad.__defaults__)   # ([],)      ← 預設值就存在這裡
bad("a")
print(bad.__defaults__)   # (['a'],)   ← 它被改掉了！
bad("b")
print(bad.__defaults__)   # (['a', 'b'],)
```

你可以直接看到那個 list 就掛在函式物件上，被所有呼叫共用。

這在實務上造成的 bug 特別難查，因為：
- 單元測試如果只呼叫一次，**永遠測不出來**
- 症狀是「跑久了資料會莫名其妙變多」，通常在生產環境才爆
- 錯誤發生的地方離原因很遠

**規則很簡單：預設值只能用不可變物件**——數字、字串、tuple、`None`、`True`/`False`、frozenset。
`list`、`dict`、`set` 一律用 `None` 再在函式內建立。

## 為什麼是 `is None` 而不是 `not tags`

```python
if not tags:      # ❌
    tags = []
```

Falsy 的東西不只 `None`，還有 `[]`、`{}`、`""`、`0`、`False`。
所以呼叫者傳一個空 list 進來時，你會**丟掉它**再建一個新的：

```python
my_list = []
result = add_tag("a", my_list)
# 正確實作：my_list 變成 ['a']，result is my_list
# 用 not tags：my_list 還是 []，result 是另一個 ['a']
```

回傳值看起來一樣，但呼叫者手上那個 list 沒被改到。
測資裡的 `check_arg` 那筆就是在驗證這個。

**`is None` 檢查的是物件身分（identity），`== None` 檢查的是值。**
對 `None` 一律用 `is`——因為 `None` 是單例，而且 `is` 不會被自訂的 `__eq__` 騙。

## 型別註解怎麼寫

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
```

`list[str] | None` 是 Python 3.10+ 的寫法（舊版是 `Optional[List[str]]`）。
**註解要誠實反映「可以傳 None」**，否則型別檢查器會在你寫 `tags.append` 時抱怨。
節點 4.9 會正式練型別註解。

## 什麼時候可變預設值是「故意的」

有一個經典用法是**用它當快取**：

```python
def fib(n, memo={}):          # 故意共用，當記憶化快取
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

這樣寫「能動」，但**不建議**：快取是全域狀態，測試之間會互相污染，
而且沒有人看得出來你是故意的。正確做法是 `functools.lru_cache`：

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

節點 4.7 會練這個。

## 常見錯誤

1. **`tags=[]`** — 這題的主角。第 2 筆測資就會抓到。
2. **`if not tags`** — 空 list 的語意錯，`check_arg` 那筆會抓到。
3. **`return tags.append(tag)`** — `append` 回傳 `None`，所以整個函式回傳 `None`。
   記住：Python 裡**就地修改的方法回傳 None**。
4. **複製一份再改** — 寫 `tags = tags + [tag]` 或 `tags = list(tags)`。
   回傳值對，但呼叫者傳進來的 list 不會被修改，`check_arg` 那筆不過。
   （如果規格要的是「不修改輸入」，那就該這樣寫——**規格說什麼就做什麼**。）
5. **`tags=None` 但忘記在函式內建立** — `None.append` 會 AttributeError。

## 延伸

同一個陷阱在其他地方也會出現：

- **class 的類別屬性**：`class A: items = []` 會被所有實例共用，
  應該在 `__init__` 裡建立（節點 1.8）
- **dataclass 的預設值**：要用 `field(default_factory=list)` 而不是 `= []`，
  Python 甚至會直接報錯阻止你
- **函式的預設參數是 `datetime.now()`** — 它只會在定義時求值一次，
  你的「現在」會永遠停在程式啟動的那一刻
