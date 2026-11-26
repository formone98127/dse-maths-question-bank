/* ===== DSE Hub — 滾輪篩選；按年份列卷／按課題列同標籤題目 ===== */
"use strict";

const PLACE = "";       // 請選擇
const ALL = "__ALL__";  // 所有

const ICON_SEARCH = `<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>`;

const PRESET_SUBJECT = (document.body && document.body.dataset.presetSubject) ? document.body.dataset.presetSubject.trim() : "";

const state = {
  mode: "year",
  subject: PRESET_SUBJECT || ALL, // /hub/math/ 會預設「數學」
  year: ALL,
  paper: ALL,
  topic: PLACE,
};

const $ = (id) => document.getElementById(id);
const resultEl = $("result");
const modeSeg = $("modeSeg");
const fPaper = $("fPaper");
const l2 = $("l2");

const btns = {
  subject: $("bSubj"),
  year: $("bYear"),
  paper: $("bPaper"),
};

const LABEL = { subject: "科目", year: "年份", paper: "卷別", topic: "課題" };
/* ===== CASE 1：未入電子題庫的卷 → 直接下載官方 PDF（window.PAPERS，見 papers.js） ===== */
const PAPER_KIND = { paper: "試卷", ms: "評卷參考", report: "考評報告", mock: "模擬卷" };

function pdfSubjects() {
  return Object.entries((window.PAPERS || {}).subjects || {}).map(([id, v]) => ({
    id, name: v.name, items: v.items || [],
  }));
}

/* 該科該年已在電子題庫（data.js）的卷別，例如 {"Paper 1","Paper 2"} */
/* sid → 題庫用的科目名（CATALOG 顯示名可能係「數學（必修部分）」，QB 用「數學」） */
const QB_SUBJECT = { math: "數學", econ: "經濟", chem: "化學", bio: "生物", phys: "物理",
                     eng: "英語", chi: "中文", bafs: "企會財", geog: "地理", hist: "歷史",
                     chist: "中史", ict: "ICT", toursm: "旅遊與款待", m1: "M1" };
function bankPapers(sid, year) {
  const out = new Set();
  const names = new Set([QB_SUBJECT[sid], sid].filter(Boolean));
  const qs = (window.QB && window.QB.questions) || [];
  for (const q of qs) {
    if (String(q.year) !== String(year)) continue;
    /* M1／M2 延伸部分：以 paper 認，唔靠 subject（兩者 subject 都係「數學」） */
    if (sid === "m1") { if (q.paper === "Paper 1M") out.add("Paper 1M"); continue; }
    if (names.has(q.subject)) out.add(String(q.paper));
  }
  return out;
}

function subjectName(id) {
  const hit = subjectsInDb().find((s) => s.id === id);
  return hit ? hit.name : id;
}

function pdfRowsFor(sid, name, year) {
  const subj = ((window.PAPERS || {}).subjects || {})[sid];
  if (!subj) return [];
  const have = bankPapers(sid, year);
  return (subj.items || [])
    .filter((it) => String(it.y) === String(year))
    .filter((it) => {
      /* CASE 2：該卷已有電子版 → 只收起「試卷」PDF（改由閱讀器右上角「全卷下載」提供）；
         評卷參考（MS）同考試報告 PDF 照出卡，方便一次過下載成份（Kin 2026-11-17） */
      const pn = it.p ? `Paper ${it.p}` : "";
      if (it.k === "paper") {
        if (pn && have.has(pn)) return false;
        if (!pn && have.size > 0) return false;   // 「全卷」PDF 而該年已有電子版
      }
      return true;
    })
    .map((it) => ({ pdf: true, sid, name, year: it.y, kind: it.k, paper: it.p, lang: it.l, url: it.u }));
}

