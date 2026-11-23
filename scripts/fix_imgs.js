// 修正 docs/hub/data.js 內 404 圖片（用 node 直接 eval JS，避免 JSON 轉義問題）
const fs = require('fs');
const path = require('path');

const REPO = '/home/one/hub_repo';
const DOCS = path.join(REPO, 'docs');
const SRC = path.join(DOCS, 'data.js');
const apply = process.argv.includes('--apply');

const src = fs.readFileSync(SRC, 'utf8');
const _win = {};
const data = new Function('window', src + '; return window.QB;')(_win);

// 建立同名 PNG 索引
const byName = new Map();
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.toLowerCase().endsWith('.png')) {
      const k = e.name.toLowerCase();
      if (!byName.has(k)) byName.set(k, []);
      byName.get(k).push(p);
    }
  }
})(DOCS);

const refs = new Set();
for (const q of data.questions) {
  for (const key of ['html', 'text']) {
    const v = q[key] || '';
    for (const m of v.matchAll(/<img[^>]+src="([^"]+)"/g)) refs.add(m[1]);
    for (const m of v.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)) refs.add(m[1]);
  }
}

const missing = [...refs].filter((r) => !fs.existsSync(path.join(DOCS, r)));
console.log(`refs=${refs.size} missing=${missing.length}`);

const fixes = new Map();
const drops = [];
for (const r of missing) {
  const cands = byName.get(path.basename(r).toLowerCase()) || [];
  if (cands.length === 1) {
    fixes.set(r, path.relative(DOCS, cands[0]).split(path.sep).join('/'));
    console.log(`  FIX ${r} -> ${fixes.get(r)}`);
  } else {
    drops.push(r);
    console.log(`  DROP ${r} (同名 ${cands.length})`);
  }
}

if (apply) {
  for (const q of data.questions) {
    for (const key of ['html', 'text']) {
      let v = q[key] || '';
      for (const [oldR, newR] of fixes) {
        v = v.split(`src="${oldR}"`).join(`src="${newR}"`);
        v = v.split(`](${oldR})`).join(`](${newR})`);
      }
      for (const d of drops) {
        v = v.replace(new RegExp(`<img[^>]+src="${d.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"[^>]*>`, 'g'), '');
        v = v.split(`![Figure](${d})`).join('');
        v = v.split(`](${d})`).join(']()');
      }
      q[key] = v;
    }
  }
  fs.writeFileSync(SRC, 'window.QB =' + JSON.stringify(data) + ';');
  console.log(`applied fixed=${fixes.size} dropped=${drops.length}`);
}
