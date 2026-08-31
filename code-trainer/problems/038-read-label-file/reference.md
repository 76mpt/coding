# 038-read-label-file · 讀標註檔並統計 — 參考解

## 標準解

```python
def read_label_file(path) -> tuple[dict, int]:
    counts, bad = {}, 0

    with open(path, encoding="utf-8") as f:      # 開檔不包 try
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                label, _ = parse_annotation(line)
            except BadAnnotation:                # 只接資料層級的錯
                bad += 1
                continue
            counts[label] = counts.get(label, 0) + 1

    return counts, bad
```

## 這題的核心：兩種錯誤要分層

```
檔案層級   不存在、是資料夾、沒權限、編碼壞掉
           → 往上拋。呼叫端給錯路徑，那是他要修的

資料層級   某一行格式壞掉
           → 接住並計數。這是預期會發生的，函式的職責就是處理它
```

**`try` 的範圍就是這個分層的實作。** `open()` 在 try 外面，所以它的例外直接往上；
`parse_annotation` 在 try 裡面，所以壞行被吸收。

寫成 `except Exception` 就把兩層混在一起了——路徑打錯會變成「這個檔案有 0 行好資料」，
然後你會盯著空的統計結果找半天。

> **只接你知道怎麼處理的例外。** 這是 1.7 這節最重要的一句話。

## `with` 做了什麼

```python
with open(path, encoding="utf-8") as f:
    ...                    # 不管是正常結束、return、還是拋例外
# 到這裡 f 一定已經關閉
```

`with` 是**上下文管理器**的語法糖，等價於：

```python
f = open(path, encoding="utf-8")
try:
    ...
finally:
    f.close()               # finally 保證會執行
```

**關鍵是 `finally`**——即使中途 `raise`，關檔也會發生。

沒關的檔案不會馬上出事（CPython 的參考計數會在物件消失時關掉），
但那是**實作細節**，PyPy 就不保證。而且在長時間執行的程式裡，
漏掉的控制代碼會累積到撞上作業系統上限：`OSError: [Errno 24] Too many open files`。

**那個錯誤的堆疊會指向「某個無辜的 open()」，而不是漏關的那個**——極難查。

## `encoding="utf-8"` 不是可選的

```python
open(path)                        # 用作業系統預設編碼
open(path, encoding="utf-8")      # 明確指定
```

不給的話 Python 用 `locale.getpreferredencoding()`：

| 平台 | 通常是 |
|---|---|
| Windows（繁中） | **cp950** |
| Linux / macOS | UTF-8 |

**同一份程式碼在你的機器上跑得好好的，到 CI 或同事的機器上就爛掉。**
隱藏測資有中文類別名，沒寫 encoding 的話在 Windows 上會拋 `UnicodeDecodeError`。

（Python 3.15 起預設會改成 UTF-8，但在那之前——以及為了讀舊程式碼——都要明寫。
`PYTHONUTF8=1` 環境變數可以強制，但**不要依賴環境設定**，寫在程式碼裡才可靠。）

## `for line in f` vs `f.read().splitlines()`

```python
for line in f:                     # 一次一行，記憶體 O(1)
    line = line.rstrip("\n")       # 但要自己去掉換行

for line in f.read().splitlines(): # 一次全讀進來，記憶體 O(檔案大小)
    ...                            # 換行自動處理掉
```

**檔案小就用第二種**（少一行、不會忘記 rstrip）。
**檔案可能很大就用第一種**——10 GB 的 log 檔用 `read()` 會直接 OOM。

標準解用第一種是為了示範串流讀取，那是 4.6「串流大檔」的預習。
注意 `rstrip("\n")` 而不是 `strip()`——後者會把行首的空白也吃掉，
而那可能是壞行報告需要保留的資訊（037 那題就要求原樣）。

## `path` 可以是 str 或 Path

```python
open("ann.txt")                    # str
open(Path("ann.txt"))              # pathlib.Path
```

**`open()` 兩種都吃**，不用轉換。這是 Python 的 `os.PathLike` 協定——
任何實作了 `__fspath__` 的物件都能當路徑用。

`pathlib` 相對於舊的 `os.path` 的好處：

```python
Path("data") / "train" / "ann.txt"        # 用 / 組路徑，跨平台
os.path.join("data", "train", "ann.txt")  # 舊寫法

p.stem, p.suffix, p.parent, p.exists()    # 屬性直接可用
```

你在 026 手工切過主檔名和副檔名——`Path` 的 `.stem` 和 `.suffix` 就是那件事的內建版。
**手寫過一次，你才知道它在幫你處理什麼。**

## 複雜度

時間 **O(檔案大小)**，空間 **O(相異類別數)**（用 `for line in f` 串流讀取的話）。

## 常見錯誤

1. **`except Exception` 或 `except:`** —— 會把 `OSError`、`FileNotFoundError` 也吞成「壞行」。有兩筆測資用 `raises` 檢查例外必須往上拋。
1b. **把例外類別抓得太窄** —— 「開資料夾」在 Linux 是 `IsADirectoryError`、在 **Windows 是 `PermissionError`**。想針對這種情況做事就得接它們的共同父類別 `OSError`，否則你的處理邏輯在另一個平台完全不會觸發。**這是跨平台程式最常見的一類 bug。**
2. **把 `open()` 包進 try** —— 同上。
3. **沒寫 `encoding="utf-8"`** —— 隱藏測資有中文類別名，Windows 上會炸。
4. **用 `line.strip()` 取代 `rstrip("\n")`** —— 這題看不出差別（`split()` 會處理掉頭尾空白），但養成區分的習慣：`strip()` 是「洗資料」，`rstrip("\n")` 是「去掉行尾的換行符號」，意圖不同。
5. **空檔案拋例外** —— 空檔案是合法的，回傳 `({}, 0)`。
6. **忘記 `continue`** —— 壞行計數之後如果沒 continue，會繼續執行下面的 `counts[label]`，而 `label` 還是上一行的值（或未定義）。

## 延伸

這三題（036 → 037 → 038）串成一條真實的資料載入管線：

```
parse_annotation    一行 → 結構化資料，壞了就說
load_annotations    一批行 → 好的 + 壞行報告
read_label_file     一個檔 → 統計 + 壞行數
```

**每一層只多做一件事，而且都可以單獨測試。** 這個分層方式在 4.1「從模糊需求到介面設計」
和 4.3「單元測試」會正式教——重點是**每一層的錯誤處理策略都不同**，
而那個策略應該由「誰有足夠資訊做決定」來決定，不是由「誰先發現錯誤」。

真實的 dataset 類別（5.10）會在這之上再包一層：快取、多執行緒預取、augmentation。
但最底下那三層永遠是這個樣子。
