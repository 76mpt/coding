#!/usr/bin/env python3
"""測試執行器（由 trainer.py 以子行程呼叫，不要直接用）。

用法: _harness.py <solution.py> <entry> <tests.json> <out.json> [--only N]

entry 可以是 "my_func" 或 "Solution.myMethod"。
每筆測資支援的欄位：
  args          list       位置參數
  args_expr     str        python 運算式回傳 args（用來產生大測資，可用 np/math/random）
  kwargs        dict       關鍵字參數
  expected      any        期望回傳值
  expected_any  list       任一個相符即算通過（答案不唯一時用）
  cmp           str        eq(預設) / approx / sorted / set / len
  tol           float      approx 的容差，預設 1e-6
  check_arg     int        改成比對呼叫後第 N 個參數（就地修改型題目）
  validator     str        python 運算式，可用 got / args / kwargs，回傳 True 即通過
  raises        str        期望拋出的例外類別名稱（如 "ValueError"）
  max_ms        float      這筆測資的時間上限，用來逼出向量化 / 正確複雜度
  hidden        bool       失敗時不顯示期望值
"""
from __future__ import annotations

import copy
import io
import json
import math
import random
import sys
import time
import traceback
from contextlib import redirect_stdout
from pathlib import Path

try:
    import numpy as np
except ImportError:  # numpy 是選用的
    np = None


def to_plain(v):
    """把 numpy 型別轉成純 python，方便比較與顯示。"""
    if np is not None:
        if isinstance(v, np.ndarray):
            return v.tolist()
        if isinstance(v, np.generic):
            return v.item()
    if isinstance(v, tuple):
        return [to_plain(x) for x in v]
    if isinstance(v, list):
        return [to_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: to_plain(x) for k, x in v.items()}
    return v


def load_entry(path: str, entry: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location("user_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入 {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["user_solution"] = mod
    spec.loader.exec_module(mod)

    if "." in entry:
        cls_name, meth = entry.split(".", 1)
        cls = getattr(mod, cls_name, None)
        if cls is None:
            raise AttributeError(f"solution.py 裡找不到 class {cls_name}")
        fn = getattr(cls(), meth, None)
        if fn is None:
            raise AttributeError(f"{cls_name} 裡找不到方法 {meth}")
        return fn
    fn = getattr(mod, entry, None)
    if fn is None:
        raise AttributeError(f"solution.py 裡找不到函式 {entry}()")
    if not callable(fn):
        raise TypeError(f"{entry} 不是函式")
    return fn


def approx_eq(a, b, tol: float) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol + tol * abs(b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(approx_eq(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(approx_eq(a[k], b[k], tol) for k in a)
    return a == b


def sortable(v):
    try:
        return sorted(v)
    except TypeError:
        return sorted(v, key=repr)


def matches(got, expected, case: dict) -> bool:
    kind = case.get("cmp", "eq")
    tol = case.get("tol", 1e-6)
    if kind == "approx":
        return approx_eq(got, expected, tol)
    if kind == "sorted":
        return sortable(got) == sortable(expected)
    if kind == "set":
        try:
            return set(map(repr, got)) == set(map(repr, expected))
        except TypeError:
            return False
    if kind == "len":
        return len(got) == expected
    return got == expected


def check(got, args, kwargs, case: dict) -> tuple[bool, str]:
    if case.get("validator"):
        env = {"got": got, "args": args, "kwargs": kwargs}
        if np is not None:
            env["np"] = np
        try:
            return bool(eval(case["validator"], env)), ""  # noqa: S307 出題者自己寫的檢查式
        except Exception as e:  # noqa: BLE001
            return False, f"validator 執行失敗: {e!r}"
    if "expected_any" in case:
        return any(matches(got, e, case) for e in case["expected_any"]), ""
    return matches(got, case.get("expected"), case), ""


def short(v, limit: int = 500) -> str:
    s = repr(v)
    return s if len(s) <= limit else s[: limit - 3] + "..."


def main() -> None:
    sol_path, entry, tests_path, out_path = sys.argv[1:5]
    only = None
    if "--only" in sys.argv:
        only = int(sys.argv[sys.argv.index("--only") + 1])

    tests = json.loads(Path(tests_path).read_text(encoding="utf-8"))
    results: list[dict] = []

    try:
        fn = load_entry(sol_path, entry)
    except Exception:
        Path(out_path).write_text(
            json.dumps({"results": [], "fatal": traceback.format_exc(limit=3)}),
            encoding="utf-8",
        )
        print(traceback.format_exc(limit=3), file=sys.stderr)
        sys.exit(0)

    gen_env = {"np": np, "math": math, "random": random}

    for i, case in enumerate(tests):
        if only is not None and only != i:
            results.append({"skipped": True})
            continue
        if case.get("args_expr"):
            args = eval(case["args_expr"], dict(gen_env))  # noqa: S307 出題者自己寫的產生器
        else:
            args = copy.deepcopy(case.get("args", []))
        kwargs = copy.deepcopy(case.get("kwargs", {}))
        buf = io.StringIO()
        t0 = time.perf_counter()
        raised: BaseException | None = None
        ret = None
        try:
            with redirect_stdout(buf):
                ret = fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            raised = e
        ms = (time.perf_counter() - t0) * 1000
        row: dict = {"ms": ms, "stdout": buf.getvalue()[:400]}

        want_exc = case.get("raises")
        if want_exc:
            if raised is None:
                row.update(ok=False, got_repr=f"沒有拋出例外，回傳 {short(to_plain(ret))}")
                if not case.get("hidden"):
                    row["expected_repr"] = f"應該 raise {want_exc}"
            else:
                names = [c.__name__ for c in type(raised).__mro__]
                row.update(ok=want_exc in names, got_repr=f"{type(raised).__name__}: {raised}")
                if not row["ok"] and not case.get("hidden"):
                    row["expected_repr"] = f"應該 raise {want_exc}"
            results.append(row)
            continue

        if raised is not None:
            row.update(
                ok=False,
                error="".join(
                    traceback.format_exception(type(raised), raised, raised.__traceback__, limit=2)
                ).strip()[-900:],
            )
            results.append(row)
            continue

        got = to_plain(args[case["check_arg"]]) if "check_arg" in case else to_plain(ret)
        ok, err = check(got, args, kwargs, case)
        limit_ms = case.get("max_ms")
        if ok and limit_ms and ms > limit_ms:
            ok = False
            err = f"答案正確但太慢：{ms:.0f}ms > 上限 {limit_ms:.0f}ms（複雜度或向量化要再想想）"
        row.update(ok=ok, got_repr=short(got))
        if err:
            row["error"] = err
        if not ok and not err and not case.get("hidden"):
            row["expected_repr"] = short(
                case.get("expected", case.get("expected_any", "（自訂檢查式）"))
            )
            if case.get("cmp", "eq") != "eq":
                row["expected_repr"] += f"  [比對方式 {case['cmp']}]"
        results.append(row)

    Path(out_path).write_text(
        json.dumps({"results": results}, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
