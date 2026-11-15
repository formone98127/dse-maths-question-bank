# -*- coding: utf-8 -*-
"""捉 Q23 嘅 raw LLM output，睇 JSON 錯喺邊。"""
import generate_analysis as ga

questions = ga.load_questions()
cands = ga.collect_candidates(questions, "數學", 2012, "Paper 2", {23})
q, opts, letter = cands[0]
cfg = ga.resolve_config.__doc__  # placeholder
cfg = {
    "base_url": "http://localhost:11434",
    "api_key": None,
    "model": "qwen3.5:9b",
    "temperature": 0.4,
    "max_tokens": 4096,
    "native_ollama": True,
}
prompt = ga.build_prompt(q, opts, letter)
messages = [
    {"role": "system", "content": ga.SYSTEM_PROMPT},
    {"role": "user", "content": prompt},
]
content = ga.call_llm(cfg, messages)
print("===== RAW START =====")
print(content)
print("===== RAW END =====")
import json
try:
    ga.parse_llm_json(content)
    print("parse: OK")
except json.JSONDecodeError as e:
    print(f"parse: FAIL {e}")
    t = content.strip()
    import re
    t2 = re.sub(r"^```(?:json)?\s*", "", t)
    t2 = re.sub(r"\s*```$", "", t2)
    print("line 5 around col 27:", repr(t2.splitlines()[4][10:60]) if len(t2.splitlines()) > 4 else "?")
    print("fixed parse region:", repr(ga._fix_json_escapes(t2).splitlines()[4][10:60]) if len(ga._fix_json_escapes(t2).splitlines()) > 4 else "?")
