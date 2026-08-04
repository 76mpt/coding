# 003-apply-discount · 滿額折扣結帳

- 階段：基本功：語法與函式 / 1.3 函式：參數與回傳
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`apply_discount`
- 提示：共 4 階（`python trainer.py hint 003-apply-discount`）
- 測資：8 筆（`python trainer.py test 003-apply-discount`）

────────────────────────────────────────────────────────────────────

實作結帳函式，函式簽章**必須完全長這樣**（這是這題的重點之一）：

```python
def apply_discount(prices, *, threshold=1000, rate=0.9) -> tuple[int, bool]:
```

規則：
1. 先把 `prices`（一個數字 list）加總得到小計。
2. 如果小計 **大於或等於** `threshold`，就打折：金額變成 `小計 × rate`，**四捨五入成整數**。
3. 否則不打折，金額就是小計。
4. 回傳 `(最終金額, 是否有打折)`，第一項是整數，第二項是布林值。

**範例**

```
apply_discount([100, 200, 300])                    ->  (600, False)   # 600 < 1000，不打折
apply_discount([500, 600])                         ->  (990, True)    # 1100 * 0.9 = 990
apply_discount([100, 200, 300], threshold=500)     ->  (540, True)    # 600 >= 500，600 * 0.9 = 540
apply_discount([1000], rate=0.75)                  ->  (750, True)
apply_discount([])                                 ->  (0, False)     # 空購物車
```

**關於簽章裡的那個 `*`**

參數列中間的 `*` 代表「它後面的參數只能用關鍵字傳」。也就是說：

```python
apply_discount([1000], threshold=500)   # ✅ 可以
apply_discount([1000], 500)             # ❌ 必須拋出 TypeError
```

這是 Python 的語言特性，你**不需要自己寫檢查**——只要簽章寫對，Python 會自動幫你擋。
測資裡有一筆就是在驗證這件事。

**限制**
- `prices` 可能是空 list。
- 價格都是非負數。
- 小計剛好等於 `threshold` 時**要**打折。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 003-apply-discount` 驗證
3. 卡住 → `python trainer.py hint 003-apply-discount`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 003-apply-discount`