function downloadPageHref(pdfUrl) {
  // /papers/<sid>/<stem>.pdf  ->  /download/<sid>/<stem>.html
  return "/download/" + String(pdfUrl).replace(/^\/papers\//, "").replace(/\.pdf$/, "") + ".html";
}

function pdfRowHtml(r) {
  const kindLbl = PAPER_KIND[r.kind] || r.kind;
  const paperLbl = r.paper ? `Paper ${r.paper}` : "全卷";
  const langLbl = r.lang === "zh" ? "中文" : r.lang === "en" ? "English" : "—";
  return `
    <a class="paper-row" href="${esc(downloadPageHref(r.url))}" title="下載 ${esc(r.name)} ${r.year} ${kindLbl}">
      <span class="paper-year">${r.year}</span>
      <span class="paper-body">
        <span class="paper-tags">
          <span class="tag subj">${esc(r.name)}</span>
          <span class="tag paper">${esc(paperLbl)}</span>
          ${r.lang === "na" ? "" : `<span class="tag lang">${esc(langLbl)}</span>`}
          <span class="tag pdf">${esc(kindLbl)}</span>
          <span class="tag dl">下載頁</span>
        </span>
        <span class="paper-title">${esc(r.name)} ${esc(paperLbl)} · ${esc(kindLbl)}</span>
      </span>
      <span class="paper-chev" aria-hidden="true"></span>
    </a>`;
}

const YEAR_LABEL = { PP: "練習卷", SP: "樣本試卷" };
const yNum = (y) => { const n = Number(y); return Number.isFinite(n) ? n : 0; };

function shortName(name) {
  return String(name).replace(/（.*?）/g, "").replace(/\s*\/.*/, "").trim();
}

function uniq(arr) {
  return [...new Set(arr)];
}

function matchDim(val, rowVal) {
  if (val === PLACE || val === ALL) return true;
  return String(val) === String(rowVal);
}

function filteredCatalog() {
  return CATALOG.filter((r) =>
    matchDim(state.subject, r.id) &&
    matchDim(state.year, r.year) &&
    matchDim(state.paper, r.paper)
  );
}

function subjectsInDb() {
  const map = new Map();
  CATALOG.forEach((r) => map.set(r.id, r.name));
  /* 未入電子題庫、但有官方 PDF 的科目（CASE 1） */
  pdfSubjects().forEach((s) => { if (!map.has(s.id)) map.set(s.id, s.name); });
  return [...map.entries()].map(([id, name]) => ({ id, name }));
}

const SID_SUBJECT = {
  math: "數學",
  econ: "經濟",
  chem: "化學",
  bio: "生物",
  phys: "物理",
};
const SUBJECT_PREFIX = {
  數學: "",
  經濟: "econ",
  化學: "chem",
  生物: "bio",
  物理: "phys",
};

function sidToSubject(sid) {
  return SID_SUBJECT[sid] || "數學";
}

function paperNo(paper) {
  const raw = String(paper || "").trim();
  const m1 = raw.match(/^M(\d+)$/i);        /* "M1" → "1M"（延伸單元） */
  if (m1) return "1M";
  if (/^Paper\s*1M$/i.test(raw)) return "1M";
  const m = raw.match(/(\d+[A-Za-z]?)/);
  return m ? m[1].toUpperCase() : "1";
}

/* PDF 目錄的卷別（p: ""／"1"／"2"／"1A"…）→ 同 CATALOG 一致的標籤 */
function paperLabelFromPdf(p) {
  const s = String(p == null ? "" : p).trim().toUpperCase();
  if (!s) return "";                 // 全卷（跨兩卷）→ 冇特定卷別
  if (s === "1") return "卷一";
  if (s === "2") return "卷二";
  if (s === "1A") return "卷一甲";
  if (s === "1B") return "卷一乙";
  return "Paper " + s;
}

function bankQuestions(sid) {
  const subj = sidToSubject(sid);
  const qs = (window.QB && Array.isArray(window.QB.questions)) ? window.QB.questions : [];
  return qs.filter((q) => q.subject === subj && q.type === "題目");
}

/* 課題選項：用題庫真實 tags（有題目才出現），按題數由多至少 */
function realTagsFor(sid) {
  const counts = new Map();
  for (const q of bankQuestions(sid)) {
    for (const t of q.tags || []) {
      counts.set(t, (counts.get(t) || 0) + 1);
    }
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "zh-Hant"))
    .map(([tag, n]) => ({ tag, n }));
}

function topicGroupOf(sid, tag) {
  const map = TOPICS[sid];
  if (!map) return "其他";
  for (const [g, ts] of Object.entries(map)) {
    if (ts.includes(tag)) return g;
  }
  return "其他";
}

function hashForQuestion(q) {
  const pref = SUBJECT_PREFIX[q.subject] ?? (q.subject === "經濟" ? "econ" : "");
  return `#${pref}${q.year}P${paperNo(q.paper)}Q${q.qno}`;
}

