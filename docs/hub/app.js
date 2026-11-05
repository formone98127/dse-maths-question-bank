/* ===== DSE 試題資料庫 — 主邏輯（下拉篩選；結果列跟 dsepaper.hk 列表感） ===== */
"use strict";

const state = { mode: "year", subject: SUBJECTS[0], year: null, paper: null, topic: null };

const $ = (id) => document.getElementById(id);
const s1 = $("s1"), s2 = $("s2"), s3 = $("s3");
const l2 = $("l2"), f3 = $("f3");
const resultEl = $("result"), modeSeg = $("modeSeg");

const opt = (v, t) => `<option value="${v}">${t}</option>`;
function fill(sel, html, val) { sel.innerHTML = html; if (val != null) sel.value = val; }

const papersOf = (s, y) => (typeof s.papers === "function" ? s.papers(y) : s.papers);
const yearsOf = (s) => {
  const [a, b] = s.years || [2012, 2026];
  return YEARS.filter((y) => y >= a && y <= b);
};
const allTopics = (s) => (s.topics ? Object.values(s.topics).flat() : []);

const ICON_VIEW = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5c-7 0-10 7-10 7s3 7 10 7 10-7 10-7-3-7-10-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z"/></svg>`;
const ICON_DL = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a1 1 0 0 1 1 1v9.6l2.8-2.8a1 1 0 1 1 1.4 1.4l-4.5 4.5a1 1 0 0 1-1.4 0L6.8 12.2a1 1 0 1 1 1.4-1.4L11 13.6V4a1 1 0 0 1 1-1zM5 19a1 1 0 0 1 1-1h12a1 1 0 1 1 0 2H6a1 1 0 0 1-1-1z"/></svg>`;

function shortName(name) {
  return name.replace(/（.*?）/g, "").replace(/\s*\/.*/, "").trim();
}

function actionsHtml({ viewHref, pdfUrl }) {
  const view = viewHref
    ? `<a class="icon-btn view" href="${viewHref}" target="_blank" rel="noopener" title="逐題睇" aria-label="逐題睇">${ICON_VIEW}</a>`
    : `<span class="icon-btn view disabled" title="逐題睇 · 待補" aria-label="逐題睇待補">${ICON_VIEW}</span>`;
  const pdf = pdfUrl
    ? `<a class="icon-btn pdf" href="${pdfUrl}" target="_blank" rel="noopener" title="下載 PDF" aria-label="下載 PDF">${ICON_DL}</a>`
    : `<span class="icon-btn pdf disabled" title="下載 PDF · 待補" aria-label="下載 PDF 待補">${ICON_DL}</span>`;
  return `<div class="paper-actions">${view}${pdf}</div>`;
}

/* ---------- 按年份模式：科目 → 年份 → 卷別 ---------- */
function renderYear() {
  s3.style.display = "";
  f3.style.display = "";
  l2.textContent = "年份";

  const ys = yearsOf(state.subject);
  if (!state.year || !ys.includes(state.year)) {
    const liveYs = state.subject.bank
      ? ys.filter((y) => state.subject.bank[y] && state.subject.bank[y].length)
      : [];
    state.year = liveYs[0] || ys[0];
  }
  const papers = papersOf(state.subject, state.year);
  if (!papers.includes(state.paper)) {
    const livePs = state.subject.bank && state.subject.bank[state.year];
    state.paper = (livePs && livePs[0]) || papers[0];
  }

  fill(s1, SUBJECTS.map((s) => opt(s.id, s.name)).join(""), state.subject.id);
  fill(s2, yearsOf(state.subject).map((y) => opt(y, y)).join(""), state.year);
  fill(s3, papers.map((p) => opt(p, p)).join(""), state.paper);

  const bankDone = state.subject.bank && state.subject.bank[state.year] && state.subject.bank[state.year].includes(state.paper);
  const bankHref = bankDone
    ? BANK_URL + (state.subject.bankTpl
      ? "#" + state.subject.bankTpl.replace("{Y}", state.year)
      : (state.year ? `#${state.year}P${state.paper.includes("二") || /Paper\s*2/i.test(state.paper) ? "2" : "1"}Q1` : ""))
    : null;
  const pdfUrl = PDF_LINKS[`${state.subject.id}|${state.year}|${state.paper}`] || null;
  const sn = shortName(state.subject.name);

  resultEl.innerHTML = `
    <article class="paper-row">
      <div class="paper-year">${state.year}</div>
      <div class="paper-body">
        <div class="paper-tags">
          <span class="tag subj">${sn}</span>
          <span class="tag cat">歷屆試題 Past Paper</span>
          <span class="tag ${bankDone ? "live" : "todo"}">${bankDone ? "電子題庫已上線" : "待補"}</span>
        </div>
        <div class="paper-title">文憑試 DSE ${sn} ${state.year} · ${state.paper}</div>
        <div class="paper-sub">${state.subject.name}${state.subject.note ? ` · ※ ${state.subject.note}` : ""}</div>
      </div>
      ${actionsHtml({ viewHref: bankHref, pdfUrl })}
    </article>`;
}

