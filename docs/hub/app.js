/* ===== DSE Hub — 滾輪篩選；只顯示資料庫有嘅卷 ===== */
"use strict";

const PLACE = "";       // 請選擇
const ALL = "__ALL__";  // 所有

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

const ICON_VIEW = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5c-7 0-10 7-10 7s3 7 10 7 10-7 10-7-3-7-10-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z"/></svg>`;
const ICON_DL = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a1 1 0 0 1 1 1v9.6l2.8-2.8a1 1 0 1 1 1.4 1.4l-4.5 4.5a1 1 0 0 1-1.4 0L6.8 12.2a1 1 0 1 1 1.4-1.4L11 13.6V4a1 1 0 0 1 1-1zM5 19a1 1 0 0 1 1-1h12a1 1 0 1 1 0 2H6a1 1 0 0 1-1-1z"/></svg>`;

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
    const sid = state.subject === PLACE || state.subject === ALL ? "math" : state.subject;
    const topics = TOPICS[sid];
    if (!topics) return [{ value: PLACE, label: "請選擇" }];
    const flat = Object.entries(topics).flatMap(([g, ts]) => ts.map((t) => ({ value: t, label: t, group: g })));
    return head.concat(flat);
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

function pdfTitleHtml(pdfUrl) {
  return pdfUrl
    ? `<a class="pdf-title-link" href="${pdfUrl}" target="_blank" rel="noopener">下載全卷 PDF</a>`
    : `<span class="pdf-title-link disabled" title="待補">下載全卷 PDF</span>`;
}

function viewIconHtml(href) {
  return href
    ? `<a class="icon-btn view" href="${href}" target="_blank" rel="noopener" title="逐題睇" aria-label="逐題睇">${ICON_VIEW}</a>`
    : `<span class="icon-btn view disabled" title="逐題睇 · 待補" aria-label="逐題睇待補">${ICON_VIEW}</span>`;
}

function viewHrefFor(r) {
  return BANK_URL + r.hash;
}

function topicBankHref(sid, topic) {
  const q = new URLSearchParams();
  q.set("subject", sid === "econ" ? "經濟" : "數學");
  if (topic && topic !== ALL && topic !== PLACE) q.set("tag", topic);
  return `${BANK_URL}?${q.toString()}`;
}

function rowHtml(r) {
  const sn = shortName(r.name);
  const pdfUrl = PDF_LINKS[`${r.id}|${r.year}|${r.paper}`] || null;
  const href = viewHrefFor(r);
  return `
    <article class="paper-row">
      <div class="paper-year">${r.year}</div>
      <div class="paper-body">
        <div class="paper-tags">
          <span class="tag subj">${sn}</span>
          <span class="tag cat">${r.paper}</span>
          <span class="tag lang">${r.lang}</span>
        </div>
        <div class="paper-title-row">
          <div class="paper-title">文憑試 DSE ${sn} ${r.year} · ${r.paper}（${r.lang}）</div>
          ${pdfTitleHtml(pdfUrl)}
        </div>
        <div class="paper-sub">${r.name}</div>
      </div>
      <div class="paper-actions">${viewIconHtml(href)}</div>
    </article>`;
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

function renderYear() {
  fPaper.style.display = "";
  l2.textContent = "年份";
  btns.year.dataset.key = "year";

  // 請選擇／所有 都當「唔篩」→ 一打開即列出資料庫已有卷
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
  const topicMap = sid ? TOPICS[sid] : null;

  if (!sid) {
    resultEl.innerHTML = emptyHtml("按課題：請先用滾輪揀一個資料庫已有嘅科目。");
    return;
  }
  if (!topicMap) {
    resultEl.innerHTML = emptyHtml("呢科暫時未有課題表（資料庫有卷，但課題索引未編）。");
    return;
  }
  if (state.topic === PLACE) {
    resultEl.innerHTML = emptyHtml("請揀課題，或揀「所有」睇呢科概覽。");
    return;
  }

  const sn = shortName(subjectsInDb().find((s) => s.id === sid)?.name || sid);
  const topicLabel = state.topic === ALL ? "全部課題" : state.topic;
  const href = topicBankHref(sid, state.topic);
  resultEl.innerHTML = `
    <article class="paper-row">
      <div class="paper-year">#</div>
      <div class="paper-body">
        <div class="paper-tags">
          <span class="tag subj">${sn}</span>
          <span class="tag cat">${topicLabel}</span>
        </div>
        <div class="paper-title-row">
          <div class="paper-title">${sn} · ${topicLabel}</div>
          ${pdfTitleHtml(null)}
        </div>
        <div class="paper-sub">${state.topic !== ALL && state.topic !== PLACE ? `篩「${topicLabel}」` : "課題概覽"}</div>
      </div>
      <div class="paper-actions">${viewIconHtml(href)}</div>
    </article>`;
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