function questionHref(q, topic) {
  const params = new URLSearchParams();
  params.set("subject", q.subject);
  if (topic && topic !== ALL && topic !== PLACE) params.set("tag", topic);
  // 英文卷要帶 lang，否則中英文兩行會開同一份（閱讀器用 lang 過濾）
  if (/英文|_EN|\(EN\)|ENG/i.test(String(q.file || ""))) params.set("lang", "en");
  return `${BANK_URL}?${params.toString()}${hashForQuestion(q)}`;
}

function questionsForTopic(sid, topic) {
  const rows = bankQuestions(sid);
  const pick = topic === ALL ? rows : rows.filter((q) => (q.tags || []).includes(topic));
  // 同一題的「題目」與「解答」帶同一組 tags → 只保留題目；中英文卷係兩份，唔可以合併
  const langOf = (q) => (/英文|_EN|\(EN\)|ENG/i.test(String(q.file || "")) ? "en" : "zh");
  const byKey = new Map();
  for (const q of pick) {
    const k = `${q.year}|${q.paper}|${q.qno}|${langOf(q)}`;
    const cur = byKey.get(k);
    if (!cur || (cur.type !== "題目" && q.type === "題目")) byKey.set(k, q);
  }
  return [...byKey.values()];
}

function optionsFor(key) {
  const rows = CATALOG.filter((r) => {
    if (key !== "subject" && state.subject !== PLACE && state.subject !== ALL && r.id !== state.subject) return false;
    if (key !== "year" && state.year !== PLACE && state.year !== ALL && String(r.year) !== String(state.year)) return false;
    if (key !== "paper" && state.paper !== PLACE && state.paper !== ALL && r.paper !== state.paper) return false;
    return true;
  });

  const head = [
    { value: PLACE, label: "請選擇" },
    { value: ALL, label: "所有" },
  ];

  if (key === "subject") {
    return head.concat(subjectsInDb().map((s) => ({ value: s.id, label: s.name })));
  }
  if (key === "year") {
    /* 年份清單：catalog + 該科 PDF 目錄（非數學科只有 PDF，靠 catalog 會冇年份可揀） */
    const yrs = new Set(rows.map((r) => r.year));
    const sid0 = state.subject !== PLACE && state.subject !== ALL ? state.subject : null;
    const sidList = sid0 ? [sid0] : pdfSubjects().map((x) => x.id);
    for (const id of sidList) {
      const items = (((window.PAPERS || {}).subjects || {})[id] || {}).items || [];
      for (const it of items) yrs.add(it.y);
    }
    return head.concat([...yrs].sort((a, b) => yNum(b) - yNum(a))
      .map((y) => ({ value: String(y), label: YEAR_LABEL[y] || String(y) })));
  }
  if (key === "paper") {
    /* 卷別選項：同時由電子題庫（CATALOG，如數學 卷一/卷二）同 PDF 目錄（未入庫科目）
       收集，統一標籤；按科目／年份現有嘅卷別才出，唔會出空選項。 */
    const labels = new Set();
    rows.forEach((r) => { if (r.paper) labels.add(String(r.paper)); });
    const sid0 = state.subject !== PLACE && state.subject !== ALL ? state.subject : null;
    const sidList = sid0 ? [sid0] : pdfSubjects().map((x) => x.id);
    const yr = (state.year !== PLACE && state.year !== ALL) ? String(state.year) : null;
    for (const id of sidList) {
      const items = (((window.PAPERS || {}).subjects || {})[id] || {}).items || [];
      for (const it of items) {
        if (yr && String(it.y) !== yr) continue;
        const lbl = paperLabelFromPdf(it.p);
        if (lbl) labels.add(lbl);
      }
    }
    const ORDER = { "卷一": 1, "卷一甲": 1.1, "卷一乙": 1.2, "卷二": 2 };
    return head.concat([...labels]
      .sort((a, b) => (ORDER[a] || 9) - (ORDER[b] || 9) || a.localeCompare(b, "zh-Hant"))
      .map((p) => ({ value: p, label: p })));
  }
  if (key === "topic") {
    const sid = state.subject === PLACE || state.subject === ALL ? null : state.subject;
    if (!sid) return [{ value: PLACE, label: "請選擇" }];
    const tags = realTagsFor(sid);
    if (!tags.length) return [{ value: PLACE, label: "請選擇" }];
    return head.concat(tags.map(({ tag, n }) => ({
      value: tag,
      label: `${tag}（${n}）`,
      group: topicGroupOf(sid, tag),
    })));
  }
  return head;
}

