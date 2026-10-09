# 068-reverse-chain-segment · 反轉軌跡中的一段 — 參考解

## 標準解：頭插法

```python
def reverse_between(head, left, right):
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)          # 假節點：讓「段前一個」永遠存在
    prev = dummy
    for _ in range(left - 1):          # prev 停在第 left-1 個節點
        prev = prev.next

    tail = prev.next                   # 段的原頭。反轉後它是段的尾巴，位置不再變動
    for _ in range(right - left):      # 把 tail 後面的節點一個一個搬到 prev 後面
        nxt = tail.next                # 要搬的那一個
        tail.next = nxt.next           # 1) 從現在的位置拆下來
        nxt.next = prev.next           # 2) 接上目前的段頭
        prev.next = nxt                # 3) 成為新的段頭

    return dummy.next                  # 不是 head：開頭可能已經換人
```

拿 `1 -> 2 -> 3 -> 4 -> 5`、`left = 2`、`right = 4` 走一遍：

```
起點        dummy -> 1 -> [2 -> 3 -> 4] -> 5        prev=1, tail=2
搬 3        dummy -> 1 -> [3 -> 2 -> 4] -> 5
搬 4        dummy -> 1 -> [4 -> 3 -> 2] -> 5
```

`tail` 從頭到尾都是那個 `2`，它的 `next` 每輪往後挪一格，最後自然指向 `5`。
**段尾接回 `right + 1` 這件事不需要特別處理**——這是頭插法最漂亮的地方。

## 另一種寫法：三段接回法

這個比較接近一般人第一次想到的樣子，也更接近「先反轉、再縫合」的直覺：

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    seg_tail = prev.next               # 段的原頭 = 反轉後的段尾
    node, before = seg_tail, None
    for _ in range(right - left + 1):  # 標準的整段反轉
        nxt = node.next
        node.next = before
        before = node
        node = nxt
    # 迴圈結束：before = 反轉後的段頭，node = 第 right+1 個節點
    prev.next = before                 # 前面接新段頭
    seg_tail.next = node               # 段尾接後面
    return dummy.next
```

兩個都是 O(n) 時間、O(1) 空間，沒有優劣之分。
頭插法行數少、不用在迴圈外做縫合；三段接回法把「整段反轉」這個可重用的動作獨立出來，
之後做「每 k 個一組反轉」（LeetCode 25）時這個結構更好擴充。

## 為什麼不要用遞迴

整段反轉用遞迴寫起來很短：

```python
def rev(node, before=None):
    if node is None:
        return before
    nxt = node.next
    node.next = before
    return rev(nxt, node)              # 尾遞迴，但 Python 不會優化它
```

Python 沒有尾呼叫優化，每一層都是真的堆疊框架，預設上限 1000 層。
20 萬個節點會直接 `RecursionError`。這就是 `curriculum.json` 把「遞迴 vs 迭代」
列進這一節技能的原因：鏈結串列的長度是資料決定的，不是你決定的，
所以凡是「走過每個節點」的遞迴在這裡都不安全。

（真正適合遞迴的鏈結串列題是那些深度有上界的，或者樹——樹的深度通常是 O(log n)。）

## 複雜度

- 時間 **O(n)**：走 `left - 1` 步找 `prev`，再搬 `right - left` 次，合起來不超過 `n`
- 空間 **O(1)**：`dummy`、`prev`、`tail`、`nxt` 四個指標，跟 `n` 無關

## 常見錯誤

1. **回傳 `head`** — `left = 1` 時 `head` 已經被搬到段的尾巴去了，回傳它只會拿到後半截。
   `reverse_between(1->2->3->4->5, 1, 5)` 這筆直接抓到：你會得到 `1 -> ...` 或是一條斷鏈。
2. **沒有假節點，自己寫 `left == 1` 的分支** — 寫得出來，但兩條路各自都要正確，
   而且兩邊都要記得改 `head`。能過測資，但下一題（合併）會讓你再寫一次同樣的分支。
3. **三行指標的順序弄亂** — 例如先寫 `prev.next = nxt` 再寫 `nxt.next = prev.next`，
   第二行就變成 `nxt.next = nxt`，鏈上立刻生出一個自環，走訪時卡死。
   寫之前先在紙上標好「拆、接後、接前」的順序。
4. **off-by-one** — 走 `left` 步而不是 `left - 1` 步，或是搬 `right - left + 1` 次而不是
   `right - left` 次。`[1,2,3,4,5]` 配 `(2, 4)` 和 `(1, 3)` 兩筆合起來很容易抓到。
5. **用值的交換代替搬節點** — 把兩端的 `val` 互換再往中間收。
   在這題上答案會對，但它需要能從兩端往中間走（鏈不行，你沒有 `prev` 指標），
   實際上你會先把值收集成 list，那就不是在練鏈結串列了。
   `orig` 那筆測資抓新建節點，而題目明說不要改 `val`。
6. **`left == right` 沒處理** — 頭插法的迴圈跑 0 次其實是對的，所以多數寫法會自然正確；
   但如果你在迴圈外做了「一定要縫合」的動作，就會把鏈接錯。

## 延伸

接下來的路線：

- **每 k 個一組反轉**（LeetCode 25）：這題的段改成一路往後切。
  用三段接回法的結構寫會順得多，而且你會發現 `dummy` 在這裡變成不可或缺。
- **判斷回文鏈**（LeetCode 234）：067 的找中點 + 這題的反轉，兩個拼起來。
  做完它你就把 2.4 的前兩題都用上了。
- **刪除排序鏈中所有重複的值**（LeetCode 82）：`dummy` 的另一個經典用途——
  第一個節點本身就可能要被刪掉。

**跟你的方向的關係**：相機軌跡在實作上常常就是一條相對位姿（relative pose）的鏈，
每個節點存「從上一幀到這一幀的變換」。把一段軌跡反向播放，
不只是把節點順序倒過來，每個變換還要換成它的逆。
順序顛倒 + 每項取逆，這正是 $(AB)^{-1} = B^{-1}A^{-1}$ 在資料結構上的樣子——
你在 051 組合線性映射時推過的那條式子。
