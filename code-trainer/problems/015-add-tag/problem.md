# 015-add-tag · 標籤累加器（可變預設值陷阱）

- 階段：基本功：語法與函式 / 1.3 函式：參數與回傳
- 語言：Python　難度：standard　互動方式：實作函式
- 要實作的入口：`add_tag`
- 提示：共 4 階（`python trainer.py hint 015-add-tag`）
- 測資：8 筆（`python trainer.py test 015-add-tag`）

────────────────────────────────────────────────────────────────────

實作 `add_tag(tag, tags=None)`：

- 如果**有**傳入 `tags`（一個 list），就把 `tag` 加到它後面，回傳這個 list。
- 如果**沒有**傳入 `tags`，就建立一個**新的空 list**，放入 `tag` 後回傳。

**範例**

```
add_tag("python")           ->  ["python"]
add_tag("b", ["a"])         ->  ["a", "b"]
add_tag("a", [])            ->  ["a"]
```

**這題真正在考的東西**

下面這個寫法**看起來完全正確，但是錯的**：

```python
def add_tag(tag, tags=[]):      # ← 陷阱在這裡
    tags.append(tag)
    return tags
```

連續呼叫三次會發生什麼事：

```
add_tag("python")   ->  ["python"]
add_tag("cpp")      ->  ["python", "cpp"]      ← 上一次的東西還在！
add_tag("math")     ->  ["python", "cpp", "math"]
```

測資會**連續呼叫你的函式好幾次**，每次都期望得到只有一個元素的 list。
如果你踩了這個陷阱，第二筆測資就會失敗。

**限制**
- `tag` 是字串，`tags` 是 list 或 `None`。
- 有傳入 `tags` 時，要**就地修改**它並回傳同一個 list（不要複製一份新的）。

這是 Python 面試最常考的題目之一，也是實務上真的會出事的 bug。

────────────────────────────────────────────────────────────────────

## 怎麼作答

1. 編輯 `solution.py`
2. `python trainer.py test 015-add-tag` 驗證
3. 卡住 → `python trainer.py hint 015-add-tag`（一次一階，會記錄）
4. 想看標準解/最佳解 → `python trainer.py answer 015-add-tag`
