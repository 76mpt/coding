# code-trainer

一套給自己用的程式練習系統：**自動出題 → 只給提示 → 你解出來之後才給標準解與最佳解**。

路線從「什麼是變數」一路排到「手寫 conv2d 和 RANSAC」，共 5 個階段 51 個節點。

---

## 三分鐘開始

```bash
cd d:\coding\code-trainer

python trainer.py doctor      # 確認環境（python / g++ / numpy）
python trainer.py status      # 看目前進度
python trainer.py open 001    # 打開第一題
```

然後編輯該題目錄下的 `solution.py`，寫完跑：

```bash
python trainer.py test 001
```

卡住的時候：

```bash
python trainer.py hint 001    # 一次解鎖一階提示（共 3–4 階）
```

真的解不出來，或已經通過想看標準寫法：

```bash
python trainer.py answer 001  # 標準解 + 最佳解 + 複雜度 + 常見錯誤
```

---

## 為什麼答案看不到

題目的**測資、提示、參考解**都經過編碼存在 `tests.enc` / `hints.enc` / `reference.enc`，
在編輯器裡打開只會看到一串亂碼。這不是加密，只是**擋住不小心瞄到**——
沒有這道防線，你解題時眼角餘光會一直飄過去。

想作弊隨時可以 base64 解碼，但那時候就是你自己的選擇了。

---

## 指令一覽

| 指令 | 作用 |
|---|---|
| `status` | 進度總覽：通過題數、連續練習天數、每階段完成度 |
| `curriculum [-v]` | 完整學習路線，`✓` 已掌握 / `~` 進行中 |
| `next` | 產生下一題的出題指令（給 AI 教練看） |
| `open <id>` | 顯示題目與你目前的狀態 |
| `test <id> [--case N]` | 跑測資，`--case N` 只跑第 N 筆 |
| `hint <id> [--show]` | 解鎖下一階提示；`--show` 重看已解鎖的 |
| `answer <id> [--yes]` | 解鎖標準解（提示沒用完會先擋一次） |
| `list [--status solved] [--node 2]` | 題目清單 |
| `review` | 今天到期該複習的題目 |
| `redo <id>` | 清空重做（舊作答存到該題的 `attempts/`） |
| `log [-n 25]` | 事件時間軸 |
| `verify [<id>]` | 用參考解驗證測資（出題後自我檢查用） |
| `doctor [--pick <python>]` | 環境檢查；`--pick` 指定跑解答用的直譯器 |
| `sync [-m 訊息]` | 用 git 同步進度到另一台電腦 |
| `seed [--force]` | 匯入內建種子題目 |

`<id>` 可以只打前綴，例如 `001` 就會對到 `001-bmi-report`。

---

## 學習路線

`curriculum.json` 定義，共 51 個節點。每個節點要通過 `target` 題（3–5 題）
**且至少一題是 0 提示 0 解答自力完成**，才算掌握。

| 階段 | 內容 | 語言 | 節點數 |
|---|---|---|---|
| **S1** | 基本功：型別、迴圈、函式、容器、字串、例外、class、複雜度直覺 | Python | 9 |
| **S2** | 資料結構與演算法（LeetCode 風格）：雙指標、雜湊、樹、圖、DP、STL | Python + C++ | 12 |
| **S3** | 競賽演算法：卡時限、差分、貪心證明、進階 DP、數論、字串、線段樹、計算幾何 | C++ | 9 |
| **S4** | 軟體工程實務：介面設計、錯誤處理、測試、重構、CLI、資料清理、剖析、並行 | Python | 9 |
| **S5** | AI / CV 研究基本功：NumPy 向量化、線代、卷積手寫、相機模型、IoU/NMS/mAP、autograd、訓練迴圈、論文復現 | Python | 12 |

全部走完約 175 題。題目是**即時生成**的，不是固定題庫，所以不會用完也不會重複。

---

## 間隔重複

通過一題之後，系統會依 `1 → 3 → 7 → 16 → 35 → 90` 天的間隔排下次複習。
**只有 0 提示自力解出**的題目才會往下一個間隔前進；用了提示的會停在原地重來。

