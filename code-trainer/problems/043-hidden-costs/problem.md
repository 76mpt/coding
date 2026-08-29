# 043-hidden-costs · 字串串接與 list 操作的隱藏成本

- 階段：基本功：語法與函式 / 1.9 複雜度直覺
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`build_report`
- 提示：共 4 階（`python trainer.py hint 043-hidden-costs`）
- 測資：9 筆（`python trainer.py test 043-hidden-costs`）

────────────────────────────────────────────────────────────────────

有些操作**看起來是 O(1)，其實是 O(n)**。寫在迴圈裡就變成 O(n²)，而且完全看不出來。

這題有兩個這樣的陷阱。

## 要實作的函式

```python
build_report(records)
```

`records` 是 `[(label, score), ...]`。回傳一個**字串**，每筆一行、**由後往前**（最後一筆排最前面），格式：

```
label:score
```

`score` 保留**三位小數**。行之間用 `\n` 分隔，**結尾沒有換行**。

**範例**

```python
build_report([("cat", 0.9), ("dog", 0.85), ("bus", 0.5)])
->  "bus:0.500\ndog:0.850\ncat:0.900"
```

（`bus` 是最後一筆，所以排最前面。）

```python
build_report([])              ->  ""
build_report([("x", 1.0)])    ->  "x:1.000"
```

## 陷阱一：字串是不可變的

```python
s = ""
for line in lines:
    s += line + "\n"        # 看起來 O(1)，其實每次都複製整個 s
```

Python 的字串**不能修改**。`s += x` 實際上是「建一個新字串、把舊的內容複製過去、再接上 x」。
所以第 k 次迴圈要複製 k 個字元，總共 `1+2+...+n = O(n²)`。

正確做法是**先收集到 list，最後一次 `join`**——`join` 會先算好總長度、只配置一次記憶體。

（CPython 對 `s += x` 有個特例優化，在某些情況下能就地擴充。
但那**只在 refcount 剛好是 1 時成立**，不能依賴——PyPy 就沒有。）

## 陷阱二：`list.insert(0, x)` 是 O(n)

```python
out = []
for line in lines:
    out.insert(0, line)     # 想要「插到最前面」→ 後面所有元素都要往後搬一格
```

list 是**連續的陣列**。在開頭插入意味著搬動後面**全部**的元素。
迴圈裡用它同樣是 O(n²)。

「由後往前」有 O(n) 的做法：**正常 append，最後反轉一次**（或直接反著走訪）。

（真的需要頻繁在頭尾插入的話，用 `collections.deque`——它的 `appendleft` 是 O(1)。
但這題不需要。）

## 效能要求

有一筆 **10 萬筆記錄**的測資，時限 1.5 秒。
**兩個陷阱只要踩到一個就會超時。**

**限制**
- `label` 是字串，`score` 是 float。
- `records` 可能是空的。
- 最多 10⁵ 筆。
- 分數用三位小數，例如 `0.5` 要輸出 `0.500`。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 043-hidden-costs` 驗證
3. 卡住 → `python trainer.py hint 043-hidden-costs`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 043-hidden-costs`
