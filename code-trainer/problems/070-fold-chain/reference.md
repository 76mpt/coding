# 070-fold-chain · 把軌跡對折重排 — 參考解

## 標準解

```python
def fold_chain(head):
    if head is None or head.next is None:
        return head

    # 1) 快慢指標找中點（067）。迴圈結束時 slow 停在索引 n // 2
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    # 2) 在 slow 前面切斷：前半長 n//2，後半長 n - n//2（後半 >= 前半）
    second = slow
    slow_prev = head
    while slow_prev.next is not slow:
        slow_prev = slow_prev.next
    slow_prev.next = None

    # 3) 反轉後半（068 的核心動作，迭代版）
    prev, node = None, second
    while node is not None:
        nxt = node.next
        node.next = prev
        prev = node
        node = nxt
    second = prev

    # 4) 交錯穿插
    first = head
    while first is not None and second is not None:
        f_next, s_next = first.next, second.next     # 兩邊的路先存起來
        first.next = second
        if f_next is None:                           # second 就是結果的最後一個
            break                                    # 不能再改它的 next，否則成環
        second.next = f_next
        first, second = f_next, s_next

    return head
```

## 為什麼奇數長度不用特判

這是這題唯一值得推一下的地方。設 `h = n // 2`：

- 前半段 = 索引 `0 … h-1`，長度 `h`
- 後半段 = 索引 `h … n-1`，長度 `n - h`

`n` 偶數時兩段都是 `n/2`；`n` 奇數時後半段多一個。
所以**後半段永遠大於或等於前半段**。

交錯的時候每一輪消耗前半一個、後半一個。前半先用完，
而前半用完的那一刻，剛接上去的後半節點就是整串的最後一個。
後半如果比前半多一個，那個「多的」就是後半反轉前的第一個節點，
也就是原鏈索引 `h` 的節點——`n` 奇數時 `h = (n-1)/2`，正是正中間。

所以題目要的「中間那個落在最後」是切對邊之後的**自然結果**，不是特例。
反過來說，如果你讓前半比後半長（例如切在 `slow` 後面），
交錯到最後會剩下前半的一個節點無處可去，你就得寫一條分支去接它。

## 另一種做法：收集節點再重接

```python
def fold_chain(head):
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    i, j = 0, len(nodes) - 1
    order = []
    while i < j:
        order.append(nodes[i]); order.append(nodes[j])
        i += 1; j -= 1
    if i == j:
        order.append(nodes[i])
    for k in range(len(order) - 1):
        order[k].next = order[k + 1]
    if order:
        order[-1].next = None
    return order[0] if order else None
```

這是**合法的**：搬的是節點不是值，`val` 沒被動過，時間也是 O(n)。
在真實專案裡我大概會寫這一版——它一眼就看得懂，而且幾乎不可能寫錯。

代價是 O(n) 額外空間。n = 2×10⁵ 時那是一個 20 萬個元素的 list，不算什麼；
但如果鏈長是資料決定的、而你在記憶體很緊的裝置上（嵌入式、車上的視覺模組），
O(1) 的那個版本就是唯一選項。

這題要你寫 O(1) 的版本，是因為那三個指標動作本身是 2.4 的全部內容。
**知道有簡單版本、也寫得出難的版本**，才有資格在實務上選前者。

## 複雜度

- 時間 **O(n)**：找中點 `n/2` 步、找切點 `n/2` 步、反轉 `n/2` 步、交錯 `n/2` 步，合計約 `2n`
- 空間 **O(1)**：`slow`、`fast`、`prev`、`node`、`nxt`、`first`、`second`、`f_next`、`s_next`
  ——九個指標，跟 n 無關

找切點那一遍可以省掉（在找中點的迴圈裡順手多記一個 `slow_prev`），
省下 `n/2` 步。值得寫一次，但別為了它把迴圈弄複雜。

## 常見錯誤

1. **忘了切斷** — 前半段的尾巴還連著後半段，反轉後半之後整條鏈變成一個環。
   小測資可能還印得出前幾個值，大測資直接超時（走訪永遠不結束）。
   這就是 067 教你偵測的那個環，這次是你自己造的。
2. **切錯邊** — 切在 `slow` 後面，讓前半比後半長。`n = 3` 這筆會抓到：
   你會得到 `1 -> 3` 然後 `2` 掉了，或是多出一條分支。
3. **交錯迴圈沒處理最後一步** — 寫成
   `first.next = second; second.next = first.next_原本的值` 卻沒檢查那個值是不是 `None`。
   最後一個 `second` 的 `next` 被指回已經接過的節點 → 環。
   這個 bug 在偶數長度上不一定現形，奇數長度一定炸。
4. **連續改兩個 `next` 卻沒先存路** — `first.next = second` 之後再讀 `first.next`
   拿到的是 `second`，不是原本的下一個。這題必須先把 `f_next`、`s_next` 存下來。
5. **搬值而不是搬節點** — 收集 `val` 成 list、重排、寫回每個節點的 `val`。
   輸出順序是對的，但節點的身分全亂了。`v0` 那筆測資專門抓這個。
6. **用遞迴反轉後半** — 深度 O(n)，20 萬個節點爆 `RecursionError`。068 已經踩過一次。

## 延伸

**2.4 到這裡收完了。** 三題合起來是一組：067 找中點（唯讀）、068 反轉一段（改接線）、
這題把兩個組合起來再加交錯。鏈結串列題幾乎都是這幾個動作的排列組合。

立刻可以自己做的：

- **判斷回文鏈**（LeetCode 234）：067 找中點 + 068 反轉後半 + 逐一比對。
  比這題更簡單，而且你已經有全部零件了。做它當作驗收。
- **每 k 個一組反轉**（LeetCode 25）：068 的一般化，`dummy` 在那裡不可或缺。
- **合併 k 條有序鏈**（LeetCode 23）：這個留到 **2.9 堆積與優先佇列**，
  因為好的解法需要 priority queue。到時候你會回頭用到今天的兩兩合併。

**跟你的方向的關係**：這題的「對折」在軌跡處理裡是真的動作——
迴圈閉合（loop closure）偵測就是在問「我現在這一幀，跟很久以前的哪一幀是同一個地方」。
最樸素的做法就是把軌跡頭尾對折起來一對一比對。
而 O(1) 空間的指標操作，是嵌入式視覺模組上真正會在意的事：
Jetson 上跑 VIO 的時候，你沒有多餘的記憶體去複製一份軌跡。
