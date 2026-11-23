/* ===== 開考倒數 — Reigns 式左右滑（純 vanilla JS） ===== */
"use strict";

(function () {
  const DECK = (window.EVE_CARDS && window.EVE_CARDS.cards) || [];
  const STORE_KEY = "dsehub.eve.v1";
  const START_DAYS = 15;
  const START_STAT = 6;
  const STAT_MAX = 10;
  const URGENT_EVERY = 6;
  const EXAM_DELAY = 4;
  const URGENT_MS = 3000;
  const STATS = ["brain", "time", "score", "mood"];
  const STAT_LABEL = { brain: "腦力", time: "時間", score: "分數", mood: "心情" };

  const $ = (id) => document.getElementById(id);
  const el = {
    home: $("home"), game: $("game"), death: $("death"),
    stack: $("stack"), stackWrap: $("stackWrap"),
    dayChip: $("dayChip"), dayNum: $("dayNum"),
    bestChip: $("bestChip"), bestNum: $("bestNum"),
    deckMeta: $("deckMeta"),
    startBtn: $("startBtn"), againBtn: $("againBtn"), homeBtn: $("homeBtn"),
    actions: $("actions"),
    btnLeft: $("btnLeft"), btnRight: $("btnRight"),
    btnLeftLabel: $("btnLeftLabel"), btnRightLabel: $("btnRightLabel"),
    mBrain: $("mBrain"), mTime: $("mTime"), mScore: $("mScore"), mMood: $("mMood"),
    meters: $("meters"),
    urgentRing: $("urgentRing"), ringFg: $("ringFg"), urgentSec: $("urgentSec"),
    deathDays: $("deathDays"), deathCause: $("deathCause"),
    deathFormula: $("deathFormula"), deathCorrect: $("deathCorrect"),
  };
  const meterEl = {
    brain: el.mBrain, time: el.mTime, score: el.mScore, mood: el.mMood,
  };

  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  function loadStore() {
    try {
      const s = JSON.parse(localStorage.getItem(STORE_KEY) || "null");
      if (s && s.v === 1) return s;
    } catch (e) { /* ignore */ }
    return { v: 1, deck_version: "eve-v1", best_days: 0, runs: 0 };
  }
  let store = loadStore();
  function saveStore() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) { /* private */ }
  }

  const byId = Object.create(null);
  DECK.forEach((c) => { byId[c.id] = c; });

  let session = null;
  let answering = false;
  let urgentTimer = null;
  let urgentDeadline = 0;
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

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function showScreen(name) {
    el.home.hidden = name !== "home";
    el.game.hidden = name !== "game";
    el.death.hidden = name !== "death";
  }

  /* ---------- 開局 ---------- */
  function startRun() {
    clearUrgent();
    const life = shuffle(DECK.filter((c) => c.kind === "life" && !c.min_days));
    const belief = shuffle(DECK.filter((c) => c.kind === "belief"));
    const urgent = shuffle(DECK.filter((c) => c.kind === "urgent"));
    const lateLife = DECK.filter((c) => c.kind === "life" && c.min_days);

    session = {
      stats: { brain: START_STAT, time: START_STAT, score: START_STAT, mood: START_STAT },
      days: START_DAYS,
      swipes: 0,
      sinceUrgent: 0,
      beliefs: {},          // beliefId → "left" | "right"
      pendingExam: [],      // {id, afterSwipe}
      used: new Set(),
      queue: [],
      lifePool: life,
      beliefPool: belief,
      urgentPool: urgent,
      lateLife: lateLife,
      examFail: null,
      survived: 0,
    };
    store.runs += 1;
    saveStore();
    showScreen("game");
    el.dayChip.hidden = false;
    el.actions.hidden = false;
    document.body.classList.add("playing");
    document.body.classList.remove("danger");
    updateMeters();
    updateDay();
    track("eve_run_start");
    fillQueue();
    renderStack();
  }

  function takeDueExams() {
    const due = [];
    const keep = [];
    session.pendingExam.forEach((p) => {
      if (session.swipes >= p.afterSwipe && !session.used.has(p.id) && byId[p.id]) {
        due.push(byId[p.id]);
        session.used.add(p.id);
      } else {
        keep.push(p);
      }
    });
    session.pendingExam = keep;
    return due;
  }

  function takeUrgent() {
    if (session.sinceUrgent < URGENT_EVERY || !session.urgentPool.length) return null;
    session.sinceUrgent = 0;
    const u = session.urgentPool.shift();
    session.used.add(u.id);
    return u;
  }

  function fillQueue() {
    // 到期考試局 → 最前；突發 → 其後；其餘補滿
    const due = takeDueExams();
    if (due.length) session.queue = due.concat(session.queue.filter((c) => !due.includes(c)));

    const urg = takeUrgent();
    if (urg && !session.queue.some((c) => c.id === urg.id)) {
      // 插喺第一張非 exam 之前，確保玩家見到紅邊
      let idx = session.queue.findIndex((c) => c.kind !== "exam");
      if (idx < 0) idx = session.queue.length;
      session.queue.splice(idx, 0, urg);
    }

    while (session.queue.length < 3) {
      const next = drawCard();
      if (!next) {
        // 牌庫空：把未到期考試局提早放出，唔好卡死
        if (session.pendingExam.length) {
          session.pendingExam.forEach((p) => { p.afterSwipe = 0; });
          const more = takeDueExams();
          more.forEach((c) => {
            if (!session.queue.some((q) => q.id === c.id)) session.queue.push(c);
          });
          if (!more.length) break;
          continue;
        }
        break;
      }
      if (session.queue.some((c) => c.id === next.id)) continue;
      session.queue.push(next);
    }
    dedupeQueue();
  }

  function drawCard() {
    // 日子夠低先出嘅生活卡
    for (let i = 0; i < session.lateLife.length; i++) {
      const c = session.lateLife[i];
      if (session.days <= c.min_days && !session.used.has(c.id)) {
        session.lateLife.splice(i, 1);
        session.used.add(c.id);
        return c;
      }
    }

    // 生活 / 信不信 交錯
    const pickBelief = session.beliefPool.length &&
      (session.lifePool.length === 0 || Math.random() < 0.45);
    if (pickBelief) {
      const b = session.beliefPool.shift();
      session.used.add(b.id);
      return b;
    }
    if (session.lifePool.length) {
      const l = session.lifePool.shift();
      session.used.add(l.id);
      return l;
    }
    if (session.beliefPool.length) {
      const b = session.beliefPool.shift();
      session.used.add(b.id);
      return b;
    }
    // 牌庫見底：只出已經到期嘅考試局（唔提早爆未到期）
    return null;
  }

  /* ---------- 畫面 ---------- */
  function updateMeters() {
    STATS.forEach((k) => {
      const v = session.stats[k];
      const pct = Math.max(0, Math.min(STAT_MAX, v)) / STAT_MAX * 100;
      meterEl[k].style.width = pct + "%";
      const wrap = el.meters.querySelector('[data-stat="' + k + '"]');
      if (v <= 1 || v >= STAT_MAX - 1) wrap.classList.add("flash");
      else wrap.classList.remove("flash");
    });
    const low = STATS.some((k) => session.stats[k] <= 2 || session.stats[k] >= STAT_MAX - 1);
    document.body.classList.toggle("danger", low);
  }

  function updateDay() {
    el.dayNum.textContent = String(session.days);
    el.dayChip.classList.toggle("warn", session.days <= 5);
  }

  function cardDom(card, cls) {
    const div = document.createElement("article");
    div.className = "tcard " + cls + (card.kind === "urgent" ? " urgent" : "");
    div.dataset.id = card.id;
    const fig = "fig-" + card.speaker;
    div.innerHTML =
      '<div class="who">' +
        '<svg viewBox="0 0 80 80" width="48" height="48" aria-hidden="true"><use href="#' + fig + '"></use></svg>' +
        '<span class="name">' + esc(card.speaker_label) + "</span>" +
      "</div>" +
      '<div class="stmt"></div>' +
      '<div class="hints">' +
        '<span class="h-l">← ' + esc(card.left.label) + "</span>" +
        '<span class="h-r">' + esc(card.right.label) + " →</span>" +
      "</div>" +
      '<span class="stamp go-l">' + esc(card.left.label) + "</span>" +
      '<span class="stamp go-r">' + esc(card.right.label) + "</span>";
    div.querySelector(".stmt").textContent = card.statement;
    return div;
  }

  function renderStack() {
    clearUrgent();
    el.stack.innerHTML = "";
    fillQueue();
    const n = Math.min(3, session.queue.length);
    if (!n) return endRun("日子過晒，卡都抽完。", null);
    for (let i = n - 1; i >= 0; i--) {
      const cls = i === 0 ? "top" : "behind-" + i;
      el.stack.appendChild(cardDom(session.queue[i], cls));
    }
    const top = session.queue[0];
    el.btnLeftLabel.textContent = top.left.label;
    el.btnRightLabel.textContent = top.right.label;
    typesetTop();
    if (top.kind === "urgent") startUrgent();
  }

  function dedupeQueue() {
    const seen = new Set();
    session.queue = session.queue.filter((c) => {
      if (seen.has(c.id)) return false;
      seen.add(c.id);
      return true;
    });
  }

  /* ---------- 突發計時 ---------- */
  function startUrgent() {
    urgentDeadline = Date.now() + URGENT_MS;
    el.urgentRing.hidden = false;
    el.urgentSec.textContent = "3";
    el.ringFg.style.strokeDashoffset = "0";
    function tick() {
      if (!session) return;
      const left = urgentDeadline - Date.now();
      if (left <= 0) {
        clearUrgent();
        timeoutUrgent();
        return;
      }
      const sec = Math.ceil(left / 1000);
      el.urgentSec.textContent = String(sec);
      el.ringFg.style.strokeDashoffset = String(97.4 * (1 - left / URGENT_MS));
      urgentTimer = requestAnimationFrame(tick);
    }
    urgentTimer = requestAnimationFrame(tick);
  }

  function clearUrgent() {
    if (urgentTimer) cancelAnimationFrame(urgentTimer);
    urgentTimer = null;
    el.urgentRing.hidden = true;
  }

  function timeoutUrgent() {
    if (answering || !session) return;
    const card = session.queue[0];
    if (!card || card.kind !== "urgent") return;
    answering = true;
    applyEffects(card.timeout || { time: -2 });
    track("eve_urgent_timeout", { card_id: card.id });
    const topDom = el.stack.querySelector(".tcard.top");
    if (topDom) topDom.classList.add("exit-l");
    session.queue.shift();
    afterSwipe(card, null);
    setTimeout(() => { answering = false; maybeEndOrNext(); }, 250);
  }

  /* ---------- 答題 ---------- */
  function applyEffects(eff) {
    if (!eff) return;
    STATS.forEach((k) => {
      if (eff[k]) session.stats[k] += eff[k];
    });
    updateMeters();
  }

  function checkDeath() {
    for (let i = 0; i < STATS.length; i++) {
      const k = STATS[i];
      const v = session.stats[k];
      if (v <= 0) {
        return { reason: STAT_LABEL[k] + "見底。", stat: k };
      }
      if (v >= STAT_MAX) {
        return { reason: STAT_LABEL[k] + "爆滿，撐唔住。", stat: k };
      }
    }
    if (session.days <= 0) {
      return { reason: "日子歸零，開考了——你未準備好。", stat: "days" };
    }
    return null;
  }

  function swipe(dir) {
    if (!session || answering || el.game.hidden) return;
    const card = session.queue[0];
    if (!card) return;
    answering = true;
    clearUrgent();

    try {
      const choice = dir === "left" ? card.left : card.right;

      if (card.kind === "exam") {
        const bel = session.beliefs[card.belief_of];
        const belCard = byId[card.belief_of];
        // trap：右滑「唔信」先啱；true：左滑「信」先啱
        const believedCorrect = belCard && (
          belCard.is_trap ? bel === "right" : bel === "left"
        );
        if (believedCorrect) {
          applyEffects({ score: 1 });
          session.examFail = null;
        } else {
          applyEffects({ score: -2, mood: -1 });
          session.examFail = {
            reason: "你信錯咗呢句：",
            formula: belCard ? belCard.statement.replace(/\n/g, " ") : "",
            correct: card.correct,
          };
        }
      } else if (choice && choice.effects) {
        applyEffects(choice.effects);
      }

      if (card.kind === "belief") {
        session.beliefs[card.id] = dir;
        if (card.exam && byId[card.exam] && !session.used.has(card.exam)) {
          const already = session.pendingExam.some((p) => p.id === card.exam);
          if (!already) {
            session.pendingExam.push({
              id: card.exam,
              afterSwipe: session.swipes + 1 + EXAM_DELAY,
            });
          }
        }
      }

      track("eve_swipe", { card_id: card.id, kind: card.kind, dir: dir });

      const topDom = el.stack.querySelector(".tcard.top");
      if (topDom) topDom.classList.add(dir === "left" ? "exit-l" : "exit-r");
      session.queue.shift();
      afterSwipe();
    } catch (err) {
      console.error("eve swipe", err);
      answering = false;
      return;
    }

    setTimeout(() => {
      answering = false;
      maybeEndOrNext();
    }, 250);
  }

  function afterSwipe(/* card, dir */) {
    session.swipes += 1;
    session.sinceUrgent += 1;
    if (session.swipes % 3 === 0) {
      session.days = Math.max(0, session.days - 1);
      updateDay();
    }
    session.survived = START_DAYS - session.days;
  }

  function maybeEndOrNext() {
    const dead = checkDeath();
    if (dead) {
      const fail = session.examFail;
      // 只要仲掛住信錯嘅帳，死亡畫面就顯示正確句（教學優先）
      return endRun(
        fail ? fail.reason : dead.reason,
        fail ? fail.correct : null,
        fail ? fail.formula : null
      );
    }
    renderStack();
  }

  function endRun(cause, correct, formula) {
    clearUrgent();
    answering = false;
    el.actions.hidden = true;
    el.dayChip.hidden = true;
    document.body.classList.remove("playing");
    const survived = session ? session.survived : 0;
    if (survived > store.best_days) {
      store.best_days = survived;
      saveStore();
    }
    el.deathDays.textContent = "你撐了 " + survived + " 日";
    el.deathCause.textContent = cause || "撐唔住。";
    if (formula) {
      el.deathFormula.hidden = false;
      el.deathFormula.textContent = formula;
      typeset(el.deathFormula);
    } else {
      el.deathFormula.hidden = true;
      el.deathFormula.textContent = "";
    }
    if (correct) {
      el.deathCorrect.hidden = false;
      el.deathCorrect.innerHTML = '<span class="dc-label">正確</span><span class="dc-body"></span>';
      el.deathCorrect.querySelector(".dc-body").textContent = correct;
      typeset(el.deathCorrect);
    } else {
      el.deathCorrect.hidden = true;
      el.deathCorrect.textContent = "";
    }
    showScreen("death");
    track("eve_run_end", { survived: survived, cause: cause });
  }

  /* ---------- 手勢 ---------- */
  let drag = null;

  function domWidth(dom) { return dom.getBoundingClientRect().width || 300; }

  el.stack.addEventListener("pointerdown", (e) => {
    const dom = e.target.closest(".tcard.top");
    if (!dom || answering || !session) return;
    drag = { id: e.pointerId, x0: e.clientX, t0: Date.now(), dom };
    el.stack.setPointerCapture(e.pointerId);
  });

  el.stack.addEventListener("pointermove", (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = e.clientX - drag.x0;
    drag.dom.style.transition = "none";
    drag.dom.style.transform = "translateX(" + dx + "px) rotate(" + (dx / 18) + "deg)";
    const half = domWidth(drag.dom) * 0.35;
    drag.dom.querySelector(".stamp.go-l").style.opacity = dx < -half ? 1 : 0;
    drag.dom.querySelector(".stamp.go-r").style.opacity = dx > half ? 1 : 0;
    drag.dx = dx;
  });

  el.stack.addEventListener("pointerup", (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = drag.dx || 0;
    const dt = Date.now() - drag.t0;
    const w = domWidth(drag.dom);
    const commit = Math.abs(dx) > w * 0.28 || (dt < 250 && Math.abs(dx) > w * 0.1);
    const dom = drag.dom;
    drag = null;
    if (commit && dx !== 0) {
      swipe(dx < 0 ? "left" : "right");
    } else {
      dom.style.transition = "transform 0.2s ease";
      dom.style.transform = "";
      dom.querySelectorAll(".stamp").forEach((s) => { s.style.opacity = 0; });
    }
  });

  el.stack.addEventListener("pointercancel", () => {
    if (!drag) return;
    drag.dom.style.transform = "";
    drag.dom.querySelectorAll(".stamp").forEach((s) => { s.style.opacity = 0; });
    drag = null;
  });

  el.btnLeft.addEventListener("click", () => swipe("left"));
  el.btnRight.addEventListener("click", () => swipe("right"));
  document.addEventListener("keydown", (e) => {
    if (el.game.hidden) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); swipe("left"); }
    if (e.key === "ArrowRight") { e.preventDefault(); swipe("right"); }
  });

  el.startBtn.addEventListener("click", startRun);
  el.againBtn.addEventListener("click", startRun);
  el.homeBtn.addEventListener("click", () => {
    clearUrgent();
    session = null;
    el.actions.hidden = true;
    el.dayChip.hidden = true;
    document.body.classList.remove("danger", "playing");
    showScreen("home");
    renderHome();
  });

  function renderHome() {
    const n = DECK.length;
    el.deckMeta.textContent = n ? "卡庫 " + n + " 張 · 撐到開考" : "卡組仲未載入。";
    if (store.best_days > 0) {
      el.bestChip.hidden = false;
      el.bestNum.textContent = String(store.best_days);
    }
  }

  renderHome();
})();
