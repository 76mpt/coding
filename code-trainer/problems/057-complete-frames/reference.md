# 057-complete-frames · 挑出所有相機都拍到的幀 — 參考解

## 標準解

```python
def complete_frames(filenames):
    def parse(raw):
        s = raw.strip().lower()
        name, dot, ext = s.rpartition('.')          # 只切最後一個點
        if not dot or ext not in ('png', 'jpg', 'jpeg'):
            return None
        if not name.startswith('cam'):
            return None
        rest = name[3:]
        sep = '_' if '_' in rest else '-'
        cam_part, _, frame_part = rest.partition(sep)
        if not (cam_part.isdigit() and frame_part.isdigit()):
            return None
        return int(cam_part), int(frame_part)        # key 設計的關鍵：轉成 int

    all_cams = set()
    by_frame = {}                                    # 幀號 → 相機集合
    for raw in filenames:
        parsed = parse(raw)
        if parsed is None:
            continue
        cam, frame = parsed
        all_cams.add(cam)
        by_frame.setdefault(frame, set()).add(cam)
    return sorted(f for f, cams in by_frame.items() if cams == all_cams)
```

時間 O(n + F log F)，F 是不同幀號的個數（最後排序）。空間 O(F × C)，C 是相機數。

## 為什麼 key 要是 int

這題的核心不是演算法，是**資料的正規化**。

原始資料裡同一個東西有很多種寫法：`000002`、`2`、`02`。如果 key 用字串，
它們會落進三個不同的格子，你得在分組之後再想辦法合併——那很麻煩也容易漏。

**在進 dict 之前先把資料轉成「標準形式」**，所有等價的東西自然就是同一個 key。
這個原則在實務上到處都是：

- 檔名比對前先 `lower()`（Windows 不分大小寫，Linux 分，跨平台資料集常炸在這）
- 路徑比對前先 `Path(p).resolve()`
- 時間戳比對前先統一時區和單位

**key 設計得好，分組邏輯就簡單；key 設計得差，就要在後面補一堆特例。**

## 另一種寫法：regex

```python
import re

PATTERN = re.compile(r"cam(\d+)[_-](\d+)\.(?:png|jpe?g)")

def complete_frames(filenames):
    all_cams, by_frame = set(), {}
    for raw in filenames:
        m = PATTERN.fullmatch(raw.strip().lower())
        if not m:
            continue
        cam, frame = int(m.group(1)), int(m.group(2))
        all_cams.add(cam)
        by_frame.setdefault(frame, set()).add(cam)
    return sorted(f for f, cams in by_frame.items() if cams == all_cams)
```

一行 regex 取代整個 `parse`，而且規則一目了然。**格式規則越多，regex 越划算**。
注意兩件事：

- 用 `fullmatch` 不是 `match`——`match` 只檢查開頭，`cam1_2.png.bak` 會被當成合法
- regex 在迴圈外面 `compile` 一次，不要每次都重新編譯

手寫版的好處是每一條規則都是一行 if，出錯時好除錯。兩種都是實務上常見的寫法。

## 常見錯誤

1. **幀號用字串當 key**——`"000002"` 和 `"2"` 分到兩格，範例就會錯。
   更隱蔽的是最後排序：字串排序 `"10" < "2"`，隱藏測資的 `[2, 9, 10]` 會變成 `[10, 2, 9]`。

2. **用 `split('.')` 取副檔名**——`cam4_1.png.bak` 切出三段，
   如果你取 `parts[1]` 會拿到 `png`，把一個備份檔當成合法影像。`rpartition` 只切最後一個點。

3. **邊掃邊判斷完整**——掃到 `cam0_1` 和 `cam1_1` 時覺得幀 1 完整了，但後面才冒出 cam2。
   `all_cams` 一定要整份掃完才確定。

4. **用 list 存相機**——重複檔名會讓同一台相機出現兩次，`len(cams) == len(all_cams)` 就會誤判。
   用 set，而且直接比集合相等，不要比長度。

5. **`int()` 直接轉，不先檢查**——`cam6_x.png` 會丟 `ValueError`。
   題目要求不合法的忽略不報錯，所以要先 `isdigit()`，或用 try/except 包起來。

6. **忘了 strip**——`"  CAM0_1.PNG "` 的副檔名會變成 `"png "`（尾巴有空白），比對失敗。

## 延伸

多相機、多感測器資料集（KITTI、nuScenes、EuRoC）的載入程式碼，**一半以上都在做這件事**：
解析檔名或時間戳、正規化、分組、找出完整的那些樣本。演算法論文不會寫，但沒有它模型根本跑不起來。

這題是「幀號完全相同才算同一幀」。真實系統裡相機之間有時間誤差，要改成「時間戳差不到 5ms 算同一幀」——
那就是 055 時間對齊的雙指標，跟這題的雜湊分組組合起來用。

下一題的 key 會是一個 **tuple**，而且要處理負數取整的陷阱。
