# 039-bounding-box-class · BoundingBox 類別 — 參考解

## 標準解

```python
class BoundingBox:
    def __init__(self, x1, y1, x2, y2):
        if x2 <= x1 or y2 <= y1:
            raise ValueError(f"框的寬高必須為正：({x1}, {y1}, {x2}, {y2})")
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def area(self):
        return self.width * self.height      # property 可以用另一個 property

    @property
    def center(self):
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def __repr__(self):
        return f"BoundingBox({self.x1}, {self.y1}, {self.x2}, {self.y2})"


def make_boxes(raw):
    return [BoundingBox(*t) for t in raw]
```

## `@property`：算出來，不要存起來

```python
@property
def area(self):
    return self.width * self.height
```

**如果在 `__init__` 裡算好存成 `self.area`，就會有兩份資料要同步。**
改了 `x2` 之後 `area` 就過時了——有一筆隱藏測資專門驗這件事：

```python
b = BoundingBox(0, 0, 3, 2)
b.x2 = 10
b.width   # 必須是 10，不是 3
b.area    # 必須是 20，不是 6
```

這跟你在 018 的 review 看到的原則一樣：**衍生資料就現算，不要維護副本**。

`@property` 讓「現算」在使用端看起來跟「存起來」一模一樣（`b.area` 不加括號），
所以你可以先寫存起來的版本、之後改成計算的，**呼叫端一行都不用改**。
這是 Python 沒有 getter/setter 樣板的原因——需要時再加上去就好。

## `__init__` 裡驗證：讓不合法的物件建不出來

```python
raw = (30, 20, 10, 40)        # 合法的 tuple，但不是合法的框
BoundingBox(30, 20, 10, 40)   # ValueError —— 當場擋下
```

用 tuple 的話，錯誤資料可以在系統裡流動很久，直到某個計算出現負面積才爆——
而那時候堆疊已經離錯誤來源很遠了。

> **把驗證放在建構子，等於讓型別系統幫你保證「只要拿到 BoundingBox，它就是合法的」。**

這叫 **make illegal states unrepresentable**，是型別設計的核心原則之一，4.1「介面設計」會正式談。

## `__repr__` 為什麼要長成那樣

```python
repr(b)   # 'BoundingBox(0, 0, 3, 2)'
```

慣例是**讓 repr 看起來像能把物件建回來的那行程式碼**。好處很實際：

- 除錯時 `print(boxes)` 直接看到內容，而不是 `<__main__.BoundingBox object at 0x7f8b1c0>`
- log 裡的 repr 可以直接複製貼上重現問題
- 測資失敗時的訊息看得懂（你今天很多題都靠這個）

`__str__` 是給終端使用者看的（可以寫成 `框 (0,0)-(3,2)`），`__repr__` 是給開發者看的。
**只寫一個的話寫 `__repr__`**——`print()` 找不到 `__str__` 會退而用它。

## `BoundingBox(*t)` 的星號

```python
t = (0, 0, 3, 2)
BoundingBox(*t)                  # 展開成四個參數
BoundingBox(t[0], t[1], t[2], t[3])   # 等價但囉嗦
```

這是 016 那題 `*args` 的反向操作：**定義時 `*` 是「收集」，呼叫時 `*` 是「展開」**。

## 什麼時候該用 class，什麼時候 tuple 就夠

| 用 tuple / dict | 用 class |
|---|---|
| 只是一包資料，馬上就用掉 | 有**行為**（方法、驗證、計算屬性） |
| 欄位少而且順序明顯 | 欄位多，需要名字 |
| 不會被傳很遠 | 會在系統裡流動，需要保證合法性 |

**不要為了用 class 而用 class。** 031 那題用 tuple 是對的（只算個面積就丟）；
這題的 BoundingBox 值得包起來，因為它會被建立、驗證、比較、排序、傳遞。

（Python 還有 `@dataclass` 可以自動生成 `__init__` 和 `__repr__`——下一題會用到。
但先手寫一次，你才知道它替你省了什麼。）

## 常見錯誤

1. **`area` 忘記加 `@property`** —— 那樣要寫 `b.area()` 才能呼叫，測資的 `got[0].area` 會拿到一個方法物件而不是數字。
2. **在 `__init__` 裡把 width/area 算好存起來** —— 小測資會過，隱藏測資改 `x2` 之後就露餡。
3. **`__repr__` 格式不對** —— 少空格、用了單引號、寫成 `<BoundingBox ...>`。測資逐字比對。
4. **驗證寫在 `make_boxes` 而不是 `__init__`** —— 那樣直接 `BoundingBox(30,20,10,40)` 就繞過了驗證。**驗證要在唯一的入口。**
5. **`center` 用整數除法 `//`** —— `(0+3)//2` 是 1 不是 1.5。中心點必須是浮點。
6. **忘記 `self`** —— `def width():` 少了 `self`，呼叫時會 TypeError。

## 延伸

這個類別會在後面長大：

| 節點 | 加什麼 |
|---|---|
| **1.8 下一題** | 類別屬性計數器、`@dataclass` |
| **1.8 第三題** | `__eq__`、`__lt__`、`__hash__` —— 讓它能排序、去重、比較 |
| **5.8 IoU/NMS** | `iou(other)` 方法；NMS 需要依分數排序，正是 `__lt__` |
| **5.10 資料管線** | 一個 `Annotation` 類別包住 box + label + score |

真實的偵測框類別（`torchvision.ops.boxes`、`detectron2.structures.Boxes`）
做的是同一件事，只是底下換成張量、一次處理幾千個框。
