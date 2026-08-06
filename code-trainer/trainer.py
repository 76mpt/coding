#!/usr/bin/env python3
"""code-trainer — 自動出題 / 階梯式提示 / 標準解與最佳解的程式練習系統。

設計原則
  1. 題目、測資、提示、參考解都經過編碼存放，你在編輯器裡看不到答案。
  2. 提示只能一階一階解鎖（hint），參考解必須明確要求（answer）才會出現。
  3. 進度、遺忘曲線複習排程都存在 state.json，教練 agent 靠 `next` 決定下一題出什麼。

常用指令
  python trainer.py status              # 進度總覽
  python trainer.py next                # 產生「下一題出題指令」給 AI 教練
  python trainer.py open <id>           # 看題目
  python trainer.py test <id>           # 跑測資
  python trainer.py hint <id>           # 解鎖下一個提示
  python trainer.py answer <id>         # 解鎖標準解 / 最佳解
  python trainer.py review              # 今天該複習的題目
  python trainer.py redo <id>           # 重做（保留舊作答，還原成空白）
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"
STATE_PATH = ROOT / "state.json"
CURRICULUM_PATH = ROOT / "curriculum.json"
HARNESS = ROOT / "_harness.py"
BRIEF_PATH = ROOT / ".next_brief.json"
CONFIG_PATH = ROOT / "config.json"  # 本機專屬設定，不進版控

REVIEW_INTERVALS_DAYS = [1, 3, 7, 16, 35, 90]
LANG_FILE = {"py": "solution.py", "cpp": "solution.cpp"}
CPP_STD = "c++20"
DEFAULT_TIMEOUT = 10.0

# ---------------------------------------------------------------- utilities


def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat()


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s)


def enc(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def dec(blob: str) -> str:
    return base64.b64decode(blob.encode("ascii")).decode("utf-8")


def write_enc(path: Path, payload) -> None:
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    path.write_text(
        "# code-trainer: 這是刻意編碼過的內容，請用 trainer.py 指令解鎖，不要手動解碼。\n"
        + enc(text)
        + "\n",
        encoding="utf-8",
    )


def read_enc(path: Path):
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    blob = "".join(ln for ln in lines if ln and not ln.startswith("#"))
    return dec(blob)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:40]


def die(msg: str, code: int = 1):
    print(f"✗ {msg}")
    sys.exit(code)


def hr(title: str = "", width: int = 68) -> str:
    if not title:
        return "─" * width
    pad = max(0, width - len(title) - 3)
    return f"── {title} " + "─" * pad


# ---------------------------------------------------------------- state


def default_state() -> dict:
    return {
        "version": 1,
        "created": iso(now()),
        "problems": {},
        "topics": {},
        "log": [],
        "counter": 0,
    }


def load_state() -> dict:
    if not STATE_PATH.exists():
        return default_state()
    st = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    for key, val in default_state().items():
        st.setdefault(key, val)
    return st


def save_state(st: dict) -> None:
    STATE_PATH.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def log_event(st: dict, event: str, pid: str = "", **detail) -> None:
    st["log"].append({"ts": iso(now()), "event": event, "id": pid, **detail})
    st["log"] = st["log"][-500:]


def topic_stats(st: dict, node: str) -> dict:
    t = st["topics"].setdefault(
        node, {"attempted": 0, "solved": 0, "clean_solved": 0, "hints_used": 0}
    )
    return t


# ---------------------------------------------------------------- 本機設定
# 不同電腦上「python」指到的直譯器可能不一樣（系統 Python、venv、MSYS2…），
# 而 S5 的題目需要 numpy。這裡自動挑一個能用的並記在 config.json（該檔不進版控）。


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def can_import(exe: str, module: str) -> bool:
    try:
        return subprocess.run(
            [exe, "-c", f"import {module}"], capture_output=True, timeout=60
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def python_candidates() -> list[str]:
    found = [sys.executable]
    for name in ("python", "python3"):
        w = shutil.which(name)
        if w:
            found.append(w)
    try:
        listing = subprocess.run(
            ["py", "-0p"], capture_output=True, text=True, timeout=30
        ).stdout
        found += re.findall(r"[A-Za-z]:\\[^\r\n]*?python\.exe", listing)
    except (OSError, subprocess.SubprocessError):
        pass
    seen, out = set(), []
    for exe in found:
        key = os.path.normcase(exe)
        if key not in seen and Path(exe).exists():
            seen.add(key)
            out.append(exe)
    return out


def solution_python(quiet: bool = False) -> str:
    """挑一個用來執行 Python 解答的直譯器，優先選有 numpy 的。"""
    env = os.environ.get("TRAINER_PYTHON")
    if env:
        return env

    cfg = load_config()
    chosen = cfg.get("python")
    if chosen and Path(chosen).exists():
        return chosen

    for exe in python_candidates():
        if can_import(exe, "numpy"):
            cfg["python"] = exe
            save_config(cfg)
            if not quiet:
                print(f"ℹ 已選用有 numpy 的 Python：{exe}\n  （記在 config.json，"
                      f"要換用 `python trainer.py doctor --pick <路徑>`）\n")
            return exe

    if not quiet:
        print("⚠ 找不到裝了 numpy 的 Python，S5 的題目會失敗。\n"
              "  安裝方式：python -m pip install numpy\n")
    return sys.executable


def load_curriculum() -> dict:
    if not CURRICULUM_PATH.exists():
        die("找不到 curriculum.json")
    return json.loads(CURRICULUM_PATH.read_text(encoding="utf-8"))


def all_nodes(cur: dict, track: str | None = None) -> list[dict]:
    out = []
    for stage in cur["stages"]:
        if track and stage.get("track", "code") != track:
            continue
        for node in stage["nodes"]:
            out.append({**node, "stage_id": stage["id"], "stage_name": stage["name"],
                        "stage_lang": stage.get("lang", ["py"]),
                        "track": stage.get("track", "code"),
                        "resources": stage.get("resources", {})})
    return out


def find_node(cur: dict, node_id: str) -> dict | None:
    for n in all_nodes(cur):
        if n["id"] == node_id:
            return n
    return None


def is_mastered(node: dict, stats: dict) -> bool:
    target = node.get("target", 3)
    return stats["solved"] >= target and stats["clean_solved"] >= 1


# ---------------------------------------------------------------- problems


def problem_dir(pid: str) -> Path:
    d = PROBLEMS / pid
    if d.is_dir():
        return d
    matches = sorted(p for p in PROBLEMS.glob(f"*{pid}*") if p.is_dir())
    if len(matches) == 1:
        return matches[0]
    if not matches:
        die(f"找不到題目 '{pid}'（用 `python trainer.py list` 看清單）")
    die("題目 id 不明確: " + ", ".join(p.name for p in matches))


def load_meta(d: Path) -> dict:
    return json.loads((d / "meta.json").read_text(encoding="utf-8"))


def prob_state(st: dict, pid: str) -> dict:
    return st["problems"].setdefault(
        pid,
        {
            "status": "open",
            "attempts": 0,
            "hints_revealed": 0,
            "answer_unlocked": False,
            "ever_unlocked": False,
            "rep": 0,
            "first_seen": iso(now()),
        },
    )


# ---------------------------------------------------------------- create


SPEC_REQUIRED = ["title", "lang", "node", "statement_md", "hints", "tests", "reference_md"]


def cmd_new(args):
    spec_path = Path(args.spec)
    if not spec_path.exists():
        die(f"找不到 spec: {spec_path}")
    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    specs = payload if isinstance(payload, list) else [payload]
    created = []
    for spec in specs:
        pid = create_problem(spec)
        created.append(pid)
        print(f"✓ {pid}   [{spec['node']}] {spec['title']}")
    if len(created) == 1:
        pid = created[0]
        print(f"\n  題目：python trainer.py open {pid}")
        print(f"  作答檔：{(problem_dir(pid) / LANG_FILE[specs[0]['lang']]).as_posix()}")
    else:
        print(f"\n共建立 {len(created)} 題。記得驗證：python trainer.py verify")


def create_problem(spec: dict, quiet: bool = False) -> str:
    missing = [k for k in SPEC_REQUIRED if k not in spec]
    if missing:
        die("spec 缺少欄位: " + ", ".join(missing))
    lang = spec["lang"]
    if lang not in LANG_FILE:
        die(f"lang 只支援 {list(LANG_FILE)}")
    mode = spec.get("mode") or ("function" if lang == "py" else "io")
    if mode == "function" and not spec.get("entry"):
        die("function 模式需要 entry（函式名，或 Class.method）")

    st = load_state()
    st["counter"] = st.get("counter", 0) + 1
    num = st["counter"]
    slug = spec.get("slug") or slugify(spec["title"]) or f"{spec['node'].replace('.', '-')}-{lang}"
    pid = f"{num:03d}-{slug}"
    d = PROBLEMS / pid
    if d.exists():
        die(f"{pid} 已存在")
    d.mkdir(parents=True)

    meta = {
        "id": pid,
        "title": spec["title"],
        "lang": lang,
        "mode": mode,
        "entry": spec.get("entry", ""),
        "node": spec["node"],
        "difficulty": spec.get("difficulty", "standard"),
        "tags": spec.get("tags", []),
        "hint_count": len(spec["hints"]),
        "test_count": len(spec["tests"]),
        "timeout": spec.get("timeout", DEFAULT_TIMEOUT),
        "source_style": spec.get("source_style", "leetcode"),
        "created": iso(now()),
    }
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    cur = load_curriculum()
    node = find_node(cur, spec["node"]) or {"name": spec["node"], "stage_name": "?"}
    header = [
        f"# {pid} · {spec['title']}",
        "",
        f"- 階段：{node.get('stage_name', '?')} / {spec['node']} {node.get('name', '')}",
        f"- 語言：{'Python' if lang == 'py' else 'C++'}　難度：{meta['difficulty']}"
        f"　互動方式：{'實作函式' if mode == 'function' else '標準輸入 / 標準輸出'}",
    ]
    if mode == "function":
        header.append(f"- 要實作的入口：`{meta['entry']}`")
    header += [
        f"- 提示：共 {len(spec['hints'])} 階（`python trainer.py hint {pid}`）",
        f"- 測資：{len(spec['tests'])} 筆（`python trainer.py test {pid}`）",
        "",
        hr(),
        "",
        spec["statement_md"].strip(),
        "",
        hr(),
        "",
        "## 怎麼作答",
        "",
        f"1. 編輯 `{LANG_FILE[lang]}`",
        f"2. `python trainer.py test {pid}` 驗證",
        f"3. 卡住 → `python trainer.py hint {pid}`（一次一階，會記錄）",
        f"4. 想看標準解/最佳解 → `python trainer.py answer {pid}`",
        "",
    ]
    (d / "problem.md").write_text("\n".join(header), encoding="utf-8")

    starter = spec.get("starter") or default_starter(lang, mode, meta["entry"])
    (d / LANG_FILE[lang]).write_text(starter.rstrip() + "\n", encoding="utf-8")
    (d / "starter.txt").write_text(starter.rstrip() + "\n", encoding="utf-8")

    write_enc(d / "tests.enc", spec["tests"])
    write_enc(d / "hints.enc", spec["hints"])
    write_enc(d / "reference.enc", spec["reference_md"])
    if spec.get("verify_code"):
        write_enc(d / "verify.enc", spec["verify_code"])
    for name, code in (spec.get("extra_files") or {}).items():
        (d / name).write_text(code, encoding="utf-8")

    ps = prob_state(st, pid)
    ps["node"] = spec["node"]
    topic_stats(st, spec["node"])
    log_event(st, "created", pid, node=spec["node"], lang=lang, difficulty=meta["difficulty"])
    save_state(st)
    return pid


def default_starter(lang: str, mode: str, entry: str) -> str:
    if lang == "py" and mode == "function":
        name = entry.split(".")[-1]
        return f"def {name}():\n    # TODO: 你的實作\n    pass\n"
    if lang == "py":
        return "import sys\n\n\ndef main() -> None:\n    data = sys.stdin.read().split()\n    # TODO\n\n\nmain()\n"
    return (
        "#include <bits/stdc++.h>\nusing namespace std;\n\n"
        "int main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n"
        "    // TODO\n    return 0;\n}\n"
    )


# ---------------------------------------------------------------- running


def run_py_function(d: Path, meta: dict, tests: list, only: int | None):
    sol = d / "solution.py"
    with tempfile.TemporaryDirectory() as tmp:
        tpath = Path(tmp) / "tests.json"
        opath = Path(tmp) / "out.json"
        tpath.write_text(json.dumps(tests, ensure_ascii=False), encoding="utf-8")
        cmd = [solution_python(), str(HARNESS), str(sol), meta["entry"], str(tpath), str(opath)]
        if only is not None:
            cmd += ["--only", str(only)]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=meta.get("timeout", DEFAULT_TIMEOUT) * max(1, len(tests)),
            )
        except subprocess.TimeoutExpired:
            return None, "整體執行超時（可能有無窮迴圈，或複雜度太高）"
        if not opath.exists():
            return None, (proc.stderr or proc.stdout or "harness 沒有輸出").strip()[-2000:]
        return json.loads(opath.read_text(encoding="utf-8")), None


def compile_cpp(d: Path) -> tuple[Path | None, str]:
    srcs = sorted(p for p in d.glob("*.cpp"))
    if not srcs:
        return None, "找不到 .cpp 檔"
    gpp = shutil.which("g++")
    if not gpp:
        return None, "找不到 g++（請安裝 MSYS2 / MinGW 並加入 PATH）"
    key = hashlib.sha1(
        ("|".join(f"{p.name}:{p.stat().st_mtime_ns}" for p in srcs)).encode()
    ).hexdigest()[:12]
    build = d / ".build"
    build.mkdir(exist_ok=True)
    exe = build / f"sol-{key}.exe"
    if exe.exists():
        return exe, ""
    for old in build.glob("sol-*.exe"):
        try:
            old.unlink()
        except OSError:
            pass
    proc = subprocess.run(
        [gpp, f"-std={CPP_STD}", "-O2", "-Wall", "-Wextra", "-Wshadow",
         *[str(p) for p in srcs], "-o", str(exe)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        return None, "編譯失敗：\n" + (proc.stderr or proc.stdout)[-3000:]
    warn = proc.stderr.strip()
    return exe, ("編譯警告：\n" + warn[-1500:] if warn else "")


def run_io(d: Path, meta: dict, tests: list, only: int | None):
    if meta["lang"] == "cpp":
        exe, msg = compile_cpp(d)
        if exe is None:
            return None, msg
        cmd = [str(exe)]
        if msg:
            print(f"⚠ {msg}\n")
    else:
        cmd = [solution_python(), str(d / "solution.py")]
    results = []
    for i, case in enumerate(tests):
        if only is not None and only != i:
            results.append({"skipped": True})
            continue
        stdin = case["stdin"] if "stdin" in case else eval(  # noqa: S307 出題者自己寫的產生器
            case["stdin_expr"], {"random": __import__("random"), "math": __import__("math")}
        )
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd, input=stdin, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=meta.get("timeout", DEFAULT_TIMEOUT),
            )
        except subprocess.TimeoutExpired:
            results.append({"ok": False, "error": "TLE 執行超時", "ms": None})
            continue
        ms = (time.perf_counter() - t0) * 1000
        if proc.returncode != 0:
            results.append({
                "ok": False, "ms": ms,
                "error": f"非零結束碼 {proc.returncode}\n{(proc.stderr or '').strip()[-800:]}",
            })
            continue
        got = normalize_out(proc.stdout)
        want = normalize_out(case.get("stdout", ""))
        ok = got == want
        row = {"ok": ok, "ms": ms, "got_repr": proc.stdout.strip()[:800],
               "expected_repr": case.get("stdout", "").strip()[:800]}
        limit_ms = case.get("max_ms")
        if ok and limit_ms and ms > limit_ms:
            row["ok"] = False
            row["error"] = f"答案正確但太慢：{ms:.0f}ms > 上限 {limit_ms:.0f}ms"
        results.append(row)
    return {"results": results}, None


def normalize_out(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def case_label(case: dict, mode: str, idx: int) -> str:
    if case.get("args_expr") or case.get("stdin_expr"):
        tag = "大測資"
        if case.get("max_ms"):
            tag += f"（時限 {case['max_ms']:.0f}ms）"
        return f"#{idx + 1} {tag}"
    if case.get("hidden"):
        return f"#{idx + 1} 隱藏測資"
    if mode == "function":
        args = case.get("args", [])
        text = ", ".join(short_repr(a) for a in args)
        if case.get("kwargs"):
            text += ", " + ", ".join(f"{k}={short_repr(v)}" for k, v in case["kwargs"].items())
        return f"#{idx + 1} ({text})"
    return f"#{idx + 1} stdin={short_repr(case.get('stdin', ''))}"


def short_repr(v, limit: int = 60) -> str:
    s = repr(v)
    return s if len(s) <= limit else s[: limit - 3] + "..."


def cmd_test(args):
    d = problem_dir(args.id)
    meta = load_meta(d)
    pid = meta["id"]
    tests = json.loads(read_enc(d / "tests.enc"))
    st = load_state()
    ps = prob_state(st, pid)
    ps["node"] = meta["node"]

    only = args.case - 1 if args.case else None
    if meta["mode"] == "function" and meta["lang"] == "py":
        out, err = run_py_function(d, meta, tests, only)
    else:
        out, err = run_io(d, meta, tests, only)

    ps["attempts"] += 1
    tstats = topic_stats(st, meta["node"])

    if err:
        print(hr(f"{pid} · 無法執行"))
        print(err)
        log_event(st, "test_error", pid)
        save_state(st)
        print("\n提示：把上面的錯誤貼給 AI 教練，它只會幫你理解錯誤、不會給答案。")
        return

    if out.get("fatal"):
        print(hr(f"{pid} · 你的程式載入失敗"))
        print(out["fatal"])
        log_event(st, "test_error", pid)
        save_state(st)
        return

    results = out["results"]
    ran = [(i, c, r) for i, (c, r) in enumerate(zip(tests, results)) if not r.get("skipped")]
    passed = [x for x in ran if x[2].get("ok")]
    failed = [x for x in ran if not x[2].get("ok")]

    print(hr(f"{pid} · {len(passed)}/{len(ran)} 通過"))
    for i, case, r in ran:
        mark = "✓" if r.get("ok") else "✗"
        ms = f"{r['ms']:.1f}ms" if r.get("ms") is not None else "  --  "
        print(f" {mark} {ms:>9}  {case_label(case, meta['mode'], i)}")

    if failed:
        i, case, r = failed[0]
        print("\n" + hr("第一個失敗的測資"))
        print(f"測資 {case_label(case, meta['mode'], i)}")
        if r.get("error"):
            print(f"  錯誤：{r['error']}")
        else:
            if case.get("hidden"):
                print("  （隱藏測資：不顯示期望輸出，通常是效能或邊界情況）")
                if case.get("note"):
                    print(f"  線索：{case['note']}")
            else:
                print(f"  期望：{r.get('expected_repr', short_repr(case.get('expected')))}")
                print(f"  實際：{r.get('got_repr', '')}")
        if r.get("stdout"):
            print(f"  你的 print 輸出：{r['stdout'][:400]}")
        if len(failed) > 1:
            print(f"\n還有 {len(failed) - 1} 筆失敗。")
        tstats["attempted"] = tstats.get("attempted", 0) + (1 if ps["attempts"] == 1 else 0)
        log_event(st, "test_fail", pid, passed=len(passed), total=len(ran))
        save_state(st)
        print("\n下一步：")
        print(f"  想自己想 → 再改 {LANG_FILE[meta['lang']]}")
        print(f"  卡住     → python trainer.py hint {pid}")
        print("  想討論   → 跟 AI 教練說「我卡在這裡」並貼上你的想法（它只會給提示）")
        return

    if only is not None:
        print("\n（只跑了單一測資，跑完整測資才會計入通過）")
        save_state(st)
        return

    first_solve = ps["status"] != "solved"
    clean = ps["hints_revealed"] == 0 and not ps["answer_unlocked"]
    ps["status"] = "solved"
    ps["solved_at"] = iso(now())
    if first_solve:
        tstats["attempted"] = tstats.get("attempted", 0) + 1
        tstats["solved"] += 1
        if clean:
            tstats["clean_solved"] += 1
        tstats["hints_used"] = tstats.get("hints_used", 0) + ps["hints_revealed"]
    if clean:
        ps["rep"] = min(ps.get("rep", 0) + 1, len(REVIEW_INTERVALS_DAYS) - 1)
    days = REVIEW_INTERVALS_DAYS[ps.get("rep", 0)]
    ps["review_due"] = iso(now() + timedelta(days=days))
    log_event(st, "solved", pid, attempts=ps["attempts"], hints=ps["hints_revealed"], clean=clean)
    save_state(st)

    slowest = max((r["ms"] for _, _, r in ran if r.get("ms")), default=0)
    print(f"\n✓ 全部通過！最慢一筆 {slowest:.1f}ms"
          f"　嘗試 {ps['attempts']} 次　用了 {ps['hints_revealed']} 個提示")
    print(f"下次複習：{days} 天後")
    print("\n建議接下來：")
    print(f"  1. python trainer.py answer {pid}   ← 看標準解 + 最佳解，比對你的寫法")
    print("  2. 跟 AI 教練說「幫我 review 這份 code」")
    print("  3. python trainer.py next            ← 下一題")


# ---------------------------------------------------------------- hint / answer


def cmd_hint(args):
    d = problem_dir(args.id)
    meta = load_meta(d)
    pid = meta["id"]
    hints = json.loads(read_enc(d / "hints.enc"))
    st = load_state()
    ps = prob_state(st, pid)
    n = ps["hints_revealed"]
    if args.show:
        if n == 0:
            print("（還沒解鎖任何提示）")
            return
        print(hr(f"{pid} · 已解鎖的提示"))
        for i in range(n):
            print(f"\n【提示 {i + 1}/{len(hints)}】\n{hints[i]}")
        return
    if n >= len(hints):
        print(f"提示已經用完（{len(hints)} 階都看過了）。")
        print(f"還是卡住 → python trainer.py answer {pid}")
        return
    ps["hints_revealed"] = n + 1
    ps["node"] = meta["node"]
    log_event(st, "hint", pid, level=n + 1)
    save_state(st)
    print(hr(f"提示 {n + 1} / {len(hints)}"))
    print(hints[n])
    remain = len(hints) - n - 1
    print("\n" + (f"還有 {remain} 階提示。" if remain else "這是最後一階提示。"))
    revealed = d / "revealed.md"
    with revealed.open("a", encoding="utf-8") as f:
        f.write(f"\n## 提示 {n + 1}（{iso(now())}）\n\n{hints[n]}\n")


def cmd_answer(args):
    d = problem_dir(args.id)
    meta = load_meta(d)
    pid = meta["id"]
    st = load_state()
    ps = prob_state(st, pid)
    hints = json.loads(read_enc(d / "hints.enc"))
    if not args.yes and ps["status"] != "solved" and ps["hints_revealed"] < len(hints):
        print(f"⚠ 你還有 {len(hints) - ps['hints_revealed']} 階提示沒用，也還沒通過測資。")
        print(f"  建議先 `python trainer.py hint {pid}`。")
        print(f"  真的要看解答：python trainer.py answer {pid} --yes")
        return
    ref = read_enc(d / "reference.enc")
    out = d / "reference.md"
    out.write_text(f"# {pid} · {meta['title']} — 參考解\n\n{ref.strip()}\n", encoding="utf-8")
    ps["answer_unlocked"] = True
    ps["ever_unlocked"] = True
    ps["node"] = meta["node"]
    log_event(st, "answer_unlocked", pid, solved_first=ps["status"] == "solved")
    save_state(st)
    print(hr(f"{pid} · 參考解已寫入"))
    print(out.as_posix())
    print()
    print(ref.strip())


def cmd_open(args):
    d = problem_dir(args.id)
    meta = load_meta(d)
    print((d / "problem.md").read_text(encoding="utf-8"))
    st = load_state()
    ps = prob_state(st, meta["id"])
    print(hr("你的狀態"))
    print(f"狀態 {ps['status']}　嘗試 {ps['attempts']} 次　"
          f"提示 {ps['hints_revealed']}/{meta['hint_count']}　"
          f"解答 {'已解鎖' if ps['answer_unlocked'] else '未解鎖'}")
    print(f"作答檔：{(d / LANG_FILE[meta['lang']]).as_posix()}")


# ---------------------------------------------------------------- next


def pick_next_node(st: dict, cur: dict, want_node: str | None, want_lang: str | None,
                   track: str | None = None):
    nodes = all_nodes(cur, track)
    if want_node:
        n = find_node(cur, want_node)
        if not n:
            die(f"curriculum 裡沒有節點 {want_node}")
        return n
    for n in nodes:
        if want_lang and want_lang not in n.get("lang", n["stage_lang"]):
            continue
        if not is_mastered(n, topic_stats(st, n["id"])):
            return n
    return nodes[-1]


def cmd_next(args):
    st = load_state()
    cur = load_curriculum()

    due = due_reviews(st)
    if due and not args.node and not args.skip_review:
        print(hr("先複習（間隔重複到期）"))
        for pid, days in due[:5]:
            meta = load_meta(problem_dir(pid))
            print(f"  {pid} · {meta['title']}（到期 {days} 天）")
        print(f"\n  python trainer.py redo {due[0][0]}   ← 清空重寫一次")
        print("  （不想複習就加 --skip-review）\n")

    node = pick_next_node(st, cur, args.node, args.lang, args.track)
    stats = topic_stats(st, node["id"])
    langs = node.get("lang", node["stage_lang"])
    lang = args.lang or langs[0]
    if lang not in langs:
        print(f"⚠ 節點 {node['id']} 建議語言是 {langs}，你指定了 {lang}\n")

    solved = stats["solved"]
    difficulty = args.difficulty or (
        "warmup" if solved == 0 else "standard" if solved == 1 else "challenge"
    )
    existing = [
        load_meta(p)["title"]
        for p in sorted(PROBLEMS.glob("*"))
        if p.is_dir() and (p / "meta.json").exists() and load_meta(p)["node"] == node["id"]
    ]
    weak = weak_spots(st, cur)

    brief = {
        "generated_at": iso(now()),
        "track": node.get("track", "code"),
        "node": node["id"],
        "node_name": node["name"],
        "node_goal": node.get("goal", ""),
        "node_skills": node.get("skills", []),
        "node_verify": node.get("verify", ""),
        "stage": node["stage_name"],
        "lang": lang,
        "mode": "function" if lang == "py" else "io",
        "difficulty": difficulty,
        "style": node.get("style", "leetcode"),
        "progress_in_node": f"{solved}/{node.get('target', 3)}",
        "avoid_titles": existing,
        "weak_spots": weak,
        "resources": node.get("resources", {}),
        "spec_schema": "見 code-trainer/README.md 的 spec 欄位說明",
    }
    BRIEF_PATH.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    print(hr("下一題出題指令（給 AI 教練）"))
    print(f"軌道    : {'數學軌' if node.get('track') == 'math' else '程式軌'}")
    print(f"階段    : {node['stage_name']}")
    print(f"節點    : {node['id']} {node['name']}（此節點進度 {solved}/{node.get('target', 3)}）")
    print(f"學習目標: {node.get('goal', '')}")
    if node.get("skills"):
        print(f"必考技能: {', '.join(node['skills'])}")
    if node.get("verify"):
        print(f"驗證方向: {node['verify']}")
    print(f"語言    : {'Python' if lang == 'py' else 'C++'}　難度: {difficulty}"
          f"　風格: {node.get('style', 'leetcode')}")
    if existing:
        print(f"避免重複: {'; '.join(existing[-6:])}")
    if weak:
        print(f"順便補弱: {'; '.join(weak)}")

    res = node.get("resources") or {}
    if res:
        print("\n" + hr("這個階段的參考資源"))
        for label, key in (("中文", "zh"), ("英文", "en")):
            for item in res.get(key, []):
                print(f"  [{label}] {item}")
    print()
    print("AI 教練請照 SKILL 規則出題：寫一份 spec JSON 到暫存檔，然後執行")
    print("  python trainer.py new --spec <spec.json>")
    print(f"（這份 brief 也存在 {BRIEF_PATH.name}）")


def weak_spots(st: dict, cur: dict) -> list[str]:
    out = []
    for n in all_nodes(cur):
        s = topic_stats(st, n["id"])
        if s["solved"] and s["hints_used"] / max(1, s["solved"]) >= 2:
            out.append(f"{n['id']} {n['name']}（平均用 {s['hints_used'] / s['solved']:.1f} 提示）")
    return out[-3:]


def due_reviews(st: dict) -> list[tuple[str, int]]:
    out = []
    for pid, ps in st["problems"].items():
        if ps.get("status") != "solved" or not ps.get("review_due"):
            continue
        if not (PROBLEMS / pid).is_dir():
            continue
        delta = (now() - parse_iso(ps["review_due"])).days
        if delta >= 0:
            out.append((pid, delta))
    return sorted(out, key=lambda x: -x[1])


def cmd_review(args):
    st = load_state()
    due = due_reviews(st)
    if not due:
        upcoming = sorted(
            ((p, ps["review_due"]) for p, ps in st["problems"].items() if ps.get("review_due")),
            key=lambda x: x[1],
        )
        print("今天沒有到期的複習 🎉")
        if upcoming:
            pid, when = upcoming[0]
            print(f"下一個：{pid} · {parse_iso(when).date()}")
        return
    print(hr(f"到期複習 {len(due)} 題"))
    for pid, days in due:
        meta = load_meta(problem_dir(pid))
        ps = st["problems"][pid]
        print(f"  {pid} · {meta['title']}")
        print(f"      節點 {meta['node']}　第 {ps.get('rep', 0)} 輪　逾期 {days} 天")
    print(f"\n開始：python trainer.py redo {due[0][0]}")


def cmd_redo(args):
    d = problem_dir(args.id)
    meta = load_meta(d)
    pid = meta["id"]
    st = load_state()
    ps = prob_state(st, pid)
    sol = d / LANG_FILE[meta["lang"]]
    attempts_dir = d / "attempts"
    attempts_dir.mkdir(exist_ok=True)
    if sol.exists():
        stamp = now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(sol, attempts_dir / f"{stamp}-{sol.name}")
    sol.write_text((d / "starter.txt").read_text(encoding="utf-8"), encoding="utf-8")
    for f in (d / "reference.md", d / "revealed.md"):
        if f.exists():
            f.unlink()
    ps["status"] = "open"
    ps["hints_revealed"] = 0
    ps["answer_unlocked"] = False
    ps["attempts"] = 0
    log_event(st, "redo", pid, rep=ps.get("rep", 0))
    save_state(st)
    print(f"✓ {pid} 已還原成空白（舊作答存到 attempts/）")
    print(f"  python trainer.py open {pid}")


# ---------------------------------------------------------------- status / list


def bar(frac: float, width: int = 10) -> str:
    filled = int(round(frac * width))
    return "█" * filled + "·" * (width - filled)


def cmd_status(args):
    st = load_state()
    cur = load_curriculum()
    probs = st["problems"]
    solved = [p for p, s in probs.items() if s.get("status") == "solved"]
    clean = [p for p in solved if not probs[p].get("ever_unlocked") and probs[p].get("hints_revealed", 0) == 0]
    print(hr("code-trainer 進度"))
    print(f"題目 {len(probs)} 題　通過 {len(solved)}　完全自力（0 提示 0 解答）{len(clean)}")
    dates = sorted({parse_iso(e["ts"]).date() for e in st["log"] if e["event"] in ("solved", "hint", "test_fail")})
    print(f"練習天數 {len(dates)}　連續 {streak(dates)} 天")
    due = due_reviews(st)
    if due:
        print(f"待複習 {len(due)} 題（python trainer.py review）")
    for track, label in (("code", "程式軌"), ("math", "數學軌")):
        stages = [s for s in cur["stages"] if s.get("track", "code") == track]
        if not stages:
            continue
        total = sum(len(s["nodes"]) for s in stages)
        done_all = sum(
            1 for s in stages for n in s["nodes"] if is_mastered(n, topic_stats(st, n["id"]))
        )
        print(f"\n{hr(f'{label}  {done_all}/{total} 節點')}")
        for stage in stages:
            nodes = stage["nodes"]
            done = sum(1 for n in nodes if is_mastered(n, topic_stats(st, n["id"])))
            print(f"{bar(done / len(nodes))} {done:>2}/{len(nodes)}  {stage['id']} {stage['name']}")
    print()
    active = []
    for stage in cur["stages"]:
        for n in stage["nodes"]:
            s = topic_stats(st, n["id"])
            if s["solved"] or s["attempted"]:
                active.append((n, s))
    if active:
        print(hr("已接觸的節點"))
        for n, s in active[-12:]:
            flag = "✓" if is_mastered(n, s) else " "
            print(f" {flag} {n['id']:<5} {n['name'][:26]:<28} 通過 {s['solved']}/{n.get('target', 3)}"
                  f"　自力 {s['clean_solved']}　提示 {s['hints_used']}")
    nxt = pick_next_node(st, cur, None, None, "code")
    print(f"\n下一題（程式軌）：{nxt['id']} {nxt['name']}"
          f"\n  → python trainer.py next")
    nxt_m = pick_next_node(st, cur, None, None, "math")
    print(f"下一題（數學軌）：{nxt_m['id']} {nxt_m['name']}"
          f"\n  → python trainer.py next --track math")


def streak(dates: list) -> int:
    if not dates:
        return 0
    today = now().date()
    if (today - dates[-1]).days > 1:
        return 0
    count, cursor = 0, dates[-1]
    for d in reversed(dates):
        if d == cursor:
            count += 1
            cursor -= timedelta(days=1)
        elif d < cursor:
            break
    return count


def cmd_list(args):
    st = load_state()
    rows = []
    for p in sorted(PROBLEMS.glob("*")):
        if not (p / "meta.json").exists():
            continue
        meta = load_meta(p)
        ps = st["problems"].get(meta["id"], {})
        if args.status and ps.get("status", "open") != args.status:
            continue
        if args.node and not meta["node"].startswith(args.node):
            continue
        rows.append((meta, ps))
    if not rows:
        print("（沒有符合的題目）")
        return
    print(hr(f"{len(rows)} 題"))
    print(f"{'id':<26}{'節點':<7}{'語言':<6}{'難度':<11}{'狀態':<8}提示")
    for meta, ps in rows:
        mark = {"solved": "✓ 通過", "open": "· 未完成"}.get(ps.get("status", "open"), ps.get("status"))
        print(f"{meta['id'][:25]:<26}{meta['node']:<7}{meta['lang']:<6}{meta['difficulty']:<11}"
              f"{mark:<8}{ps.get('hints_revealed', 0)}/{meta['hint_count']}")


def cmd_log(args):
    st = load_state()
    for e in st["log"][-args.n:]:
        extra = {k: v for k, v in e.items() if k not in ("ts", "event", "id")}
        print(f"{e['ts']}  {e['event']:<15} {e['id']:<26} {extra if extra else ''}")


def cmd_curriculum(args):
    cur = load_curriculum()
    st = load_state()
    for stage in cur["stages"]:
        if args.track and stage.get("track", "code") != args.track:
            continue
        track_tag = "數學軌" if stage.get("track") == "math" else "程式軌"
        print("\n" + hr(f"[{track_tag}] {stage['id']} {stage['name']}"))
        print(f"  語言 {stage.get('lang')}　{stage.get('goal', '')}")
        if args.verbose and stage.get("resources"):
            for label, key in (("中文", "zh"), ("英文", "en")):
                for item in stage["resources"].get(key, []):
                    print(f"    [{label}] {item}")
        for n in stage["nodes"]:
            s = topic_stats(st, n["id"])
            flag = "✓" if is_mastered(n, s) else ("~" if s["solved"] else " ")
            print(f"  {flag} {n['id']:<6}{n['name']}")
            if args.verbose:
                print(f"        目標：{n.get('goal', '')}")
                if n.get("skills"):
                    print(f"        技能：{', '.join(n['skills'])}")
                if n.get("verify"):
                    print(f"        用程式驗證：{n['verify']}")


def cmd_doctor(args):
    if args.pick:
        exe = str(Path(args.pick).resolve())
        if not Path(exe).exists():
            die(f"找不到 {exe}")
        cfg = load_config()
        cfg["python"] = exe
        save_config(cfg)
        print(f"✓ 已指定執行解答用的 Python：{exe}")
        print(f"  numpy：{'有' if can_import(exe, 'numpy') else '沒有'}")
        return

    print(hr("環境檢查"))
    print(f"專案位置      {ROOT}")
    print(f"trainer 執行於 {sys.version.split()[0]}  {sys.executable}")

    exe = solution_python(quiet=True)
    print(f"執行解答用     {exe}")
    if os.environ.get("TRAINER_PYTHON"):
        print("              （來自環境變數 TRAINER_PYTHON）")
    elif load_config().get("python"):
        print("              （來自 config.json，可用 --pick 更換）")

    print()
    for mod, note in (("numpy", "S5 的題目需要"), ("torch", "節點 5.9 之後才需要"),
                      ("cv2", "節點 5.4 之後才需要")):
        ok = can_import(exe, mod)
        print(f"  {'✓' if ok else '–'} {mod:<8}{'可用' if ok else '未安裝（' + note + '）'}")

    gpp = shutil.which("g++")
    if gpp:
        v = subprocess.run([gpp, "--version"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace").stdout.splitlines()[0]
        print(f"  ✓ g++     {v}")
    else:
        print("  ✗ g++     找不到（C++ 題目無法編譯，請安裝 MSYS2/MinGW 並加入 PATH）")

    print()
    print(f"題庫          {len(list(PROBLEMS.glob('*/meta.json')))} 題")
    print(f"進度紀錄      {'state.json 存在' if STATE_PATH.exists() else '尚未建立'}")
    root = repo_root()
    if root:
        remote = git("remote", "get-url", "origin").stdout.strip()
        print(f"版本控制      repo 根目錄 {root}")
        print(f"              遠端 {remote or '（未設定，sync 只會在本機留紀錄）'}")
    else:
        print("版本控制      未初始化（無法用 sync 同步）")

    if len(python_candidates()) > 1:
        print("\n本機偵測到的 Python：")
        for c in python_candidates():
            print(f"  {'✓ numpy' if can_import(c, 'numpy') else '  無 numpy'}   {c}")


SKILL_DIR = ROOT / ".claude" / "skills" / "code-trainer"
SKILL_FILE = SKILL_DIR / "SKILL.md"


def skill_description() -> str:
    """讀出正本 SKILL.md 的 description，讓指標檔永遠跟正本一致。"""
    fallback = ("程式練習教練。當使用者要練習寫程式、要出題、卡在 code-trainer 的題目、"
                "要提示、要看標準解、要 review 作答時使用。")
    if not SKILL_FILE.exists():
        return fallback
    m = re.search(r"^description:\s*(.+)$", SKILL_FILE.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else fallback


def pointer_skill_text() -> str:
    return f"""---
