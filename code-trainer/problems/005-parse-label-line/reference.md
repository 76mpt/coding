# 005-parse-label-line · 解析標註檔的一行 — 參考解

## 標準解

```python
def parse_label_line(line: str) -> dict:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise ValueError(f"需要 5 個欄位，得到 {len(parts)} 個：{line!r}")

    label = parts[0].lower()
    if not label:
        raise ValueError(f"類別名稱不可為空：{line!r}")

    x1, y1, x2, y2 = [int(p) for p in parts[1:]]   # int() 自己會擋非整數
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"框無效 ({x1},{y1},{x2},{y2})：{line!r}")

    return {"label": label, "box": [x1, y1, x2, y2]}
```

O(len(line)) 時間、O(1) 額外空間。

結構就是三段 **guard clause** 之後回傳——所有驗證都在前面擋掉，主邏輯不用巢狀。

## 為什麼不自己檢查「是不是整數」

新手常寫：

```python
if not parts[1].isdigit():            # ❌ 三個問題
    raise ValueError(...)
```

1. `"-5".isdigit()` 是 **False**，負座標會被誤判成錯誤。
2. `"１２３".isdigit()` 是 **True**（全形數字），但 `int()` 也能處理，白檢查了。
3. 你重複實作了 `int()` 已經做對的事，而且做得比較差。

**讓專門的函式自己拋錯**，這是 Python 的 EAFP 風格
（Easier to Ask Forgiveness than Permission，先做再說、錯了再處理），
對照的是 LBYL（Look Before You Leap，先檢查再做）。

只有在需要**更好的錯誤訊息**時，才值得包一層：

```python
try:
    x1, y1, x2, y2 = [int(p) for p in parts[1:]]
except ValueError as e:
    raise ValueError(f"座標必須是整數：{line!r}") from e
```

`from e` 會保留原始例外的 traceback（顯示成「The above exception was the direct cause of...」），
除錯時能同時看到「我的訊息」和「真正壞在哪」。**包裝例外時一定要加 `from e`**。

## 實務版：一次處理整個檔案

單行解析只是零件，真實情境長這樣：

```python
from pathlib import Path

def load_labels(path: Path) -> tuple[list[dict], list[tuple[int, str]]]:
    boxes, errors = [], []
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.strip()
            if not raw or raw.startswith("#"):     # 跳過空行與註解
                continue
            try:
                boxes.append(parse_label_line(raw))
            except ValueError as e:
                errors.append((lineno, str(e)))
    return boxes, errors
```

三個實務重點：

1. **行號**（`enumerate(f, start=1)`）— 沒有行號的錯誤訊息在幾萬行的檔案裡沒有用。
2. **收集錯誤而不是第一個就中斷** — 一次跑完看到全部 37 個壞行，
   比修一個跑一次修 37 次快得多。
3. **`encoding="utf-8"`** — Windows 上不指定會用系統預設編碼（cp950），
   遇到中文標註直接爆炸。**開檔一律明寫 encoding**。

## 常見錯誤

1. **忘記 `.strip()`** — `"cat, 12".split(",")` 得到 `["cat", " 12"]`，
   注意前面那個空格。`int(" 12")` 剛好可以（int 會自己忽略空白），
   但 `label` 就會變成 `" dog"` 而不是 `"dog"`，測資不會過。
2. **用 `isdigit()` 檢查** — 見上，負數會壞。
3. **先取 `parts[0]` 再檢查長度** — 如果 `line` 是空字串，`split` 得到 `[""]`，
   長度 1，但你已經先摸了 `parts[1]` 就會 IndexError（型別是 IndexError 不是 ValueError，測資不過）。
   **順序很重要：先檢查長度，再存取元素。**
4. **回傳 None 或印訊息取代 raise** — 呼叫端無法區分「解析失敗」和「這行沒有框」。
   拋例外才能強迫呼叫端做決定。
5. **框無效用 `<` 而不是 `<=`** — 寬度為 0 的框（`x1 == x2`）在後續計算 IoU 時
   面積是 0，會產生 0/0。這種退化框必須擋掉，這也是隱藏測資在測的。

## 延伸

真實的標註格式還有幾種，之後會遇到：

- **YOLO**：`class_id cx cy w h`，而且座標是**正規化到 0–1** 的相對值
- **COCO**：JSON，box 是 `[x, y, width, height]`（左上角 + 寬高，不是兩個角）
- **Pascal VOC**：XML，`xmin/ymin/xmax/ymax`

**格式轉換時最常見的 bug 就是搞混 `[x1,y1,x2,y2]` 和 `[x,y,w,h]`**——
兩者的前兩項一樣，所以錯了不會爆炸，只會讓框畫在奇怪的位置、mAP 莫名其妙很低。
養成習慣：函式名或變數名裡就標明格式，例如 `box_xyxy`、`box_xywh`。

節點 4.6 會練完整的資料清理管線，節點 5.8 會用這裡解析出來的框去算 IoU 和 mAP。
