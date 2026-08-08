# 028-find-image-names · 從文字中挑出影像檔名

- 階段：基本功：語法與函式 / 1.5 字串處理
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`find_images`
- 提示：共 4 階（`python trainer.py hint 028-find-image-names`）
- 測資：12 筆（`python trainer.py test 028-find-image-names`）

────────────────────────────────────────────────────────────────────

你拿到一份別人手寫的實驗筆記，裡面夾雜著影像檔名。要把它們抽出來做成清單。

實作 `find_images(text)`，回傳文字裡所有**影像檔名**，依**第一次出現的順序**。

**什麼算影像檔名**

把 `text` 用空白切成一個個「詞」，一個詞同時滿足下面兩條才算：

1. 以 `.jpg`、`.jpeg` 或 `.png` 結尾，**不分大小寫**（`.PNG`、`.JpG` 都算）。
2. 副檔名前面**至少有一個字元**當主檔名（所以 `".png"` 本身不算）。

**去重**

同一個檔名只保留**第一次**出現的那個。判斷「同一個」時**不分大小寫**——
`"a.jpg"` 和 `"A.JPG"` 視為同一個檔案（Windows 和 macOS 的檔案系統就是這樣）。

**回傳的字串要保留原始大小寫**，不要轉小寫。

**範例**

```
find_images("cat.jpg dog.PNG notes.txt")   ->  ["cat.jpg", "dog.PNG"]
find_images("a.jpg A.JPG b.png")           ->  ["a.jpg", "b.png"]
find_images("no images here")              ->  []
find_images("IMG_001.JPEG")                ->  ["IMG_001.JPEG"]
find_images(".png x.png")                  ->  ["x.png"]
```

第 2 個範例是重點：`A.JPG` 被當成 `a.jpg` 的重複而丟掉，
但留下來的是**先出現的 `a.jpg`、保持它原本的小寫**。

**限制**
- `text` 可能是空字串，這時回傳 `[]`。
- 詞與詞之間可能有多個空白、換行、tab。
- 詞裡面不會有標點符號（不用處理 `cat.jpg,` 這種結尾逗號）。
- 最多 10⁵ 個詞。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 028-find-image-names` 驗證
3. 卡住 → `python trainer.py hint 028-find-image-names`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 028-find-image-names`