/* ---------- 按課題模式：科目 → 課題 ---------- */
function renderTopic() {
  s3.style.display = "none";
  f3.style.display = "none";
  l2.textContent = "課題";

  fill(s1, SUBJECTS.map((s) => opt(s.id, s.name)).join(""), state.subject.id);
  const s = state.subject;
  const sn = shortName(s.name);

  if (!s.topics) {
    fill(s2, opt("", "課題表編製中"), "");
    resultEl.innerHTML = `
      <article class="paper-row">
        <div class="paper-year">—</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">${sn}</span>
            <span class="tag todo">課題表編製中</span>
          </div>
          <div class="paper-title">${s.name}</div>
          <div class="paper-sub">呢科嘅課題表編製緊，稍後加入</div>
        </div>
        ${actionsHtml({ viewHref: null, pdfUrl: null })}
      </article>`;
    return;
  }

  if (!state.topic || !allTopics(s).includes(state.topic))
    state.topic = allTopics(s)[0];
  const groups = Object.entries(s.topics)
    .map(([g, ts]) => `<optgroup label="${g}">${ts.map((t) => opt(t, t)).join("")}</optgroup>`)
    .join("");
  fill(s2, groups, state.topic);

  const anyBank = !!s.bank;
  resultEl.innerHTML = `
    <article class="paper-row">
      <div class="paper-year">#</div>
      <div class="paper-body">
        <div class="paper-tags">
          <span class="tag subj">${sn}</span>
          <span class="tag cat">${state.topic}</span>
          <span class="tag ${anyBank ? "live" : "todo"}">${anyBank ? "有電子題可睇" : "待補"}</span>
        </div>
        <div class="paper-title">${s.name} · ${state.topic}</div>
        <div class="paper-sub">呢個課題嘅題目索引會陸續加入；有電子題庫嘅科目可以而家入去睇</div>
        <div class="topic-hint">提示：切返「按年份」可以揀指定年份同卷別。</div>
      </div>
      ${actionsHtml({ viewHref: anyBank ? BANK_URL : null, pdfUrl: null })}
    </article>`;
}

/* ---------- 事件 ---------- */
s1.addEventListener("change", (e) => {
  state.subject = SUBJECTS.find((x) => x.id === e.target.value);
  state.year = state.paper = state.topic = null;
  render();
});
s2.addEventListener("change", (e) => {
  if (state.mode === "year") { state.year = +e.target.value; state.paper = null; }
  else state.topic = e.target.value;
  render();
});
s3.addEventListener("change", (e) => { state.paper = e.target.value; render(); });
modeSeg.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-mode]");
  if (!btn || btn.dataset.mode === state.mode) return;
  state.mode = btn.dataset.mode;
  state.year = state.paper = state.topic = null;
  render();
});

function render() {
  modeSeg.querySelectorAll("button").forEach((b) =>
    b.classList.toggle("on", b.dataset.mode === state.mode)
  );
  state.mode === "year" ? renderYear() : renderTopic();
}
render();
