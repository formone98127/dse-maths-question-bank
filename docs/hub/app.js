/* ===== DSE Hub — 滾輪篩選；按年份列卷／按課題列同標籤題目 ===== */
"use strict";

const PLACE = "";       // 請選擇
const ALL = "__ALL__";  // 所有

const ICON_SEARCH = `<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>`;

const state = {
  mode: "year",
  subject: ALL, // 預設「所有」
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
  const m = String(paper || "").match(/(\d+[A-Za-z]?)/);
  return m ? m[1].toUpperCase() : "1";
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
    return head.concat(uniq(rows.map((r) => r.year)).sort((a, b) => yNum(b) - yNum(a)).map((y) => ({ value: String(y), label: YEAR_LABEL[y] || String(y) })));
  }
  if (key === "paper") {
    return head.concat(uniq(rows.map((r) => r.paper)).map((p) => ({ value: p, label: p })));
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
  "#2012P2Q1": "/math/2012/paper-2-en/",
  "#2013P2Q1": "/math/2013/paper-2-en/",
};

function viewHrefFor(r) {
  if (r.path) return r.path;
  if (LANDING_BY_HASH[r.hash]) return LANDING_BY_HASH[r.hash];
  const code = PAPER_CODE[r.paper] || "paper-1";
  const slug = r.lang === "英文" ? `${code}-en` : code;
  return `/${r.id}/${r.year}/${slug}/`;
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
  return `
    <a class="paper-row" href="${href}" title="檢視 ${sn} ${YEAR_LABEL[r.year] || r.year} ${paperLbl}">
      <span class="paper-year">${YEAR_LABEL[r.year] || r.year}</span>
      <span class="paper-body">
        <span class="paper-tags">
          <span class="tag subj">${esc(sn)}</span>
          <span class="tag paper">${esc(paperLbl)}</span>
          <span class="tag lang">${esc(langLbl)}</span>
        </span>
        <span class="paper-title">${esc(title)}</span>
      </span>
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

  const rows = sortRows(filteredCatalog());
  if (!rows.length) {
    resultEl.innerHTML = emptyHtml("找不到符合條件的試卷。請改選「所有」或放寬篩選。");
    return;
  }
  const count = `<p class="list-count">共 ${rows.length} 卷</p>`;
  resultEl.innerHTML = count + rows.map(rowHtml).join("");
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

let reelInvoker = null;

function openReel(key, invoker) {
  reelKey = key;
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
  if (reelInvoker) {
    reelInvoker.focus();
    reelInvoker = null;
  }
}

function highlightReel() {
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
    } else if (reelKey === "year") {
      state.paper = ALL;
    }
  }
  closeReel();
  render();
}

reelWheel.addEventListener("scroll", () => {
  highlightReel();
  clearTimeout(reelSnapTimer);
  reelSnapTimer = setTimeout(() => {
    const i = Math.round(reelWheel.scrollTop / ITEM_H);
    reelWheel.scrollTo({ top: i * ITEM_H, behavior: "smooth" });
    highlightReel();
  }, 80);
});

reelWheel.addEventListener("click", (e) => {
  const item = e.target.closest(".reel-item");
  if (!item) return;
  const i = +item.dataset.i;
  reelWheel.scrollTo({ top: i * ITEM_H, behavior: "smooth" });
  reelIndex = i;
  highlightReel();
});

$("reelDone").addEventListener("click", commitReel);
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