function displayLabel(key, value) {
  if (value === PLACE || value == null) return "請選擇";
  if (value === ALL) return "所有";
  if (key === "subject") {
    const s = subjectsInDb().find((x) => x.id === value);
    return s ? s.name : value;
  }
  if (key === "topic" && state.subject !== PLACE && state.subject !== ALL) {
    const hit = realTagsFor(state.subject).find((x) => x.tag === value);
    return hit ? `${hit.tag}（${hit.n}）` : String(value);
  }
  return String(value);
}

function syncButtons() {
  btns.subject.textContent = displayLabel("subject", state.subject);
  btns.year.textContent = displayLabel(state.mode === "topic" ? "topic" : "year", state.mode === "topic" ? state.topic : state.year);
  btns.paper.textContent = displayLabel("paper", state.paper);
  ["subject", "year", "paper"].forEach((k) => {
    const b = btns[k];
    const v = k === "year" && state.mode === "topic" ? state.topic : state[k];
    b.classList.toggle("placeholder", v === PLACE || v == null);
    b.classList.toggle("filtered", !(v === PLACE || v === ALL || v == null));
  });
}

const PAPER_CODE = {
  "卷一": "paper-1",
  "卷二": "paper-2",
  "卷一甲": "paper-1a",
  "卷一乙": "paper-1b",
  "Paper 1": "paper-1",
  "Paper 2": "paper-2",
  "Paper 1A": "paper-1a",
  "Paper 1B": "paper-1b",
};

/* Catalog lang can disagree with the real landing folder (e.g. 2012/2013 卷二). */
const LANDING_BY_HASH = {
  "#2012P2Q1": "/hub/math/2012/paper-2-en/",
  "#2013P2Q1": "/hub/math/2013/paper-2-en/",
};

function viewHrefFor(r) {
  if (r.path) return r.path;
  /* Kin 定案：卡片一律直接入題目（唔經中間卷頁） */
  if (String(r.id).toLowerCase() === "m1" || String(r.id).toLowerCase() === "m2") {
    return "/" + (r.hash || "");
  }
  /* Kin 定案：卡片一律直接入題目（唔經中間卷頁），數學同 M1／M2 一致 */
  if (r.id === "math") return "/" + (r.hash || "");
  return null;
}

const SUBJECT_EN = { "數學": "Maths", "經濟": "Econ", "化學": "Chem",
  "生物": "Bio", "物理": "Phys", "英語": "Eng" };
function rowHtml(r) {
  const en = r.lang === "英文";
  const paperEn = String(r.paper).replace("卷", "Paper ")
    .replace("一", "1").replace("二", "2").replace("三", "3").replace("四", "4").replace("五", "5");
  const sn = en ? (SUBJECT_EN[shortName(r.name)] || shortName(r.name)) : shortName(r.name);
  const paperLbl = en ? paperEn : r.paper;
  const langLbl = en ? "English" : r.lang;
  const href = viewHrefFor(r);
  const title = en
    ? `DSE ${sn} · ${paperEn} (English)`
    : `文憑試 DSE ${sn} · ${r.paper}（${r.lang}）`;
  const rowBody = `
      <span class="paper-year">${YEAR_LABEL[r.year] || r.year}</span>
      <span class="paper-body">
        <span class="paper-tags">
          <span class="tag subj">${esc(sn)}</span>
          <span class="tag paper">${esc(paperLbl)}</span>
          <span class="tag lang">${esc(langLbl)}</span>
        </span>
        <span class="paper-title">${esc(title)}</span>
      </span>`;
  /* 未有落地板（例如 M1 掃描緊）：render 做靜態行，唔好出 404 死鏈 */
  if (!href) return `<div class="paper-row is-static" title="即將上線">${rowBody}</div>`;
  return `
    <a class="paper-row" href="${href}" title="檢視 ${sn} ${YEAR_LABEL[r.year] || r.year} ${paperLbl}">${rowBody}
      <span class="paper-chev" aria-hidden="true"></span>
    </a>`;
}

