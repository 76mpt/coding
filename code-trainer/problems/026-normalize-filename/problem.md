# 026-normalize-filename · 正規化檔名

- 階段：基本功：語法與函式 / 1.5 字串處理
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`normalize_filename`
- 提示：共 4 階（`python trainer.py hint 026-normalize-filename`）
- 測資：11 筆（`python trainer.py test 026-normalize-filename`）

────────────────────────────────────────────────────────────────────

整理資料集的時候，影像檔名常常是別人隨手取的：大小寫混亂、有空白、有多餘的底線。
訓練前要先把它們統一成乾淨的格式，不然同一張圖在不同機器上會被當成兩個檔案。

實作 `normalize_filename(name)`，把一個檔名正規化。

**規則**（依序做）

1. 去掉頭尾的空白。
2. **只把副檔名（最後一個 `.` 之後的部分）轉小寫**，主檔名的大小寫保留。
3. 主檔名裡的空白一律換成底線 `_`。
4. 連續多個底線壓成一個。
5. 去掉主檔名頭尾的底線。

沒有 `.` 的檔名就當作「只有主檔名、沒有副檔名」，回傳時也不要加 `.`。

**範例**

```
normalize_filename("  IMG 0021.JPG  ")     ->  "IMG_0021.jpg"
normalize_filename("my___photo.PNG")       ->  "my_photo.png"
normalize_filename("_ cat  dog _.Jpeg")    ->  "cat_dog.jpeg"
normalize_filename("README")               ->  "README"
normalize_filename("a.b.TXT")              ->  "a.b.txt"
```

第 3 個範例值得看清楚：空白換成底線之後會產生 `_`、`cat`、`dog` 之間的多個底線，
壓縮和去頭尾要在那之後做。

第 5 個範例提醒你：副檔名是**最後一個** `.` 之後的部分，`a.b` 整段都是主檔名。

**限制**
- `name` 是非空字串，可能含前後空白。
- 主檔名去掉底線後保證不是空的。
- 只會出現 ASCII 字母、數字、空白、底線、點。

**特別注意邊界**：`"data.tar.GZ"` 的副檔名只有 `GZ`，主檔名是 `data.tar`，結果是 `"data.tar.gz"`。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 026-normalize-filename` 驗證
3. 卡住 → `python trainer.py hint 026-normalize-filename`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 026-normalize-filename`
