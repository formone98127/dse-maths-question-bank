# -*- coding: utf-8 -*-
"""Generate RPG-style interactive skill tree at docs/skills/book/index.html.

Uses vendored Cytoscape + ELK (+ Pixi sparkle). Data from math_skill_book.json.
"""
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
<title>數學 RPG 技能樹｜20 課題 · 知識點解鎖｜DSE Hub</title>
<meta name="description" content="DSE 數學必修 RPG 技能樹：點撃解鎖知識點、睇先備關係同公式。">
<link rel="canonical" href="https://hkdse.exampaper.cloud/skills/book/">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<script src="vendor/cytoscape.min.js"></script>
<script src="vendor/elk.bundled.js"></script>
<script src="vendor/cytoscape-elk.js"></script>
<script src="vendor/pixi.min.js"></script>
<style>
:root {{
  --ink: #f4e8c8;
  --mut: #b7a789;
  --line: rgba(244, 232, 200, 0.14);
  --panel: rgba(18, 14, 10, 0.88);
  --panel-solid: #16110d;
  --gold: #e2c36b;
  --gold-2: #9a7420;
  --alg: #6fd6b0;
  --geo: #7db4e8;
  --data: #e0b06a;
  --locked: #6a6f78;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}}
* {{ box-sizing: border-box; }}
html, body {{ height: 100%; }}
body {{
  margin: 0;
  color: var(--ink);
  background: #070605 url("assets/bg-map.svg") center / cover fixed;
  font: 15px/1.55 "PingFang HK", "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
  -webkit-font-smoothing: antialiased;
  overflow: hidden;
}}
a {{ color: var(--gold); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.app {{
  display: grid;
  grid-template-rows: auto 1fr;
  height: 100%;
  height: 100dvh;
}}
.top {{
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 16px;
  background: linear-gradient(180deg, rgba(10,8,6,0.95), rgba(10,8,6,0.72));
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(8px);
  z-index: 5;
}}
.brand {{ font-weight: 800; letter-spacing: 0.04em; color: var(--gold); }}
.top-nav {{ display: flex; gap: 14px; flex-wrap: wrap; font-size: 13px; color: var(--mut); }}
.main {{
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  min-height: 0;
}}
@media (max-width: 980px) {{
  body {{ overflow: auto; }}
  .app {{ height: auto; min-height: 100dvh; }}
  .main {{ grid-template-columns: 1fr; grid-template-rows: auto 55vh auto; }}
}}
.side, .info {{
  background: var(--panel);
  border-right: 1px solid var(--line);
  overflow: auto;
  padding: 14px;
}}
.info {{ border-right: 0; border-left: 1px solid var(--line); }}
.side h2, .info h2 {{
  margin: 0 0 10px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--mut);
}}
.stats {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
  margin-bottom: 14px;
}}
.stat {{
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px;
  background: rgba(255,255,255,0.03);
}}
.stat b {{ display: block; font-size: 20px; color: var(--gold); font-variant-numeric: tabular-nums; }}
.stat span {{ font-size: 12px; color: var(--mut); }}
.group-label {{
  margin: 14px 0 8px;
  font-size: 13px; font-weight: 700;
}}
.group-label.alg {{ color: var(--alg); }}
.group-label.geo {{ color: var(--geo); }}
.group-label.data {{ color: var(--data); }}
.topic-list {{ display: grid; gap: 8px; }}
.topic-btn {{
  appearance: none; width: 100%;
  text-align: left;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.03);
  color: var(--ink);
  border-radius: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: transform 0.2s var(--ease), border-color 0.2s, background 0.2s;
}}
.topic-btn:hover {{ transform: translateY(-1px); border-color: rgba(226,195,107,0.45); }}
.topic-btn.active {{
  border-color: var(--gold);
  background: linear-gradient(135deg, rgba(226,195,107,0.18), rgba(255,255,255,0.03));
  box-shadow: 0 0 0 1px rgba(226,195,107,0.25) inset;
}}
.topic-btn .name {{ font-weight: 700; display: block; margin-bottom: 4px; }}
.topic-btn .meta {{ font-size: 12px; color: var(--mut); }}
.stage-wrap {{
  position: relative;
  min-height: 0;
  background: rgba(0,0,0,0.25);
}}
#cy {{
  position: absolute; inset: 0;
}}
#fx {{
  position: absolute; inset: 0; pointer-events: none; z-index: 2;
}}
.hint-bar {{
  position: absolute; left: 12px; right: 12px; bottom: 12px; z-index: 3;
  display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
  pointer-events: none;
}}
.hint-bar > * {{ pointer-events: auto; }}
.pill {{
  background: rgba(12,10,8,0.85);
  border: 1px solid var(--line);
  color: var(--mut);
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 12px;
}}
.btn {{
  appearance: none;
  border: 1px solid var(--gold-2);
  background: linear-gradient(180deg, #e2c36b, #9a7420);
  color: #1a1208;
  font-weight: 800;
  border-radius: 999px;
  padding: 8px 14px;
  cursor: pointer;
  font-size: 13px;
}}
.btn.ghost {{
  background: rgba(12,10,8,0.85);
  color: var(--ink);
  border-color: var(--line);
  font-weight: 600;
}}
.empty {{
  color: var(--mut);
  padding: 24px 8px;
  text-align: center;
}}
.ability-row {{ display: grid; gap: 6px; margin-bottom: 16px; }}
.ability {{
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 12px;
  background: rgba(255,255,255,0.03);
}}
.ability strong {{ display: block; color: var(--gold); margin-bottom: 2px; }}
.kp-card, .formula {{
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 10px;
  background: rgba(255,255,255,0.03);
}}
.kp-card.locked {{ opacity: 0.55; }}
.kp-card .id, .formula .id {{
  font-size: 11px; color: var(--mut);
  font-family: ui-monospace, Consolas, monospace;
}}
.kp-card h3, .formula h3 {{
  margin: 4px 0 8px; font-size: 16px;
}}
.badge {{
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid var(--line);
  margin-right: 6px;
}}
.badge.on {{ color: #9dffd0; border-color: rgba(157,255,208,0.35); }}
.badge.off {{ color: var(--locked); }}
.prereq {{ font-size: 12px; color: var(--mut); margin-top: 6px; }}
.latex {{ overflow-x: auto; margin-top: 6px; color: #fff; }}
.legend {{
  display: flex; gap: 10px; flex-wrap: wrap;
  font-size: 12px; color: var(--mut); margin-bottom: 12px;
}}
.legend i {{
  display: inline-block; width: 10px; height: 10px; border-radius: 50%;
  margin-right: 4px; vertical-align: middle;
}}
.legend .l-on {{ background: #2f9b78; }}
.legend .l-off {{ background: #5a6270; }}
.legend .l-sel {{ background: #e2c36b; }}
</style>
</head>
<body>
<div class="app">
  <header class="top">
    <div class="brand">數學 RPG 技能樹</div>
    <nav class="top-nav">
      <a href="/hub/">DSE Hub</a>
      <a href="/skills/">技能地圖</a>
      <a href="cards/">風格6 卡片收集</a>
      <span id="progressLabel">進度 0%</span>
    </nav>
  </header>
  <div class="main">
    <aside class="side">
      <h2>冒險進度</h2>
      <div class="stats" id="stats"></div>
      <div class="legend">
        <span><i class="l-on"></i>已解鎖</span>
        <span><i class="l-off"></i>未解鎖</span>
        <span><i class="l-sel"></i>選中</span>
      </div>
      <h2>選擇技能分支</h2>
      <div id="topicList"></div>
    </aside>
    <section class="stage-wrap">
      <div id="cy"></div>
      <canvas id="fx"></canvas>
      <div class="hint-bar">
        <div class="pill" id="branchHint">揀左邊一個課題開始</div>
        <button type="button" class="btn" id="btnUnlock">解鎖選中技能</button>
        <button type="button" class="btn ghost" id="btnReset">重置本分支進度</button>
        <button type="button" class="btn ghost" id="btnFit">置中地圖</button>
      </div>
    </section>
    <aside class="info">
      <h2>全科能力</h2>
      <div class="ability-row" id="abilities"></div>
      <h2>技能詳情</h2>
      <div id="detail"><div class="empty">點地圖上嘅技能格，睇知識點同公式</div></div>
    </aside>
  </div>
</div>
<script id="BOOK_DATA" type="application/json">{data_json}</script>
<script>
(function () {{
  const book = JSON.parse(document.getElementById('BOOK_DATA').textContent);
  const groupOrder = {json.dumps(GROUP_ORDER, ensure_ascii=False)};
  const toneMap = {json.dumps(GROUP_TONE, ensure_ascii=False)};
  const STORE_KEY = 'dsehub-rpg-skill-unlocks-v1';

  if (window.cytoscapeElk && window.cytoscape && window.ELK) {{
    cytoscape.use(cytoscapeElk);
  }}

  const kpName = {{}};
  const formulaByKp = {{}};
  book.topics.forEach(t => {{
    (t.knowledge_points || []).forEach(k => {{ kpName[k.id] = k.name; }});
    (t.formulas || []).forEach(f => {{
      (formulaByKp[f.knowledge_point_id] = formulaByKp[f.knowledge_point_id] || []).push(f);
    }});
  }});

  const nKp = book.topics.reduce((s, t) => s + (t.knowledge_points || []).length, 0);
  const nF = book.topics.reduce((s, t) => s + (t.formulas || []).length, 0);
  document.getElementById('stats').innerHTML = [
    ['課題', book.topics.length],
    ['知識點', nKp],
    ['公式', nF],
    ['能力', book.abilities.length],
  ].map(([k, v]) => `<div class="stat"><b>${{v}}</b><span>${{k}}</span></div>`).join('');

  document.getElementById('abilities').innerHTML = book.abilities.map(a =>
    `<div class="ability"><strong>${{a.name}}</strong>${{a.desc || ''}}</div>`
  ).join('');

  function loadUnlocks() {{
    try {{ return JSON.parse(localStorage.getItem(STORE_KEY) || '{{}}') || {{}}; }}
    catch {{ return {{}}; }}
  }}
  function saveUnlocks(map) {{
    localStorage.setItem(STORE_KEY, JSON.stringify(map));
  }}
  let unlocks = loadUnlocks(); // {{ [kpId]: true }}

  // seed roots unlocked for first-time users
  book.topics.forEach(t => {{
    (t.knowledge_points || []).forEach(k => {{
      if (!(k.prereqs || []).length && unlocks[k.id] === undefined) unlocks[k.id] = true;
    }});
  }});
  saveUnlocks(unlocks);

  function progressPct() {{
    const ids = [];
    book.topics.forEach(t => (t.knowledge_points || []).forEach(k => ids.push(k.id)));
    const on = ids.filter(id => unlocks[id]).length;
    return ids.length ? Math.round(100 * on / ids.length) : 0;
  }}
  function refreshProgress() {{
    document.getElementById('progressLabel').textContent = '進度 ' + progressPct() + '%';
  }}
  refreshProgress();

  const byGroup = {{}};
  book.topics.forEach(t => {{
    const g = t.group || '其他';
    (byGroup[g] = byGroup[g] || []).push(t);
  }});
  const list = document.getElementById('topicList');
  list.innerHTML = groupOrder.filter(g => byGroup[g]).map(g => {{
    const tone = toneMap[g] || 'alg';
    const buttons = byGroup[g].map(t => `
      <button type="button" class="topic-btn" data-id="${{t.id}}">
        <span class="name">${{t.name}}</span>
        <span class="meta">${{(t.knowledge_points || []).length}} 技能格 · ${{(t.formulas || []).length}} 公式</span>
      </button>`).join('');
    return `<div class="group-label ${{tone}}">${{g}}</div><div class="topic-list">${{buttons}}</div>`;
  }}).join('');

  let currentTopicId = null;
  let selectedKp = null;
  let cy = null;

  function canUnlock(kp) {{
    const pre = kp.prereqs || [];
    return pre.every(id => unlocks[id]);
  }}

  function typeset(node) {{
    if (window.MathJax && MathJax.typesetPromise) {{
      MathJax.typesetPromise([node]).catch(() => {{}});
    }}
  }}

  function showDetail(topic, kpId) {{
    const box = document.getElementById('detail');
    if (!kpId) {{
      box.innerHTML = `<div class="empty">點地圖上嘅技能格，睇知識點同公式</div>`;
      return;
    }}
    const kp = (topic.knowledge_points || []).find(k => k.id === kpId);
    if (!kp) return;
    const unlocked = !!unlocks[kp.id];
    const ready = canUnlock(kp);
    const pre = (kp.prereqs || []).map(id => kpName[id] || id).join('、') || '無（起點技能）';
    const formulas = (formulaByKp[kp.id] || []).map(f => `
      <div class="formula">
        <div class="id">${{f.id}}</div>
        <h3>${{f.name}}</h3>
        <div class="latex">$$${{f.latex}}$$</div>
      </div>`).join('') || `<div class="empty">呢格未掛公式</div>`;
    box.innerHTML = `
      <div class="kp-card ${{unlocked ? '' : 'locked'}}">
        <div class="id">${{kp.id}}</div>
        <h3>${{kp.name}}</h3>
        <span class="badge ${{unlocked ? 'on' : 'off'}}">${{unlocked ? '已解鎖' : (ready ? '可解鎖' : '未解鎖')}}</span>
        <div class="prereq">先要識：${{pre}}</div>
      </div>
      <h2>相關公式</h2>
      ${{formulas}}`;
    typeset(box);
  }}

  // Pixi sparkle layer
  let sparkApp = null;
  async function ensureFx() {{
    try {{
      const canvas = document.getElementById('fx');
      const wrap = document.querySelector('.stage-wrap');
      const w = wrap.clientWidth || 800;
      const h = wrap.clientHeight || 600;
      canvas.width = w; canvas.height = h;
      if (!window.PIXI) return null;
      if (sparkApp) {{
        sparkApp.renderer.resize(w, h);
        return sparkApp;
      }}
      sparkApp = new PIXI.Application();
      await sparkApp.init({{
        canvas,
        width: w,
        height: h,
        backgroundAlpha: 0,
        antialias: true,
      }});
      return sparkApp;
    }} catch (err) {{
      console.warn('Pixi FX unavailable', err);
      return null;
    }}
  }}
  async function sparkleAt(x, y) {{
    const app = await ensureFx();
    if (!app) return;
    for (let i = 0; i < 18; i++) {{
      const g = new PIXI.Graphics();
      g.circle(0, 0, 2 + Math.random() * 3);
      g.fill(0xffe9a8);
      g.x = x; g.y = y;
      app.stage.addChild(g);
      const ang = Math.random() * Math.PI * 2;
      const dist = 30 + Math.random() * 70;
      const life = 400 + Math.random() * 400;
      const t0 = performance.now();
      const tick = () => {{
        const t = (performance.now() - t0) / life;
        if (t >= 1) {{ app.stage.removeChild(g); g.destroy(); return; }}
        g.x = x + Math.cos(ang) * dist * t;
        g.y = y + Math.sin(ang) * dist * t;
        g.alpha = 1 - t;
        requestAnimationFrame(tick);
      }};
      requestAnimationFrame(tick);
    }}
  }}

  function buildElements(topic) {{
    const nodes = [];
    const edges = [];
    (topic.knowledge_points || []).forEach(k => {{
      const unlocked = !!unlocks[k.id];
      nodes.push({{
        data: {{
          id: k.id,
          label: k.name,
          unlocked,
          ready: canUnlock(k),
        }},
        classes: unlocked ? 'unlocked' : (canUnlock(k) ? 'ready' : 'locked'),
      }});
      (k.prereqs || []).forEach(p => {{
        edges.push({{ data: {{ id: p + '->' + k.id, source: p, target: k.id }} }});
      }});
    }});
    return nodes.concat(edges);
  }}

  function styleFor() {{
    return [
      {{
        selector: 'node',
        style: {{
          'background-fit': 'cover',
          'background-clip': 'none',
          'background-opacity': 1,
          'background-color': 'transparent',
          'border-width': 0,
          'width': 70,
          'height': 70,
          'label': 'data(label)',
          'color': '#f4e8c8',
          'text-valign': 'bottom',
          'text-halign': 'center',
          'text-margin-y': 8,
          'font-size': 12,
          'font-weight': 700,
          'text-wrap': 'wrap',
          'text-max-width': 110,
          'text-outline-width': 2,
          'text-outline-color': '#0a0806',
          'overlay-padding': 8,
        }}
      }},
      {{
        selector: 'node.unlocked',
        style: {{ 'background-image': 'assets/node-unlocked.png' }}
      }},
      {{
        selector: 'node.ready',
        style: {{
          'background-image': 'assets/node-locked.svg',
          'border-width': 2,
          'border-color': '#e2c36b',
        }}
      }},
      {{
        selector: 'node.locked',
        style: {{ 'background-image': 'assets/node-locked.svg', 'opacity': 0.72 }}
      }},
      {{
        selector: 'node:selected',
        style: {{
          'background-image': 'assets/node-active.png',
          'width': 76,
          'height': 76,
          'color': '#ffe9a8',
          'opacity': 1,
        }}
      }},
      {{
        selector: 'edge',
        style: {{
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'arrow-scale': 1.1,
          'line-color': '#7a6540',
          'target-arrow-color': '#c9a227',
          'width': 2,
          'opacity': 0.85,
        }}
      }}
    ];
  }}

  function renderTopic(topicId) {{
    const topic = book.topics.find(t => t.id === topicId);
    if (!topic) return;
    currentTopicId = topicId;
    selectedKp = null;
    document.querySelectorAll('.topic-btn').forEach(btn => {{
      btn.classList.toggle('active', btn.dataset.id === topicId);
    }});
    document.getElementById('branchHint').textContent =
      topic.name + ' · 由上到下解鎖 · 起點已點亮';

    const elements = buildElements(topic);
    if (cy) {{ cy.destroy(); cy = null; }}
    cy = cytoscape({{
      container: document.getElementById('cy'),
      elements,
      style: styleFor(),
      minZoom: 0.4,
      maxZoom: 2.2,
      wheelSensitivity: 0.25,
      layout: {{
        name: (window.cytoscapeElk && window.ELK) ? 'elk' : 'breadthfirst',
        elk: {{
          algorithm: 'layered',
          'elk.direction': 'DOWN',
          'elk.spacing.nodeNode': 48,
          'elk.layered.spacing.nodeNodeBetweenLayers': 70,
        }},
        directed: true,
        padding: 40,
        spacingFactor: 1.35,
        animate: true,
        animationDuration: 350,
      }},
    }});

    cy.on('tap', 'node', (evt) => {{
      selectedKp = evt.target.id();
      showDetail(topic, selectedKp);
    }});
    cy.on('tap', (evt) => {{
      if (evt.target === cy) {{
        selectedKp = null;
        showDetail(topic, null);
      }}
    }});
    showDetail(topic, null);
    ensureFx();
  }}

  list.addEventListener('click', (e) => {{
    const btn = e.target.closest('.topic-btn');
    if (!btn) return;
    renderTopic(btn.dataset.id);
  }});

  document.getElementById('btnFit').addEventListener('click', () => {{
    if (cy) cy.fit(undefined, 48);
  }});

  document.getElementById('btnReset').addEventListener('click', () => {{
    if (!currentTopicId) return;
    const topic = book.topics.find(t => t.id === currentTopicId);
    (topic.knowledge_points || []).forEach(k => {{
      unlocks[k.id] = !(k.prereqs || []).length;
    }});
    saveUnlocks(unlocks);
    refreshProgress();
    renderTopic(currentTopicId);
  }});

  document.getElementById('btnUnlock').addEventListener('click', async () => {{
    if (!currentTopicId || !selectedKp || !cy) return;
    const topic = book.topics.find(t => t.id === currentTopicId);
    const kp = (topic.knowledge_points || []).find(k => k.id === selectedKp);
    if (!kp) return;
    if (unlocks[kp.id]) {{
      document.getElementById('branchHint').textContent = '呢格已經解鎖咗';
      return;
    }}
    if (!canUnlock(kp)) {{
      document.getElementById('branchHint').textContent = '仲未滿足先備技能，唔可以解鎖';
      return;
    }}
    unlocks[kp.id] = true;
    saveUnlocks(unlocks);
    refreshProgress();
    const node = cy.getElementById(kp.id);
    const p = node.renderedPosition();
    await sparkleAt(p.x, p.y);
    renderTopic(currentTopicId);
    // reselect
    selectedKp = kp.id;
    if (cy) {{
      const n2 = cy.getElementById(kp.id);
      n2.select();
      showDetail(topic, kp.id);
    }}
    document.getElementById('branchHint').textContent = '解鎖成功：' + kp.name;
  }});

  window.addEventListener('resize', () => {{ ensureFx(); if (cy) cy.resize(); }});

  // default open first topic
  if (book.topics[0]) renderTopic(book.topics[0].id);
}})();
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"topics={len(book['topics'])} kps={sum(len(t['knowledge_points']) for t in book['topics'])}")


if __name__ == "__main__":
    main()
