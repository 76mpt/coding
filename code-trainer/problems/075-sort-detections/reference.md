# 075-sort-detections · 偵測框的多鍵排序 — 參考解

## 標準解

```python
def sort_detections(dets):
    # argsort：排索引而不是排紀錄。(cls, -score) 讓一個遞增排序同時表達兩個方向
    order = sorted(range(len(dets)), key=lambda i: (dets[i][0], -dets[i][1]))
    return (order, [dets[i] for i in order])
```

兩行。`-score` 是整題的關鍵：tuple 比較是逐項的，
所以 `(cls, -score)` 遞增 ⟺ 「`cls` 遞增，同 `cls` 內 `score` 遞減」。

而且**不需要任何東西來保證平手時的順序**——Python 的 `sorted` 本來就是穩定的，
而 `(cls, -score)` 完全相同時，它們保持原順序，也就是索引遞增。免費拿到第 3 條規定。

## 另一種做法：兩次穩定排序

```python
def sort_detections(dets):
    order = list(range(len(dets)))
    order.sort(key=lambda i: -dets[i][1])      # 1) 次要鍵：score 遞減
    order.sort(key=lambda i: dets[i][0])       # 2) 主要鍵：cls 遞增（穩定）
    return (order, [dets[i] for i in order])
```

**順序是反的**：先排最不重要的鍵，最後排最重要的。
第二次排序只看 `cls`，所以 `cls` 相同的那一群在它眼裡全是平手，
穩定性保證它們維持第一輪排好的 `score` 順序。

這招的價值在於**當某個鍵無法取負號的時候**。例如主要鍵是字串而且要遞減排：
`-"abc"` 不存在，`(cls, -name)` 寫不出來。那時候兩次排序是最乾淨的解，
或者用 `reverse=True` 排那一輪（它保持穩定，見下）。

代價是跑兩遍 `O(n log n)`，常數大一倍。資料量大的時候用第一種。

## Python 排序的三個細節

**1. `sorted` 與 `list.sort` 保證穩定。** 用的是 Timsort，
它對「已經部分排好」的資料特別快（會偵測遞增/遞減的 run）。
這題的大測資 `cls` 只有 10 種、`score` 只有 20 種，平手極多，Timsort 跑得很舒服。

**2. `reverse=True` 保持穩定，`reversed(sorted(...))` 不保持。** 這是最容易踩的坑：

```python
x = [("a", 1), ("b", 1), ("c", 1)]
sorted(x, key=lambda t: t[1], reverse=True)       # [('a',1), ('b',1), ('c',1)]  原順序
list(reversed(sorted(x, key=lambda t: t[1])))     # [('c',1), ('b',1), ('a',1)]  倒過來
```

兩者對「沒有平手」的資料結果一樣，所以這個 bug 可以潛伏很久。
Python 的 `reverse=True` 不是「排完再反轉」——它在比較時就反向，
所以相等元素的原順序被保住。這是文件明確保證的行為。

**3. `key=` 比 `cmp_to_key` 快得多。** `key=` 對每個元素呼叫一次（`O(n)` 次），
算出來的鍵存起來重複用；`cmp_to_key` 是每次比較都呼叫一次（`O(n log n)` 次）。
20 萬筆差了快 20 倍。只有在「順序關係無法用單一鍵表達」時才需要 `cmp_to_key`
（例如那種循環式的自訂順序）。

## C++ 的對應（2.12 會用到）

```cpp
// std::sort 不保證穩定！要穩定得用 std::stable_sort
std::stable_sort(order.begin(), order.end(), [&](int a, int b) {
    if (dets[a].cls != dets[b].cls) return dets[a].cls < dets[b].cls;
    return dets[a].score > dets[b].score;
});
```

兩個陷阱：

- **`std::sort` 不穩定**（它是 introsort）。要穩定語意就用 `std::stable_sort`，
  或者把索引加進比較函式當最後一個鍵（這題也可以這樣做）。
- **比較函式必須是嚴格弱序**（strict weak ordering）：
  平手時必須回傳 `false`。寫成 `<=` 會讓 `std::sort` 讀到容器外面，
  在 release 版本上直接 segfault——而且是那種只在大資料上才現形的崩潰。
  上面那個寫法是對的：第一個 `if` 處理「不相等」，最後 `return` 用嚴格的 `>`。

## 複雜度

- 時間 **O(n log n)**，`n = 2×10⁵` 時約 350 萬次比較
- 空間 **O(n)**：`order` 和 `sorted_dets`，以及 `key=` 算出來的 n 個 tuple

## 常見錯誤

1. **`sorted(dets, key=lambda d: (d[0], d[1]), reverse=True)`** — `cls` 也變成遞減了。
   第一筆測資就抓到：`cls=1` 的會排在 `cls=0` 前面。
2. **`reversed(sorted(...))`** — 平手的順序被倒過來。
   「八個全平手」那筆會得到 `[7,6,...,0]` 而不是 `[0,1,...,7]`。
   這是這題最想抓的錯，因為它在沒有平手的資料上完全正確。
3. **兩次排序的順序寫反** — 先排 `cls` 再排 `score`，結果變成「`score` 遞減優先」。
   第三筆測資（`cls` 1 和 2 混著、score 大量平手）會現形。
4. **回傳 `dets` 自己排序後的結果，但 `order` 另外算** — 兩者對不上。
   題目要求 `sorted_dets[i] == dets[order[i]]`，直接從 `order` 生成就不會錯。
5. **就地排序 `dets`** — `dets.sort(...)` 改動了呼叫者的 list。
   這題不會因此失敗（測資每次都重新產生），但實務上這是很糟的副作用。
   要排索引，不要動輸入。
6. **`-score` 在 `score` 是字串時爆掉** — 這題的 `score` 保證是數值，所以安全。
   但養成習慣：取負號這招只對數值有效。

## 延伸

2.6 還有兩題，會走另外三個技能點：

- **區間排序題**：合併重疊的時間區間、算最大同時重疊數。
  那類題目的解法第一步永遠是「先排序」——而排哪個鍵（左端點還是右端點）
  決定了題目是簡單還是不可能。
- **第 k 大 + 計數排序**：當值的範圍很小時，`O(n log n)` 不是下限，`O(n + M)` 才是。

再往後：

- **2.9 堆積與優先佇列**：同樣是 top-k，但用 heap 做到 `O(n log k)`，
  而且能處理「資料一直來、不能全部存下來」的串流情況。
- **2.12 C++ 與 STL**：上面那段 `stable_sort` 和嚴格弱序。

**跟你的方向的關係**：這題就是 **NMS**（non-maximum suppression）的第一步。
真實的 NMS 流程是：按類別分組 → 每組內按信心分數遞減排序 →
從最高分的框開始，把跟它 IoU 超過閾值的框全部抑制掉 → 取下一個還沒被抑制的。
你剛排出來的順序就是那個「從最高分開始」的掃描順序，
而 `010-iou-matrix`（S5，還沒做）會給你那個 IoU 的部分。
穩定性在這裡是真的重要：平手時順序不固定，同一張圖跑兩次會得到不同的框，
而那種不確定性在評估模型時會讓你懷疑人生。
