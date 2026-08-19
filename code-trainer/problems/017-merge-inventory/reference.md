# 017-merge-inventory · 合併庫存 — 參考解

## 標準解

```python
def merge_inventory(a: dict, b: dict) -> dict:
    merged = dict(a)                                   # 淺複製，不動輸入
    for key, value in b.items():
        merged[key] = merged.get(key, 0) + value       # 沒有就當 0
    return {k: v for k, v in merged.items() if v > 0}  # 過濾
```

O(len(a) + len(b)) 時間、O(len(a) + len(b)) 空間。

## 用 Counter 的版本

```python
from collections import Counter

def merge_inventory(a: dict, b: dict) -> dict:
    return {k: v for k, v in (Counter(a) + Counter(b)).items() if v > 0}
```

`Counter` 支援 `+` 運算，會自動把相同 key 的值相加。

⚠️ **但 `Counter` 的 `+` 會自動丟掉 ≤ 0 的項目**，這題剛好符合需求所以能用；
如果規格是「保留負數」，`Counter + Counter` 就會給你錯的答案。
另外 `Counter(a) + Counter(b)` 回傳的是 `Counter` 不是 `dict`——
`Counter` 是 `dict` 的子類別，多數情況可以互換，但型別註解要寫對。

**方便的工具要知道它的隱含行為**，不然它幫你做的事會變成你的 bug。

## `dict.get` vs `setdefault` vs `defaultdict`

三個都在解「key 可能不存在」的問題，用途不同：

```python
d.get(k, 0)              # 只讀，不會改 d
d.setdefault(k, []) .append(x)   # 沒有就塞一個預設值進去，然後回傳它
                                 # 適合「值是容器，要往裡面加東西」

from collections import defaultdict
d = defaultdict(list)
d[k].append(x)           # 存取不存在的 key 時自動建立
```

判斷：
- **只是要讀** → `get`
- **要往容器裡加東西，而且 dict 是現成的** → `setdefault`
- **整個 dict 都是你建的，會加很多次** → `defaultdict`

⚠️ `defaultdict` 有個陷阱：**單純讀取一個不存在的 key 也會建立它**：

```python
d = defaultdict(list)
if d["nope"]:            # 只是想檢查，但 d 已經多了一個 key
    ...
print(len(d))            # 1
```

## 賦值不是複製

```python
merged = a               # 兩個名字指向同一個 dict
merged = dict(a)         # 新 dict（淺複製）
merged = a.copy()        # 同上
import copy
merged = copy.deepcopy(a)  # 深複製，連裡面的物件也複製
```

**什麼時候需要深複製？** 當 dict 的**值本身是可變物件**時：

```python
a = {"boxes": [[0, 0, 1, 1]]}
shallow = dict(a)
shallow["boxes"].append([2, 2, 3, 3])   # a["boxes"] 也變了！
```

這題的值是整數（不可變），淺複製就夠。
**但如果哪天值變成 list（例如 `{"cat": [box1, box2]}`），就必須深複製。**

## 常見錯誤

1. **`merged = a`** — 不是複製，`a` 會被改到。隱藏測資的 `check_arg` 就是在抓這個。
2. **保留條件寫成 `v >= 0`** — `{"a": 0}` 那筆不過。
   規格說「≤ 0 移除」，保留的是嚴格大於 0。
3. **邊走訪邊刪除** — `RuntimeError: dictionary changed size during iteration`。
   要嘛建新 dict，要嘛先收集 key 再刪。
4. **直接 `merged[key] += value`** — key 不存在時 KeyError。
5. **用 `a.update(b)`** — 那是**覆蓋**不是相加，`{"apple":3}` 會直接變成 `{"apple":2}`。
   `update` 的語意是「用 b 的值蓋掉 a 的值」。

## 延伸

「合併並累加」在真實工作裡到處都是：

- **梯度累積**：多個 mini-batch 的梯度字典相加（`{param_name: grad}`）
- **分散式訓練**：各張 GPU 的統計量合併（all-reduce 就是這件事）
- **資料集統計**：多個分片的類別計數合併
- **log 聚合**：多台機器的錯誤計數合併

PyTorch 裡的 `state_dict` 就是一個大 dict，模型合併、EMA、模型平均全都是這個模式的變形。
