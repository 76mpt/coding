# 032-label-maps · 類別名稱與編號的對照表 — 參考解

## 標準解

```python
def label_maps(names: list[str]) -> tuple[dict, dict]:
    uniq = list(dict.fromkeys(names))              # 去重保序
    name_to_id = {n: i for i, n in enumerate(uniq)}
    id_to_name = {i: n for i, n in enumerate(uniq)}
    return name_to_id, id_to_name
```

三行。每一行做一件事，而且每一件都是 Python 的標準慣用法。

### `dict.fromkeys` 為什麼能去重保序

```python
dict.fromkeys(["cat", "dog", "cat"])   # {'cat': None, 'dog': None}
list(dict.fromkeys(["cat", "dog", "cat"]))   # ['cat', 'dog']
```

兩個性質疊起來：

- **dict 的 key 不能重複** —— 第二個 `cat` 覆蓋掉第一個，但位置不變
- **Python 3.7 起 dict 保證插入順序** —— 所以走訪出來就是首次出現的順序

（3.6 是實作細節，3.7 才寫進語言規格。在那之前大家用 `collections.OrderedDict`。）

**用 set 就不行**：`set` 不保證順序，`list(set(names))` 每次執行的順序可能不同，這種 bug 極難查——本機測十次都對，上線就亂掉。

### `enumerate` 的順序陷阱

```python
for i, n in enumerate(uniq):     # enumerate 給的是 (索引, 元素)
    ...
{n: i for i, n in enumerate(uniq)}
  ↑  ↑     ↑  ↑
 key val  解包順序固定是 (索引, 元素)
```

**解包的順序是固定的（索引在前），但寫進 dict 時哪個當 key 是你決定的。** 兩行只差在冒號兩邊對調，所以特別容易寫反——寫完用 `id_to_name[name_to_id[n]] == n` 驗一次最快。

## 為什麼要兩個方向

這不是為了出題，是真實需求：

| 時機 | 用哪個 |
|---|---|
| 準備訓練資料：把標註檔的 `"cat"` 轉成 `0` | `name_to_id` |
| 模型推論完，把 `argmax` 出來的 `2` 轉回 `"bird"` 給人看 | `id_to_name` |
| 畫混淆矩陣、寫報告的座標軸標籤 | `id_to_name` |

**而且順序必須固定。** 如果今天訓練時 `cat=0`，明天重跑變成 `cat=2`，你之前存的 checkpoint 就全錯了——模型還是輸出 0，但 0 的意義變了。這是資料管線最常見的災難之一，而根源往往就是某處用了 `set` 或 `sorted` 而沒意識到順序會變。

**PyTorch 的 `ImageFolder` 就是這樣做的**（它用資料夾名稱排序後編號），`torchvision` 的 `class_to_idx` 屬性正是這題的 `name_to_id`。

## 另一種寫法：只走一遍

標準解走了三遍（`fromkeys` 一遍、兩個 comprehension 各一遍）。要只走一遍：

```python
def label_maps(names):
    name_to_id = {}
    for n in names:
        if n not in name_to_id:
            name_to_id[n] = len(name_to_id)     # 目前有幾個，就是下一個編號
    return name_to_id, {i: n for n, i in name_to_id.items()}
```

`len(name_to_id)` 當編號很漂亮——**不用另外維護計數器**，dict 的大小自己就是下一個可用的編號。

哪個好？三遍版**每一行的意圖更清楚**（去重、編號、反轉），而且都是 O(n)，常數差別在這個規模下無感。單遍版在資料極大時省一點記憶體（不用建 `uniq`）。**可讀性優先的話選標準解。**

## 複雜度

時間 **O(n)**，空間 **O(d)**（d 是相異類別數）。

大測資有 10⁵ 個元素、500 個相異類別。如果你用 list 存「看過哪些」再 `in` 檢查，會變成 O(n·d) = 5×10⁷ 次比較——**這正是 019 那題的教訓**，只是那次測資的 d 太小讓你逃過了，這次沒有。

## 常見錯誤

1. **用 `set` 去重** —— 順序不保證，測資 `["z", "y", "x"]` 會抓到（如果變成字母序，`x` 就拿 0 了）。
2. **先 `sorted(set(names))`** —— 順序穩定了，但變成字母序，題目要的是出現順序。
3. **`enumerate` 的解包寫反** —— `{i: n for n, i in ...}` 會得到 `{'cat': 0}` 反過來的東西。兩個 dict 都寫反的話還會「自洽」，只是全錯。
4. **編號從 1 開始** —— 題目說從 0。分類模型的標籤慣例也是 0-based（`nn.CrossEntropyLoss` 預期 `[0, C)`）。
5. **只回傳一個 dict** —— 題目要兩個。
6. **重複的名稱拿最後一次的編號** —— 例如用 `{n: i for i, n in enumerate(names)}`（直接對原始 names 做），`cat` 會被後面的覆蓋掉、編號變成 2。這是最隱蔽的一個：小測資看不出來，因為覆蓋只在有重複時發生。

## 延伸

這題的三個零件之後會一直用：

- **`dict.fromkeys` 去重保序** —— 資料清理的標配（4.6）
- **`enumerate`** —— 只要你需要「第幾個」就會用到
- **雙向 dict** —— 詞彙表（vocab）也是同一個結構：token ↔ id。NLP 的 tokenizer、CV 的類別表，本質相同

**節點 5.10 訓練迴圈與資料管線**會讓你完整寫一次 dataset，那時候 `class_to_idx` 就是你自己建的。
