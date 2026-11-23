# -*- coding: utf-8 -*-
"""Generate interactive visual skill book at docs/skills/book/index.html."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "docs" / "skills"
OUT = SKILLS / "book" / "index.html"

GROUP_ORDER = ["數與代數", "度量、圖形與空間", "數據處理"]
GROUP_TONE = {
    "數與代數": "alg",
    "度量、圖形與空間": "geo",
    "數據處理": "data",
}


def main() -> None:
    book = json.loads((SKILLS / "math_skill_book.json").read_text(encoding="utf-8"))
    data_json = json.dumps(book, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>數學技能冊（視覺版）｜20 課題 · 知識點 · 公式｜DSE Hub</title>
<meta name="description" content="DSE 數學必修技能冊視覺瀏覽：20 大課題、知識點先後、公式同 8 種能力。">
<link rel="canonical" href="https://hkdse.exampaper.cloud/skills/book/">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
:root {{
  --ink: #14201a;
  --mut: #5a6b62;
  --line: rgba(20, 32, 26, 0.12);
  --paper: #f3f6f2;
  --panel: #ffffff;
  --alg: #1f6f5a;
  --alg-soft: #d8efe6;
  --geo: #2a5f8f;
  --geo-soft: #d7e6f4;
  --data: #8a5a1e;
  --data-soft: #f3e6cf;
  --acc: #1f6f5a;
  --shadow: 0 10px 28px rgba(20, 32, 26, 0.08);
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background:
    radial-gradient(1200px 500px at 10% -10%, #e4f0ea 0%, transparent 55%),
    radial-gradient(900px 420px at 100% 0%, #e3ebf4 0%, transparent 50%),
    var(--paper);
  font: 16px/1.65 "PingFang HK", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--acc); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 18px; }}
header.site {{
  position: sticky; top: 0; z-index: 20;
  backdrop-filter: blur(10px);
  background: rgba(243, 246, 242, 0.88);
  border-bottom: 1px solid var(--line);
}}
header.site .wrap {{
  display: flex; align-items: center; justify-content: space-between;
  gap: 12px; padding: 12px 18px; font-size: 14px; color: var(--mut);
}}
.brand {{ font-weight: 700; color: var(--ink); letter-spacing: 0.02em; }}
.hero {{
  padding: 36px 0 8px;
  animation: rise 0.7s var(--ease) both;
}}
.hero h1 {{
  margin: 0 0 10px;
  font-size: clamp(28px, 4.5vw, 42px);
  line-height: 1.15;
  letter-spacing: -0.02em;
}}
.hero p {{
  margin: 0;
  max-width: 42rem;
  color: var(--mut);
  font-size: 17px;
}}
.stats {{
  display: flex; flex-wrap: wrap; gap: 10px;
  margin: 22px 0 8px;
  animation: rise 0.8s var(--ease) 0.08s both;
}}
.stat {{
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 14px;
  box-shadow: var(--shadow);
}}
.stat b {{ font-variant-numeric: tabular-nums; }}
.abilities {{
  margin: 28px 0 10px;
  animation: rise 0.8s var(--ease) 0.12s both;
}}
.abilities h2 {{ margin: 0 0 10px; font-size: 15px; color: var(--mut); font-weight: 600; }}
.ability-row {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 8px;
}}
.ability {{
  background: rgba(255,255,255,0.72);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 13px;
  transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease);
}}
.ability:hover {{ transform: translateY(-2px); box-shadow: var(--shadow); }}
.ability strong {{ display: block; font-size: 14px; margin-bottom: 2px; }}
.ability span {{ color: var(--mut); font-size: 12px; line-height: 1.4; }}
.section {{ margin: 34px 0 10px; animation: rise 0.75s var(--ease) both; }}
.section-head {{
  display: flex; align-items: baseline; justify-content: space-between;
  gap: 12px; margin-bottom: 12px;
}}
.section-head h2 {{ margin: 0; font-size: 22px; letter-spacing: -0.01em; }}
.section-head .count {{ color: var(--mut); font-size: 13px; }}
.tone-alg .section-head h2 {{ color: var(--alg); }}
.tone-geo .section-head h2 {{ color: var(--geo); }}
.tone-data .section-head h2 {{ color: var(--data); }}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}}
.tile {{
  appearance: none; border: 1px solid var(--line);
  background: var(--panel);
  border-radius: 16px;
  padding: 16px 16px 14px;
  text-align: left;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform 0.28s var(--ease), border-color 0.28s var(--ease), box-shadow 0.28s var(--ease);
}}
.tile:hover {{ transform: translateY(-3px); }}
.tile:focus-visible {{ outline: 2px solid var(--acc); outline-offset: 2px; }}
.tile.active {{ border-color: currentColor; box-shadow: 0 12px 30px rgba(20,32,26,0.14); }}
.tone-alg .tile {{ color: var(--alg); }}
.tone-geo .tile {{ color: var(--geo); }}
.tone-data .tile {{ color: var(--data); }}
.tile .name {{ color: var(--ink); font-size: 17px; font-weight: 700; margin: 0 0 8px; }}
.tile .meta {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.chip {{
  font-size: 12px; color: var(--mut);
  background: rgba(20,32,26,0.04);
  border-radius: 999px; padding: 3px 8px;
}}
.tone-alg .tile.active {{ background: var(--alg-soft); }}
.tone-geo .tile.active {{ background: var(--geo-soft); }}
.tone-data .tile.active {{ background: var(--data-soft); }}
.detail {{
  margin: 28px 0 60px;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 20px;
  box-shadow: var(--shadow);
  overflow: hidden;
  min-height: 220px;
  animation: rise 0.55s var(--ease) both;
}}
.detail-empty {{
  padding: 48px 28px;
  color: var(--mut);
  text-align: center;
}}
.detail-head {{
  padding: 22px 24px 14px;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(180deg, rgba(255,255,255,0.2), transparent);
}}
.detail-head .eyebrow {{
  font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--mut); margin: 0 0 6px;
}}
.detail-head h3 {{ margin: 0 0 6px; font-size: 26px; letter-spacing: -0.02em; }}
.detail-head .id {{ font-size: 13px; color: var(--mut); font-family: ui-monospace, Consolas, monospace; }}
.detail-body {{
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 0;
}}
@media (max-width: 820px) {{
  .detail-body {{ grid-template-columns: 1fr; }}
}}
.col {{ padding: 18px 22px 24px; }}
.col + .col {{ border-left: 1px solid var(--line); }}
@media (max-width: 820px) {{
  .col + .col {{ border-left: 0; border-top: 1px solid var(--line); }}
}}
.col h4 {{
  margin: 0 0 12px;
  font-size: 13px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--mut);
}}
.kp {{
  position: relative;
  padding: 12px 12px 12px 14px;
  border-left: 3px solid var(--line);
  margin: 0 0 10px;
  border-radius: 0 10px 10px 0;
  background: rgba(20,32,26,0.02);
}}
.kp .kid {{
  font-size: 11px; color: var(--mut);
  font-family: ui-monospace, Consolas, monospace;
}}
.kp .kname {{ font-weight: 700; margin: 2px 0 4px; }}
.prereqs {{ font-size: 12px; color: var(--mut); }}
.prereqs code {{
  font-size: 11px;
  background: rgba(20,32,26,0.06);
  padding: 1px 5px;
  border-radius: 4px;
}}
.formula {{
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 12px;
  margin: 0 0 10px;
  background: #fbfcfb;
}}
.formula .fname {{ font-weight: 700; margin-bottom: 4px; }}
.formula .fid {{
  font-size: 11px; color: var(--mut);
  font-family: ui-monospace, Consolas, monospace;
}}
.formula .latex {{
  margin-top: 6px;
  overflow-x: auto;
  font-size: 15px;
}}
footer.page {{
  color: var(--mut);
  font-size: 13px;
  padding: 0 0 48px;
}}
@keyframes rise {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
</head>
<body>
<header class="site">
  <div class="wrap">
    <div><a href="/hub/">← DSE Hub</a> · <a href="/skills/">技能地圖</a></div>
    <div class="brand">數學技能冊</div>
  </div>
</header>
<main class="wrap">
  <section class="hero">
    <h1>數學技能冊（視覺版）</h1>
    <p>點一個課題，就會睇到佢下面嘅細知識點、要先識咩、同常用公式。全部編號固定，之後計分同報告都用同一套。</p>
    <div class="stats" id="stats"></div>
  </section>

  <section class="abilities">
    <h2>全科共用 8 種能力</h2>
    <div class="ability-row" id="abilities"></div>
  </section>

  <div id="groups"></div>

  <section class="detail" id="detail" aria-live="polite">
    <div class="detail-empty">← 上面揀一個課題，細節會喺呢度出現</div>
  </section>

  <footer class="page">
    技能分類為本站整理，非考評局官方。<br>
    <a href="/skills/">技能地圖總覽</a> · <a href="/hub/">DSE Hub</a>
  </footer>
</main>
<script id="BOOK_DATA" type="application/json">{data_json}</script>
<script>
(function () {{
  const book = JSON.parse(document.getElementById('BOOK_DATA').textContent);
  const groupOrder = {json.dumps(GROUP_ORDER, ensure_ascii=False)};
  const toneMap = {json.dumps(GROUP_TONE, ensure_ascii=False)};
  const kpIndex = {{}};
  book.topics.forEach(t => (t.knowledge_points || []).forEach(k => {{ kpIndex[k.id] = k.name; }}));

  const nKp = book.topics.reduce((s, t) => s + (t.knowledge_points || []).length, 0);
  const nF = book.topics.reduce((s, t) => s + (t.formulas || []).length, 0);
  document.getElementById('stats').innerHTML = [
    ['課題', book.topics.length],
    ['知識點', nKp],
    ['公式', nF],
    ['能力', book.abilities.length],
  ].map(([k, v]) => `<div class="stat"><b>${{v}}</b> ${{k}}</div>`).join('');

  document.getElementById('abilities').innerHTML = book.abilities.map(a =>
    `<div class="ability" title="${{a.id}}"><strong>${{a.name}}</strong><span>${{a.desc || ''}}</span></div>`
  ).join('');

  const byGroup = {{}};
  book.topics.forEach(t => {{
    const g = t.group || '其他';
    (byGroup[g] = byGroup[g] || []).push(t);
  }});

  const groupsEl = document.getElementById('groups');
  groupsEl.innerHTML = groupOrder.filter(g => byGroup[g]).map(g => {{
    const tone = toneMap[g] || 'alg';
    const tiles = byGroup[g].map(t => `
      <button type="button" class="tile" data-id="${{t.id}}" aria-pressed="false">
        <div class="name">${{t.name}}</div>
        <div class="meta">
          <span class="chip">${{(t.knowledge_points || []).length}} 知識點</span>
          <span class="chip">${{(t.formulas || []).length}} 公式</span>
        </div>
      </button>`).join('');
    return `<section class="section tone-${{tone}}">
      <div class="section-head"><h2>${{g}}</h2><div class="count">${{byGroup[g].length}} 個課題</div></div>
      <div class="grid">${{tiles}}</div>
    </section>`;
  }}).join('');

  const detail = document.getElementById('detail');
  let selected = null;

  function typeset(node) {{
    if (window.MathJax && MathJax.typesetPromise) {{
      MathJax.typesetPromise([node]).catch(() => {{}});
    }}
  }}

  function showTopic(id) {{
    const t = book.topics.find(x => x.id === id);
    if (!t) return;
    selected = id;
    document.querySelectorAll('.tile').forEach(el => {{
      const on = el.dataset.id === id;
      el.classList.toggle('active', on);
      el.setAttribute('aria-pressed', on ? 'true' : 'false');
    }});
    const kps = (t.knowledge_points || []).map(k => {{
      const pre = (k.prereqs || []).map(p => `<code title="${{kpIndex[p] || p}}">${{p}}</code>`).join(' ') || '無（起點）';
      return `<div class="kp">
        <div class="kid">${{k.id}}</div>
        <div class="kname">${{k.name}}</div>
        <div class="prereqs">先要識：${{pre}}</div>
      </div>`;
    }}).join('') || '<p style="color:var(--mut)">未有知識點</p>';

    const formulas = (t.formulas || []).map(f => `
      <div class="formula">
        <div class="fid">${{f.id}} · 掛喺 ${{f.knowledge_point_id}}</div>
        <div class="fname">${{f.name}}</div>
        <div class="latex">$$${{f.latex}}$$</div>
      </div>`).join('') || '<p style="color:var(--mut)">未有公式</p>';

    detail.innerHTML = `
      <div class="detail-head">
        <p class="eyebrow">${{t.group || ''}}</p>
        <h3>${{t.name}}</h3>
        <div class="id">${{t.id}}</div>
      </div>
      <div class="detail-body">
        <div class="col"><h4>知識點（有先後）</h4>${{kps}}</div>
        <div class="col"><h4>公式</h4>${{formulas}}</div>
      </div>`;
    typeset(detail);
    detail.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
  }}

  groupsEl.addEventListener('click', (e) => {{
    const btn = e.target.closest('.tile');
    if (!btn) return;
    showTopic(btn.dataset.id);
  }});

  // open first topic by default for an immediate visual
  if (book.topics[0]) showTopic(book.topics[0].id);
}})();
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
