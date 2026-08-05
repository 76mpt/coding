# code-trainer

一套給自己用的練習系統：**自動出題 → 只給提示 → 你解出來之後才給標準解與最佳解**。

兩條平行軌道、99 個節點，從「什麼是變數」一路排到「手寫 SE(3) 指數映射」與「推導 diffusion 的損失」。

- **程式軌**（51 節點）：語法 → 演算法 → 競賽 → 工程實務 → CV/AI 實作
- **數學軌**（48 節點）：線代機率 → 最佳化訊號 → 3D/SLAM → 學習理論 → 表徵學習 → 生成模型

題目是**即時生成**的，不是固定題庫，所以不會用完也不會重複。

---

## 目錄

- [三分鐘開始](#三分鐘開始)
- [怎麼練](#怎麼練) ← 訓練流程、提示策略、兩軌怎麼分配
- [指令一覽](#指令一覽)
- [題幹大綱](#題幹大綱) ← 99 個節點的完整清單
- [數學資源對應科目](#數學資源對應科目) ← 中英文課程對照
- [為什麼答案看不到](#為什麼答案看不到)
- [檔案結構](#檔案結構)
- [在多台電腦上使用](#在多台電腦上使用)
- [出題用的 spec 格式](#出題用的-spec-格式)

---

## 三分鐘開始

```bash
cd d:\coding\code-trainer

python trainer.py doctor      # 確認環境（python / g++ / numpy）
python trainer.py status      # 看目前進度
python trainer.py open 001    # 打開第一題
```

編輯該題目錄下的 `solution.py`，寫完跑：

```bash
python trainer.py test 001
```

卡住 → `python trainer.py hint 001`　　真的要看答案 → `python trainer.py answer 001`

---

## 怎麼練

### 一次練習的標準流程

```
 ┌─ 1. sync ─────── 拿到另一台電腦的最新進度（只有一台就跳過）
 │
 ├─ 2. review ───── 有到期複習就先做，複習優先於新題
 │
 ├─ 3. next ─────── 讓系統決定該練什麼，交給 AI 教練出題
 │
 ├─ 4. open ─────── 讀題。先在腦中想清楚再動手
 │
 ├─ 5. 寫 + test ── 反覆迭代（這裡才是真正在學的地方）
 │      ↑ 卡住 → hint（一階一階來）
 │
 ├─ 6. answer ───── 通過之後才看標準解，對照自己的寫法
 │
 └─ 7. sync ─────── 把進度推上去
```

實際指令：

```bash
python trainer.py sync                  # 1
python trainer.py review                # 2
python trainer.py next                  # 3  程式軌
python trainer.py next --track math     # 3' 數學軌
python trainer.py open 007              # 4
python trainer.py test 007              # 5
python trainer.py hint 007              # 5' 卡住時
python trainer.py answer 007            # 6
python trainer.py sync                  # 7
```

### 出題交給 AI 教練

`next` 只會印出「該出什麼題」的指令，**不會自己生題目**。真正出題的是 AI 教練
（Claude Code，規則在 `.claude/skills/code-trainer/SKILL.md`）。

在 `code-trainer` 資料夾開啟 Claude Code，直接說「出下一題」或「出一題數學題」就好。
教練會照 `next` 的 brief 出題、寫測資、**跑 `verify` 確認測資無誤**，才交給你。

### 提示要怎麼用

提示分 3–4 階，**一階比一階具體**，最後一階是程式骨架但關鍵處留空。

| 階段 | 內容 | 什麼時候該按 |
|---|---|---|
| 1 | 確認你理解題目 + 指出該往哪想 | 讀完題完全沒方向，超過 10 分鐘 |
| 2 | 點出關鍵觀察（想到就會了的那件事） | 有方向但推不下去 |
| 3 | 具體策略：用什麼資料結構、為什麼對 | 知道方向但不知道怎麼落地 |
| 4 | 程式骨架，核心那一兩行留空 | 想法清楚但寫不出來 |

**按提示之前先做這件事**：把你目前的想法寫下來（哪怕只有一句「我覺得要排序但不知道排完幹嘛」）。
沒有想法就按提示，等於在看答案。

提示用量會被記錄。用了提示的題目**不會**推進間隔重複的間隔，會停在原地重來——
這是刻意的，因為「靠提示做出來」不代表你會了。

### 什麼時候可以看答案

`answer` 在你「提示還沒用完、也還沒通過」時會**先擋一次**，要加 `--yes` 才會給。

建議的判斷標準：

- ✅ **已經通過** → 一定要看。標準解裡有複雜度分析、常見錯誤、延伸應用，這是最高投報率的部分。
- ✅ **四階提示都用完，又卡了 30 分鐘以上** → 看吧，然後隔幾天 `redo` 重做一次。
- ❌ **只是懶** → 別看。看答案的當下都會覺得「我懂了」，那是錯覺。

### 通過之後要做什麼（很多人跳過這步，但這裡才是差距）

1. `python trainer.py answer <id>` 看標準解，比對自己的寫法差在哪
2. 跟 AI 教練說「**幫我 review 這份 code**」——這時它可以放開講，因為你已經解出來了
3. 問自己：**如果測資大 100 倍，我的寫法還能過嗎？**
4. 記下標準解裡「常見錯誤」那段有沒有你剛好犯過的

### 間隔重複

通過一題之後，系統依 `1 → 3 → 7 → 16 → 35 → 90` 天排下次複習。
**只有 0 提示 0 解答自力解出**的題目才會往下一個間隔前進。

```bash
python trainer.py review        # 看今天該複習什麼
python trainer.py redo 003      # 清空重寫（舊作答存到該題的 attempts/）
```

寫程式不是讀過就會，是要能在三週後空手寫出來才算會。

### 什麼叫「掌握一個節點」

每個節點有 `target`（3–5 題）。要同時滿足兩個條件才算掌握、才會前進：

1. 通過 `target` 題
2. 其中**至少一題是 0 提示 0 解答**完成的

`status` 裡的 `✓` 就是這個意思。

### 兩軌怎麼分配

**別平均分配。** 初期程式軌吃重（要先寫得出來），數學軌一週 1–2 題就好。

| 週次 | 程式軌 | 數學軌 | 搭配課程 |
|---|---|---|---|
| 1–4 | S1.1–1.5 基本功 | M0.1–M0.3 線映射、子空間、最小平方 | 3B1B 中文 → 蘇柏青線代 |
| 5–8 | S1.6–1.9 + S2.1 | M0.4–M0.6 特徵值、SVD、條件數 | MIT 18.06 |
| 9–12 | S2.2–2.5 | M0.7–M0.9 梯度、矩陣微分、貝氏 | 18.S096 + Stat 110 |
| 13+ | S2.6–2.12 | M0.10–M1.x | EE364A、EE261 |

**M0.5（SVD）是整條數學線的樞紐**——之後 M2.3 homography、M2.4 基礎矩陣、
M4.5 PCA 全都會回來用它。到那節值得多花時間。

### 數學軌的題目長什麼樣

**不是紙筆計算題**（那用紙筆就好）。每題都是「**把數學寫成程式，再用程式證明自己算對了**」：

| 節點 | 你要做的事 |
|---|---|
| M0.2 子空間與正交性 | 手寫 Gram-Schmidt，跟 `np.linalg.qr` 比對 |
| M0.7 梯度 | 用有限差分驗證自己推導的解析梯度（gradient check） |
| M0.8 矩陣微分 | 手推 softmax + cross-entropy 的反向傳播，跟 PyTorch autograd 比對 |
| M1.4 Gauss-Newton / LM | 手寫 LM 擬合非線性曲線，跟 `scipy.optimize.least_squares` 比迭代次數 |
| M2.3 Homography | 從 4 組對應點估 H 做影像 warp，比較有無資料正規化的數值差異 |
| M2.8 李群 SO(3)/SE(3) | 實作 exp/log 映射驗證往返一致，用擾動模型數值驗證解析 Jacobian |
| M3.2 集中不等式 | 用模擬驗證 Hoeffding 界的緊緻度 |
| M5.3 score matching | 1D 混合高斯上解析算 score，用 Langevin 取樣比對真實分布 |

每個節點的 `verify` 欄位就定義了驗證方式，`curriculum -v --track math` 可以全部看到。

---

## 指令一覽

| 指令 | 作用 |
|---|---|
| `status` | 進度總覽：兩軌完成度、通過題數、連續練習天數 |
| `curriculum [-v] [--track code\|math]` | 完整學習路線，`✓` 已掌握 / `~` 進行中；`-v` 顯示技能與資源 |
| `next [--track math] [--node 2.5] [--lang cpp] [--difficulty ...]` | 產生下一題的出題指令（給 AI 教練看） |
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
| `skill [--install] [--user]` | 檢視/重建 AI 教練的 skill 指標檔 |
| `sync [-m 訊息]` | 用 git 同步進度到另一台電腦 |
| `seed [--force]` | 匯入內建種子題目 |
| `new --spec <file>` | 從 spec JSON 建題（AI 教練用） |

`<id>` 可以只打前綴，例如 `001` 就會對到 `001-bmi-report`。

---

## 題幹大綱

99 個節點的完整清單。「題數」是該節點要通過幾題才算掌握。
定義在 `curriculum.json`，可以自己改。

### 程式軌

#### S1　基本功：語法與函式（Python，9 節點）
> 能把一段中文需求翻成可執行、可測試的 Python 函式。不碰演算法技巧，只練把想法寫出來。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| 1.1 | 變數、型別、數值運算 | 型別轉換、`//` 與 `%`、round 與浮點誤差、f-string | 3 |
| 1.2 | 條件判斷與迴圈 | 布林運算、range、累加器模式、巢狀迴圈、early return | 3 |
| 1.3 | 函式：參數與回傳 | 預設參數陷阱、`*args/**kwargs`、keyword-only、回傳 tuple | 3 |
| 1.4 | list / tuple / dict / set | 切片、`dict.get/setdefault`、set 運算、`sorted` 的 key、enumerate/zip | 4 |
| 1.5 | 字串處理 | split/join/strip、大小寫與 in、replace、簡單 regex、編碼 | 3 |
| 1.6 | comprehension 與函式式寫法 | list/dict/set comprehension、generator、any/all/sum、lambda | 3 |
| 1.7 | 例外處理與檔案 I/O | `with open`、try/except/else/finally、自訂例外、raise 時機、pathlib | 3 |
| 1.8 | class 與物件 | 實例 vs 類別屬性、dunder、dataclass、組合優於繼承 | 3 |
| 1.9 | 複雜度直覺 | 時間/空間複雜度、常數項、list vs set 查找、字串串接成本 | 2 |

#### S2　資料結構與演算法（Python + C++，12 節點）
> 面試與研究都要的核心。每題都要能說出複雜度，並知道最佳解為什麼最佳。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| 2.1 | 陣列與雙指標 | 對撞指標、快慢指標、滑動視窗、就地修改 | 4 |
| 2.2 | 雜湊表 | dict/unordered_map、計數、分組、前綴和+雜湊 | 4 |
| 2.3 | 堆疊與佇列 | 括號配對、單調堆疊、deque、BFS 佇列 | 3 |
| 2.4 | 鏈結串列 | dummy head、反轉、快慢指標找環、合併 | 3 |
| 2.5 | 二分搜尋 | lower/upper_bound、左閉右開、**二分答案**、旋轉陣列 | 4 |
| 2.6 | 排序與自訂比較 | sort key/comparator、穩定排序、區間排序、第 k 大 | 3 |
| 2.7 | 遞迴與回溯 | 遞迴三要素、排列組合子集、剪枝、路徑還原 | 4 |
| 2.8 | 樹與 DFS / BFS | 前中後序、層序、遞迴回傳資訊、BST、LCA | 4 |
| 2.9 | 堆積與優先佇列 | heapq/priority_queue、top-k、合併 k 序列、延遲刪除 | 3 |
| 2.10 | 圖論基礎 | 鄰接表、BFS 最短路、連通塊、拓撲排序、並查集 | 4 |
| 2.11 | 動態規劃入門 | 狀態定義、記憶化、一維/二維 DP、滾動陣列 | 5 |
| 2.12 | C++ 與 STL 上手 | vector/string、map/set、sort/lower_bound、reference、快速 I/O | 4 |

#### S3　競賽演算法（C++，9 節點）
> 在時限與記憶體限制下寫出正確又夠快的解。標準輸入輸出、大測資、卡常數。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| 3.1 | 卡時限與 I/O 優化 | sync_with_stdio、避免複製、reserve、cache 友善、估算 10⁸ | 3 |
| 3.2 | 前綴和與差分 | 一維/二維前綴和、差分陣列、區間加值、子矩陣和 | 3 |
| 3.3 | 貪心與證明 | 排序後貪心、**交換論證**、反例構造、區間排程 | 3 |
| 3.4 | 進階動態規劃 | 背包、區間 DP、bitmask DP、樹形 DP、轉移優化 | 5 |
| 3.5 | 圖論進階 | Dijkstra、Bellman-Ford、Floyd、Kruskal/Prim、Tarjan SCC | 4 |
| 3.6 | 數學與數論 | 快速冪、擴展歐幾里得、篩法、模逆元、組合數與容斥 | 4 |
| 3.7 | 字串演算法 | KMP、字串雜湊、Z-function、Trie、回文 | 3 |
| 3.8 | 進階資料結構 | BIT、線段樹、懶標記、稀疏表 RMQ、離散化 | 4 |
| 3.9 | 計算幾何入門 | 向量與叉積、點線關係、凸包、線段相交、浮點誤差 | 3 |

#### S4　軟體工程實務（Python，9 節點）
> 從「跑得出答案」到「別人敢用、半年後你自己還看得懂」。題目會像真實 ticket。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| 4.1 | 從模糊需求到介面設計 | 釐清需求、輸入輸出契約、邊界與非法輸入、命名 | 3 |
| 4.2 | 錯誤處理與防禦性設計 | 驗證與早退、例外階層、錯誤訊息、重試與超時、logging | 3 |
| 4.3 | 單元測試與 TDD | 測試命名、邊界案例設計、parametrize、fixture/mock | 3 |
| 4.4 | 重構與可讀性 | 抽函式、消除重複、降低巢狀、純函式化、測試護欄 | 3 |
| 4.5 | CLI 工具與設定 | argparse、退出碼、stdin/stdout 管線、設定檔與環境變數 | 2 |
| 4.6 | 資料格式與資料清理 | csv/json、schema 驗證、缺值策略、編碼問題、串流大檔 | 3 |
| 4.7 | 效能剖析與記憶體 | timeit/cProfile、熱點定位、generator、批次、lru_cache | 3 |
| 4.8 | 並行與非同步 | threading vs multiprocessing、GIL、Executor、asyncio、競態 | 3 |
| 4.9 | 型別註解與工具鍊 | typing 泛型、Protocol、mypy 思維、lint/format、套件化 | 2 |

#### S5　AI / Computer Vision 研究基本功（Python，12 節點）
> 把論文裡的公式變成正確、向量化、可驗證的程式。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| 5.1 | NumPy 向量化 | broadcasting、軸操作、布林遮罩、reshape/transpose、避免複製 | 5 |
| 5.2 | 線性代數實作 | 矩陣乘法語意、最小平方、SVD/特徵值用途、數值穩定性 | 3 |
| 5.3 | 機率、統計與取樣 | log-sum-exp、softmax/cross-entropy、隨機種子、分佈取樣 | 3 |
| 5.4 | 影像表示與幾何變換 | HWC vs CHW、色彩空間、雙線性內插、affine/warp、邊界 | 4 |
| 5.5 | 卷積與池化手寫 | stride/padding/dilation、**im2col**、pooling、輸出尺寸公式 | 4 |
| 5.6 | 相機模型與多視角幾何 | 齊次座標、投影矩陣、homography、RANSAC、重投影誤差 | 4 |
| 5.7 | 特徵、匹配與對齊 | 梯度與邊緣、Harris 角點、描述子匹配、ratio test、拼接 | 3 |
| 5.8 | 評估指標實作 | IoU 矩陣、**NMS**、PR 曲線、**mAP**、不平衡分類指標 | 4 |
| 5.9 | 自動微分與反向傳播 | 計算圖、chain rule、backward 實作、梯度檢查 | 4 |
| 5.10 | 訓練迴圈與資料管線 | dataset/dataloader、augmentation、LR schedule、checkpoint | 4 |
| 5.11 | 除錯與效能（PyTorch） | shape 除錯、device/dtype 錯配、梯度診斷、profiling | 4 |
| 5.12 | 從論文到程式（復現） | 公式轉張量運算、對齊符號與維度、單元測試驗證數學、消融 | 4 |

### 數學軌

#### M0　Tier 0 基礎（12 節點）
> 線代、機率、微積分三根柱子。每個概念都要能用程式驗證一次。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M0.1 | 向量、矩陣與線性映射 | 矩陣即線性映射、基底變換、行/列空間、乘法的幾何意義 | 2 |
| M0.2 | 子空間、秩與正交性 | 秩與零空間、四個基本子空間、正交補、Gram-Schmidt | 2 |
| M0.3 | 投影與最小平方 | 投影矩陣、normal equation、殘差正交性、過定方程組 | 3 |
| M0.4 | 特徵值與特徵向量 | 特徵分解、對角化、譜定理、冪迭代、正定性 | 2 |
| M0.5 | **SVD 與低秩近似** | SVD 幾何、Eckart-Young、偽逆、**用 SVD 解齊次方程** | 3 |
| M0.6 | 矩陣範數與條件數 | 範數、條件數、誤差放大、為什麼不要直接求逆 | 2 |
| M0.7 | 梯度、Jacobian 與 Hessian | 方向導數、最陡上升、Jacobian、曲率、鏈鎖律 | 3 |
| M0.8 | 矩陣微分與反向傳播 | 排版慣例、常見層的梯度、VJP、計算圖、梯度檢查 | 3 |
| M0.9 | 機率基礎與貝氏 | 條件機率、全機率、貝氏定理、條件獨立、期望變異數 | 3 |
| M0.10 | 常見分布與最大概似 | 高斯性質、MLE 推導、MAP 與正則化、log-sum-exp、共軛先驗 | 3 |
| M0.11 | KL 散度與交叉熵 | 熵、交叉熵、KL 非對稱、forward vs reverse KL、Jensen | 2 |
| M0.12 | 多變數高斯與共變異 | 共變異矩陣、馬氏距離、白化、邊緣化與條件化、不確定度橢圓 | 2 |

#### M1　Tier 1：最佳化、訊號、數值（9 節點）
> 從「會算」到「算得穩、算得快」。決定你之後能不能 debug 自己的研究 code。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M1.1 | 凸集、凸函數與凸最佳化 | 凸性判別、全域最優、常見凸函數、非凸的困難 | 2 |
| M1.2 | 梯度下降家族與收斂性 | 步長與 Lipschitz、momentum、自適應 LR、條件數的影響 | 3 |
| M1.3 | 拉格朗日對偶與 KKT | 拉格朗日函數、對偶、強弱對偶、KKT、約束轉正則化 | 2 |
| M1.4 | **非線性最小平方：GN 與 LM** | 殘差與 Jacobian、Gauss-Newton、LM 阻尼、Huber、稀疏結構 | 3 |
| M1.5 | 傅立葉級數與轉換 | 傅立葉級數、DFT、頻譜意義、FFT、複數表示 | 2 |
| M1.6 | 卷積定理與濾波 | 卷積 vs 相關、**卷積定理**、低通高通、可分離濾波器 | 3 |
| M1.7 | 取樣定理、aliasing 與金字塔 | Nyquist、aliasing、抗鋸齒、高斯/拉普拉斯金字塔 | 2 |
| M1.8 | 數值線代：QR、Cholesky、迭代法 | QR、Cholesky、共軛梯度、稀疏矩陣、分解的選擇 | 2 |
| M1.9 | 浮點誤差與病態問題 | 機器精度、災難性抵消、數值穩定改寫、log 空間、f32 vs f64 | 2 |

#### M2　Tier 2-A：3D 視覺 / SLAM / 姿態估計（10 節點，含 C++）
> 從單張影像的射影幾何，一路走到多視角的 bundle adjustment。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M2.1 | 齊次座標與射影幾何 | 齊次座標、射影平面、點線對偶、無窮遠點 | 2 |
| M2.2 | 相機模型、內外參與標定 | 針孔模型、內參 K、外參 R,t、投影矩陣 P、徑向畸變 | 3 |
| M2.3 | 單應矩陣與 DLT | homography 自由度、DLT、**資料正規化**、用 SVD 解 Ah=0 | 3 |
| M2.4 | 對極幾何、E 與 F 矩陣 | 對極約束、基礎矩陣、本質矩陣、八點法、從 E 分解 R,t | 3 |
| M2.5 | 三角測量與 PnP | 線性三角測量、重投影誤差、PnP、P3P、退化情形 | 3 |
| M2.6 | RANSAC 與穩健估計 | RANSAC 流程、**迭代次數的機率推導**、內點閾值、穩健核 | 3 |
| M2.7 | 旋轉表示 | 旋轉矩陣、Rodrigues、四元數、萬向鎖、SLERP | 3 |
| M2.8 | **李群李代數 SO(3)/SE(3)** | 群與流形、exp/log 映射、hat/vee、左右擾動、SE(3) Jacobian | 3 |
| M2.9 | 圖最佳化與 bundle adjustment | 因子圖、稀疏 Hessian、**Schur 補**、邊緣化、g2o/Ceres | 3 |
| M2.10 | EKF 與不確定度傳播 | 卡爾曼濾波、EKF 線性化、不確定度傳播、濾波 vs 最佳化 | 2 |

#### M3　Tier 2-B：學習理論 / 泛化分析（6 節點）
> 回答「為什麼模型在沒看過的資料上也能 work」。把工程做成研究的分水嶺。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M3.1 | 統計學習框架與 ERM | 真實 vs 經驗風險、ERM、可學習性、no free lunch、歸納偏置 | 2 |
| M3.2 | 集中不等式 | Markov/Chebyshev、**Hoeffding**、McDiarmid、聯集界 | 2 |
| M3.3 | VC 維與 Rademacher 複雜度 | 打散與 VC 維、成長函數、Rademacher、泛化界的形式 | 2 |
| M3.4 | 偏差-變異數與雙下降 | 偏差變異數分解、過參數化、**雙下降**、插值機制 | 2 |
| M3.5 | 最佳化的隱式正則化 | 隱式偏好、最小範數解、平坦最小值、batch size 與泛化 | 2 |
| M3.6 | NTK 與無限寬網路 | 神經正切核、懶惰訓練、寬度極限、特徵學習 vs 核機制 | 2 |

#### M4　Tier 2-C：表徵學習 / 自監督（5 節點）
> 沒有標籤要怎麼學到好的表徵，以及「好」的數學定義是什麼。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M4.1 | 資訊理論：熵與互資訊 | 熵與條件熵、互資訊、資料處理不等式、資訊瓶頸 | 3 |
| M4.2 | 對比學習的數學 | **InfoNCE**、互資訊下界推導、溫度參數、alignment/uniformity | 3 |
| M4.3 | 度量學習與嵌入幾何 | 餘弦 vs L2、球面幾何、triplet loss、難負樣本挖掘 | 2 |
| M4.4 | 維度崩塌與白化 | 完全 vs 維度崩塌、共變異的秩、白化、stop-gradient | 2 |
| M4.5 | 流形假設與降維 | 流形假設、PCA 兩種推導、t-SNE、UMAP、視覺化陷阱 | 2 |

#### M5　Tier 2-D：生成模型（6 節點）
> 從變分推論一路推到 score-based SDE 與 flow matching。數學密度最高的階段。

| 節點 | 主題 | 必考技能 | 題數 |
|---|---|---|---|
| M5.1 | 變分推論與 ELBO | ELBO 推導、重參數化、KL 項與重建項、後驗坍塌 | 3 |
| M5.2 | 隨機過程與布朗運動 | 馬可夫鏈、維納過程、隨機遊走極限、Itô 直覺、轉移核 | 2 |
| M5.3 | SDE、Fokker-Planck 與 score matching | 前向/反向 SDE、Fokker-Planck、**score function**、Langevin | 3 |
| M5.4 | Diffusion 的完整推導 | 前向加噪閉式解、反向參數化、**從 ELBO 到 simple loss**、排程 | 3 |
| M5.5 | Flow matching 與最佳傳輸 | 連續正規化流、條件流匹配、最佳傳輸、Wasserstein | 2 |
| M5.6 | 取樣器與 ODE 求解 | probability flow ODE、**DDIM**、ODE 求解器、CFG | 2 |

---

## 數學資源對應科目

執行 `python trainer.py next --track math` 或 `curriculum -v --track math` 時，
對應階段的資源會直接印出來。以下是完整對照。

**使用原則**：中文材料用來**快速理解**，英文材料用來**建立工作語言**。
論文、文件、社群全是英文，所以不能只走中文線。
建議做法：**筆記寫英文術語、解釋寫中文**（例如「SVD（奇異值分解）：把矩陣拆成旋轉→縮放→旋轉」）。

| 科目 | 對應節點 | 中文 | 英文 |
|---|---|---|---|
| **線代（直覺）** | M0.1–M0.2 | 3Blue1Brown《線性代數的本質》官方中文（bilibili） | 3Blue1Brown *Essence of Linear Algebra* |
| **線代（紮實）** | M0.1–M0.6 | **台大開放式課程 蘇柏青《線性代數》**（原生繁中，最紮實的中文線代課） | **MIT 18.06 Linear Algebra**（Gilbert Strang） |
| **矩陣方法 / ML 線代** | M0.5–M0.6、M1.8 | 《矩陣分析與應用》張賢達 | **MIT 18.065 Matrix Methods in Data Analysis, Signal Processing and ML**（Strang，對 ML 最對口） |
| **多變數微積分** | M0.7 | 台大開放式課程 朱樺《微積分》 | MIT 18.02 Multivariable Calculus |
| **矩陣微分 / 反傳** | M0.8 | 花書《深度學習》中文版（GitHub `exacity/deeplearningbook-chinese`）第 6 章 | **MIT 18.S096 Matrix Calculus for ML and Beyond**；*The Matrix Cookbook*（查表用） |
| **機率統計** | M0.9–M0.12 | **台大開放式課程 葉丙成《機率》**；浙大《概率論與數理統計》（中國大學MOOC） | **Harvard Stat 110**（Blitzstein）；MIT 6.041 |
| **ML 數學總論** | M0 全部 | 李沐《動手學深度學習》`d2l.ai/zh`（附錄數學章，每個概念都有 PyTorch 程式碼） | **《Mathematics for Machine Learning》`mml-book.github.io`（免費 PDF）** |
| **最佳化** | M1.1–M1.4 | 《凸優化》Boyd 中譯本 | **Stanford EE364A Convex Optimization I**（Boyd，影片與教科書 PDF 全免費） |
| **非線性最小平方** | M1.4、M2.9 | 高翔《視覺SLAM十四講》第 6 章 | Nocedal & Wright, *Numerical Optimization* |
| **傅立葉 / 訊號** | M1.5–M1.7 | 3Blue1Brown 傅立葉系列中文 | **Stanford EE261 The Fourier Transform and its Applications**（Osgood，YouTube 全套） |
| **數值方法** | M1.8–M1.9 | 《數值分析》各校教材 | Trefethen & Bau, *Numerical Linear Algebra* |
| **3D 視覺 / 多視角幾何** | M2.1–M2.6 | **高翔《視覺SLAM十四講》+ `gaoxiang12/slambook2`**（中文圈天花板，C++ 實作齊全）；《電腦視覺：演算法與應用》Szeliski 中譯本 | **Hartley & Zisserman, *Multiple View Geometry***（標準參考書）；**TUM Multiple View Geometry**（Cremers，YouTube） |
| **傳統 CV 原理** | M2.2、S5.4–5.7 | 《電腦視覺：演算法與應用》中譯本 | **First Principles of Computer Vision**（Shree Nayar，Columbia，YouTube） |
| **SLAM / 李群** | M2.7–M2.10 | **《視覺SLAM十四講》第 4、9、10 章**（李代數講得極清楚） | **Solà et al., *A Micro Lie Theory for State Estimation in Robotics***（arXiv）；**Cyrill Stachniss SLAM course**（Bonn，YouTube） |
| **學習理論** | M3 全部 | 李宏毅《機器學習》理論章節；花書中文版第 5 章 | **Shalev-Shwartz & Ben-David, *Understanding Machine Learning***（免費 PDF）；Mohri et al., *Foundations of ML* |
| **資訊理論** | M0.11、M4.1 | 花書中文版第 3 章 | **MacKay, *Information Theory, Inference, and Learning Algorithms***（免費 PDF + 劍橋課程影片） |
| **表徵學習 / 自監督** | M4 全部 | **李宏毅《機器學習》自監督章節**；跟李沐學AI 論文精讀（SimCLR/MoCo/CLIP/MAE） | Oord et al., *CPC*（InfoNCE 原始論文）；Wang & Isola, *Alignment and Uniformity* |
| **生成模型 / diffusion** | M5 全部 | **李宏毅《生成式AI》系列**（diffusion 中文講解最清楚的一份）；跟李沐學AI（DDPM、Stable Diffusion） | **Lilian Weng, *What are Diffusion Models?***；**Yang Song 的 score-based 系列**；Lipman et al., *Flow Matching* |
| **隨機微分方程** | M5.2–M5.3 | — | Särkkä & Solin, *Applied Stochastic Differential Equations*（免費 PDF） |
| **深度學習通論** | S5、M0.8 | **李宏毅《機器學習》/《深度學習》系列**（YouTube，繁中）；**李沐《動手學深度學習》`d2l.ai/zh`** | `d2l.ai`（英文版，同章對照）；Kevin Murphy, *Probabilistic Machine Learning*（免費 PDF） |

### 四個特別推薦

| 資源 | 為什麼 |
|---|---|
| **李宏毅（台大電機）** | 華語圈最好的 ML/DL 課程，繁中、台灣用語、不迴避數學但講得極白話。**最沒有摩擦的起點。** |
| **李沐《動手學深度學習》** | 每個數學概念後面立刻接可執行的 PyTorch 程式碼，跟這套系統的練法同構。**中英文版都有**，同章對照著看，術語自動對上。 |
| **高翔《視覺SLAM十四講》** | 走 3D/SLAM 的中文天花板。李群李代數、非線性最佳化、後端優化全講到，**每章都有可編譯的 C++**——正好接上 S2.12/S3 練的 STL。 |
| **台大開放式課程** | 唯一「原生繁體中文」的紮實數學課源（線代/機率/微積分），不是字幕翻譯。 |

### 繁簡術語對照

| 台灣 | 大陸 |
|---|---|
| 最佳化 | 优化 |
| 演算法 | 算法 |
| 資訊理論 | 信息论 |
| 機率 | 概率 |
| 矩陣 / 卷積 / 梯度下降 / 奇異值分解 | 同（技術詞高度重疊） |

---

## 為什麼答案看不到

題目的**測資、提示、參考解**都經過編碼存在 `tests.enc` / `hints.enc` / `reference.enc`，
在編輯器裡打開只會看到一串亂碼。這不是加密，只是**擋住不小心瞄到**——
沒有這道防線，你解題時眼角餘光會一直飄過去。

想作弊隨時可以 base64 解碼，但那時候就是你自己的選擇了。

---

## 檔案結構

```
code-trainer/
├── trainer.py          主程式
├── _harness.py         測試執行器（子行程呼叫，不用直接動）
├── curriculum.json     99 節點雙軌學習路線
├── seed.py             內建種子題目
├── state.json          你的進度（純文字 JSON，可以自己看）
├── config.json         本機 Python 路徑（不進版控，自動產生）
├── .claude/skills/     AI 教練規則（跟著同步）
└── problems/
    └── 006-container-with-most-water/
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

整個專案是**自足**的：沒有絕對路徑寫死在程式裡，所有狀態都在資料夾內。

### 已經設定好的狀態

repo 根目錄是 **`d:\coding`**（不是 `code-trainer`），這樣上層的
`.claude/skills/` 指標檔也會一起同步。遠端是私人 repo `https://github.com/76mpt/coding`。

```
d:\coding\                    ← repo 根目錄
├── .gitignore
├── .claude/skills/           ← 教練規則指標檔（會同步）
└── code-trainer/             ← 練習系統本體
```

### 第二台電腦怎麼接上

```bash
git clone https://github.com/76mpt/coding d:\coding
cd d:\coding\code-trainer
python trainer.py doctor                  # 自動找出這台有 numpy 的 Python
python trainer.py skill --install         # 重建指標檔（路徑不同時必做）
python trainer.py status                  # 確認進度接上了
```

`git config --global user.name/user.email` 也要在新機器上設定，否則 `sync` 的 commit 會失敗。

### 每次練習前後

```bash
python trainer.py sync
```

`pull --rebase` → `commit` → `push` 一行搞定。
**開始練之前跑一次**拿到另一台的最新進度，**練完再跑一次**推上去。

### 會同步什麼

| 同步 | 不同步（`.gitignore`） |
|---|---|
| `state.json` 進度、提示用量、複習排程 | `config.json` 本機 Python 路徑 |
| `problems/` 題目、你的作答、已解鎖的提示與解答 | `problems/*/.build/` C++ 編譯產物 |
| `problems/*/attempts/` 舊作答（看自己的進步） | `__pycache__/`、`.next_brief.json` |
| `curriculum.json`、`seed.py`、教練規則 | 編輯器設定 |

### 唯一要注意的事

**不要在兩台電腦上同時練習。** `state.json` 是一個檔案，兩邊各自改過又 push 就會衝突。
解法（`sync` 失敗時也會提示）：

```bash
git checkout --theirs state.json   # 留另一台的進度
git checkout --ours   state.json   # 留這一台的進度
git add state.json && git rebase --continue
```

### 環境需求

| 需求 | 用途 | 沒有的話 |
|---|---|---|
| Python 3.10+ | 全部 | 不能用 |
| `numpy` | S5、數學軌全部 | 那些題目會失敗 |
| `g++`（MSYS2 / MinGW / gcc） | S2.12、S3、M2.8–M2.9 | C++ 題不能編譯 |
| `git` | `sync` | 改用雲端資料夾同步 |
| `torch` | S5.9 之後、M0.8 | 少數題目會失敗 |

`trainer.py` 本身**只用標準函式庫**，不需要 `pip install` 任何東西。

**關於 Python 直譯器**：不同電腦上 `python` 可能指到不同的東西（系統 Python、venv、MSYS2…），
其中某些沒有 numpy。`trainer.py` 會自動掃描本機所有 Python、挑一個有 numpy 的來跑解答，
記在 `config.json`（不進版控）。手動指定：

```bash
python trainer.py doctor --pick C:\Python312\python.exe
$env:TRAINER_PYTHON = "C:\Python312\python.exe"      # 環境變數優先權最高
```

---

## 出題用的 spec 格式

AI 教練用 `python trainer.py new --spec <file.json>` 建題，建完**必須**跑
`python trainer.py verify <id>` 確認測資與參考解一致。

### 題目層級

| 欄位 | 必填 | 說明 |
|---|---|---|
| `title` | ✅ | 題目名稱 |
| `slug` | | 英文 id 片段，省略則由 title 產生 |
| `lang` | ✅ | `py` / `cpp` |
| `node` | ✅ | curriculum 節點 id，如 `2.1` 或 `M2.8` |
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
