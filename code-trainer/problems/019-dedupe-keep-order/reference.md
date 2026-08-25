# 019-dedupe-keep-order · 去重但保留順序 — 參考解

## 標準解

```python
def dedupe_keep_order(items: list) -> tuple[list, int]:
    seen = set()
    kept = []
    for x in items:
        if x not in seen:
            seen.add(x)
            kept.append(x)
    return kept, len(items) - len(kept)
```

**O(n) 時間、O(n) 空間。** 這是最佳解。

注意 `removed` 沒有在迴圈裡累加，而是最後用 `len(items) - len(kept)` 推導——
**能算出來的就不要另外維護**，少一個變數就少一個不同步的機會。

## 用 dict 的一行版（Python 3.7+）

```python
def dedupe_keep_order(items: list) -> tuple[list, int]:
    kept = list(dict.fromkeys(items))
    return kept, len(items) - len(kept)
```

`dict.fromkeys(items)` 用 items 當 key 建一個 dict——
**key 自動去重，而且 Python 3.7+ 保證維持插入順序**。

這是目前 Python 圈公認最漂亮的「保序去重」寫法，
比手寫版稍快（迴圈在 C 層）。但**新手應該先寫得出手寫版**，
因為它讓你看見「set 查詢」這個關鍵動作；一行版把它藏起來了。

## 這題的核心：`in` 的複雜度

| 容器 | `x in c` | 為什麼 |
|---|---|---|
| `list` / `tuple` | **O(n)** | 線性掃描，一個一個比 |
| `set` / `dict` | **O(1)** 平均 | 算雜湊值 → 直接定位 |
| `str` | O(n·m) | 子字串搜尋 |

用 list 當 `seen` 的話：

```python
kept = []
for x in items:
    if x not in kept:      # ❌ 每次都掃過整個 kept
        kept.append(x)
```

n 次迴圈 × 每次最多 O(n) 掃描 = **O(n²)**。
20 萬元素、1000 個相異值時大約是 2×10⁸ 次比較，Python 要跑好幾十秒。

**「頻繁檢查存在性」就用 set/dict，這是效能直覺的第一課。**
在 CV 裡的典型場景：檢查某個 image_id 是否已處理、某個 anchor 是否已匹配——
用 list 的話資料集一大就爆。

## set 的代價

set 不是免費的：

- **元素必須可雜湊（hashable）** — list、dict、set 本身不行。
  要對 list 去重的話得先轉成 tuple：`tuple(box)`。
- **額外記憶體** — 這題同時存了 `seen` 和 `kept`，空間是 2 倍。
- **雜湊碰撞** — 最壞情況退化成 O(n)，但實務上幾乎不會遇到
  （除非有人刻意構造，那叫雜湊碰撞攻擊）。

如果元素不可雜湊，退而求其次是**排序後比對相鄰**（O(n log n)），
但那會破壞順序——就是 C++ 的 `sort + unique` 做法（你在 008 題做過）。

## 為什麼不能用 `list(set(items))`

```python
list(set([3, 1, 3, 2]))     # 可能是 [1, 2, 3]，也可能是別的順序
```

`set` 的走訪順序由**雜湊值**決定，跟插入順序無關。
對小整數看起來像是排序過（因為 `hash(n) == n`），
但對字串就是完全不可預測的——而且**同一份程式在不同次執行可能不同**
（Python 預設開啟字串雜湊隨機化，防雜湊碰撞攻擊）。

**任何依賴 set 走訪順序的程式碼都是不可重現的 bug。**
研究工作特別要小心：實驗結果不可重現，常常就是這種地方。

## 常見錯誤

1. **`if x not in kept`（用 list 查）** — 正確但 O(n²)，大測資超時。
2. **`list(set(items))`** — 順序不對，而且不可重現。
3. **`seen.append(x)`** — set 沒有 `append`，要用 `add`。
4. **回傳 `len(set(items))` 當作保留數量** — 這題碰巧一樣，
   但如果元素不可雜湊或有 `nan`（`nan != nan`）就會出錯。
5. **同時維護 `removed` 計數器卻忘記更新** — 所以標準解直接用長度相減。

## 延伸

「保序去重」在實務上的變形：

- **依某個欄位去重**：`seen.add(r["id"])` 而不是整筆記錄
  （例如同一張圖的重複標註）
- **保留最後一次而非第一次**：先 `reversed(items)` 再去重再反轉回來
- **近似去重**：浮點數或特徵向量不能直接比相等，
  要用容差或**局部敏感雜湊（LSH）**——這在影像去重、資料集清理裡是標準工具

CV 的實際場景：訓練前檢查資料集有沒有重複影像（用 perceptual hash 去重），
避免同一張圖同時出現在 train 和 test——**這是最常見的資料洩漏來源之一**。
