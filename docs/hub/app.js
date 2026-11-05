/* ===== DSE Hub — 滾輪篩選；按年份列卷／按課題列同標籤題目 ===== */
"use strict";

const PLACE = "";       // 請選擇
const ALL = "__ALL__";  // 所有

const ICON_VIEW = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5c-7 0-10 7-10 7s3 7 10 7 10-7 10-7-3-7-10-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z"/></svg>`;

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

/* 課題選項：用題庫真實 tags（有題先出現），按題數多至少 */
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
  return `${BANK_URL}?${params.toString()}${hashForQuestion(q)}`;
}

function questionsForTopic(sid, topic) {
  const rows = bankQuestions(sid);
  if (topic === ALL) return rows;
  return rows.filter((q) => (q.tags || []).includes(topic));
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
    return head.concat(uniq(rows.map((r) => r.year)).sort((a, b) => b - a).map((y) => ({ value: String(y), label: String(y) })));
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
  });
}

function viewHrefFor(r) {
  return BANK_URL + r.hash;
}

function viewIconHtml(href) {
  return `<a class="icon-btn view" href="${href}" target="_blank" rel="noopener" title="檢視" aria-label="檢視">${ICON_VIEW}</a>`;
}

function rowHtml(r) {
  const sn = shortName(r.name);
  const href = viewHrefFor(r);
  return `
    <article class="paper-row">
      <a class="paper-main" href="${href}" target="_blank" rel="noopener" title="直接檢視題目">
        <div class="paper-year">${r.year}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">${sn}</span>
            <span class="tag cat">${r.paper}</span>
            <span class="tag lang">${r.lang}</span>
          </div>
          <div class="paper-title">文憑試 DSE ${sn} ${r.year} · ${r.paper}（${r.lang}）</div>
          <div class="paper-sub">${r.name}</div>
        </div>
      </a>
      <div class="paper-actions">${viewIconHtml(href)}</div>
    </article>`;
}

function questionRowHtml(q, topic) {
  const href = questionHref(q, topic);
  const pLabel = `Paper ${paperNo(q.paper)}`;
  const tags = (q.tags || []).slice(0, 3).map((t) => `<span class="tag cat">${esc(t)}</span>`).join("");
  return `
    <article class="paper-row">
      <a class="paper-main" href="${href}" target="_blank" rel="noopener" title="直接檢視題目">
        <div class="paper-year">${q.year}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">${esc(q.subject)}</span>
            <span class="tag lang">${esc(pLabel)}</span>
            <span class="tag live">Q${q.qno}</span>
            ${tags}
          </div>
          <div class="paper-title">${esc(q.subject)} ${q.year} ${esc(pLabel)} Q${q.qno}</div>
          <div class="paper-sub">${esc(q.title || "")}</div>
        </div>
      </a>
      <div class="paper-actions">${viewIconHtml(href)}</div>
    </article>`;
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
      <p>${msg}</p>
    </div>`;
}

function sortRows(rows) {
  return rows.sort(
    (a, b) =>
      b.year - a.year ||
      String(a.lang).localeCompare(String(b.lang), "zh-Hant") ||
      a.name.localeCompare(b.name, "zh-Hant") ||
      a.paper.localeCompare(b.paper, "zh-Hant")
  );
}

function sortQuestions(rows) {
  return rows.sort(
    (a, b) =>
      b.year - a.year ||
      paperNo(a.paper).localeCompare(paperNo(b.paper)) ||
      a.qno - b.qno
  );
}

function renderYear() {
  fPaper.style.display = "";
  l2.textContent = "年份";
  btns.year.dataset.key = "year";

  const rows = sortRows(filteredCatalog());
  if (!rows.length) {
    resultEl.innerHTML = emptyHtml("呢組條件喺資料庫搵唔到卷。試下改「所有」或者放寬條件。");
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
    resultEl.innerHTML = emptyHtml("按課題：請先用滾輪揀一個資料庫已有嘅科目。");
    return;
  }
  if (!bankQuestions(sid).length) {
    resultEl.innerHTML = emptyHtml("呢科暫時未載入題目資料。");
    return;
  }
  if (state.topic === PLACE) {
    resultEl.innerHTML = emptyHtml("請揀課題，或揀「所有」列出呢科全部題目。");
    return;
  }

  const rows = sortQuestions(questionsForTopic(sid, state.topic));
  if (!rows.length) {
    resultEl.innerHTML = emptyHtml("呢個課題暫時冇對應題目。");
    return;
  }

  const topicLabel = state.topic === ALL ? "全部課題" : state.topic;
  const count = `<p class="list-count">共 ${rows.length} 題 · ${topicLabel}（撳列或眼仔檢視；入去後可上一題／下一題集中溫習）</p>`;
  resultEl.innerHTML = count + rows.map((q) => questionRowHtml(q, state.topic)).join("");
}

function render() {
  modeSeg.querySelectorAll("button").forEach((b) =>
    b.classList.toggle("on", b.dataset.mode === state.mode)
  );
  syncButtons();
  state.mode === "year" ? renderYear() : renderTopic();
}

/* ---------- Reel（滾輪） ---------- */
const reel = $("reel");
const reelWheel = $("reelWheel");
const reelTitle = $("reelTitle");
const ITEM_H = 40;
let reelKey = null;
let reelOpts = [];
let reelIndex = 0;
let reelSnapTimer = null;

function openReel(key) {
  reelKey = key;
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
  });
}

function closeReel() {
  reel.hidden = true;
  document.body.classList.remove("reel-open");
  reelKey = null;
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
  btn.addEventListener("click", () => openReel(btn.dataset.key));
});

modeSeg.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-mode]");
  if (!btn || btn.dataset.mode === state.mode) return;
  state.mode = btn.dataset.mode;
  state.topic = PLACE;
  render();
});

render();
