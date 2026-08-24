# 003-apply-discount · 滿額折扣結帳 — 參考解

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
