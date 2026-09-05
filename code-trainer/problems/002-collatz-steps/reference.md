# 002-collatz-steps · Collatz 序列的步數與峰值 — 參考解

## 標準解

```python
def collatz(n: int) -> tuple[int, int]:
    steps = 0
    largest = n              # 起點本身也要納入比較

    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        largest = max(largest, n)
        steps += 1

    return steps, largest
```

這是「累加器模式」的教科書範例：迴圈外初始化，迴圈內更新，迴圈後回傳。
`steps` 累加次數、`largest` 累積最大值，兩個各自獨立。

## 更精簡的寫法

```python
def collatz(n: int) -> tuple[int, int]:
    steps, largest = 0, n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        largest = max(largest, n)
        steps += 1
    return steps, largest
```

`n = A if 條件 else B` 是條件運算式（其他語言叫三元運算子）。
只在「兩個分支都只是給同一個變數賦值」時才用它——否則 `if/else` 更清楚。

## 位元運算版（競賽風格，看看就好）

```python
def collatz(n: int) -> tuple[int, int]:
    steps, largest = 0, n
    while n != 1:
        n = n >> 1 if n & 1 == 0 else 3 * n + 1
        if n > largest:
            largest = n
        steps += 1
    return steps, largest
```

`n & 1` 取最低位元判斷奇偶，`n >> 1` 右移一位等於除以 2。
在 C++ 競賽裡這會快一些；在 Python 裡差異很小，可讀性反而更差。
**知道有這種寫法**比**用它**重要——你之後讀別人的競賽 code 會常看到。

## 複雜度

時間 O(k)，k 是序列長度。k 沒有已知的上界公式（這正是 Collatz 猜想未解的部分），
但實務上對 n ≤ 10^6，k 最多幾百步。空間 O(1)——只用了兩個變數。

留意：**用 O(1) 空間是刻意的**。如果你為了求最大值先把整條序列存進 list 再 `max(seq)`，
答案一樣對，但空間變成 O(k)。當題目只需要「彙總結果」而不需要「完整過程」時，
邊走邊算是更好的習慣——這個直覺在處理大資料集時會救你一命。

## 常見錯誤

1. **用 `/` 而不是 `//`** — 最容易踩的坑。`n / 2` 讓 n 變成 float，
   之後 `n != 1` 比的是 `1.0 != 1`（這其實是 False，所以還會停），
   但回傳的最大值會變成 `16.0` 而不是 `16`，測資就不過。
2. **最大值初始化成 0 或 1** — 那 `collatz(1)` 會回傳 `(0, 1)` 剛好碰對，
   但如果初始化成 0 而 n 一路遞減，答案就錯了。初始值設成 `n` 最安全。
3. **在更新 n 之前才更新 largest** — 會漏掉最後一步產生的值。
   不過因為序列最後一定收在 1（最小值），這題碰巧看不出差別。
   養成習慣：**先產生新值，再拿新值去更新彙總量**。
4. **步數多算或少算一次** — 把 `steps += 1` 放在 `while` 迴圈外面或條件判斷裡。
   最可靠的檢查法：拿 `n = 2`（答案是 1 步）和 `n = 1`（答案是 0 步）手動跑一遍。

## 延伸

如果要算「1 到 10^6 之間，哪個起點的步數最多」，直接對每個 n 各跑一次是 O(n·k)，會很慢。
正確做法是**記憶化**：把算過的 n 對應的步數存起來，遇到算過的就直接查表。
這是動態規劃的雛形，你在節點 2.11 會正式學到。
