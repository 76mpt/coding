# 018-group-by-label · 依類別分組標註 — 參考解

## 標準解

```python
def group_by_label(records: list[dict]) -> dict:
    groups = {}
    for r in records:
        groups.setdefault(r["label"], []).append(r["box"])
    return groups
```

**O(n) 時間、O(n) 空間。** 這是最佳解——你至少要看過每筆記錄一次。

## 三種等價寫法

```python
# A. 明確的 if/else —— 最好讀，新手推薦
for r in records:
    label = r["label"]
    if label not in groups:
        groups[label] = []
    groups[label].append(r["box"])

# B. setdefault —— 一行，不需要額外 import
groups.setdefault(r["label"], []).append(r["box"])

# C. defaultdict —— 實務上最常見
from collections import defaultdict
groups = defaultdict(list)
for r in records:
    groups[r["label"]].append(r["box"])
return dict(groups)          # 轉回普通 dict 比較安全
```

**怎麼選？**

| 情況 | 選哪個 |
|---|---|
| dict 是你從頭建的、要 append 很多次 | **C `defaultdict`**（最快，因為不用每次查 key） |
| dict 是別人給的，只加幾次 | **B `setdefault`** |
| 邏輯複雜、還要做別的事 | **A `if/else`**（最清楚） |

⚠️ `setdefault` 有個小缺點：**不論 key 在不在，第二個參數都會被求值**。
所以 `d.setdefault(k, expensive())` 每次都會呼叫 `expensive()`。
這題的 `[]` 很便宜所以沒差。

## `itertools.groupby` 在這裡不能用

```python
from itertools import groupby
# ❌ 這是錯的
{k: list(g) for k, g in groupby(records, key=lambda r: r["label"])}
```

`itertools.groupby` **只會把「相鄰」且 key 相同的元素分成一組**（跟 SQL 的 GROUP BY 不一樣）。
範例裡的 `cat, dog, cat` 會被分成**三組**，第三組的 `cat` 蓋掉第一組。

要用它就得先排序：`groupby(sorted(records, key=...), key=...)`，
但那變成 O(n log n)，而且**破壞了原本的順序**（題目要求保持順序）。

**dict 分組是 O(n)，排序分組是 O(n log n)。除非你本來就需要排序，否則用 dict。**

## 為什麼順序自動就對了

題目要求「每個類別底下的 box 維持原本順序」，但標準解沒有做任何排序。原因：

1. 你是**照 `records` 的順序**掃過去的，`append` 是加到尾端，所以同一類別內部順序自然正確。
2. Python **3.7+ 保證 dict 維持插入順序**（3.6 是實作細節，3.7 寫進語言規格）。
   所以 `groups` 的 key 順序 = 各類別第一次出現的順序。

**能靠既有語意自然成立的需求，就不要額外寫程式去保證。**

## 為什麼 O(類別數 × n) 會超時

錯誤寫法：

```python
labels = {r["label"] for r in records}          # 先收集所有類別
return {lb: [r["box"] for r in records if r["label"] == lb] for lb in labels}
```

看起來很 pythonic，但**對每個類別都完整掃一遍 records**。
50 個類別 × 10 萬筆 = 500 萬次比較。大測資就是在抓這個。

**看到「巢狀的資料走訪」就要警覺**：外層迴圈 × 內層迴圈 = 相乘的複雜度。

## 常見錯誤

1. **`groups[label].append(box)` 沒有先建立 list** — 第一次遇到該 label 時 KeyError。
2. **`groups[label] = box`** — 覆蓋而不是累積，每個類別只會留下最後一個 box。
3. **用 `itertools.groupby` 沒先排序** — 不相鄰的同類別會被拆成多組。
4. **回傳 `defaultdict` 沒轉回 dict** — 多數情況沒事，但如果呼叫端做
   `if label in groups` 之外的操作（例如 `groups[label]` 檢查存在性），
   `defaultdict` 會**默默建立**那個 key，資料就髒了。
5. **每個類別各掃一遍** — 見上，複雜度爆炸。

## 延伸

這個「分組」操作在資料處理裡是最基本的動作之一：

- **pandas**：`df.groupby("label")["box"].apply(list)`
- **SQL**：`SELECT label, ... FROM t GROUP BY label`
- **MapReduce**：整個 shuffle 階段就是在做分組

在 CV 的實際用途：

- **計算 mAP** 時要把預測與 ground truth **依類別分組**，每個類別各自算一條 PR 曲線（節點 5.8）
- **資料集分析**：每個類別有幾個框、框的尺寸分布如何 → 決定 anchor 大小
- **類別不平衡處理**：分組後才知道要對哪些類別過採樣

你在節點 5.8 實作 mAP 時，第一步就是這個函式。
