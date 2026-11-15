# -*- coding: utf-8 -*-
import json, re, sys

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
            out.append(t[i : i + 2])
            i += 2
            continue
        out.append("\\\\")
        i += 1
    return "".join(out)

def parse(t):
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return json.loads(_fix_json_escapes(t))

cases = [
    # (原始輸出, 期望解析結果)
    (r'{"a": "$\dfrac{1}{2} \times \theta$"}', "$\\dfrac{1}{2} \\times \\theta$"),
    (r'{"a": "$\\dfrac{1}{2}$ 已正確跳脫"}', "$\\dfrac{1}{2}$ 已正確跳脫"),
    (r'{"a": "第一行\n第二行\t- 點列"}', "第一行\n第二行\t- 點列"),
    (r'{"a": "你好 合法 unicode"}', "你好 合法 unicode"),
    (r'{"a": "$30^\circ$, $\angle ABC$"}', "$30^\\circ$, $\\angle ABC$"),
    (r'{"a": "$\sin\theta$, $\sqrt{2}$, $\frac{a}{b}$"}', "$\\sin\\theta$, $\\sqrt{2}$, $\\frac{a}{b}$"),
    (r'{"a": "$\underbrace{6}$"}', "$\\underbrace{6}$"),
    (r'{"a": "set A $A \subset B$ 且 $\pi \approx 3.14$"}', "set A $A \\subset B$ 且 $\\pi \\approx 3.14$"),
    (r'{"a": "分行\n- A\n- B"}', "分行\n- A\n- B"),
    (r'{"a": "$x \leq 5$ 同 $y \ne 3$"}', "$x \\leq 5$ 同 $y \\ne 3$"),
    (r'{"a": "\t縮排"}', "\t縮排"),
]
fails = 0
for raw, expect in cases:
    try:
        got = parse(raw)["a"]
        if got == expect:
            print("OK ", repr(got))
        else:
            fails += 1
            print("DIFF", repr(got), "!= expected", repr(expect))
    except Exception as e:
        fails += 1
        print("FAIL", e)
sys.exit(1 if fails else 0)
