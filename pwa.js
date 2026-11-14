/* ===== DSE Hub — 一鍵安裝 Web App（PWA） ===== */
"use strict";

(function () {
  var scriptSrc = document.currentScript ? document.currentScript.src : location.href;
  var swUrl = new URL("sw.js", scriptSrc).href;

  var standalone =
    (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) ||
    window.navigator.standalone === true;
  var deferred = null;
  var listeners = [];

  if (standalone) document.documentElement.classList.add("pwa-standalone");

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferred = e;
    listeners.forEach(function (fn) { fn(true); });
  });

  window.addEventListener("appinstalled", function () {
    deferred = null;
    document.documentElement.classList.add("pwa-installed");
    listeners.forEach(function (fn) { fn(false); });
  });

  function promptInstall() {
    if (!deferred) return Promise.resolve(false);
    var ev = deferred;
    ev.prompt();
    return ev.userChoice.then(function (choice) {
      if (choice && choice.outcome === "accepted") deferred = null;
      listeners.forEach(function (fn) { fn(!!deferred); });
      return !!(choice && choice.outcome === "accepted");
    }).catch(function () { return false; });
  }

  window.DSEPWA = {
    isStandalone: standalone,
    canInstall: function () { return !!deferred; },
    promptInstall: promptInstall,
    onAvailability: function (fn) { listeners.push(fn); fn(!!deferred); }
  };

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register(swUrl).catch(function () { /* 離線快取不可用時照常上網 */ });
    });
  }

  document.addEventListener("click", function (e) {
    var tip = document.getElementById("installTip");

    var close = e.target.closest("[data-install-close]");
    if (close) {
      if (tip) tip.hidden = true;
      return;
    }

    var btn = e.target.closest("[data-install-app]");
    if (!btn) return;
    e.preventDefault();

    if (standalone) {
      if (tip) tip.hidden = true;
      btn.setAttribute("data-state", "installed");
      return;
    }

    if (deferred) {
      promptInstall();
      return;
    }

    if (tip) {
      tip.hidden = false;
      tip.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  });
})();
