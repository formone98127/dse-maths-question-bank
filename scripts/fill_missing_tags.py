#!/usr/bin/env python3
"""補齊題庫 tags：① 解答沿用同一題目的 tags；② 手動補 5 條冇標籤的 MC 題。
保留原 data.js 結構（BOM、window.QB = …、indent=1）。
"""
import json, re, sys
from collections import Counter

P = '/home/one/hub_repo/docs/data.js'
raw = open(P, encoding='utf-8-sig').read()
start = raw.index('{'); end = raw.rindex('}')
data = json.loads(raw[start:end+1])
qs = data['questions']

MANUAL = {
    ('2019', 'Paper 2', '16'): ['四邊形', '面積比', '比率與比例'],
    ('2019', 'Paper 2', '38'): ['扇形面積', '三角形面積'],
    ('2016', 'Paper 2', '11'): ['比率與比例', '代數化簡'],
    ('2016', 'Paper 2', '20'): ['面積比', '四邊形'],
    ('2016', 'Paper 2', '23'): ['對稱軸', '對稱'],
}

# 索引：題目 tags
qtag = {}
for q in qs:
    if q['type'] == '題目' and q.get('tags'):
        qtag.setdefault((str(q['year']), q['paper'], str(q['qno'])), q['tags'])

n_sol = n_manual = 0
for q in qs:
    key = (str(q['year']), q['paper'], str(q['qno']))
    if not q.get('tags'):
        if q['type'] == '解答' and key in qtag:
            q['tags'] = list(qtag[key]); n_sol += 1
        elif q['type'] == '題目' and key in MANUAL:
            q['tags'] = list(MANUAL[key]); n_manual += 1

data['count'] = len(qs)
out = 'window.QB = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n'
open(P, 'w', encoding='utf-8').write(out)

left = [q for q in qs if not q.get('tags')]
print(f'解答補 tags: {n_sol}；手動補: {n_manual}；仍無 tags: {len(left)}')
print('count:', len(qs))
