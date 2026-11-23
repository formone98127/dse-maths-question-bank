# -*- coding: utf-8 -*-
"""MC 選擇題 AI 深度分析產生器。

由 docs/data.js 取出 MC 題（題幹 + 四個選項）與解答卷配對正確答案，
組成中文分析 prompt 呼叫 LLM（任何 OpenAI 相容 /chat/completions 端點：
OpenAI、Anthropic 相容端點、Ollama、LM Studio 等），驗證輸出 JSON 後
寫入 docs/analysis/<sid>/<year>/<paper-slug>/q<qno>.json。

設定來源（後者覆蓋前者）：
  1. 環境變數：OPENAI_API_KEY / ANTHROPIC_API_KEY / ANALYSIS_BASE_URL /
     ANALYSIS_MODEL / ANALYSIS_API_KEY
  2. repo 根目錄 analysis_config.local.json（不入 git）：
     {"provider": "openai|anthropic|custom", "base_url": "...",
      "api_key": "...", "model": "...", "temperature": 0.4, "max_tokens": 4096}

用法：
  python generate_analysis.py --list
  python generate_analysis.py --dry-run --subject 數學 --year 2012 --paper "Paper 2" --question 1
  python generate_analysis.py --subject 數學 --year 2012 --paper "Paper 2" --question 1 --question 2 --question 3
  python generate_analysis.py --subject 數學 --year 2012 --paper "Paper 2" --range 1-20
  python generate_analysis.py --subject 數學 --year 2012 --paper "Paper 2" --range 1-5,8,12-15
  python generate_analysis.py --subject 數學 --year 2012 --paper "Paper 2" --range 18-20 \
      --provider anthropic --model claude-opus-5 --temperature 0.3 --max-tokens 8192
已存在的 JSON 預設跳過；--force 重新產生。
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
ANALYSIS_DIR = DOCS / "analysis"
CONFIG_FILE = ROOT / "analysis_config.local.json"

SID_TO_SUBJECT = {"math": "數學", "econ": "經濟", "chem": "化學", "bio": "生物", "phys": "物理"}
SUBJECT_TO_SID = {v: k for k, v in SID_TO_SUBJECT.items()}
PAPER_CODE = {
    "Paper 1": "paper-1",
    "Paper 2": "paper-2",
    "Paper 1A": "paper-1a",
    "Paper 1B": "paper-1b",
    "卷一": "paper-1",
    "卷二": "paper-2",
    "卷一甲": "paper-1a",
    "卷一乙": "paper-1b",
}
SUBJECT_PREFIX = {"數學": "", "經濟": "econ", "化學": "chem", "生物": "bio", "物理": "phys"}

PROVIDER_PRESETS = {
    "openai": {"base_url": "https://api.openai.com/v1", "key_env": "OPENAI_API_KEY", "model": "gpt-4o"},
    "anthropic": {"base_url": "https://api.anthropic.com/v1", "key_env": "ANTHROPIC_API_KEY", "model": "claude-sonnet-5"},
    "custom": {"base_url": None, "key_env": "ANALYSIS_API_KEY", "model": None},
}

ERROR_CATEGORIES = {"Conceptual", "Calculation", "Reading-Formatting", "Methodological"}
BLOOM_LEVELS = {"記憶", "理解", "應用", "分析", "評鑑", "創造"}
SKILL_BOOK_PATH = ROOT / "docs" / "skills" / "math_skill_book.json"

_SKILL_BOOK_CACHE = None


def load_skill_book():
    """Load fixed math skill book (ids only allowed in skills hooks)."""
    global _SKILL_BOOK_CACHE
    if _SKILL_BOOK_CACHE is not None:
        return _SKILL_BOOK_CACHE
    if not SKILL_BOOK_PATH.is_file():
        raise SystemExit(f"缺技能冊: {SKILL_BOOK_PATH}（先跑 scripts/build_math_skill_foundation.py）")
    book = json.loads(SKILL_BOOK_PATH.read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in book["topics"]}
    kps, formulas = {}, {}
    for t in book["topics"]:
        for k in t["knowledge_points"]:
            kps[k["id"]] = {**k, "topic_id": t["id"], "topic_name": t["name"]}
        for f in t["formulas"]:
            formulas[f["id"]] = {**f, "topic_id": t["id"]}
    abilities = {a["id"]: a for a in book["abilities"]}
    _SKILL_BOOK_CACHE = (book, topics, kps, formulas, abilities)
    return _SKILL_BOOK_CACHE


def skill_catalog_for_prompt():
    book, topics, kps, formulas, abilities = load_skill_book()
    lines = ["【技能冊（skills 欄位只准用下列 id，禁止自創）】"]
    lines.append("abilities: " + ", ".join(f"{a['id']}={a['name']}" for a in book["abilities"]))
    for t in book["topics"]:
        kp_s = ", ".join(f"{k['id']}:{k['name']}" for k in t["knowledge_points"])
        f_s = ", ".join(f"{f['id']}:{f['name']}" for f in t["formulas"])
        lines.append(f"{t['id']} {t['name']} | KP: {kp_s} | F: {f_s}")
    return "\n".join(lines)


SYSTEM_PROMPT = """你是一位擁有 20 年經驗的頂尖數學教育專家與測驗心理學家（Psychometrician）。你的任務是對輸入的「數學選擇題」進行深度的解構與預先分析：精準剖析這道題目的考點、預測學生的作答行為，並針對每一個錯誤選項進行「逆向工程」，找出對應的思考盲點。

