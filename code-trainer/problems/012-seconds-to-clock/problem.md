# 012-seconds-to-clock · 秒數轉時鐘格式

- 階段：基本功：語法與函式 / 1.1 變數、型別、數值運算
- 語言：Python　難度：warmup　互動方式：實作函式
- 要實作的入口：`seconds_to_clock`
- 提示：共 4 階（`python trainer.py hint 012-seconds-to-clock`）
- 測資：9 筆（`python trainer.py test 012-seconds-to-clock`）

────────────────────────────────────────────────────────────────────

實作 `seconds_to_clock(seconds)`，把秒數轉成 `HH:MM:SS` 格式的字串。

規則：
- 時、分、秒各自**至少補零到兩位數**。
- **小時不繞回**：86400 秒（一天）是 `"24:00:00"`，不是 `"00:00:00"`。
- 小時可以超過兩位數，這時就照實顯示（不要截斷）。

**範例**

```
seconds_to_clock(0)       ->  "00:00:00"
seconds_to_clock(3661)    ->  "01:01:01"     # 1 小時 1 分 1 秒
seconds_to_clock(86399)   ->  "23:59:59"
seconds_to_clock(86400)   ->  "24:00:00"     # 不繞回 00
seconds_to_clock(360000)  ->  "100:00:00"    # 小時三位數，照實顯示
```

**限制**
- `0 <= seconds <= 10^9`，是整數。
- 不需要處理負數。

**提示方向**：3600 秒是一小時，60 秒是一分鐘。你需要的是「除法的商」和「除法的餘數」。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 012-seconds-to-clock` 驗證
3. 卡住 → `python trainer.py hint 012-seconds-to-clock`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 012-seconds-to-clock`
