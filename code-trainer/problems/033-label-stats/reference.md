# 033-label-stats · 標籤合法性檢查 — 參考解

## 標準解

```python
def label_stats(labels: list[int], num_classes: int) -> tuple[bool, int, set]:
    ok       = all(0 <= v < num_classes for v in labels)
    count    = sum(1 for v in labels if 0 <= v < num_classes)
    distinct = {v for v in labels if 0 <= v < num_classes}
    return ok, count, distinct
```

三行結構完全平行，只有最外層不同：`all(...)`、`sum(...)`、`{...}`。

### `0 <= v < num_classes` 是一個運算式

Python 支援**連續比較**：

```python
0 <= v < num_classes            # 讀起來就像數學
0 <= v and v < num_classes      # 等價，但囉嗦
```

而且連續比較**只求值 `v` 一次**——如果 `v` 是個昂貴的函式呼叫，這個差別是實質的。多數語言沒有這個語法（C 裡 `0 <= v < 3` 會先算 `0 <= v` 得到 0 或 1，再跟 3 比，永遠是 True）。

## `all()` 的短路，以及為什麼不能加中括號

```python
all(cond for v in labels)      # generator：遇到第一個 False 立刻停
all([cond for v in labels])    # 先算完 10⁶ 個布林值建成 list，再檢查
```

**多兩個中括號，短路就失效了。** 大測資的第一個元素就不合法：generator 版看一個元素就回傳 False，list 版要跑完全部 100 萬個。

這跟你在 021-log-sum-exp 學到的「genexp vs list 差 3700 倍記憶體」是同一件事的另一面——**這次省的是時間**。

`any()` 對稱：遇到第一個 True 就停。

**注意 `sum()` 沒有短路**（它必須看完全部才知道總和），所以第二行本來就會走完整串，那是無法避免的。

## 空真（vacuous truth）

```python
all([])   # True
any([])   # False
```

第一次看到都覺得怪。想法是這樣：

- `all` 在問「**有沒有反例**」。空集合裡找不到反例 → 沒有反例 → True。
- `any` 在問「**有沒有例子**」。空集合裡找不到例子 → False。

數學上「所有獨角獸都會飛」是真的，因為你舉不出一隻不會飛的獨角獸。這個約定讓邏輯規則保持一致（例如 `all(A + B) == all(A) and all(B)` 在空集合時也要成立）。

**實務上這常常正是你要的**：空的批次「沒有非法標籤」是合理的結論，不該報錯。

## `sum(1 for ...)` 還是 `sum(cond for ...)`

```python
sum(1 for v in labels if 0 <= v < num_classes)     # 過濾後每個算 1
sum(0 <= v < num_classes for v in labels)          # True 就是 1，直接加布林值
```

**兩者等價**，因為 Python 的 `bool` 是 `int` 的子類別，`True == 1`、`False == 0`。

第二種更短，但第一種**意圖更明顯**（「我在數東西」）。第二種依賴「布林值可以當數字加」這個知識，第一次讀會停頓一下。

（順帶：`len([v for v in labels if 條件])` 也對，但會建一個中間 list。要數個數就用 `sum`。）

## 三行能不能併成一遍走訪

可以，但**不值得**：

```python
def label_stats(labels, num_classes):
    ok, count, distinct = True, 0, set()
    for v in labels:
        if 0 <= v < num_classes:
            count += 1
            distinct.add(v)
        else:
            ok = False
    return ok, count, distinct
```

**走一遍而不是三遍**，理論上快 3 倍。但：

- 失去 `all()` 的短路（雖然這裡本來就要數完 count，所以無所謂）
- 九行 vs 三行，而且要自己維護三個狀態
- 三個 comprehension 版本的**每一行都在說一件事**，改規格時只動一行

**這題選三行版。** 走三遍聽起來浪費，但每遍都是 C 層的緊迫迴圈，實際上常常比一個 Python 層的複雜迴圈還快。**先寫清楚的，量過再優化。**

## 複雜度

時間 **O(n)**（三遍線性），空間 **O(d)**（d 是相異合法標籤數）。

## 常見錯誤

1. **`all([...])` 加了中括號** —— 功能對，但短路失效。大測資會慢很多。
2. **範圍寫成 `0 <= v <= num_classes`** —— 右邊要開區間。測資 `([1], 1)` 專門抓：`num_classes=1` 時只有 0 合法。
3. **忘記負數** —— 只檢查 `v < num_classes` 會讓 `-1` 通過。測資 `[-1, -2]` 抓這個。
4. **空 list 回傳 `False`** —— 以為「沒東西所以不算合法」。`all([])` 是 True，這是語言定義，不是可以商量的。
5. **第三項回傳 list 或 sorted list** —— 題目要 `set`。有一筆隱藏測資專門檢查型別。
6. **`count` 用 `len(distinct)`** —— 那是**相異**個數，不是總個數。`[2,2,2]` 的 count 是 3、distinct 是 `{2}`，測資會抓。

## 延伸

這個函式是**資料驗證（data validation）**的縮影，而資料驗證是 4.2「錯誤處理與防禦性設計」和 4.6「資料格式與資料清理」的主題。

真實情境裡，標籤越界的來源通常是：標註工具改過類別表、合併兩個資料集但沒對齊 `class_to_idx`（正是上一題 `032-label-maps` 在防的事）、或 one-indexed 的標註檔沒轉成 0-indexed。

**PyTorch 的 `nn.CrossEntropyLoss` 對越界標籤的反應**：在 CPU 上拋 `IndexError`，在 GPU 上可能是 `device-side assert triggered` 這種毫無資訊的錯誤——**所以要在資料進模型之前就擋掉**，那正是這個函式的位置。
