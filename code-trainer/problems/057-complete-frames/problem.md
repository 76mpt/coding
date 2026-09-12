# 057-complete-frames · 挑出所有相機都拍到的幀

- 階段：資料結構與演算法（LeetCode 風格） / 2.2 雜湊表
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`complete_frames`
- 提示：共 4 階（`python trainer.py hint 057-complete-frames`）
- 測資：11 筆（`python trainer.py test 057-complete-frames`）

────────────────────────────────────────────────────────────────────

多相機系統把每台相機的每一幀存成一個檔案。整理資料集的第一件事，是挑出**所有相機都有拍到**的那些幀——少了任何一台，那一幀之後就沒辦法做多視角重建。

麻煩的是檔名來自不同工具、甚至是人手打的，格式很髒：

```
"cam0_000001.png"
"CAM1-1.PNG"            ← 大寫、分隔符不同、沒補零
"  cam01_000002.jpg "   ← 前後有空白；cam01 和 cam1 是同一台
"notes.txt"             ← 根本不是影像
```

實作 `complete_frames(filenames)`，回傳**所有相機都有的幀號**，由小到大排序的 list。
「所有相機」指的是**整份輸入裡出現過的每一台相機**。

**範例**

```python
complete_frames([
    "cam0_000001.png", "cam1_000001.png",
    "cam0_000002.png", "CAM1-2.JPG",
    "cam0_000003.png",
    "notes.txt",
])
->  [1, 2]
```

出現過的相機是 0 和 1。幀 1、幀 2 兩台都有（`000002` 和 `2` 是同一幀），幀 3 只有 cam0。

```python
complete_frames(["cam2_7.png", "cam2_3.png"])   ->  [3, 7]    # 只有一台相機，它拍的每一幀都算
complete_frames(["readme.md", "cam_1.png"])     ->  []        # 沒有任何合法檔名
```

**合法檔名的規則**
- 先去掉前後空白，**大小寫不分**
- 格式是 `cam<數字><分隔符><數字>.<副檔名>`，分隔符是 `_` 或 `-`，**剛好一個**
- 副檔名是 `png`、`jpg`、`jpeg` 之一
- 數字可以有前導零：`cam01` 和 `cam1` 是同一台，`000002` 和 `2` 是同一幀
- 不符合規則的檔名**整個忽略**，不要報錯

**限制**
- `0 <= len(filenames) <= 2 * 10^5`
- 同一個檔名可能重複出現，重複不影響答案
- 回傳 `list[int]`

**效能要求**：測資裡有一筆十幾萬個檔名的大測資與時間上限。
對每個幀號都回頭掃一遍整份清單是 O(n²)，會超時。

這題考的是 2.2 的「**會設計 key**」：用什麼當 dict 的 key，`"000002"` 和 `"2"` 才會自動落進同一格？

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 057-complete-frames` 驗證
3. 卡住 → `python trainer.py hint 057-complete-frames`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 057-complete-frames`
