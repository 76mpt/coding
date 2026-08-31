# 037-load-annotations · 壞行跳過，好行保留 — 參考解

## 標準解

```python
def load_annotations(lines: list[str]) -> tuple[list, list]:
    good, bad = [], []
    for lineno, line in enumerate(lines, 1):      # 行號從 1 開始
        if not line.strip():                      # 空白行略過
            continue
        try:
            good.append(parse_annotation(line))
        except BadAnnotation:                     # 只接自己的例外
            bad.append((lineno, line))            # 記原始內容
    return good, bad
```

六行。四個決定各佔一行，每一個都值得說明。

## 決定一：`try` 在迴圈裡面

```python
for line in lines:          for line in lines:
    try:                        ...
        ...                 # try 在外面 ← 第一個壞行就中斷整個迴圈
    except: ...
```

**`try/except` 的範圍決定了「失敗的粒度」。** 包住一行 = 一行壞掉只損失一行；
包住整個迴圈 = 一行壞掉全部停擺。

這個選擇沒有標準答案，取決於需求：批次匯入通常要「盡量救」，
轉帳交易則要「一步錯全部回滾」。**重點是它是個決定，不是預設。**

## 決定二：`except BadAnnotation` 而不是 `except Exception`

```python
except BadAnnotation:      # 只接「這行資料壞了」
except Exception:          # 連你自己的 bug 都吞掉
```

如果你把變數名打錯，`except Exception` 會把 `NameError` 也接住，然後那一行被歸類成「壞資料」。
**你會花好幾小時找一個根本不存在的資料問題。**

> **只接你知道怎麼處理的例外。** 其他的讓它往上拋——那是給你看的錯誤。

這條規則在 4.2 會反覆出現。`except Exception: pass` 是 Python 最惡名昭彰的反模式。

## 決定三：`enumerate(lines, 1)`

```python
enumerate(lines)       # 0, 1, 2, ...
enumerate(lines, 1)    # 1, 2, 3, ...
```

第二個參數是起始值。比 `i + 1` 好，因為**起點只寫一次**——用 `i+1` 的話每個用到的地方都要記得加。

人類數行號從 1 開始（編輯器、`git diff`、編譯器錯誤訊息都是）。
報告給人看的行號用 0-based 是很惱人的 bug。

## 決定四：記錄的是原始的 `line`

```python
bad.append((lineno, line))            # 原樣
bad.append((lineno, line.strip()))    # 洗過的
```

**壞行報告的用途是讓人去修那一行。** 洗過之後，「結尾多了一個 tab」「開頭有全形空白」
這類問題就看不出來了——而那正是最常見的壞行成因。

`strip()` 只用在**判斷**（是不是空白行），不改變存下來的內容。

## 為什麼空白行不算壞行

```python
if not line.strip():
    continue
```

檔案結尾通常有一個換行，讀進來就是一個空字串。標註工具也常在段落間留空行。
**把這些算成「壞行」的話，報告會被雜訊淹沒，真正的問題就找不到了。**

注意 `"   ".strip()` 是 `""`，而空字串的布林值是 False——這就是 `not line.strip()` 的原理
（truthiness，你在 021、016、026 都用過）。

## 這題真正的主題：分層

```
parse_annotation    「這行壞了，壞在哪」          ← 拋出
load_annotations    「壞了就跳過並記下來」        ← 處理
呼叫端              「壞超過 5% 就中止訓練」      ← 決策
```

**三層各司其職，而且都可以獨立替換。** 換一個呼叫端想要「一壞就中止」，
只要改 `load_annotations` 那層，`parse_annotation` 一個字都不用動。

這就是例外機制存在的理由——**它讓「發現問題的地方」和「決定怎麼辦的地方」可以分開**。
回傳錯誤碼做不到這件事（每一層都要檢查、每一層都要轉發）。

## 複雜度

時間 **O(n)**（n 是總字元數），空間 O(輸出大小)。

**Python 的 try/except 在沒有例外發生時幾乎是零成本**（零成本例外機制），
所以把 try 放在迴圈裡不會有效能問題。但**拋出**例外是貴的——大測資有 5 萬個壞行，
如果實測發現慢，那是拋例外的成本，不是 try 的成本。

（這也是為什麼「用例外控制正常流程」是反模式：例外應該是例外情況。）

## 常見錯誤

1. **`try` 包住整個迴圈** —— 第一個壞行就中斷，後面的好行全丟。測資第 6 筆（壞行在中間）專門抓。
2. **`except Exception`** —— 會過測資，但實務上會吞掉你自己的 bug。
3. **行號從 0 開始，或跳過空白行時不計數** —— 隱藏測資的 `z` 在第 5 行，如果空白行不算就會變成第 3 行。
4. **記錄 `line.strip()`** —— 隱藏測資 `'bad  line  here'` 檢查原樣保留。
5. **空白行算成壞行** —— `["   ", ""]` 應該回傳 `([], [])`。
6. **回傳 dict 而不是 list** —— 題目要兩個 list，而且順序有意義。

## 延伸

這個「**逐項處理、失敗隔離、統一報告**」的模式在資料工程裡叫 **dead letter queue**：
處理不了的東西不丟掉，放進一個獨立的佇列等人來看。

你之後會在這些地方遇到它：

| 場景 | 壞的那一筆 |
|---|---|
| **資料集載入**（5.10） | 損毀的圖片檔 → 跳過並記錄，不要讓一張壞圖擋住整個 epoch |
| **批次推論** | 某張圖 shape 不對 → 記下檔名，其他照跑 |
| **爬蟲/ETL**（4.6） | 某筆 JSON 格式錯 → 進 dead letter，不中斷整批 |

**共同點：一筆壞掉不該讓一萬筆停擺，但也不能安靜地消失。**
