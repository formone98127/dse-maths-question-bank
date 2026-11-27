/* ===== 伏位快問 — Tinder 式滑動卡遊戲（純 vanilla JS） ===== */
"use strict";

(function () {
  const DECK = (window.TRAP_CARDS && window.TRAP_CARDS.cards) || [];
  const STORE_KEY = "dsehub.trap.v1";
  const MIXED_N = 20;
  const BANK_SUBJECT = "數學";

  const $ = (id) => document.getElementById(id);
  const el = {
    home: $("home"), game: $("game"), summary: $("summary"),
    topicChips: $("topicChips"), stack: $("stack"), stackWrap: $("stackWrap"),
    hintLayer: $("hintLayer"), verdict: $("verdict"), hintText: $("hintText"),
    srcLink: $("srcLink"), actions: $("actions"),
    btnTrap: $("btnTrap"), btnReal: $("btnReal"),
    streak: $("streak"), modeChip: $("modeChip"), progress: $("progress"),
    deckMeta: $("deckMeta"),
    sumStats: $("sumStats"), weakHead: $("weakHead"), weakList: $("weakList"),
    againBtn: $("againBtn"), homeBtn: $("homeBtn"),
  };

  /* ---------- GA4 ---------- */
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  /* ---------- 進度 store（localStorage，版本化） ---------- */
  function loadStore() {
    try {
      const s = JSON.parse(localStorage.getItem(STORE_KEY) || "null");
      if (s && s.v === 1) return s;
    } catch (e) { /* 旧/壞資料棄用 */ }
    return { v: 1, deck_version: "trap-v1", cards: {}, streak_best: 0, topics: {}, sessions: 0 };
  }
  let store = loadStore();
  function saveStore() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) { /* 私隱模式照玩 */ }
  }

  /* ---------- session ---------- */
  /* 綜合：偏重未見過＋歷史弱課題；專項：單課題易→難 */
  let session = null; // {mode, topic, queue:[card], total, answered, correct, streak, bestStreak, seenIds:Set}

  function topicAccuracy(t) {
    const s = store.topics[t];
    if (!s || !(s.right + s.wrong)) return null;
    return s.right / (s.right + s.wrong);
  }

  function buildMixed() {
    const pool = DECK.slice();
    const acc = (c) => {
      const a = topicAccuracy(c.topic);
      const seen = store.cards[c.id] ? 1 : 0;
      // 未見過排先；弱課題排先；歷史錯得多排先
      const cardStat = store.cards[c.id] || { wrong: 0 };
      return seen + (a == null ? 0.5 : a) * 2 - Math.min(cardStat.wrong, 3) * 0.4 + hash01(c.id);
    };
    pool.sort((a, b) => acc(a) - acc(b));
    return pool.slice(0, Math.min(MIXED_N, DECK.length));
  }

  function hash01(id) { // 穩定偽隨機，避免次次同一排序
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) >>> 0;
    return (h % 1000) / 1000;
  }

  function startSession(mode, topic) {
    const cards = mode === "mixed" ? buildMixed()
      : DECK.filter((c) => c.topic === topic).sort((a, b) => a.difficulty - b.difficulty || hash01(a.id) - hash01(b.id));
    if (!cards.length) return;
    session = {
      mode, topic: topic || null,
      queue: cards.slice(),
      total: cards.length, answered: 0, correct: 0,
      streak: 0, bestStreak: 0, firstIds: new Set(cards.map((c) => c.id)),
      topicTally: {}, // topic → {right, wrong}
    };
    store.sessions += 1;
    saveStore();
    showScreen("game");
    el.modeChip.textContent = mode === "mixed" ? "綜合" : topic;
    el.modeChip.hidden = false;
    el.actions.hidden = false;
    el.progress.hidden = false;
    el.streak.hidden = false;
    el.streak.querySelector("b").textContent = "0";
    updateProgress();
    track("trap_session_start", { mode, topic: topic || undefined });
    renderStack();
  }

  function updateProgress() {
    if (!session) return;
    const left = session.queue.length;
    const done = Math.max(0, session.total - left);
    el.progress.textContent = done + " / " + session.total;
  }

  /* ---------- 卡片疊渲染 ---------- */
  let mjReady = false;
  window.onMathJaxReady = () => { mjReady = true; typesetTop(); };

  function typeset(node) {
    if (mjReady && window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([node]).catch(() => {});
    }
  }
  function typesetTop() {
    const top = el.stack.querySelector(".tcard.top .stmt");
    if (top) typeset(top.closest(".tcard"));
  }

  function cardDom(card, cls) {
    const div = document.createElement("article");
    div.className = "tcard " + cls;
    const dots = "●".repeat(card.difficulty) + "○".repeat(3 - card.difficulty);
    div.innerHTML =
      `<div class="meta"><span>${esc(card.topic)}</span><span class="dots" aria-label="難度 ${card.difficulty}">${dots}</span></div>` +
      `<div class="stmt">${esc(card.statement).replace(/\n/g, "<br>")}</div>` +
      `<span class="stamp real">真 ✓</span><span class="stamp trap">伏 ✗</span>`;
    // 陳述係 LaTeX 原文，要交返俾 MathJax，唔可以當 HTML
    div.querySelector(".stmt").textContent = card.statement;
    return div;
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function renderStack() {
    el.stack.innerHTML = "";
    el.hintLayer.hidden = true;
    const n = Math.min(3, session.queue.length);
    if (!n) return endSession();
    for (let i = n - 1; i >= 0; i--) {
      const cls = i === 0 ? "top" : "behind-" + i;
      const dom = cardDom(session.queue[i], cls);
      el.stack.appendChild(dom);
    }
    updateProgress();
    typesetTop();
    if (mjReady) {
      // 閒時預排下一卡
      const nxt = el.stack.querySelector(".tcard.behind-1");
      if (nxt) requestIdle(() => typeset(nxt));
    }
  }

  function requestIdle(fn) {
    if (window.requestIdleCallback) window.requestIdleCallback(fn);
    else setTimeout(fn, 200);
  }

  /* ---------- 答題 ---------- */
  function answer(calledTrap) {
    if (!session || answering || !el.hintLayer.hidden) return;
    const card = session.queue[0];
    if (!card) return;
    answering = true;
    const correct = calledTrap === card.is_trap;
    const firstTry = session.firstIds.has(card.id);

    session.answered += 1;
    if (correct) {
      session.correct += 1;
      session.streak += 1;
      session.bestStreak = Math.max(session.bestStreak, session.streak);
      bump(card, "right");
    } else {
      session.streak = 0;
      bump(card, "wrong");
      if (navigator.vibrate) navigator.vibrate(60);
      el.stack.classList.remove("shake");
      void el.stack.offsetWidth; // 重觸發 animation
      el.stack.classList.add("shake");
    }
    el.streak.querySelector("b").textContent = session.streak;
    track("trap_card_answer", {
      card_id: card.id, topic: card.topic, is_trap: card.is_trap,
      correct, first_try: firstTry,
    });

    const topDom = el.stack.querySelector(".tcard.top");
    if (correct) {
      session.queue.shift();
      if (topDom) {
        topDom.classList.add("good");
        topDom.classList.add(calledTrap ? "exit-l" : "exit-r");
      }
      setTimeout(next, 250);
    } else {
      if (topDom) {
        topDom.classList.add("bad");
        // 錯卡唔走，彈返中間 + 提示層
        topDom.style.transform = "";
      }
      showHint(card);
      // 重排到 3–5 位後
      session.queue.shift();
      const back = Math.min(3 + Math.floor(Math.random() * 3), session.queue.length);
      session.queue.splice(back, 0, card);
      setTimeout(next, 0); // 提示層蓋住，dismiss 先至真正過卡
    }
  }

  function bump(card, kind) {
    const c = store.cards[card.id] || (store.cards[card.id] = { right: 0, wrong: 0, last: "" });
    c[kind] += 1;
    c.last = new Date().toISOString().slice(0, 10);
    const t = store.topics[card.topic] || (store.topics[card.topic] = { right: 0, wrong: 0 });
    t[kind] += 1;
    const tally = session.topicTally[card.topic] || (session.topicTally[card.topic] = { right: 0, wrong: 0 });
    tally[kind] += 1;
    if (kind === "right" && session.streak > store.streak_best) store.streak_best = session.streak;
    saveStore();
  }

  function next() {
    answering = false;
    if (!el.hintLayer.hidden) return; // 等使用者睇完提示
    renderStack();
  }

  function showHint(card) {
    el.verdict.textContent = card.is_trap ? "呢個係伏！" : "呢句係真嘅！";
    el.verdict.className = "verdict " + (card.is_trap ? "no" : "ok");
    el.hintText.textContent = card.hint;
    if (card.source_ref) {
      const p = new URLSearchParams({ subject: BANK_SUBJECT, tag: card.topic });
      el.srcLink.href = "/?" + p.toString() + "#" + card.source_ref;
      el.srcLink.hidden = false;
    } else {
      el.srcLink.hidden = true;
    }
    el.hintLayer.hidden = false;
  }

  el.hintLayer.addEventListener("click", (e) => {
    if (e.target.closest(".src-link")) return;
    el.hintLayer.hidden = true;
    renderStack();
  });

  /* ---------- 手勢（Pointer Events 統一 touch/mouse） ---------- */
  let answering = false;
  let drag = null; // {id, x0, t0, dom}

  el.stack.addEventListener("pointerdown", (e) => {
    const dom = e.target.closest(".tcard.top");
    if (!dom || !el.hintLayer.hidden || answering) return;
    drag = { id: e.pointerId, x0: e.clientX, t0: Date.now(), dom };
    el.stack.setPointerCapture(e.pointerId);
  });

  el.stack.addEventListener("pointermove", (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = e.clientX - drag.x0;
    drag.dom.style.transition = "none";
    drag.dom.style.transform = `translateX(${dx}px) rotate(${dx / 18}deg)`;
    const half = domWidth(drag.dom) * 0.4;
    drag.dom.querySelector(".stamp.trap").style.opacity = dx < -half ? 1 : 0;
    drag.dom.querySelector(".stamp.real").style.opacity = dx > half ? 1 : 0;
    drag.dx = dx;
  });

  function domWidth(dom) { return dom.getBoundingClientRect().width || 300; }

  el.stack.addEventListener("pointerup", (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = drag.dx || 0;
    const dt = Date.now() - drag.t0;
    const w = domWidth(drag.dom);
    const commit = Math.abs(dx) > w * 0.3 || (dt < 250 && Math.abs(dx) > w * 0.12);
    const dom = drag.dom;
    drag = null;
    if (commit && dx !== 0) {
      answer(dx < 0);
    } else {
      dom.style.transition = "transform 0.2s ease";
      dom.style.transform = "";
      dom.querySelectorAll(".stamp").forEach((s) => (s.style.opacity = 0));
    }
  });
  el.stack.addEventListener("pointercancel", () => {
    if (!drag) return;
    drag.dom.style.transform = "";
    drag.dom.querySelectorAll(".stamp").forEach((s) => (s.style.opacity = 0));
    drag = null;
  });

  /* 掣 + 鍵盤行同一條 answer() 路 */
  el.btnTrap.addEventListener("click", () => answer(true));
  el.btnReal.addEventListener("click", () => answer(false));
  document.addEventListener("keydown", (e) => {
    if (el.game.hidden) return;
    if (!el.hintLayer.hidden) {
      if (["ArrowLeft", "ArrowRight", "Enter", " "].includes(e.key)) {
        e.preventDefault();
        el.hintLayer.hidden = true;
        renderStack();
      }
      return;
    }
    if (e.key === "ArrowLeft") answer(true);
    if (e.key === "ArrowRight") answer(false);
  });

  /* ---------- 總結 ---------- */
  function endSession() {
    el.actions.hidden = true;
    el.streak.hidden = true;
    el.progress.hidden = true;
    el.modeChip.hidden = true;
    const acc = session.answered ? Math.round((session.correct / session.answered) * 100) : 0;
    el.sumStats.innerHTML =
      cell(session.total, "清咗卡數") + cell(acc + "%", "答對率") +
      cell(session.bestStreak, "最長連勝") + cell(store.streak_best, "歷史連勝");
    const weak = Object.entries(session.topicTally)
      .map(([t, s]) => ({ t, r: s.right / (s.right + s.wrong) }))
      .filter((x) => x.r < 0.6)
      .sort((a, b) => a.r - b.r);
    el.weakHead.hidden = !weak.length;
    el.weakList.innerHTML = weak.map(({ t, r }) => {
      const p = new URLSearchParams({ subject: BANK_SUBJECT, tag: t });
      return `<a href="/dse-maths-question-bank/?${p.toString()}" target="_blank" rel="noopener">${esc(t)} ${Math.round(r * 100)}% →</a>`;
    }).join("");
    showScreen("summary");
    track("trap_session_end", {
      answered: session.answered, accuracy: acc / 100, best_streak: session.bestStreak,
    });
  }
  function cell(v, label) {
    return `<div class="cell"><b>${esc(String(v))}</b><span>${esc(label)}</span></div>`;
  }

  /* ---------- 畫面切換 ---------- */
  function showScreen(name) {
    el.home.hidden = name !== "home";
    el.game.hidden = name !== "game";
    el.summary.hidden = name !== "summary";
  }

  /* ---------- 起始頁 ---------- */
  function renderHome() {
    const topics = [...new Set(DECK.map((c) => c.topic))];
    if (el.deckMeta) {
      el.deckMeta.textContent = DECK.length
        ? `卡庫 ${DECK.length} 張 · ${topics.length} 個課題`
        : "";
    }
    el.topicChips.innerHTML = DECK.length
      ? topics.sort((a, b) => a.localeCompare(b, "zh-Hant"))
          .map((t) => {
            const n = DECK.filter((c) => c.topic === t).length;
            return `<button type="button" data-topic="${esc(t)}">${esc(t)} <span class="n">${n}</span></button>`;
          }).join("")
      : `<p class="sub">卡組仲未載入。</p>`;
  }

  el.home.addEventListener("click", (e) => {
    const mixed = e.target.closest("[data-mode=mixed]");
    if (mixed) return startSession("mixed");
    const chip = e.target.closest("[data-topic]");
    if (chip) startSession("topic", chip.dataset.topic);
  });
  el.againBtn.addEventListener("click", () => {
    session.mode === "mixed" ? startSession("mixed") : startSession("topic", session.topic);
  });
  el.homeBtn.addEventListener("click", () => {
    el.actions.hidden = true;
    el.streak.hidden = true;
    el.progress.hidden = true;
    el.modeChip.hidden = true;
    showScreen("home");
  });

  renderHome();

  /* URL 直接開局：/trap/?mode=mixed 或 /trap/?topic=概率 */
  (function autostart() {
    const p = new URLSearchParams(location.search);
    if (p.get("mode") === "mixed") return startSession("mixed");
    const t = p.get("topic");
    if (t && DECK.some((c) => c.topic === t)) startSession("topic", t);
  })();
})();