function questionRowHtml(q, topic) {
  const href = questionHref(q, topic);
  const pLabel = `Paper ${paperNo(q.paper)}`;
  const isEn = /英文|_EN|\(EN\)|ENG/i.test(String(q.file || ""));
  const topicTags = (q.tags || []).slice(0, 3)
    .map((t) => `<span class="tag topic">${esc(t)}</span>`)
    .join("");
  return `
    <a class="paper-row" href="${href}" target="_blank" rel="noopener" title="檢視 ${esc(q.subject)} ${YEAR_LABEL[q.year] || q.year} ${pLabel} Q${q.qno}">
      <span class="paper-year">${YEAR_LABEL[q.year] || q.year}</span>
      <span class="paper-body">
        <span class="paper-tags">
          <span class="tag subj">${esc(q.subject)}</span>
          <span class="tag paper">${esc(pLabel)}</span>
          <span class="tag q">Q${q.qno}</span>
          <span class="tag lang">${isEn ? "English" : "中文"}</span>
          ${topicTags}
        </span>
        <span class="paper-title">${esc(q.subject)} ${pLabel} Q${q.qno}</span>
        ${q.title ? `<span class="paper-sub">${esc(q.title)}</span>` : ""}
      </span>
      <span class="paper-chev" aria-hidden="true"></span>
    </a>`;
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function emptyHtml(msg) {
  return `
    <div class="empty">
      ${ICON_SEARCH}
      <p>${msg}</p>
    </div>`;
}

function sortRows(rows) {
  // 甲／乙 用 collation 唔穩定（實測會乙排喺甲前），用固定次序
  const P = { 卷一甲: 1, 卷一乙: 2, 卷一: 1, 卷二: 2, 卷三: 3, 卷四: 4, 卷五: 5 };
  const pkey = (p) => P[String(p)] ?? 9;
  return rows.sort(
    (a, b) =>
      yNum(b.year) - yNum(a.year) ||
      pkey(a.paper) - pkey(b.paper) ||
      String(a.lang).localeCompare(String(b.lang), "zh-Hant") ||
      a.name.localeCompare(b.name, "zh-Hant")
  );
}

function sortQuestions(rows) {
  return rows.sort(
    (a, b) =>
      yNum(b.year) - yNum(a.year) ||
      paperNo(a.paper).localeCompare(paperNo(b.paper)) ||
      a.qno - b.qno
  );
}


function resourceTopicGroup(sid, tag) {
  const fromTopics = topicGroupOf(sid, tag);
  if (fromTopics && fromTopics !== "其他") return fromTopics;
  const extra = (window.HUB_TOPIC_GROUPS || {})[sid] || {};
  for (const [g, ts] of Object.entries(extra)) {
    if ((ts || []).includes(tag)) return g;
  }
  return fromTopics || "其他";
}

function rankRelatedResources(sid, topic) {
  const all = Array.isArray(window.HUB_RESOURCES) ? window.HUB_RESOURCES : [];
  const specific = topic && topic !== ALL && topic !== PLACE;
  const group = specific ? resourceTopicGroup(sid, topic) : null;
  const scored = [];
  for (const r of all) {
    const sameSubj = r.subject === sid;
    const isGeneral = !r.subject || r.subject === "general";
    let score = -1;
    if (!specific) {
      // 「所有」：科目級資源先行，再係同科課題頁，最後先一般資源。
      if (sameSubj && r.level === "subject") score = 0;
      else if (sameSubj) score = 1;
      else if (isGeneral) score = 2;
    } else {
      const tags = r.tags || [];
      const groups = r.groups || [];
      const tagHit = sameSubj && tags.includes(topic);
      const groupHit = sameSubj && group && group !== "其他" && groups.includes(group);
      if (tagHit) score = 0;
      else if (groupHit) score = 1;
      else if (sameSubj && r.level === "subject") score = 2;
      else if (isGeneral) score = 3;
    }
    if (score >= 0) scored.push({ r, score });
  }
  scored.sort((a, b) => a.score - b.score || String(a.r.title).localeCompare(String(b.r.title), "zh-Hant"));
  return scored.map((x) => x.r);
}

function relatedResourcesHtml(sid, topic) {
  const rows = rankRelatedResources(sid, topic);
  if (!rows.length) return "";
  const items = rows.map((r) => {
    const href = esc(r.href);
    const ext = /^https?:\/\//.test(r.href) ? ' rel="noopener"' : "";
    return `
    <a class="hub-related-card" href="${href}"${ext}>
      <p class="hub-related-kicker">${esc(r.kicker || "溫習資源")}</p>
      <h3>${esc(r.title)}</h3>
      <p>${esc(r.desc || "")}</p>
    </a>`;
  }).join("");
  return `
<section class="hub-related" aria-labelledby="hub-related-heading">
  <h2 id="hub-related-heading">相關有用資源</h2>
  <div class="hub-related-grid">${items}</div>
</section>`;
}

function renderYear() {
  fPaper.style.display = "";
  l2.textContent = "年份";
  btns.year.dataset.key = "year";

  const bankRows = sortRows(filteredCatalog());
  /* CASE 1：補上未入題庫但有官方 PDF 的卷（連評卷參考／考評報告下載） */
  const pdfRows = [];
  const wantSubj = (state.subject !== PLACE && state.subject !== ALL)
    ? [state.subject] : pdfSubjects().map((s) => s.id);
  for (const sid of wantSubj) {
    const nm = subjectName(sid);
    const subjItems = (((window.PAPERS || {}).subjects || {})[sid] || {}).items || [];
    const years = (state.year !== PLACE && state.year !== ALL)
      ? [Number(state.year)] : [...new Set(subjItems.map((i) => i.y))];
    for (const y of years) pdfRows.push(...pdfRowsFor(sid, nm, y));
  }
  const rows = bankRows.concat(pdfRows)
    .filter((r) => !r.pdf || state.year === PLACE || state.year === ALL || String(r.year) === String(state.year))
    .filter((r) => {
      /* 卷別：電子題庫行已由 filteredCatalog 過濾；PDF 行要在這裡按卷別比對 */
      if (state.paper === PLACE || state.paper === ALL) return true;
      if (!r.pdf) return true;
      return paperLabelFromPdf(r.paper) === state.paper;
    })
    .sort((a, b) => (b.year - a.year) || String(a.name || "").localeCompare(String(b.name || ""), "zh-Hant"));

  if (!rows.length) {
    resultEl.innerHTML = emptyHtml("找不到符合條件的試卷。請改選「所有」或放寬篩選。");
    return;
  }
  const nBank = rows.filter((r) => !r.pdf).length;
  const count = `<p class="list-count">共 ${rows.length} 項（電子題庫 ${nBank} 卷 · PDF 下載 ${rows.length - nBank} 份）</p>`;
  resultEl.innerHTML = count + rows.map((r) => (r.pdf ? pdfRowHtml(r) : rowHtml(r))).join("");
}

function renderTopic() {
  fPaper.style.display = "none";
  l2.textContent = "課題";
  btns.year.dataset.key = "topic";

  const sid = state.subject === PLACE || state.subject === ALL ? null : state.subject;

  if (!sid) {
    resultEl.innerHTML = emptyHtml("按課題：請先選擇一個資料庫已有的科目。");
    return;
  }
  if (!bankQuestions(sid).length) {
    resultEl.innerHTML = emptyHtml("此科目暫未載入題目資料。");
    return;
  }
  if (state.topic === PLACE) {
    resultEl.innerHTML = emptyHtml("請選擇課題，或選「所有」列出此科目的全部題目。");
    return;
  }

  const rows = sortQuestions(questionsForTopic(sid, state.topic));
  if (!rows.length) {
    resultEl.innerHTML = emptyHtml("此課題暫無對應題目。") + relatedResourcesHtml(sid, state.topic);
    return;
  }

  const topicLabel = state.topic === ALL ? "全部課題" : state.topic;
  const count = `<p class="list-count">共 ${rows.length} 題 · ${topicLabel}（進入後可上一題／下一題集中溫習）</p>`;
  const related = relatedResourcesHtml(sid, state.topic);
  resultEl.innerHTML = count + rows.map((q) => questionRowHtml(q, state.topic)).join("") + related;
}

function render() {
  modeSeg.querySelectorAll("button").forEach((b) => {
    const on = b.dataset.mode === state.mode;
    b.classList.toggle("on", on);
    b.setAttribute("aria-selected", String(on));
  });
  syncButtons();
  topicSearchWrap.hidden = state.mode !== "topic";
  tsOptions = subjectSelected() ? optionsFor("topic").slice(2) : allSubjectTagOptions();
  topicSearch.value = "";
  closeTopicList();
  state.mode === "year" ? renderYear() : renderTopic();
}

/* ---------- Reel（滾輪） ---------- */
const reel = $("reel");
const reelWheel = $("reelWheel");
const reelTitle = $("reelTitle");
const topicSearchWrap = $("topicSearchWrap");
const topicSearch = $("topicSearch");
const topicSearchList = $("topicSearchList");
const ITEM_H = 44;
let reelKey = null;
let reelOpts = [];
let reelIndex = 0;
let reelSnapTimer = null;
let reelTarget = null; /* tap 目標 index：smooth scroll 期間唔准 scroll 事件覆蓋 */

let reelInvoker = null;

function openReel(key, invoker) {
  reelKey = key;
  reelTarget = null;
  reelInvoker = invoker || null;
  reelOpts = optionsFor(key);
  const cur = key === "topic" ? state.topic : state[key];
  let idx = reelOpts.findIndex((o) => String(o.value) === String(cur));
  if (idx < 0) idx = 0;
  reelIndex = idx;
  reelTitle.textContent = LABEL[key] || key;

  reelWheel.innerHTML =
    `<div class="reel-pad"></div>` +
    reelOpts.map((o, i) => `<div class="reel-item${i === idx ? " on" : ""}" data-i="${i}">${o.label}</div>`).join("") +
    `<div class="reel-pad"></div>`;

  reel.hidden = false;
  document.body.classList.add("reel-open");
  requestAnimationFrame(() => {
    reelWheel.scrollTop = idx * ITEM_H;
    highlightReel();
    $("reelDone").focus();
  });
}

/* ---------- 常駐課題搜尋 bar（只喺「按課題」模式顯示） ---------- */
let tsOptions = [];

function subjectSelected() {
  return state.subject !== PLACE && state.subject !== ALL ? state.subject : null;
}

// 未揀科目時：跨科彙總題庫所有課題（同名合併題數）
function allSubjectTagOptions() {
  const acc = new Map();
  subjectsInDb().forEach((s) => {
    realTagsFor(s.id).forEach(({ tag, n }) => {
      const cur = acc.get(tag);
      if (cur) {
        cur.n += n;
        if (!cur.sids.includes(s.id)) cur.sids.push(s.id);
      } else {
        acc.set(tag, { value: tag, n, sids: [s.id] });
      }
    });
  });
  return [...acc.values()]
    .sort((a, b) => b.n - a.n || a.value.localeCompare(b.value, "zh-Hant"))
    .map((o) => ({
      value: o.value,
      label: `${o.value}（${o.n}）`,
      group: o.sids.length > 1 ? `${o.sids.length} 科` : "",
      sid: o.sids[0],
    }));
}

function closeTopicList() {
  topicSearchList.hidden = true;
  topicSearchList.innerHTML = "";
}

function renderTopicList(q) {
  const hits = q
    ? tsOptions.filter((o) => String(o.label).toLowerCase().includes(q))
    : tsOptions.slice();
  if (!hits.length) {
    topicSearchList.innerHTML = `<div class="ts-empty">無符合課題</div>`;
    topicSearchList.hidden = false;
    return;
  }
  topicSearchList.innerHTML = hits.slice(0, 30).map((o) => {
    const g = o.group && o.group !== "其他" ? `<span class="ts-n">${o.group}</span>` : "";
    const s = o.sid && !subjectSelected() ? ` data-s="${o.sid}"` : "";
    return `<div class="ts-item" data-v="${o.value}"${s}><span>${o.label}</span>${g}</div>`;
  }).join("");
  topicSearchList.hidden = false;
}

topicSearch.addEventListener("input", () => {
  const q = topicSearch.value.trim().toLowerCase();
  q ? renderTopicList(q) : closeTopicList();
});
topicSearch.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    const first = topicSearchList.querySelector(".ts-item");
    if (first) first.click();
  }
});
topicSearchList.addEventListener("click", (e) => {
  const item = e.target.closest(".ts-item");
  if (!item) return;
  if (item.dataset.s && !subjectSelected()) state.subject = item.dataset.s;
  state.topic = item.dataset.v;
  closeTopicList();
  render();
});
document.addEventListener("click", (e) => {
  if (!topicSearchWrap.contains(e.target)) closeTopicList();
});

