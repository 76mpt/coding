# 038-read-label-file · 讀標註檔並統計

- 階段：基本功：語法與函式 / 1.7 例外處理與檔案 I/O
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`read_label_file`
- 提示：共 4 階（`python trainer.py hint 038-read-label-file`）
- 測資：9 筆（`python trainer.py test 038-read-label-file`）

────────────────────────────────────────────────────────────────────

前兩題處理的是「已經在記憶體裡的字串」。這題要真的**開檔案**。

實作 `read_label_file(path)`，讀一個標註檔，回傳 `(每個類別出現幾次, 壞行數)`：

```
( {label: 次數}, 壞行數 )
```

**檔案格式**（跟 036、037 同一套）

```
cat 10 20 30 40
dog 1 2 3 4
cat 5 5 9 9
```

每行 `label x1 y1 x2 y2`。空白行略過。壞行**不中斷**，只計數。

**範例**

假設 `ann.txt` 內容是上面那三行：

```python
read_label_file("ann.txt")   ->  ({"cat": 2, "dog": 1}, 0)
```

**三個一定要處理的情況**

| 情況 | 要做什麼 |
|---|---|
| 檔案不存在 | `raise FileNotFoundError` |
| 路徑指向一個**資料夾** | 讓 `open()` 拋出的 `OSError` 往上傳 |
| 檔案存在但整個是空的 | 回傳 `({}, 0)`，不要拋例外 |

**前兩個不用你自己檢查**——`open()` 遇到這兩種情況本來就會拋例外。
你要做的是**不要把它們吞掉**：別寫一個 `except Exception` 把所有錯誤都變成「壞行」。

⚠️ **注意「開資料夾」的例外類別跟作業系統有關**：

```
Linux / macOS   IsADirectoryError
Windows         PermissionError
```

兩個都繼承自 **`OSError`**。所以測資檢查的是 `OSError`——
**這正是「不要把例外類別抓得太窄」的實例**：寫 `except IsADirectoryError` 的程式在 Windows 上不會生效。

**為什麼要用 `with open(...)`**

```python
with open(path, encoding="utf-8") as f:      # 離開區塊自動關檔
    ...
```

不用 `with` 的話，如果讀到一半拋出例外，檔案就**不會被關閉**。
少量檔案看不出問題，但一個長時間執行的程式漏掉幾千個檔案控制代碼，
就會撞到作業系統的上限（`OSError: Too many open files`）——而那時候你已經很難查是哪裡漏的了。

**編碼要明寫**

`open(path)` 不給 `encoding` 的話，Python 會用**作業系統的預設編碼**——
Windows 上通常是 cp950/cp1252，Linux 上是 UTF-8。**同一份程式在兩台機器上行為不同**，
而且中文字會直接爛掉。永遠寫 `encoding="utf-8"`。

**限制**
- `path` 是字串或 `pathlib.Path`，兩種都要能吃。
- 檔案是 UTF-8。
- 最多 10⁵ 行。
- 回傳的第一項是 dict（沒有任何好行時是空 dict）。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 038-read-label-file` 驗證
3. 卡住 → `python trainer.py hint 038-read-label-file`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 038-read-label-file`
