#!/usr/bin/env python3
"""把官方 MS「答對率」寫入 docs/data.js 的 answer_pct（Paper 2 題目）。

來源：/tmp/mc_pct.json  {year: {qno: [letter, pct]}}
- 2012/2018 來自 dse_scan/question-bank/cleaned*_p2/*.json
- 2013/2016/2019/2020/2025 由官方 MS 尾頁逐個讀出，並與 answers.js 對卷核對過（0 不符）
"""
import json

P = '/home/one/hub_repo/docs/data.js'
pct = json.load(open('/tmp/mc_pct.json'))
raw = open(P, encoding='utf-8-sig').read()
data = json.loads(raw[raw.index('{'):raw.rindex('}')+1])

n_ans = n_pct = 0
for q in data['questions']:
    if q['type'] != '題目':
        continue
    y = str(q['year'])
    if y not in pct or q['paper'] != 'Paper 2':
        continue
    e = pct[y].get(str(q['qno']))
    if not e:
        continue
    letter, p = e
    if not q.get('answer'):
        q['answer'] = letter
        n_ans += 1
    q['answer_pct'] = p
    n_pct += 1

data['count'] = len(data['questions'])
open(P, 'w', encoding='utf-8').write('window.QB = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')

qs = data['questions']
print(f'answer 補 {n_ans} 條；answer_pct 寫入 {n_pct} 條')
by_year = {}
for q in qs:
    if q.get('answer_pct') is not None:
        by_year[str(q['year'])] = by_year.get(str(q['year']), 0) + 1
print('每年有答對率題數:', dict(sorted(by_year.items())))
print('total questions:', len(qs))
