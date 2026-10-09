# 067-chain-midpoint-and-loop · 追蹤鏈的中點與迴圈 — 參考解

## 標準解

```python
def scan_chain(head):
    # 快慢指標：slow 一步，fast 兩步
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # fast 從後面追上 slow => 有環
            return (True, -1, None)

    # 迴圈正常結束 => fast 撞到底 => 沒有環
    # 而且此時 slow 正好停在索引 n // 2（證明見下）
    n = 0
    node = head
    while node is not None:
        n += 1
        node = node.next

    return (False, n, slow.val if slow is not None else None)
```

一個迴圈同時解決兩件事：環的偵測，以及中點的定位。
長度那一遍是額外的，但它跑在「已知沒有環」的前提下，所以安全。

## 為什麼快的一定會追上慢的

這是 Floyd 判圈法（龜兔賽跑）。假設環的長度是 `c`。

慢指標進入環之後，兩個指標都在環裡面了。
把它們在環上的距離（快的要再走多少步才會踩到慢的所在位置）記成 `d`，`0 <= d < c`。
每一輪快的走 2 步、慢的走 1 步，所以 **`d` 每輪恰好減少 1**。
`d` 是非負整數且嚴格遞減，所以最多 `c` 輪之後 `d = 0`，也就是兩個指標重合。

反過來說，沒有環的時候快指標單調往前，`n` 個節點最多 `n / 2` 輪就撞到 `None`，
不可能無限跑。所以這個迴圈必定終止，而終止的方式就告訴你答案。

## 為什麼 slow 停在索引 n // 2

迴圈每跑一輪，`slow` 前進 1、`fast` 前進 2。跑完 `k` 輪時 `slow` 在索引 `k`、`fast` 在索引 `2k`。
迴圈在「`fast` 或 `fast.next` 是 `None`」時停下，也就是 `2k >= n - 1` 第一次成立的時候：

- `n` 是奇數：`fast` 落在索引 `n - 1`（最後一個節點，`fast.next` 是 `None`），此時 `k = (n - 1) / 2 = n // 2`
- `n` 是偶數：`fast` 落在索引 `n`（已經是 `None`），此時 `k = n / 2 = n // 2`

兩種情況都是 `n // 2`。手走一遍（n = 4 停在索引 2、n = 5 停在索引 2）比記這段推導有用。

## 其他寫法

**用 set 記 id**（這題不要用，但值得知道長怎樣）：

```python
seen = set()
node = head
while node is not None:
    if id(node) in seen:
        return (True, -1, None)
    seen.add(id(node))
    node = node.next
```

時間一樣是 O(n)，但空間變成 O(n)。在串流資料上這是致命的——你不知道鏈有多長，
記憶體會一路長上去。快慢指標的價值就在 **O(1) 空間**。

**先收集成 list 再取中點**：

```python
vals = []
node = head
while node is not None:
    vals.append(node.val)
    node = node.next
return (False, len(vals), vals[len(vals) // 2] if vals else None)
```

在沒有環的輸入上完全正確，而且比快慢指標好讀。
但遇到有環的輸入它會無限 append 直到記憶體爆掉——這就是為什麼這題一定要先判環。

## 複雜度

- 時間 **O(n)**：快指標最多走 `n` 步（無環）或 `n + c` 步（有環），長度那一遍再 `n` 步
- 空間 **O(1)**：只有兩個指標和一個計數器，跟 `n` 無關

## 常見錯誤

1. **迴圈條件只檢查 `fast`** — 寫成 `while fast is not None:`，然後 `fast.next.next` 在 `fast.next` 是
   `None` 時爆 `AttributeError`。偶數長度的鏈（例如 `[1,2]`）立刻抓到。
2. **環的判斷放在移動之前** — 一開始 `slow is fast` 成立，第一筆測資就回傳 `(True, -1, None)`。
3. **用 `==` 比較節點** — `ListNode` 沒有定義 `__eq__`，所以 `==` 退化成身分比較，這題剛好不會錯；
   但習慣上比節點要用 `is`，因為一旦有人加了 `__eq__`（例如比 `val`），`==` 就會在兩個值相同的
   不同節點上誤判有環。`[5,5,5]` 這種測資會抓到。
4. **中點取錯邊** — 回傳索引 `(n - 1) // 2` 那個（偏左中點）。`[1,2,3,4]` 會得到 2 而不是 3。
5. **空鏈炸掉** — `slow` 是 `None` 時直接 `slow.val`。`scan_chain(None)` 這筆就是在抓這個。
6. **有環時還去數長度** — 判斷完有環卻沒有提早 `return`，接著跑 `while node is not None:` 就卡死。
   大測資的那筆有環，會直接超時。

## 延伸

同一個手法你其實已經用過一次了：**053-compact-detections** 的就地壓縮也是兩個指標不同速度地往前走。
差別只在那題的「下一個」是 `i + 1`，這題的「下一個」是 `node.next`。
資料結構換了，想法沒換——這是整個 2.4 節點要你建立的感覺。

接下來值得自己找來做的：

- **找出環的入口節點**（LeetCode 142）：重合之後把一個指標放回 `head`，兩個都改成一步一步走，
  再次重合的地方就是入口。證明只要列一條等式，很漂亮，推一次會對快慢指標有完全不同的理解。
- **判斷回文鏈**（LeetCode 234）：用中點把鏈切兩半、反轉後半、對比。
  這題的「找中點」就是那題的第一步，而「反轉」是 2.4 的下一題。

**跟你的方向的關係**：SLAM 裡的關鍵幀（keyframe）彼此串成鏈，迴圈閉合（loop closure）偵測到的
「我回到之前來過的地方」在資料結構上就是一個環。偵測迴圈、找出迴圈的入口、估計迴圈的長度，
是 pose graph 優化的前置步驟。你今天練的是它最小的那個版本。
