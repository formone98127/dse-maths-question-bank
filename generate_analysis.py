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
已存在的 JSON 預設跳過；--force 重新產生。
"""

import argparse
import datetime
import json
import os
import re
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
    "A": {"is_correct": boolean, "error_category": null 或 "Conceptual"|"Calculation"|"Reading-Formatting"|"Methodological", "error_tag": "字串, 簡短錯誤標籤, 正確選項填 null", "student_thought_process": "字串, 學生選到這項的具體錯誤計算/思考過程, 正確選項填 null"},
    "B": { ... },
    "C": { ... },
    "D": { ... }
  },
  "scaffolding_hints": ["Hint 1 啟發: 點出思考方向或關鍵字, 不給公式", "Hint 2 知識: 提供本題需要的公式或第一步具體列式", "Hint 3 破題: 解題過程最關鍵的轉折點"],
  "quick_solution_strategy": "字串, 30 字以內的速解法或最有效率的切入點"
}

要求：
- 全部內容使用繁體中文；數學式一律用 LaTeX（$...$ 行內、$$...$$ 展示）。
- 恰有一個選項 is_correct 為 true，且必須等於題目提供的正確答案字母。
- 正確選項的 error_category / error_tag / student_thought_process 必須是 null。
- error_category 四類定義：Conceptual（概念與邏輯錯誤）、Calculation（計算與代數操作粗心）、Reading-Formatting（審題不清、未注意單位或條件）、Methodological（使用了無效或低效的解題策略）。
- student_thought_process 必須寫出該選項對應的具體錯誤計算過程（例如把什麼看錯、哪一步展開錯），不要泛泛而談。
- 三個提示須漸進：Hint 1 不洩漏公式與答案，Hint 3 不直接寫出最終答案。"""


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
    """由配對的解答記錄取 **答案：X**；再與來源 MD 的答案速查表核對。"""
    for s in questions:
        if (
            s.get("type") == "解答"
            and s.get("subject") == q["subject"]
            and s.get("year") == q["year"]
            and s.get("paper") == q["paper"]
            and s.get("qno") == q["qno"]
        ):
            m = ANS_RE.search(s.get("text") or "")
            if m:
                return m.group(1), s
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


def collect_candidates(questions, subject=None, year=None, paper=None, qnos=None):
    out = []
    for q in questions:
        if q.get("type") != "題目":
            continue
        if subject and q.get("subject") != subject:
            continue
        if year and int(q.get("year", 0)) != year:
            continue
        if paper and q.get("paper") != paper:
            continue
        if qnos and int(q.get("qno", -1)) not in qnos:
            continue
        opts, _ = extract_mc(q)
        if not opts:
            continue
        letter, sol = answer_from_solution(questions, q)
        if not letter:
            continue
        sheet = load_answer_sheet(sol)
        if sheet.get(int(q["qno"]), letter) != letter:
            print(f"⚠ 答案不一致 q{q['qno']}：解答內文={letter}，速查表={sheet[int(q['qno'])]}（以速查表為準）")
            letter = sheet[int(q["qno"])]
        out.append((q, opts, letter))
    return out


# ---------- LLM client（OpenAI 相容 /chat/completions） ----------

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
        "temperature": float(cfg.get("temperature", 0.4)),
        "max_tokens": int(cfg.get("max_tokens", 4096)),
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


def parse_llm_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return json.loads(t)


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
    return errs


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
    for attempt in range(1, 4):
        content = call_llm(cfg, messages)
        try:
            obj = parse_llm_json(content)
        except json.JSONDecodeError as e:
            errs = [f"JSON 解析失敗：{e}"]
        else:
            errs = validate_analysis(obj, answer)
            if not errs:
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
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subject", choices=list(SID_TO_SUBJECT.values()))
    ap.add_argument("--year", type=int)
    ap.add_argument("--paper")
    ap.add_argument("--question", type=int, action="append", help="題號，可重複")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true", help="列出可分析的 MC 題（含配對答案）")
    ap.add_argument("--provider", choices=list(PROVIDER_PRESETS))
    ap.add_argument("--base-url")
    ap.add_argument("--api-key")
    ap.add_argument("--model")
    args = ap.parse_args()

    questions = load_questions()
    qnos = set(args.question) if args.question else None
    cands = collect_candidates(questions, args.subject, args.year, args.paper, qnos)

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
    for q, opts, letter in cands:
        if process(q, opts, letter, cfg, dry_run=args.dry_run, force=args.force):
            ok += 1
    if not args.dry_run:
        print(f"完成：{ok}/{len(cands)} 題成功。session tokens：prompt={TOKEN_TOTALS['prompt']} completion={TOKEN_TOTALS['completion']}")
        print("費用 = tokens × 你所用模型的單價，請自行對照供應商價目表。")


if __name__ == "__main__":
    main()
