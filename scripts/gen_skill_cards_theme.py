# -*- coding: utf-8 -*-
"""Generate card-collection theme preview at docs/skills/book/cards/index.html."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "docs" / "skills"
OUT = SKILLS / "book" / "cards" / "index.html"
GROUP_ORDER = ["數與代數", "度量、圖形與空間", "數據處理"]


def main() -> None:
    book = json.loads((SKILLS / "math_skill_book.json").read_text(encoding="utf-8"))
    data = json.dumps(book, ensure_ascii=False)
    groups = json.dumps(GROUP_ORDER, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>風格 6｜卡片收集風技能冊｜DSE Hub</title>
<meta name="description" content="數學技能冊卡片收集風格預覽：每格知識點似遊戲卡，適合手機瀏覽。">
<link rel="canonical" href="https://hkdse.exampaper.cloud/skills/book/cards/">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$']] }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
:root {{
  --ink: #1c2430;
  --mut: #5d6b7c;
  --line: rgba(28,36,48,0.12);
  --desk: #e8eef5;
  --card: #fffdf8;
  --foil: #c9a44a;
  --rare: #3d7ea6;
  --epic: #6b4ea2;
  --locked: #8a93a0;
  --ok: #1f7a5c;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background:
    radial-gradient(900px 420px at 0% 0%, #d7e6f6 0%, transparent 55%),
    radial-gradient(800px 380px at 100% 10%, #f3e7cf 0%, transparent 50%),
    linear-gradient(180deg, #f4f7fb, var(--desk));
  font: 15px/1.55 "PingFang HK", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
}}
a {{ color: #1f5f8f; text-decoration: none; }}
.wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 16px 48px; }}
header.top {{
  position: sticky; top: 0; z-index: 10;
  backdrop-filter: blur(10px);
  background: rgba(244,247,251,0.9);
  border-bottom: 1px solid var(--line);
  padding: 12px 0;
}}
.top-inner {{
  max-width: 1100px; margin: 0 auto; padding: 0 16px;
  display: flex; justify-content: space-between; gap: 12px; align-items: center;
}}
.brand {{ font-weight: 800; letter-spacing: 0.02em; }}
.badge-style {{
  font-size: 12px; font-weight: 700;
  background: #1c2430; color: #fff;
  border-radius: 999px; padding: 4px 10px;
}}
.hero {{ padding: 22px 0 8px; }}
.hero h1 {{ margin: 0 0 8px; font-size: clamp(24px, 4vw, 34px); letter-spacing: -0.02em; }}
.hero p {{ margin: 0; color: var(--mut); max-width: 40rem; }}
.tabs {{
  display: flex; gap: 8px; overflow-x: auto; padding: 14px 0 8px;
  -webkit-overflow-scrolling: touch;
}}
.tab {{
  flex: 0 0 auto;
  appearance: none; border: 1px solid var(--line);
  background: #fff; color: var(--ink);
  border-radius: 999px; padding: 8px 14px;
  font-weight: 700; cursor: pointer;
}}
.tab.active {{
  background: #1c2430; color: #fff; border-color: #1c2430;
}}
.toolbar {{
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  margin: 8px 0 16px; color: var(--mut); font-size: 13px;
}}
.btn {{
  appearance: none; border: 1px solid var(--line);
  background: #fff; border-radius: 999px;
  padding: 8px 12px; font-weight: 700; cursor: pointer;
}}
.btn.primary {{
  background: linear-gradient(180deg, #f0d78a, #c9a44a);
  border-color: #b8923a; color: #2a1f08;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: 14px;
}}
.card {{
  position: relative;
  aspect-ratio: 3 / 4.2;
  border-radius: 18px;
  border: 1px solid var(--line);
  background: var(--card);
  box-shadow: 0 10px 24px rgba(28,36,48,0.08);
  padding: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease);
  text-align: left;
  color: inherit;
  font: inherit;
}}
.card:hover {{ transform: translateY(-4px) rotate(-0.4deg); box-shadow: 0 16px 30px rgba(28,36,48,0.14); }}
.card:focus-visible {{ outline: 2px solid #1f5f8f; outline-offset: 2px; }}
.card.selected {{
  box-shadow: 0 0 0 3px rgba(61,126,166,0.35), 0 16px 30px rgba(28,36,48,0.14);
  transform: translateY(-4px);
}}
.card.locked {{
  filter: grayscale(0.35);
  background: linear-gradient(160deg, #eef1f5, #dfe5ec);
}}
.card .rarity {{
  position: absolute; top: 10px; right: 10px;
  font-size: 10px; font-weight: 800; letter-spacing: 0.06em;
  padding: 3px 7px; border-radius: 999px; color: #fff;
}}
.card.r-common .rarity {{ background: #7a8694; }}
.card.r-rare .rarity {{ background: var(--rare); }}
.card.r-epic .rarity {{ background: var(--epic); }}
.card.r-legend .rarity {{ background: linear-gradient(90deg, #c9a44a, #8a5a1e); }}
.art {{
  height: 42%;
  border-radius: 12px;
  margin-top: 18px;
  display: grid; place-items: center;
  background:
    radial-gradient(circle at 30% 30%, rgba(255,255,255,0.7), transparent 45%),
    linear-gradient(145deg, #d9e8f6, #f7ecd7);
  border: 1px solid rgba(28,36,48,0.08);
  font-size: 34px;
}}
.card.locked .art {{
  background: linear-gradient(145deg, #cfd6df, #b8c0cb);
  color: #5a6572;
}}
.card .cid {{
  margin-top: 10px;
  font-size: 10px; color: var(--mut);
  font-family: ui-monospace, Consolas, monospace;
}}
.card .cname {{
  margin: 4px 0 0;
  font-size: 14px; font-weight: 800;
  line-height: 1.25;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}}
.status {{
  position: absolute; left: 10px; bottom: 10px;
  font-size: 11px; font-weight: 800;
  padding: 3px 8px; border-radius: 999px;
  border: 1px solid var(--line); background: #fff;
}}
.status.on {{ color: var(--ok); }}
.status.off {{ color: var(--locked); }}
.panel {{
  margin-top: 18px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 10px 24px rgba(28,36,48,0.06);
  min-height: 140px;
}}
.panel h2 {{ margin: 0 0 8px; font-size: 18px; }}
.panel .meta {{ color: var(--mut); font-size: 13px; margin-bottom: 10px; }}
.formula {{
  border: 1px dashed var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  margin-top: 8px;
  background: #fbfcfe;
}}
.formula .fid {{ font-size: 11px; color: var(--mut); font-family: ui-monospace, Consolas, monospace; }}
.empty {{ color: var(--mut); text-align: center; padding: 18px; }}
footer {{ margin-top: 22px; color: var(--mut); font-size: 13px; }}
</style>
</head>
<body>
<header class="top">
  <div class="top-inner">
    <div>
      <a href="../">← RPG 技能樹</a>
      · <a href="/skills/">技能地圖</a>
    </div>
    <div><span class="badge-style">風格 6 · 卡片收集</span></div>
  </div>
</header>
<main class="wrap">
  <section class="hero">
    <h1>卡片收集風預覽</h1>
    <p>每粒知識點係一張卡。已解鎖可以收進卡冊；未解鎖會變灰。適合手機左右掃、逐張睇。</p>
  </section>
  <div class="tabs" id="tabs"></div>
  <div class="toolbar">
    <span id="branchMeta"></span>
    <button type="button" class="btn primary" id="btnUnlock">解鎖選中卡</button>
    <button type="button" class="btn" id="btnReset">重置本課題</button>
    <span id="progress">進度 0%</span>
  </div>
  <div class="grid" id="grid"></div>
  <section class="panel" id="panel"><div class="empty">點一張卡睇詳情同公式</div></section>
  <footer>呢頁係風格預覽。解鎖進度同 RPG 樹分開儲存，唔會互相覆蓋。</footer>
</main>
<script id="BOOK" type="application/json">{data}</script>
<script>
(function(){{
  const book = JSON.parse(document.getElementById('BOOK').textContent);
  const groupOrder = {groups};
  const STORE = 'dsehub-card-theme-unlocks-v1';
  const icons = ['📐','🔢','📈','🔷','✳️','📘','🎯','🧩'];
  const kpName = {{}};
  const formulaByKp = {{}};
  book.topics.forEach(t => {{
    (t.knowledge_points||[]).forEach(k => kpName[k.id]=k.name);
    (t.formulas||[]).forEach(f => {{
      (formulaByKp[f.knowledge_point_id]=formulaByKp[f.knowledge_point_id]||[]).push(f);
    }});
  }});

  function load() {{ try {{ return JSON.parse(localStorage.getItem(STORE)||'{{}}')||{{}}; }} catch {{ return {{}}; }} }}
  function save(m) {{ localStorage.setItem(STORE, JSON.stringify(m)); }}
  let unlocks = load();
  book.topics.forEach(t => (t.knowledge_points||[]).forEach(k => {{
    if (!(k.prereqs||[]).length && unlocks[k.id] === undefined) unlocks[k.id] = true;
  }}));
  save(unlocks);

  function depth(kp, memo={{}}) {{
    if (memo[kp.id] != null) return memo[kp.id];
    const pre = kp.prereqs || [];
    if (!pre.length) return memo[kp.id]=0;
    const map = Object.fromEntries((current.knowledge_points||[]).map(x=>[x.id,x]));
    return memo[kp.id] = 1 + Math.max(...pre.map(id => map[id] ? depth(map[id], memo) : 0));
  }}
  function rarity(d) {{
    if (d >= 3) return ['legend','傳說'];
    if (d === 2) return ['epic','史詩'];
    if (d === 1) return ['rare','稀有'];
    return ['common','普通'];
  }}
  function canUnlock(kp) {{ return (kp.prereqs||[]).every(id => unlocks[id]); }}
  function allProgress() {{
    const ids=[]; book.topics.forEach(t=>(t.knowledge_points||[]).forEach(k=>ids.push(k.id)));
    const on=ids.filter(id=>unlocks[id]).length;
    return ids.length ? Math.round(100*on/ids.length) : 0;
  }}

  let current = book.topics[0];
  let selected = null;

  const tabs = document.getElementById('tabs');
  tabs.innerHTML = book.topics.map(t =>
    `<button type="button" class="tab" data-id="${{t.id}}">${{t.name}}</button>`
  ).join('');

  function typeset(el) {{
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([el]).catch(()=>{{}});
  }}

  function renderPanel() {{
    const panel = document.getElementById('panel');
    if (!selected) {{ panel.innerHTML = `<div class="empty">點一張卡睇詳情同公式</div>`; return; }}
    const kp = (current.knowledge_points||[]).find(k=>k.id===selected);
    if (!kp) return;
    const on = !!unlocks[kp.id];
    const ready = canUnlock(kp);
    const pre = (kp.prereqs||[]).map(id=>kpName[id]||id).join('、') || '無（起始卡）';
    const forms = (formulaByKp[kp.id]||[]).map(f=>`
      <div class="formula"><div class="fid">${{f.id}}</div><strong>${{f.name}}</strong>
      <div>$$${{f.latex}}$$</div></div>`).join('') || `<div class="empty">呢張卡未掛公式</div>`;
    panel.innerHTML = `
      <h2>${{kp.name}}</h2>
      <div class="meta">${{kp.id}} · ${{on?'已收集':(ready?'可以解鎖':'未解鎖')}} · 先要識：${{pre}}</div>
      ${{forms}}`;
    typeset(panel);
  }}

  function render() {{
    document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.id===current.id));
    document.getElementById('branchMeta').textContent =
      current.group + ' · ' + current.name + ' · ' + (current.knowledge_points||[]).length + ' 張卡';
    document.getElementById('progress').textContent = '總進度 ' + allProgress() + '%';
    const grid = document.getElementById('grid');
    const memo = {{}};
    grid.innerHTML = (current.knowledge_points||[]).map((k,i) => {{
      const d = depth(k, memo);
      const [rk, rn] = rarity(d);
      const on = !!unlocks[k.id];
      const icon = on ? icons[i % icons.length] : '🔒';
      return `<button type="button" class="card r-${{rk}} ${{on?'':'locked'}} ${{selected===k.id?'selected':''}}" data-id="${{k.id}}">
        <span class="rarity">${{rn}}</span>
        <div class="art">${{icon}}</div>
        <div class="cid">${{k.id}}</div>
        <div class="cname">${{k.name}}</div>
        <span class="status ${{on?'on':'off'}}">${{on?'已收集':'未收集'}}</span>
      </button>`;
    }}).join('');
    renderPanel();
  }}

  tabs.addEventListener('click', e => {{
    const b = e.target.closest('.tab'); if (!b) return;
    current = book.topics.find(t=>t.id===b.dataset.id);
    selected = null; render();
  }});
  document.getElementById('grid').addEventListener('click', e => {{
    const c = e.target.closest('.card'); if (!c) return;
    selected = c.dataset.id; render();
  }});
  document.getElementById('btnUnlock').addEventListener('click', () => {{
    if (!selected) return;
    const kp = (current.knowledge_points||[]).find(k=>k.id===selected);
    if (!kp) return;
    if (unlocks[kp.id]) return;
    if (!canUnlock(kp)) {{ alert('仲未滿足先備卡，唔可以解鎖'); return; }}
    unlocks[kp.id]=true; save(unlocks); render();
  }});
  document.getElementById('btnReset').addEventListener('click', () => {{
    (current.knowledge_points||[]).forEach(k => {{ unlocks[k.id] = !(k.prereqs||[]).length; }});
    save(unlocks); selected=null; render();
  }});

  render();
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
