# 041-detection-dunders · 讓物件能比較、排序、去重 — 參考解

## 標準解

```python
class Detection:
    def __init__(self, label, box, score):
        self.label = label
        self.box = tuple(box)          # 轉成 tuple 才能 hash
        self.score = score

    def _key(self):
        return (self.label, self.box)  # 決定相等性的那組欄位，只寫一次

    def __repr__(self):
        return f"Detection({self.label!r}, {self.box}, {self.score})"

    def __eq__(self, other):
        return isinstance(other, Detection) and self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def __lt__(self, other):
        return self.score < other.score


def rank_detections(raw):
    dets, seen = [], set()
    for label, box, score in raw:
        d = Detection(label, box, score)
        if d in seen:
            continue
        seen.add(d)
        dets.append(d)
    return sorted(dets, key=lambda d: (-d.score, d.label))
```

## `_key()` 這個小方法為什麼值得寫

`__eq__` 和 `__hash__` **必須用同一組欄位**。抽成一個方法之後，
那組欄位只寫在一個地方——之後規格改成「相等性也要看 score」，你只改一行。

分開寫的話，改了一邊忘了另一邊，就會產生**極難查的 bug**：
兩個物件 `==` 是 True 但 hash 不同 → 放進 set 會變成兩筆 → 去重失效，而且不會報錯。

## `__eq__` 和 `__hash__` 為什麼必須成對

Python 的規則：

```
a == b  ⟹  hash(a) == hash(b)
```

（反過來不必成立——hash 碰撞是允許的，set 會再用 `==` 確認。）

**一旦你自訂 `__eq__`，Python 會自動把 `__hash__` 設成 `None`**，讓你的類別 unhashable：

```python
class Foo:
    def __eq__(self, other): return True

{Foo()}    # TypeError: unhashable type: 'Foo'
```

這是刻意的保護——預設的 `__hash__` 基於記憶體位址，
你改了 `__eq__` 之後兩者就對不上了，Python 寧可讓你當場報錯，也不要讓 set/dict 安靜地壞掉。

**所以要嘛兩個都寫，要嘛兩個都不寫。**

（想要一個不可變、可 hash 的值物件，`@dataclass(frozen=True)` 會自動幫你產生兩個。
這題手寫是為了讓你知道它在做什麼。）

## `self.box = tuple(box)` 那行

**list 不能 hash，tuple 可以。**

```python
hash((0, 0, 1, 1))     # 可以
hash([0, 0, 1, 1])     # TypeError: unhashable type: 'list'
```

原因是 hash 必須穩定：list 改了內容 hash 就變了，放進 set 之後就再也找不到它。
**Python 乾脆禁止可變物件被 hash。**

測資傳進來的 box 是 list（JSON 沒有 tuple），所以建構時要轉。
這也順帶讓 `Detection` 更安全——外面改了原本的 list，不會影響已經建好的物件。

## `__lt__` 和 `sorted(key=...)` 的分工

這題兩個都要，但它們**不是同一件事**：

| | 用途 |
|---|---|
| `__lt__` | 這個型別的**自然順序**。`max()`、`min()`、`sorted()` 不給 key 時用它 |
| `key=` | **這一次排序**的規則。會蓋過 `__lt__` |

`Detection` 的自然順序是「分數高低」（`__lt__` 比 score），
但這題要的是「分數由高到低、同分看 label」——那是**特定需求**，用 `key` 表達。

```python
sorted(dets, key=lambda d: (-d.score, d.label))
                            ↑        ↑
                        負號讓大的在前   同分時的第二層
```

**這正是你在 004-top-k-words 推出來的技巧**，只是那次是 `(-count, word)`。

（想讓 `>` `<=` `>=` 也能用，可以加 `@functools.total_ordering` 裝飾器——
有了 `__eq__` 和 `__lt__`，它會自動補出其他四個。）

## 為什麼去重要用 set 而不是 list

```python
if d in seen:      # seen 是 set → O(1)
if d in dets:      # dets 是 list → O(n)
```

大測資有 10⁵ 筆、3 萬個相異。用 list 會是 O(n·d) = 3×10⁹ 次比較，直接超時。

**這正是 019-dedupe-keep-order 的教訓**——那次的測資 d 太小讓 list 版逃過了，這次不會。
而且這次你必須實作 `__hash__` 才能把物件放進 set，**兩件事在這裡接了起來**。

## 常見錯誤

1. **只寫 `__eq__` 不寫 `__hash__`** —— `seen.add(d)` 直接 `TypeError: unhashable type`。
2. **`__eq__` 和 `__hash__` 用不同欄位** —— 最陰險的一種。去重會失效但不報錯，因為 hash 不同就進不了同一個桶。
3. **`box` 沒轉成 tuple** —— `hash()` 對 list 會炸。
4. **`__eq__` 把 score 也算進去** —— 範例第三筆（同框同類別但分數不同）就不會被去掉。
5. **只用 `__lt__` 排序不給 key** —— `sorted(dets)` 會變成「分數由低到高」，而且同分時順序不定。
6. **`__repr__` 的 label 沒加 `!r`** —— 會印成 `Detection(x, ...)` 而不是 `Detection('x', ...)`。測資逐字比對。
7. **`__eq__` 沒檢查型別** —— `d == "cat"` 會在存取 `other.label` 時 AttributeError。回傳 `NotImplemented` 或先 `isinstance` 才對。

## 延伸

這題就是 **5.8 節 NMS（非極大值抑制）的前半段**：

```
1. 依分數排序          ← 這題做的
2. 從最高分開始，把跟它 IoU 太高的其他框刪掉
3. 重複直到沒有框
```

差別在真正的 NMS 用 **IoU 門檻**判斷「重複」，而不是「框完全相同」——
因為模型不會吐出兩個一模一樣的框，只會吐出高度重疊的。
那需要 `iou(other)` 方法，而 IoU 要用到 039 的 `area` 屬性。

**039 → 040 → 041 這三題把一個類別從「資料容器」長成「有行為、能排序、能去重的值物件」**，
而 5.8 會再給它加上幾何計算。這就是物件導向真正的用途——不是為了封裝而封裝，
是讓一個概念在程式裡有一個明確的、可以長大的位置。
