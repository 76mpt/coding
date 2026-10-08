# 067-chain-midpoint-and-loop · 追蹤鏈的中點與迴圈

- 階段：資料結構與演算法（LeetCode 風格） / 2.4 鏈結串列
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`scan_chain`
- 提示：共 4 階（`python trainer.py hint 067-chain-midpoint-and-loop`）
- 測資：12 筆（`python trainer.py test 067-chain-midpoint-and-loop`）

────────────────────────────────────────────────────────────────────

到目前為止你碰的資料都住在 list 裡：索引一給就跳到位，`len()` 一叫就知道有多長。
鏈結串列把這兩件事都拿掉了——你手上只有一個起點，每個節點只知道「下一個是誰」。
想知道有幾個節點，只能一步一步走過去數；想回頭看前一個，沒有路。

這一節要練的就是在這種只能往前、不能回頭的結構上，不把節點弄丟。

追蹤器把每一幀的狀態串成一條鏈，節點長這樣（`solution.py` 裡已經給好了）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

正常情況下最後一個節點的 `next` 是 `None`。但這條鏈是好幾個模組接起來的，
接線出錯的時候，某個節點的 `next` 會指回前面已經走過的節點——鏈上出現了**環**。
一旦有環，天真的 `while node is not None:` 就是無窮迴圈，整個追蹤器會停在那裡不動。

實作 `scan_chain(head)`，回傳 `(has_loop, length, mid_val)` 三個值：

- `has_loop`：這條鏈上有沒有環
- `length`：沒有環時是節點總數；**有環時固定回傳 `-1`**（有環的話長度沒有意義）
- `mid_val`：沒有環時是中點節點的值；**有環時回傳 `None`**

中點的定義：節點從 0 開始編號，取索引 `n // 2` 的那一個。
所以 5 個節點取索引 2（正中間），4 個節點取索引 2（**偏右邊**那一個）。
空鏈的 `length` 是 0，`mid_val` 是 `None`。

**範例**

```python
scan_chain(1 -> 2 -> 3 -> 4 -> 5)   ->  (False, 5, 3)
scan_chain(1 -> 2 -> 3 -> 4)        ->  (False, 4, 3)    # 4 個節點取索引 2，不是索引 1
scan_chain(7)                       ->  (False, 1, 7)
scan_chain(None)                    ->  (False, 0, None)
```

```python
#  1 -> 2 -> 3 -> 4
#       ^---------+
scan_chain(上面這條)                 ->  (True, -1, None)
```

## 兩個問題其實是同一招

「有沒有環」和「中點在哪」聽起來是兩件無關的事，但它們都只要走一遍鏈就能回答，
而且用的是**同一個手法**。想清楚那個手法是什麼，這題就只剩邊界條件要小心了。

順序上要注意：**先確定有沒有環，再做別的**。
反過來做的話，有環的輸入會讓你在數長度的那一步就卡死。

**限制**
- `0 <= n <= 2 * 10^5`，節點值是整數
- 這題是唯讀的掃描，不要改動鏈的結構
- 額外空間 **O(1)**。拿一個 `set` 記走過的節點 id 時間上也是 O(n)，測資也會過，
  但那就沒練到這題要教的東西——真正處理串流資料的時候你不會有那個空間
- 大測資有時間上限，其中一筆**有環**；先收集成 list 再處理的寫法會直接卡死

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 067-chain-midpoint-and-loop` 驗證
3. 卡住 → `python trainer.py hint 067-chain-midpoint-and-loop`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 067-chain-midpoint-and-loop`