```bash
python trainer.py review        # 看今天該複習什麼
python trainer.py redo 003      # 清空重寫一次
```

寫程式不是讀過就會，是要能在三週後空手寫出來才算會。

---

## 檔案結構

```
code-trainer/
├── trainer.py          主程式
├── _harness.py         測試執行器（子行程呼叫，不用直接動）
├── curriculum.json     51 節點學習路線
├── seed.py             內建種子題目
├── state.json          你的進度（純文字 JSON，可以自己看）
└── problems/
    └── 003-container-with-most-water/
        ├── problem.md      題目
        ├── solution.py     ← 你在這裡作答
        ├── starter.txt     起始碼備份（redo 用）
        ├── meta.json       題目中繼資料
        ├── tests.enc       測資（編碼）
        ├── hints.enc       提示（編碼）
        ├── reference.enc   參考解（編碼）
        ├── verify.enc      出題者的參考實作（驗證測資用）
        ├── revealed.md     你已解鎖的提示（解鎖後才出現）
        ├── reference.md    標準解（answer 之後才出現）
        └── attempts/       redo 之前的舊作答
```

---

## 在多台電腦上使用

整個專案是**自足**的：沒有絕對路徑寫死在程式裡，所有狀態都在這個資料夾內。
把資料夾同步過去就能接著練。

### 用 git（建議）

第一台電腦，開一個**私人** repo（進度紀錄不需要公開）：

```bash
cd d:\coding\code-trainer
git init -b main
git add -A
git commit -m "初始化 code-trainer"
git remote add origin <你的私人 repo 網址>
git push -u origin main
```

第二台電腦：

```bash
git clone <你的私人 repo 網址> code-trainer
cd code-trainer
python trainer.py doctor      # 會自動找出這台機器上有 numpy 的 Python
```

之後**每次練完**在任一台電腦執行：

```bash
python trainer.py sync
```

它會 `pull --rebase` → `commit` → `push`，一行搞定。
開始練之前也跑一次，確保拿到另一台的最新進度。

### 會同步什麼

| 同步 | 不同步（`.gitignore`） |
|---|---|
| `state.json` 進度、提示用量、複習排程 | `config.json` 本機 Python 路徑 |
| `problems/` 題目、你的作答、已解鎖的提示與解答 | `problems/*/.build/` C++ 編譯產物 |
| `problems/*/attempts/` 舊作答（看自己的進步） | `__pycache__/`、`.next_brief.json` |
| `curriculum.json`、`seed.py`、教練規則 | |

### 唯一要注意的事

**不要在兩台電腦上同時練習。** `state.json` 是一個檔案，兩邊各自改過又 push
就會產生 git 衝突。解法很簡單（`sync` 失敗時它也會提示）：

```bash
git checkout --theirs state.json   # 留另一台的進度
git checkout --ours   state.json   # 留這一台的進度
git add state.json && git rebase --continue
```

養成「開始前 sync、結束後 sync」的習慣就不會遇到。

### 不想用 git

直接把整個 `code-trainer` 資料夾放進 OneDrive / Dropbox / Google Drive 也可以，
一樣要遵守「不要同時在兩台機器上練」。缺點是沒有版本歷史，
好處是不用管 git。

### 另一台電腦的環境需求

| 需求 | 用途 | 沒有的話 |
|---|---|---|
| Python 3.10+ | 全部 | 不能用 |
| `numpy` | S5（AI/CV 階段） | 只有 S5 的題目會失敗 |
| `g++`（MSYS2 / MinGW / Linux gcc） | S2.12、S3 的 C++ 題 | 只有 C++ 題不能編譯 |
| `git` | `sync` 指令 | 改用雲端資料夾同步 |

`trainer.py` 本身**只用標準函式庫**，不需要 `pip install` 任何東西。

**關於 Python 直譯器**：不同電腦上 `python` 可能指到不同的東西
（系統 Python、venv、MSYS2 內建的那個…），而其中某些沒有 numpy。
`trainer.py` 會自動掃描本機所有 Python、挑一個有 numpy 的來跑解答，
並記在 `config.json`（此檔不進版控，每台機器各自產生）。

