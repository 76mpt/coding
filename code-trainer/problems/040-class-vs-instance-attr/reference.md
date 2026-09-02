# 040-class-vs-instance-attr · 類別屬性與實例屬性 — 參考解

## 標準解

```python
class Dataset:
    count = 0                       # 類別屬性：所有實例共用

    def __init__(self, name):
        self.name = name
        self.samples = []           # 實例屬性：每個實例一份
        Dataset.count += 1          # 明確指名要改類別的那個

    def add(self, sample):
        self.samples.append(sample)

    def __len__(self):
        return len(self.samples)


def build_datasets(specs):
    Dataset.count = 0
    out = []
    for name, samples in specs:
        d = Dataset(name)
        for s in samples:
            d.add(s)
        out.append(d)
    return out, Dataset.count
```

## 陷阱一：可變的類別屬性被共用

```python
class Dataset:
    samples = []            # 只在「定義類別」時執行一次
```

**類別主體是一段程式碼，在 `class` 語句執行時跑一次。** 所以那個 `[]` 只被建立一次，
之後所有實例的 `self.samples` 都指向同一個物件。

```python
a = Dataset("train"); a.add("x")
b = Dataset("val")
b.samples                # ['x']
a.samples is b.samples   # True
```

寫在 `__init__` 裡才對——**`__init__` 每建一個實例就執行一次**，每次產生新的 list。

> 這跟 015 的 `def f(tags=[])` 是**同一個根源**：
> 預設值也只在「定義函式」時求值一次。
> **可變物件只被建立一次，就會被所有人共用。**

注意**不可變**的類別屬性沒這個問題——`count = 0` 很安全，因為 `int` 改不了，
任何「修改」都會產生新物件。所以陷阱只發生在 list、dict、set 這些可變型別上。

## 陷阱二：`self.count += 1` 不會改到類別屬性

```python
self.count += 1
# 等價於
self.count = self.count + 1
#     ↑            ↑
#   賦值        讀取
```

Python 的屬性查找是**不對稱**的：

| 動作 | 行為 |
|---|---|
| **讀取** `self.count` | 先找實例，找不到就往類別找（**會找到類別屬性**） |
| **賦值** `self.count = x` | **一律建立/覆寫實例屬性**，不會碰類別屬性 |

所以 `self.count += 1` 的實際效果是：讀到類別的 0，然後在**這個實例**上建一個新的 `count = 1`。
類別的 `count` 從頭到尾是 0，而每個實例都有自己的 1。

**要改共用的那個，必須明確指名**：

```python
Dataset.count += 1        # 直接指名類別
type(self).count += 1     # 或者透過實例拿到它的類別（子類別會分別計數）
```

隱藏測資 `got[1]==4` 專門抓這個——用 `self.count += 1` 的話會回傳 0。

## `__len__`：讓 `len()` 能用在你的物件上

```python
def __len__(self):
    return len(self.samples)
```

定義了它，`len(d)` 就能用。這是 **Python 的協定（protocol）機制**：
內建函式和語法不檢查你的型別，只檢查你有沒有實作對應的 dunder。

| 你想支援 | 實作 |
|---|---|
| `len(x)` | `__len__` |
| `x[i]` | `__getitem__` |
| `for i in x` | `__iter__` |
| `x == y` | `__eq__` |
| `x < y` | `__lt__` |
| `print(x)` | `__repr__` / `__str__` |
| `with x:` | `__enter__` / `__exit__` |

**這叫鴨子型別（duck typing）**：不管你是什麼類別，只要會 `__len__`，`len()` 就吃你。
下一題會用 `__eq__` 和 `__lt__` 讓 BoundingBox 能排序和去重。

（順帶：定義了 `__len__` 之後，你的物件也有了真值——**`len` 是 0 的物件在 `if` 裡是 False**。
所以 `if dataset:` 會變成「這個 dataset 有沒有樣本」，不是「這個變數是不是 None」。這個副作用要知道。）

## 為什麼 `build_datasets` 要歸零

因為 `count` 是**全域可變狀態**——它跨呼叫存活。不歸零的話第二次呼叫會從上次的數字接著加。

**這正是類別屬性計數器的缺點**：它是隱藏的全域變數。實務上要小心：

- 多執行緒同時建立實例會 race（`+=` 不是原子操作）
- 測試之間會互相污染（所以測試框架常要 `setUp` 重置）
- 子類別繼承時的行為容易搞混

**需要計數的話，通常更好的做法是「呼叫端自己數」**（`len(out)`）而不是讓類別記著。
這題用它是為了讓你踩到 `self.count += 1` 那個坑。

## 常見錯誤

1. **`samples = []` 寫在 class 主體** —— 這題的主角。測資檢查 `got[0][0].samples is not got[0][1].samples`。
2. **`self.count += 1`** —— count 永遠回傳 0。隱藏測資抓。
3. **忘記歸零** —— 單獨跑一筆測資會過，跑整批就會累加。
4. **`__len__` 回傳非整數或負數** —— Python 會 TypeError/ValueError。
5. **`add` 寫成 `self.samples = self.samples + [s]`** —— 能動，但每次都建新 list，10⁴ 筆會變 O(n²)。用 `append`。
6. **在 `__init__` 裡寫 `samples=[]` 當參數預設值** —— 015 那個陷阱的變形，同樣所有實例共用。

## 延伸

類別屬性的合法用途是**「所有實例共通、而且不會被修改」的東西**：

```python
class Detector:
    CLASSES = ("person", "car", "dog")     # 用 tuple，不可變
    DEFAULT_THRESHOLD = 0.5
```

注意用 `tuple` 而不是 `list`——**不可變就不會被誤改**，也就不會有共用問題。
這是「用型別防止錯誤」的又一個例子。

4.9「型別註解與工具鍊」會教 `ClassVar[...]` 標記類別屬性，讓 mypy 幫你檢查。
而 `@dataclass` 會直接禁止可變的類別預設值（要求你用 `field(default_factory=list)`），
**等於把這個陷阱寫進語言的工具裡**。