function closeReel() {
  reel.hidden = true;
  document.body.classList.remove("reel-open");
  reelKey = null;
  reelTarget = null;
  if (reelInvoker) {
    reelInvoker.focus();
    reelInvoker = null;
  }
}

function highlightReel(force) {
  if (!force && reelTarget !== null) {
    /* 手指／滑鼠剛 tap 某項，smooth scroll 未到位前唔好被舊 scrollTop 覆蓋 */
    reelIndex = reelTarget;
    reelWheel.querySelectorAll(".reel-item").forEach((el, n) => el.classList.toggle("on", n === reelIndex));
    return;
  }
  const i = Math.round(reelWheel.scrollTop / ITEM_H);
  reelIndex = Math.max(0, Math.min(reelOpts.length - 1, i));
  reelWheel.querySelectorAll(".reel-item").forEach((el, n) => el.classList.toggle("on", n === reelIndex));
}

function commitReel() {
  if (reelKey == null) return;
  const opt = reelOpts[reelIndex];
  if (!opt) return closeReel();
  const v = opt.value;

  if (reelKey === "topic") {
    state.topic = v;
  } else {
    state[reelKey] = v;
    if (reelKey === "subject") {
      state.year = ALL;
      state.paper = ALL;
      state.topic = PLACE;
      /* /hub/math/ 分支揀「所有」→ 返全科 hub */
      if (PRESET_SUBJECT && v === ALL) {
        closeReel();
        location.href = "/hub/";
        return;
      }
      /* Kin 定案（2026-11-26）：喺 Hub 篩選揀「數學（必修部分）」→ 進入數學分支 /hub/math/ */
      if (v === "math") {
        closeReel();
        location.href = "/hub/math/";
        return;
      }
    } else if (reelKey === "year") {
      state.paper = ALL;
    }
  }
  closeReel();
  render();
}