name: code-trainer
description: {skill_description()}
---

# code-trainer 教練（指標）

這份是**指標**，不是內容。真正的教練規則放在專案裡，會跟著 git 一起同步到每台電腦：

**立刻讀取並完整遵循下面這個檔案，然後照它的指示執行：**

```
{SKILL_FILE}
```

規則只維護那一份，避免兩邊內容走鐘。
如果專案被搬到別的路徑，在新位置執行 `python trainer.py skill --install` 重新產生這個檔案。

在讀到那份檔案之前，你只需要知道一條規則：
**不要主動給題目的答案或解法程式碼，只給提示。**
"""


def cmd_skill(args):
    if not SKILL_FILE.exists():
        die(f"找不到教練規則正本：{SKILL_FILE}")

    if not args.install:
        print(hr("教練規則"))
        print(f"正本（跟著專案同步）：\n  {SKILL_FILE}\n")
        print("已安裝的指標檔：")
        found = False
        for cand in (ROOT.parent / ".claude" / "skills" / "code-trainer" / "SKILL.md",
                     Path.home() / ".claude" / "skills" / "code-trainer" / "SKILL.md"):
            if cand.exists():
                print(f"  ✓ {cand}")
                found = True
        if not found:
            print("  （沒有。只有在專案資料夾內開 Claude Code 時才會載入教練規則）")
        print("\n重建指標檔：")
        print(f"  python trainer.py skill --install          → {ROOT.parent}")
        print("  python trainer.py skill --install --user   → 使用者家目錄（任何地方都能用）")
        print("  python trainer.py skill --install --target <資料夾>")
        return

    if args.user:
        base = Path.home()
    elif args.target:
        base = Path(args.target).expanduser().resolve()
        if not base.is_dir():
            die(f"找不到資料夾 {base}")
    else:
        base = ROOT.parent

    dest_dir = base / ".claude" / "skills" / "code-trainer"
    if dest_dir.resolve() == SKILL_DIR.resolve():
        die("目標就是正本所在位置，不需要也不可以在這裡放指標檔。")

    dest = dest_dir / "SKILL.md"
    if dest.exists() and not args.force:
        existing = dest.read_text(encoding="utf-8")
        if "指標" not in existing and "轉向" not in existing:
            die(f"{dest} 已經存在而且不像是指標檔，怕蓋掉你的東西。確定要覆寫請加 --force")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest.write_text(pointer_skill_text(), encoding="utf-8")
    print(f"✓ 指標檔已寫入\n  {dest}")
    print(f"\n它指向正本：\n  {SKILL_FILE}")
    print(f"\n效果：在 {base} 底下開啟 Claude Code 時，教練模式會自動載入。")


# ---------------------------------------------------------------- 日程表

PLAN_PATH = ROOT / "plan.json"


def load_plan() -> dict:
    if not PLAN_PATH.exists():
        die("找不到 plan.json")
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def plan_position(st: dict, plan: dict):
    """回傳 (第幾週從 1 起算, 目前階段, 該階段第幾週, 累計起始週)。沒設開始日就回 None。"""
    started = st.get("plan", {}).get("started")
    if not started:
        return None
    days = (now().date() - parse_iso(started).date()).days
    week = days // 7 + 1
    cursor = 0
    for phase in plan["phases"]:
        if week <= cursor + phase["weeks"]:
            return week, phase, week - cursor, cursor
        cursor += phase["weeks"]
    return week, plan["phases"][-1], week - cursor + plan["phases"][-1]["weeks"], cursor


def node_progress(st: dict, cur: dict, ids: list[str]) -> tuple[int, int]:
    done = 0
    for nid in ids:
        n = find_node(cur, nid)
        if n and is_mastered(n, topic_stats(st, nid)):
            done += 1
    return done, len(ids)


def cmd_plan(args):
    st = load_state()
    plan = load_plan()
    if args.start:
        when = now() if args.start == "today" else parse_iso(args.start)
        st.setdefault("plan", {})["started"] = iso(when)
        st["plan"]["hours_per_week"] = args.hours or plan.get("hours_per_week", 10)
        log_event(st, "plan_start", "", started=st["plan"]["started"])
        save_state(st)
        print(f"✓ 日程表開始日設為 {parse_iso(st['plan']['started']).date()}")
        print(f"  每週時數目標 {st['plan']['hours_per_week']} 小時")
        print("\n每天執行：python trainer.py today")
        return

    pos = plan_position(st, plan)
    print(hr(plan["title"]))
    print(f"{plan['assumption']}\n")
    total = sum(p["weeks"] for p in plan["phases"])
    cursor = 0
    cur = load_curriculum()
    for phase in plan["phases"]:
        span = f"週 {cursor + 1}–{cursor + phase['weeks']}"
        mark = "▶" if pos and phase["id"] == pos[1]["id"] else " "
        cdone, ctot = node_progress(st, cur, phase["code"])
        mdone, mtot = node_progress(st, cur, phase["math"])
        print(f"{mark} {phase['id']}  {span:<12} {phase['name']}")
        print(f"     程式軌 {cdone}/{ctot} 節點　數學軌 {mdone}/{mtot} 節點")
        print(f"     里程碑：{phase['milestone']}")
        cursor += phase["weeks"]
    print(f"\n總長 {total} 週（約 {total / 4.33:.0f} 個月）")
    if not pos:
        print("\n還沒設定開始日：python trainer.py plan --start today")


def cmd_today(args):
    st = load_state()
    cur = load_curriculum()
    plan = load_plan()
    pos = plan_position(st, plan)
    today = now()
    weekday = today.weekday()
    rhythm = plan["rhythm"][weekday]

    header = today.strftime("%Y-%m-%d")
    if pos:
        week, phase, week_in_phase, _ = pos
        header += f"　第 {week} 週　{phase['id']} {phase['name']}（本階段第 {week_in_phase}/{phase['weeks']} 週）"
    print(hr(header))

    print(f"今天（{rhythm['day']}）：{rhythm['slot']}　約 {rhythm['minutes']} 分鐘")
    print(f"  {rhythm['detail']}\n")

    due = due_reviews(st)
    if due:
        print(hr(f"① 先複習 {len(due)} 題（優先於新題）"))
        for pid, days in due[:3]:
            meta = load_meta(problem_dir(pid))
            print(f"  python trainer.py redo {pid}    ← {meta['title']}（逾期 {days} 天）")
        print()

    if rhythm["minutes"] == 0:
        print("今天休息。落後就補一題，沒落後就去做別的事。")
        print("  python trainer.py status    ← 看看這週的成果")
        return

    want_math = "數學軌" in rhythm["slot"]
    review_only = "複習" in rhythm["slot"] and not want_math
    if review_only and due:
        pass  # 上面已經列出複習清單，今天就做那些
    else:
        if review_only:
            print(hr("② 今天沒有到期複習，改做一題新的"))
        else:
            print(hr(f"② 今天的題目（{'數學軌' if want_math else '程式軌'}）"))
        track = "math" if want_math else "code"
        nxt = pick_next_node(st, cur, None, None, track)
        print(f"  節點 {nxt['id']} {nxt['name']}")
        print(f"  python trainer.py next{' --track math' if want_math else ''}")

    if "課程" in rhythm["slot"] and pos:
        print("\n" + hr("③ 課程"))
        print(f"  {pos[1]['course']}")

    if pos:
        week, phase, _, _ = pos
        cdone, ctot = node_progress(st, cur, phase["code"])
        mdone, mtot = node_progress(st, cur, phase["math"])
        print("\n" + hr("本階段進度"))
        print(f"  程式軌 {bar(cdone / max(ctot, 1))} {cdone}/{ctot}　"
              f"{' '.join(phase['code'])}")
        print(f"  數學軌 {bar(mdone / max(mtot, 1))} {mdone}/{mtot}　"
              f"{' '.join(phase['math'])}")
        print(f"  重點：{phase['focus']}")
        print(f"  里程碑：{phase['milestone']}")
    else:
        print("\n（還沒設定日程表開始日：python trainer.py plan --start today）")


def git(*argv, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *argv], capture_output=capture,
                          text=True, encoding="utf-8", errors="replace")


def repo_root() -> Path | None:
    """專案所在的 git repo 根目錄（可能是 ROOT 本身，也可能是它的上層）。"""
    if not shutil.which("git"):
        return None
    res = git("rev-parse", "--show-toplevel")
    if res.returncode != 0 or not res.stdout.strip():
        return None
    return Path(res.stdout.strip())


def cmd_sync(args):
    """把進度與題庫同步到 git remote，讓另一台電腦接著練。"""
    if not shutil.which("git"):
        die("找不到 git。請先安裝 git，或改用雲端資料夾（OneDrive / Dropbox）同步整個資料夾。")
    root = repo_root()
    if root is None:
        print("這個資料夾還不在任何 git repo 裡。要開始同步，執行：\n")
        print(f"  cd {ROOT}")
        print("  git init -b main")
        print("  git add -A && git commit -m \"初始化 code-trainer\"")
        print("  git remote add origin <你的私人 repo 網址>")
        print("  git push -u origin main\n")
        print("之後兩台電腦都用 `python trainer.py sync` 就好。")
        return
    if root.resolve() != ROOT.resolve():
        print(f"（repo 根目錄在上層：{root}，會一併同步該資料夾底下的東西）\n")

    has_remote = bool(git("remote").stdout.strip())
    if not has_remote:
        print("⚠ 還沒設定遠端 repo，目前只會在本機留版本紀錄。")
        print("  要讓另一台電腦接得上，先開一個私人 repo 再執行：")
        print("    git remote add origin <你的私人 repo 網址>")
        print("    git push -u origin main\n")

    if has_remote:
        print(hr("拉取遠端進度"))
        pull = git("pull", "--rebase", "--autostash")
        print((pull.stdout + pull.stderr).strip() or "（沒有新東西）")
        if pull.returncode != 0:
            print("\n✗ pull 失敗。最常見的原因是兩台電腦都練了同一題造成 state.json 衝突。")
            print("  解法：決定要留哪一邊，然後")
            print("    git checkout --theirs state.json   # 留遠端那台的進度")
            print("    git checkout --ours   state.json   # 留這台的進度")
            print("    git add state.json && git rebase --continue")
            sys.exit(1)

    status = git("status", "--porcelain").stdout.strip()
    if not status:
        print("\n沒有新的變更要上傳。")
        if has_remote:
            print("兩邊已經同步。")
        return

    print("\n" + hr("本機變更"))
    print(status)
    st = load_state()
    solved = sum(1 for s in st["problems"].values() if s.get("status") == "solved")
    msg = args.message or f"練習進度：{solved} 題通過（{now().strftime('%Y-%m-%d %H:%M')}）"
    git("add", "-A")
    commit = git("commit", "-m", msg)
    print((commit.stdout + commit.stderr).strip())

    if not has_remote:
        print("\n（尚未設定 remote，只有在本機建立版本。）")
        print("  git remote add origin <你的私人 repo 網址> && git push -u origin main")
        return

    print("\n" + hr("上傳"))
    push = git("push")
    print((push.stdout + push.stderr).strip() or "完成")
    if push.returncode != 0:
        sys.exit(1)


def verify_one(d: Path) -> tuple[bool, str]:
    """用出題者附的參考程式碼跑一遍測資，確認題目與測資本身沒錯。不影響進度。"""
    meta = load_meta(d)
    vpath = d / "verify.enc"
    if not vpath.exists():
        return True, "（此題沒有附驗證用參考程式碼，略過）"
    code = read_enc(vpath)
    tests = json.loads(read_enc(d / "tests.enc"))
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / d.name
        shutil.copytree(d, work, ignore=shutil.ignore_patterns(".build", "attempts"))
        (work / LANG_FILE[meta["lang"]]).write_text(code, encoding="utf-8")
        if meta["mode"] == "function" and meta["lang"] == "py":
            out, err = run_py_function(work, meta, tests, None)
        else:
            out, err = run_io(work, meta, tests, None)
    if err:
        return False, err
    if out.get("fatal"):
        return False, out["fatal"]
    bad = [i for i, r in enumerate(out["results"]) if not r.get("ok")]
    if bad:
        detail = []
        for i in bad[:3]:
            r = out["results"][i]
            detail.append(
                f"  測資 #{i + 1}: 期望 {r.get('expected_repr', '?')} / 實際 {r.get('got_repr', '')}"
                + (f" / 錯誤 {r.get('error')}" if r.get("error") else "")
            )
        return False, f"{len(bad)}/{len(tests)} 筆測資與參考解不符：\n" + "\n".join(detail)
    slow = max((r["ms"] for r in out["results"] if r.get("ms")), default=0)
    return True, f"{len(tests)} 筆測資全部與參考解相符（最慢 {slow:.0f}ms）"


def cmd_verify(args):
    dirs = [problem_dir(args.id)] if args.id else sorted(
        p for p in PROBLEMS.glob("*") if (p / "meta.json").exists()
    )
    fails = 0
    for d in dirs:
        ok, msg = verify_one(d)
        if not ok:
            fails += 1
        print(f"{'✓' if ok else '✗'} {d.name}: {msg}")
    print(f"\n{len(dirs) - fails}/{len(dirs)} 題驗證通過")
    if fails:
        sys.exit(1)


def cmd_seed(args):
    sys.path.insert(0, str(ROOT))
    import seed  # noqa: PLC0415

    created = seed.run(create_problem, force=args.force)
    print(f"\n✓ 匯入 {created} 題種子題目")
    print("開始：python trainer.py status")


# ---------------------------------------------------------------- cli


def main():
    p = argparse.ArgumentParser(prog="trainer", description="程式練習教練系統")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="進度總覽")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("next", help="產生下一題的出題指令")
    s.add_argument("--node", help="指定 curriculum 節點，例如 2.5 或 M2.8")
    s.add_argument("--track", choices=["code", "math"], default="code",
                   help="程式軌（預設）或數學軌")
    s.add_argument("--lang", choices=["py", "cpp"])
    s.add_argument("--difficulty", choices=["warmup", "standard", "challenge", "contest"])
    s.add_argument("--skip-review", action="store_true")
    s.set_defaults(func=cmd_next)

    s = sub.add_parser("new", help="用 spec JSON 建立題目（AI 教練用）")
    s.add_argument("--spec", required=True)
    s.set_defaults(func=cmd_new)

    s = sub.add_parser("open", help="顯示題目")
    s.add_argument("id")
    s.set_defaults(func=cmd_open)

    s = sub.add_parser("test", help="跑測資")
    s.add_argument("id")
    s.add_argument("--case", type=int, help="只跑第 N 筆（1 起算）")
    s.set_defaults(func=cmd_test)

    s = sub.add_parser("hint", help="解鎖下一階提示")
    s.add_argument("id")
    s.add_argument("--show", action="store_true", help="重看已解鎖的提示")
    s.set_defaults(func=cmd_hint)

    s = sub.add_parser("answer", help="解鎖標準解 / 最佳解")
    s.add_argument("id")
    s.add_argument("--yes", action="store_true", help="跳過確認")
    s.set_defaults(func=cmd_answer)

    s = sub.add_parser("list", help="題目清單")
    s.add_argument("--status", choices=["open", "solved"])
    s.add_argument("--node")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("review", help="到期複習清單")
    s.set_defaults(func=cmd_review)

    s = sub.add_parser("today", help="今天該做什麼（按表操課）")
    s.set_defaults(func=cmd_today)

    s = sub.add_parser("plan", help="看日程表 / 設定開始日")
    s.add_argument("--start", metavar="YYYY-MM-DD", help="設定開始日，或用 today")
    s.add_argument("--hours", type=int, help="每週可投入時數")
    s.set_defaults(func=cmd_plan)

    s = sub.add_parser("redo", help="清空重做一題")
    s.add_argument("id")
    s.set_defaults(func=cmd_redo)

    s = sub.add_parser("curriculum", help="看完整學習路線")
    s.add_argument("-v", "--verbose", action="store_true", help="顯示目標、技能與參考資源")
    s.add_argument("--track", choices=["code", "math"], help="只看其中一軌")
    s.set_defaults(func=cmd_curriculum)

    s = sub.add_parser("log", help="最近事件")
    s.add_argument("-n", type=int, default=25)
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("doctor", help="環境檢查")
    s.add_argument("--pick", metavar="PYTHON", help="指定執行解答用的 Python 直譯器路徑")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("skill", help="檢視或重建 Claude Code 教練規則的指標檔")
    s.add_argument("--install", action="store_true", help="寫入指標檔")
    s.add_argument("--user", action="store_true", help="裝到家目錄，任何資料夾都能用")
    s.add_argument("--target", help="裝到指定資料夾")
    s.add_argument("--force", action="store_true", help="覆寫已存在的檔案")
    s.set_defaults(func=cmd_skill)

    s = sub.add_parser("sync", help="用 git 同步進度與題庫到另一台電腦")
    s.add_argument("-m", "--message", help="自訂 commit 訊息")
    s.set_defaults(func=cmd_sync)

    s = sub.add_parser("verify", help="用參考解驗證題目測資（出題後自我檢查）")
    s.add_argument("id", nargs="?", help="省略則驗證全部")
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("seed", help="匯入內建種子題目")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_seed)

    PROBLEMS.mkdir(exist_ok=True)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