想手動指定：

```bash
python trainer.py doctor --pick C:\Python312\python.exe
# 或用環境變數（優先權最高）
$env:TRAINER_PYTHON = "C:\Python312\python.exe"
```

### 教練規則放在哪

`.claude/skills/code-trainer/SKILL.md` 在**專案內**，所以會跟著同步。
在 `code-trainer` 資料夾開啟 Claude Code 就會自動載入。

如果你習慣在上層資料夾（例如 `d:\coding`）開啟 Claude Code，
那裡也有一份同名 skill，內容只是「去讀專案裡那份」的指標，避免兩邊規則走鐘。
換電腦時如果路徑不同，記得把那個指標檔裡的路徑改掉，或直接在專案資料夾裡開啟。

---

## 出題用的 spec 格式

AI 教練用 `python trainer.py new --spec <file.json>` 建題。欄位如下：

### 題目層級

| 欄位 | 必填 | 說明 |
|---|---|---|
| `title` | ✅ | 題目名稱 |
| `slug` | | 英文 id 片段，省略則由 title 產生 |
| `lang` | ✅ | `py` / `cpp` |
| `node` | ✅ | curriculum 節點 id，如 `2.1` |
| `mode` | | `function`（實作函式，預設 py）/ `io`（stdin→stdout，預設 cpp） |
| `entry` | function 模式 | 函式名，或 `Solution.method` |
| `difficulty` | | `warmup` / `standard` / `challenge` / `contest` |
| `statement_md` | ✅ | 題目敘述（markdown） |
| `starter` | | 起始程式碼 |
| `hints` | ✅ | 字串陣列，一階比一階具體 |
| `tests` | ✅ | 見下表 |
| `reference_md` | ✅ | 標準解 + 最佳解 + 複雜度 + 常見錯誤 |
| `verify_code` | | 參考實作原始碼，供 `verify` 驗證測資 |
| `timeout` | | 每筆測資的秒數上限，預設 10 |
| `extra_files` | | `{檔名: 內容}`，例如 C++ 的 driver |

### 測資欄位（function 模式）

| 欄位 | 說明 |
|---|---|
| `args` | 位置參數陣列 |
| `args_expr` | Python 運算式產生 args，用來生大測資（可用 `np` / `math` / `random`） |
| `kwargs` | 關鍵字參數 |
| `expected` | 期望回傳值 |
| `expected_any` | 陣列，符合任一個即通過（答案不唯一時） |
| `cmp` | `eq`(預設) / `approx` / `sorted` / `set` / `len` |
| `tol` | `approx` 的容差，預設 `1e-6` |
| `check_arg` | 改成比對呼叫後的第 N 個參數（就地修改型題目） |
| `validator` | Python 運算式，可用 `got` / `args` / `kwargs` / `np`，回傳 True 即通過 |
| `raises` | 期望拋出的例外類別名，如 `"ValueError"` |
| `max_ms` | 這筆測資的時間上限，用來逼出正確複雜度 |
| `hidden` | 失敗時不顯示期望值 |
| `note` | 隱藏測資失敗時給的線索 |

### 測資欄位（io 模式）

| 欄位 | 說明 |
|---|---|
| `stdin` | 標準輸入字串 |
| `stdin_expr` | Python 運算式產生 stdin（大測資用） |
| `stdout` | 期望輸出（比對時每行去尾空白、去頭尾空行） |
| `max_ms` / `hidden` / `note` | 同上 |

C++ 用 `g++ -std=c++20 -O2 -Wall -Wextra -Wshadow` 編譯，會顯示警告。
編譯結果快取在該題的 `.build/`。

---

## 環境

- Python 3.12（`numpy` 供 S5 使用）
- g++ 13.1（MSYS2）— C++ 題需要
- 沒有其他相依套件，`trainer.py` 只用標準函式庫

`python trainer.py doctor` 會列出實際偵測到的版本。