你必須輸出一個有效的 JSON 物件（嚴禁輸出 markdown code fences 或任何 JSON 以外的文字），嚴格遵守以下 Schema：

{
  "metadata": {
    "primary_topic": "字串, 例如: 一元二次方程式",
    "secondary_topics": ["陣列, 1-3 個次考點/先備知識"],
    "required_formulas": ["陣列, 解題必須用到的核心公式或定理"],
    "bloom_taxonomy_level": "記憶|理解|應用|分析|評鑑|創造 之一",
    "estimated_time_seconds": 一般程度學生的合理作答秒數（30-300 整數）
  },
  "options_analysis": {
    "A": {"is_correct": boolean, "error_category": null 或 "Conceptual"|"Calculation"|"Reading-Formatting"|"Methodological", "error_tag": "字串, 簡短錯誤標籤, 正確選項填 null", "student_thought_process": "字串, 80字以內, 正確選項填 null"},
    "B": { ... },
    "C": { ... },
    "D": { ... }
  },
  "scaffolding_hints": ["Hint 1 啟發", "Hint 2 知識", "Hint 3 破題"],
  "quick_solution_strategy": "字串, 30 字以內"
}

要求：
- 全部內容使用繁體中文；數學式一律用 LaTeX（$...$ 行內、$$...$$ 展示）。
- 恰有一個選項 is_correct 為 true，且必須等於題目提供的正確答案字母。
- 正確選項的 error_category / error_tag / student_thought_process 必須是 null。
- error_category 四類：Conceptual、Calculation、Reading-Formatting、Methodological。
- student_thought_process 每項不超過 80 字，寫具體錯步，不要長篇。
- 三個提示須漸進：Hint 1 不洩漏公式與答案，Hint 3 不直接寫出最終答案。
- 不要輸出 skills 欄位。"""

CAT_TO_ABILITY = {
    "Conceptual": "A-ALG",
    "Calculation": "A-CALC",
    "Reading-Formatting": "A-COND",
    "Methodological": "A-CHAIN",
}


# ---------- data.js 載入 ----------

def load_questions():
    text = (DOCS / "data.js").read_text(encoding="utf-8")
    assign = text.index("=")
    data, _ = json.JSONDecoder().raw_decode(text[assign + 1 :].lstrip())
    return data["questions"]


def paper_code_of(paper):
    code = PAPER_CODE.get(str(paper or "").strip())
    if not code:
        raise SystemExit(f"未知的卷別: {paper!r}")
    return code


def hash_for_question(q):
    pref = SUBJECT_PREFIX.get(q.get("subject"), "")
    m = re.search(r"(\d+[A-Za-z]?)", str(q.get("paper") or ""))
    pno = m.group(1).upper() if m else "1"
    return f"#{pref}{q['year']}P{pno}Q{q['qno']}"


# ---------- MC 解析與答案配對 ----------

OPT_RE = re.compile(r"^-\s*([A-D])[.．、]\s*(.+)$", re.M)
ANS_RE = re.compile(r"\*\*答案：([A-D])")


def extract_mc(q):
    """回傳 (options dict, answer letter or None)。options 缺四個則回傳 None。"""
    opts = dict(OPT_RE.findall(q.get("text") or ""))
    if sorted(opts) != list("ABCD"):
        return None, None
    return {k: v.strip() for k, v in opts.items()}, None


def answer_from_solution(questions, q):
    """由配對的解答記錄取 **答案：X**；再與來源 MD 的答案速查表核對。
    冇解答記錄時，用題目記錄上 inject_answers 注入嘅 `answer` 欄位（compact data.js）。"""
    for s in questions:
        if (
            s.get("type") == "解答"
            and s.get("subject") == q["subject"]
            and str(s.get("year")) == str(q["year"])
            and s.get("paper") == q["paper"]
            and str(s.get("qno")) == str(q["qno"])
        ):
            m = ANS_RE.search(s.get("text") or "")
            if m:
                return m.group(1), s
    ans = str(q.get("answer") or "").strip().upper()
    if ans in ("A", "B", "C", "D"):
        return ans, None
    return None, None


def load_answer_sheet(sol_record):
    """解析解答 MD 檔內的答案速查表（| 題號 | … | / | 答案 | **X** | …）。"""
    fname = sol_record.get("file") if sol_record else None
    if not fname:
        return {}
    path = None
    for cand in [ROOT / fname, *ROOT.glob(f"*/{fname}")]:
        if cand.is_file():
            path = cand
            break
    if not path:
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    sheet = {}
    i = 0
    while i < len(lines) - 1:
        h, v = lines[i], lines[i + 1]
        if h.strip().startswith("|") and "題號" in h and v.strip().startswith("|") and "答案" in v:
            hs = [c.strip() for c in h.strip().strip("|").split("|")]
            vs = [c.strip() for c in v.strip().strip("|").split("|")]
            for col, cell in zip(hs[1:], vs[1:]):
                m = re.fullmatch(r"\*?\*?([A-D])\*?\*?", cell)
                if m and col.isdigit():
                    sheet[int(col)] = m.group(1)
            i += 2
            continue
        i += 1
    return sheet


def _year_matches(q_year, year) -> bool:
    if year is None:
        return True
    raw = str(q_year or "").strip()
    try:
        return int(raw) == int(year)
    except ValueError:
        return raw == str(year)


def _is_chinese_question(q: dict) -> bool:
    f = str(q.get("file") or "")
    if "英文" in f or "English" in f or re.search(r"(?i)(^|[_\-/])en([_\-/]|$)", f):
        return False
    if "中文" in f or "zh" in f.lower():
        return True
    return bool(re.search(r"[\u4e00-\u9fff]", q.get("text") or ""))


def collect_candidates(questions, subject=None, year=None, paper=None, qnos=None, chinese_only=True):
    """Collect MC questions with answers. Default chinese_only avoids zh/en duplicates."""
    out = []
    for q in questions:
        if q.get("type") != "題目":
            continue
        if subject and q.get("subject") != subject:
            continue
        if not _year_matches(q.get("year"), year):
            continue
        if paper and q.get("paper") != paper:
            continue
        if qnos and int(re.sub(r"\D", "", str(q.get("qno", ""))) or -1) not in qnos:
            continue
        if chinese_only and not _is_chinese_question(q):
            continue
        opts, _ = extract_mc(q)
        if not opts:
            continue
        letter, sol = answer_from_solution(questions, q)
        if not letter:
            continue
        sheet = load_answer_sheet(sol)
        qno_i = int(re.sub(r"\D", "", str(q["qno"])) or 0)
        if sheet.get(qno_i, letter) != letter:
            print(f"⚠ 答案不一致 q{qno_i}：解答內文={letter}，速查表={sheet[qno_i]}（以速查表為準）")
            letter = sheet[qno_i]
        out.append((q, opts, letter))
    return out


# ---------- LLM client（OpenAI 相容 /chat/completions） ----------

def parse_qno_spec(spec):
    """解析題號規格：「1-20」、「5」、「1-5,8,12-15」皆可，回傳題號集合。"""
    qnos = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                raise SystemExit(f"題號範圍無效：{part!r}（起始不可大於結束）")
            qnos.update(range(lo, hi + 1))
        elif part.isdigit():
            qnos.add(int(part))
        else:
            raise SystemExit(f"題號規格無效：{part!r}（可用 5 或 1-20，逗號分隔多段）")
    return qnos


def resolve_config(args):
    cfg = {}
    if CONFIG_FILE.is_file():
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    provider = args.provider or cfg.get("provider") or os.environ.get("ANALYSIS_PROVIDER") or "openai"
    if provider not in PROVIDER_PRESETS:
        raise SystemExit(f"未知 provider: {provider}（可用: openai / anthropic / custom）")
    preset = PROVIDER_PRESETS[provider]
    base_url = args.base_url or cfg.get("base_url") or os.environ.get("ANALYSIS_BASE_URL") or preset["base_url"]
    api_key = args.api_key or cfg.get("api_key") or os.environ.get("ANALYSIS_API_KEY") or (
        os.environ.get(preset["key_env"]) if preset["key_env"] else None
    )
    model = args.model or cfg.get("model") or os.environ.get("ANALYSIS_MODEL") or preset["model"]
    if not base_url:
        raise SystemExit("custom provider 必須提供 base_url（CLI --base-url、設定檔或 ANALYSIS_BASE_URL）")
    if not api_key and not (base_url and base_url.startswith(("http://localhost", "http://127.0.0.1"))):
        raise SystemExit(
            f"找不到 API key：請設定 {preset['key_env']} 環境變數、ANALYSIS_API_KEY，"
            f"或在 analysis_config.local.json 填 api_key（本地 LLM 可免 key）"
        )
    if not model:
        raise SystemExit("必須提供 model（CLI --model、設定檔 model 或 ANALYSIS_MODEL）")
    return {
        "base_url": base_url.rstrip("/"),
        "api_key": api_key,
        "model": model,
        "temperature": args.temperature if args.temperature is not None else float(cfg.get("temperature", 0.4)),
        "max_tokens": args.max_tokens if args.max_tokens is not None else int(cfg.get("max_tokens", 4096)),
        # Ollama（:11434）走原生 /api/chat，才能帶 think:false 關掉思考模式
        "native_ollama": bool(cfg.get("native_ollama", ":11434" in base_url)),
    }


TOKEN_TOTALS = {"prompt": 0, "completion": 0}


def call_llm(cfg, messages):
    if cfg.get("native_ollama"):
        # 原生 /api/chat：可關 thinking（qwen3 系預設思考會食晒 token）
        body = json.dumps(
            {
                "model": cfg["model"],
                "messages": messages,
                "stream": False,
                "think": False,
                "options": {"temperature": cfg["temperature"], "num_predict": cfg["max_tokens"]},
            }
        ).encode("utf-8")
        url = f"{cfg['base_url'].removesuffix('/v1')}/api/chat"
    else:
        body = json.dumps(
            {
                "model": cfg["model"],
                "messages": messages,
                "temperature": cfg["temperature"],
                "max_tokens": cfg["max_tokens"],
            }
        ).encode("utf-8")
        url = f"{cfg['base_url']}/chat/completions"
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {cfg['api_key']}"} if cfg["api_key"] else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API {e.code}: {e.read().decode('utf-8', 'replace')[:500]}") from e
    if cfg.get("native_ollama"):
        usage = {
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
        }
        content = (data.get("message") or {}).get("content", "")
    else:
        usage = data.get("usage") or {}
        content = data["choices"][0]["message"]["content"]
    TOKEN_TOTALS["prompt"] += usage.get("prompt_tokens", 0) or 0
    TOKEN_TOTALS["completion"] += usage.get("completion_tokens", 0) or 0
    print(f"  tokens: prompt={usage.get('prompt_tokens', '?')} completion={usage.get('completion_tokens', '?')}")
    return content


# LaTeX 命令白名單：字首同 JSON 合法 escape（\b \f \n \r \t \u）撞咗嘅常用命令
# （\theta \frac \times \neq \underbrace …），要優先當 LaTeX 處理。
LATEX_CMDS = {
    "background", "binom", "boxed", "bmod",
    "frac", "forall",
    "neq", "ne", "nabla", "notin", "not", "nmid", "newline",
    "right", "reals", "rfloor", "rangle",
    "theta", "therefore", "times", "text", "tan", "tfrac", "to", "top", "triangle",
    "underbrace", "underline", "cup", "cap", "circ", "cdot", "cdots", "cos", "cot", "csc",
    "sin", "sqrt", "sum", "sec", "sup", "leq", "le", "geq", "ge", "log", "ln", "lim", "land", "lor",
}


def _fix_json_escapes(t):
    """LLM 寫 LaTeX（\dfrac \theta 等）時常漏 JSON 跳脫。逐個 backslash 判斷：
    係合法 JSON escape 就保留，係 LaTeX 命令就補成 \\\\，避免 \theta 靜靜變 tab。"""
    out = []
    i, n = 0, len(t)
    while i < n:
        c = t[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        nxt = t[i + 1] if i + 1 < n else ""
        if nxt in ('"', "\\", "/"):
            out.append(t[i : i + 2])
            i += 2
            continue
        if nxt == "u" and re.fullmatch(r"[0-9a-fA-F]{4}", t[i + 2 : i + 6] or ""):
            out.append(t[i : i + 6])
            i += 6
            continue
        word = re.match(r"[a-zA-Z]+", t[i + 1 :]).group(0) if nxt.isalpha() else ""
        if word and word.lower() in LATEX_CMDS:
            out.append("\\\\")
            i += 1
            continue
        if nxt in "bfnrt":
            out.append(t[i : i + 2])  # JSON escape；撞名 LaTeX 已喺白名單處理
            i += 2
            continue
        # \u 冇 4 位 hex、或其他非法 escape（\d \e \}…）＝其餘 LaTeX 命令
        out.append("\\\\")
        i += 1
    return "".join(out)


def parse_llm_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    # 修 LaTeX escape + Python 式 True/False/None
    t = re.sub(r":\s*True\b", ": true", t)
    t = re.sub(r":\s*False\b", ": false", t)
    t = re.sub(r":\s*None\b", ": null", t)
    return json.loads(_fix_json_escapes(t))


# ---------- 驗證 ----------

def validate_analysis(obj, answer):
    errs = []
    if not isinstance(obj, dict):
        return ["輸出不是 JSON 物件"]
    md = obj.get("metadata")
    if not isinstance(md, dict):
        errs.append("缺 metadata")
    else:
        for k in ("primary_topic", "secondary_topics", "required_formulas", "bloom_taxonomy_level", "estimated_time_seconds"):
            if k not in md:
                errs.append(f"metadata 缺 {k}")
        if md.get("bloom_taxonomy_level") not in BLOOM_LEVELS:
            errs.append(f"bloom_taxonomy_level 必須是 {'/'.join(sorted(BLOOM_LEVELS))}，得到 {md.get('bloom_taxonomy_level')!r}")
        t = md.get("estimated_time_seconds")
        if not isinstance(t, int) or not (30 <= t <= 300):
            errs.append(f"estimated_time_seconds 必須是 30-300 整數，得到 {t!r}")
        if not isinstance(md.get("secondary_topics"), list) or not md["secondary_topics"]:
            errs.append("secondary_topics 須為非空陣列")
        if not isinstance(md.get("required_formulas"), list):
            errs.append("required_formulas 須為陣列")

    oa = obj.get("options_analysis")
    if not isinstance(oa, dict) or sorted(oa) != list("ABCD"):
        errs.append("options_analysis 須恰好包含 A/B/C/D")
    else:
        correct = [k for k, v in oa.items() if isinstance(v, dict) and v.get("is_correct") is True]
        if correct != [answer]:
            errs.append(f"is_correct=true 的選項是 {correct}，必須是 ['{answer}']")
        for k, v in oa.items():
            if not isinstance(v, dict):
                errs.append(f"options_analysis.{k} 不是物件")
                continue
            cat = v.get("error_category")
            if v.get("is_correct"):
                if cat is not None or v.get("error_tag") is not None:
                    errs.append(f"正確選項 {k} 的 error_category/error_tag 須為 null")
            else:
                if cat not in ERROR_CATEGORIES:
                    errs.append(f"{k} error_category 須是 {'/'.join(sorted(ERROR_CATEGORIES))} 或 null，得到 {cat!r}")
                if not v.get("error_tag") or not v.get("student_thought_process"):
                    errs.append(f"{k} 缺 error_tag 或 student_thought_process")

    hints = obj.get("scaffolding_hints")
    if not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(h, str) and h.strip() for h in hints):
        errs.append("scaffolding_hints 須為 3 個非空字串")
    if not obj.get("quick_solution_strategy"):
        errs.append("缺 quick_solution_strategy")
    # skills 由 attach_skills_post() 事後掛上，唔再要求 LLM 輸出
    return errs


def attach_skills_post(q: dict, analysis: dict) -> dict:
    """用題庫 tags + 分析 metadata，掛上技能冊 id；錯選項用 error_category 對能力。"""
    book, topics, kps, formulas, abilities = load_skill_book()
    cross_path = ROOT / "docs" / "skills" / "math_tag_crosswalk.json"
    cross = {}
    if cross_path.is_file():
        cross = json.loads(cross_path.read_text(encoding="utf-8")).get("map") or {}

    tags = list(q.get("tags") or [])
    md = analysis.get("metadata") or {}
    blob = " ".join(tags) + " " + str(md.get("primary_topic") or "") + " " + " ".join(md.get("secondary_topics") or [])
    blob += " " + (q.get("text") or "")

    votes = {}
    for tag in tags:
        hit = cross.get(tag)
        if hit:
            tid = hit["topic_id"]
            votes[tid] = votes.get(tid, 0) + 2
    # keyword bump from skill book topic names
    for t in book["topics"]:
        if t["name"] in blob:
            votes[t["id"]] = votes.get(t["id"], 0) + 1
    topic_id = max(votes, key=votes.get) if votes else "T-EQN"

    kp_ids = []
    for t in book["topics"]:
        if t["id"] != topic_id:
            continue
        for k in t["knowledge_points"]:
            if any(part in blob for part in re.split(r"[：:／/、]", k["name"]) if len(part) >= 2):
                kp_ids.append(k["id"])
        if not kp_ids:
            kp_ids = [k["id"] for k in t["knowledge_points"][:2]]
        break
    kp_ids = kp_ids[:3] or ["K-EQN-01"]

    formula_ids = []
    for t in book["topics"]:
        for f in t["formulas"]:
            if f["knowledge_point_id"] in kp_ids:
                formula_ids.append(f["id"])
    formula_ids = formula_ids[:4]

    ability_ids = ["A-ALG", "A-CALC"]
    faults = {}
    oa = analysis.get("options_analysis") or {}
    for opt, v in oa.items():
        if not isinstance(v, dict) or v.get("is_correct"):
            continue
        aid = CAT_TO_ABILITY.get(v.get("error_category"), "A-ALG")
        faults[opt] = {
            "knowledge_point_id": kp_ids[0] if kp_ids else None,
            "formula_id": formula_ids[0] if formula_ids else None,
            "ability_id": aid if aid in abilities else "A-ALG",
        }
        if faults[opt]["knowledge_point_id"] is None and faults[opt]["formula_id"] is None:
            faults[opt]["knowledge_point_id"] = next(iter(kps))

    return {
        "topic_id": topic_id if topic_id in topics else next(iter(topics)),
        "knowledge_point_ids": [k for k in kp_ids if k in kps],
        "formula_ids": [f for f in formula_ids if f in formulas],
        "ability_ids": [a for a in ability_ids if a in abilities],
        "option_faults": faults,
    }


def soft_answer_leak_warning(obj, answer, options):
    """提示層若直接出現正確選項的完整內容，僅警告不擋。"""
    correct_text = options[answer].strip("$ ")
    for i, h in enumerate(obj.get("scaffolding_hints", []), 1):
        if correct_text and correct_text in h.replace("$", "").replace(" ", ""):
            print(f"  ⚠ Hint {i} 疑似洩漏答案內容（{correct_text}），請人工檢查")


# ---------- 輸出 ----------

def out_path_for(q):
    sid = SUBJECT_TO_SID[q["subject"]]
    code = paper_code_of(q["paper"])
    return ANALYSIS_DIR / sid / str(q["year"]) / code / f"q{q['qno']}.json"


def build_prompt(q, options, answer):
    lines = [
        f"科目：{q['subject']}　年份：{q['year']}　卷別：{q['paper']}　第 {q['qno']} 題",
        "",
        "【題目】",
        q["text"].strip(),
        "",
        "【選項】",
    ]
    for k in "ABCD":
        lines.append(f"{k}. {options[k]}")
    lines += ["", f"【正確答案】{answer}"]
    return "\n".join(lines)


# ---------- 主流程 ----------

def process(q, options, answer, cfg, dry_run=False, force=False):
    path = out_path_for(q)
    if path.is_file() and not force:
        print(f"↷ 已存在，跳過 {path.relative_to(ROOT)}（--force 可重新產生）")
        return False
    prompt = build_prompt(q, options, answer)
    est_tokens = int(len(prompt) / 1.6)  # CJK 粗估
    if dry_run:
        print(f"--- DRY RUN {q['subject']} {q['year']} {q['paper']} Q{q['qno']}（估計輸入 ~{est_tokens} tokens）---")
        print(prompt)
        return False
    print(f"→ 分析 {q['subject']} {q['year']} {q['paper']} Q{q['qno']}（model={cfg['model']}，輸入 ~{est_tokens} tokens）")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    content = ""
    for attempt in range(1, 4):
        try:
            content = call_llm(cfg, messages)
        except (TimeoutError, urllib.error.URLError, RuntimeError) as e:
            errs = [f"API 請求失敗（{type(e).__name__}）：{str(e)[:200]}"]
            print(f"  ✗ 第 {attempt} 次請求失敗：{errs[0]}")
            continue
        try:
            obj = parse_llm_json(content)
        except json.JSONDecodeError as e:
            errs = [f"JSON 解析失敗：{e}"]
        else:
            obj.pop("skills", None)  # 忽略模型若仍輸出
            errs = validate_analysis(obj, answer)
            if not errs:
                skills = attach_skills_post(q, obj)
                payload = {
                    "question": {
                        "subject": q["subject"],
                        "year": q["year"],
                        "paper": q["paper"],
                        "qno": q["qno"],
                        "hash": hash_for_question(q),
                    },
                    "model": cfg["model"],
                    "generated": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "analysis": obj,
                    "skills": skills,
                }
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                soft_answer_leak_warning(obj, answer, options)
                print(f"  ✓ 寫入 {path.relative_to(ROOT)}")
                return True
        print(f"  ✗ 第 {attempt} 次驗證失敗：{errs}")
        if attempt < 3:
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "你的輸出有以下問題，請修正後重新輸出完整 JSON（仍嚴禁 markdown fences）：\n- " + "\n- ".join(errs)})
    print(f"  ✗ 三次失敗，放棄 Q{q['qno']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    bad = path.with_suffix(".bad")
    bad.write_text(content or "", encoding="utf-8")
    print(f"  ↳ raw output 已存 {bad.relative_to(ROOT)}")
    return False


# ---------- 逐題上線（--publish）：build → commit → push → CI 自動部署 ----------

def publish_one(q):
    """單題分析寫入後即刻重建 SEO 頁、commit、push。push 觸發 CI 部署 Hostinger + Pages。"""
    print("  ↗ publish：重建 SEO 頁…")
    r = subprocess.run([sys.executable, "build_seo.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("  ✗ build_seo.py 失敗：", (r.stdout or "") + (r.stderr or ""))
        return False
    subprocess.run(["git", "add", "docs"], cwd=ROOT, check=False)  # 建置產物全部喺 docs/
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=False).returncode == 0:
        print("  ↗ publish：冇嘢要 commit（已上線）")
        return True
    msg = f"analysis: {q['subject']} {q['year']} {q['paper']} 第 {q['qno']} 題深度分析"
    c = subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=False)
    if c.returncode != 0:
        print("  ✗ git commit 失敗")
        return False
    for attempt in range(3):
        p = subprocess.run(["git", "push"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode == 0:
            print(f"  ↗ 已上線：/{SUBJECT_TO_SID[q['subject']]}/{q['year']}/…/q{q['qno']}/（CI 部署中）")
            return True
        # 遠端有新 commit（另一部機）：rebase 後重建再試
        print("  ↗ push 被拒，rebase + 重建後重試…")
        subprocess.run(["git", "pull", "--rebase", "-q"], cwd=ROOT, check=False)
        # 若 pull --rebase 留低衝突（罕見：upstream 動咗同一批生成頁），放棄 rebase 保住本地版
        subprocess.run(["git", "rebase", "--abort"], cwd=ROOT, capture_output=True)
        subprocess.run([sys.executable, "build_seo.py"], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "add", "docs"], cwd=ROOT, check=False)  # 只加 docs/，唔好掃埋本地其他改動
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=False).returncode != 0:
            subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=False)
    print("  ✗ push 三次失敗，內容保留喺本地，稍後手動 push")
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subject", choices=list(SID_TO_SUBJECT.values()))
    ap.add_argument("--year", type=int)
    ap.add_argument("--paper")
    ap.add_argument("--question", type=int, action="append", help="題號，可重複")
    ap.add_argument("--range", dest="qno_range",
                    help="題號範圍，如 1-20 或 1-5,8,12-15（與 --question 可併用）")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--publish", action="store_true",
                    help="每題成功後即刻 build_seo + commit + push（CI 自動部署上線）")
    ap.add_argument("--list", action="store_true", help="列出可分析的 MC 題（含配對答案）")
    ap.add_argument("--all-langs", action="store_true",
                    help="包含英文卷（預設只取中文，避免中英重複；2022 卷二等只有英文時要用）")
    ap.add_argument("--provider", choices=list(PROVIDER_PRESETS))
    ap.add_argument("--base-url")
    ap.add_argument("--api-key")
    ap.add_argument("--model")
    ap.add_argument("--temperature", type=float, help="覆蓋設定檔 temperature（預設 0.4）")
    ap.add_argument("--max-tokens", type=int, help="覆蓋設定檔 max_tokens（預設 4096）")
    args = ap.parse_args()

    questions = load_questions()
    qnos = set(args.question) if args.question else set()
    if args.qno_range:
        qnos |= parse_qno_spec(args.qno_range)
    qnos = qnos or None
    cands = collect_candidates(
        questions, args.subject, args.year, args.paper, qnos,
        chinese_only=not args.all_langs,
    )

    if args.list:
        for q, opts, letter in cands:
            marked = " ".join(f"[{k}] {v}" for k, v in opts.items())
            print(f"{q['subject']} {q['year']} {q['paper']} Q{q['qno']:<2} 答案={letter}　{marked}")
        print(f"共 {len(cands)} 題可分析")
        return

    if not cands:
        raise SystemExit("找不到符合條件、含四個選項且能配對答案的 MC 題（--list 可查看）")
    if args.dry_run and len(cands) > 3:
        cands = cands[:3]

    cfg = None if args.dry_run else resolve_config(args)
    ok = 0
    published = 0
    for q, opts, letter in cands:
        if process(q, opts, letter, cfg, dry_run=args.dry_run, force=args.force):
            ok += 1
            if args.publish and publish_one(q):
                published += 1
    if not args.dry_run:
        print(f"完成：{ok}/{len(cands)} 題成功。session tokens：prompt={TOKEN_TOTALS['prompt']} completion={TOKEN_TOTALS['completion']}")
        if args.publish:
            print(f"上線：{published} 題已 push（CI 部署 Hostinger + GitHub Pages）")
        print("費用 = tokens × 你所用模型的單價，請自行對照供應商價目表。")


if __name__ == "__main__":
    main()