reelWheel.addEventListener("scroll", () => {
  const tgt = reelTarget;
  if (tgt !== null && Math.abs(reelWheel.scrollTop - tgt * ITEM_H) <= 1.5) {
    reelTarget = null; /* 已到位，之後交返 scroll 主導 */
  }
  highlightReel();
  clearTimeout(reelSnapTimer);
  reelSnapTimer = setTimeout(() => {
    if (reelTarget !== null) return;
    const i = Math.round(reelWheel.scrollTop / ITEM_H);
    reelWheel.scrollTo({ top: i * ITEM_H, behavior: "smooth" });
    highlightReel(true);
  }, 80);
});

reelWheel.addEventListener("click", (e) => {
  const item = e.target.closest(".reel-item");
  if (!item) return;
  const i = +item.dataset.i;
  reelTarget = i;
  reelIndex = i;
  reelWheel.querySelectorAll(".reel-item").forEach((el, n) => el.classList.toggle("on", n === i));
  reelWheel.scrollTo({ top: i * ITEM_H, behavior: "smooth" });
  /* 保險：smooth scroll 可能唔觸發 scroll（已喺位），400ms 後強制清 flag */
  setTimeout(() => { reelTarget = null; }, 400);
});

$("reelDone").addEventListener("click", () => { reelTarget = null; commitReel(); });
$("reelCancel").addEventListener("click", closeReel);
$("reelBackdrop").addEventListener("click", closeReel);

Object.values(btns).forEach((btn) => {
  btn.addEventListener("click", () => openReel(btn.dataset.key, btn));
});

modeSeg.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-mode]");
  if (!btn || btn.dataset.mode === state.mode) return;
  state.mode = btn.dataset.mode;
  state.topic = PLACE;
  render();
});


(function applyQuery() {
  const p = new URLSearchParams(location.search);
  const sid = p.get("subject");
  if (sid && SID_SUBJECT[sid]) state.subject = sid;
  const mode = p.get("mode");
  if (mode === "topic" || mode === "year") state.mode = mode;
  const year = p.get("year");
  if (year) state.year = year;
  const paper = p.get("paper");
  if (paper) state.paper = paper;
  const topic = p.get("topic") || p.get("tag");
  if (topic) {
    state.topic = topic;
    if (mode !== "year") state.mode = "topic";
  }
})();

render();
