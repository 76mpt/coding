# 040-class-vs-instance-attr · 類別屬性與實例屬性

- 階段：基本功：語法與函式 / 1.8 class 與物件
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`build_datasets`
- 提示：共 4 階（`python trainer.py hint 040-class-vs-instance-attr`）
- 測資：8 筆（`python trainer.py test 040-class-vs-instance-attr`）

────────────────────────────────────────────────────────────────────

這題考 Python 物件模型最容易踩的坑：**類別屬性 vs 實例屬性**。

**要實作的 `Dataset`**

```python
d = Dataset("train")

d.name              ->  "train"       # 每個實例自己的
d.samples           ->  []            # 每個實例自己的，一開始是空的
d.add("img1.jpg")                     # 加一筆樣本
len(d)              ->  1             # __len__

Dataset.count       ->  1             # 類別屬性：總共建過幾個 Dataset
```

| 屬性 | 屬於誰 | 說明 |
|---|---|---|
| `name` | **實例** | 每個 dataset 有自己的名字 |
| `samples` | **實例** | 每個 dataset 有自己的樣本清單 |
| `count` | **類別** | 所有實例共用一個計數器，記錄建了幾個 |

**要實作的入口函式**

```python
build_datasets(specs)
```

`specs` 是 `[(名字, [樣本, ...]), ...]`。對每一組建一個 `Dataset`，把樣本逐一 `add` 進去。
回傳 `(datasets, Dataset.count)`。

**計數器要先歸零**——`build_datasets` 一開始要把 `Dataset.count` 設回 0，
這樣重複呼叫才不會累加。

**範例**

```python
ds, n = build_datasets([("train", ["a", "b"]), ("val", ["c"])])

ds[0].name       ->  "train"
ds[0].samples    ->  ["a", "b"]
ds[1].samples    ->  ["c"]          # val 不該看到 train 的樣本
len(ds[0])       ->  2
n                ->  2              # 建了兩個 Dataset

build_datasets([])   ->  ([], 0)
```

## 這題的陷阱

下面這個寫法**看起來完全正確，但是錯的**：

```python
class Dataset:
    samples = []          # ← 陷阱：這是類別屬性，所有實例共用同一個 list

    def __init__(self, name):
        self.name = name

    def add(self, s):
        self.samples.append(s)
```

```python
a = Dataset("train"); a.add("x")
b = Dataset("val")
b.samples             # ['x'] ← b 從來沒 add 過，卻看得到 a 的東西！
a.samples is b.samples  # True ← 它們根本是同一個 list
```

**`samples` 要在 `__init__` 裡建立**，那樣每個實例才會有自己的一份。

這跟你在 **015-add-tag** 遇到的可變預設參數陷阱是**同一個根源**：

> **可變物件如果只被建立一次，就會被所有人共用。**

類別主體只在「定義類別時」執行一次，函式的預設值也只在「定義函式時」求值一次。

**限制**
- `specs` 可能是空 list。
- 名字是字串，樣本也是字串。
- 最多 10⁴ 個 dataset。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 040-class-vs-instance-attr` 驗證
3. 卡住 → `python trainer.py hint 040-class-vs-instance-attr`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 040-class-vs-instance-attr`
