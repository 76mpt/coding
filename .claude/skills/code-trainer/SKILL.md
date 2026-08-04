---
name: code-trainer
description: 程式練習教練。當使用者要練習寫程式、要出題、卡在 code-trainer 的題目、要提示、要看標準解、要 review 作答、或提到 trainer.py / 練習 / 出題 / 刷題 / LeetCode / 競賽題時使用。負責依 curriculum.json 生成題目、給階梯式提示、在使用者明確要求時才給標準解與最佳解。
---

# code-trainer 教練（指標）

這份是**指標**，不是內容。真正的教練規則放在專案裡，會跟著 git 一起同步到每台電腦：

**立刻讀取並完整遵循下面這個檔案，然後照它的指示執行：**

```
D:\coding\code-trainer\.claude\skills\code-trainer\SKILL.md
```

規則只維護那一份，避免兩邊內容走鐘。
如果專案被搬到別的路徑，在新位置執行 `python trainer.py skill --install` 重新產生這個檔案。

在讀到那份檔案之前，你只需要知道一條規則：
**不要主動給題目的答案或解法程式碼，只給提示。**
