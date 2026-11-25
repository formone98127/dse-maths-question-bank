/* GA4 事件追蹤（靜態注入，全 landing 頁載入）。
 * 問題頁由 build_seo 寫入 data-* 屬性（data-qpage data-topic data-year data-paper data-qno data-lang）。
 * 事件：question_reveal / scroll_90 / quiz_complete / share_click / copy_link
 * 冇 data-qpage 嘅頁只報 scroll_90（站內深讀訊號）。 */
(function () {
  "use strict";
  if (!window.gtag) return; // GA4 未載入（如 adblock）就唔使做嘢

  var body = document.body;
  if (!body) return;
  var dims = function (extra) {
    var o = extra || {};
    if (body.hasAttribute("data-qpage")) {
      o.topic = body.getAttribute("data-topic") || "(none)";
      o.year = body.getAttribute("data-year") || "";
      o.paper = body.getAttribute("data-paper") || "";
      o.qno = body.getAttribute("data-qno") || "";
      o.lang = body.getAttribute("data-lang") || "";
    }
    return o;
  };
  var ev = function (name, params) {
    try {
      gtag("event", name, dims(params));
    } catch (e) { /* ignore */ }
  };

  // --- 答案揭露：任何 details/summary 或 .reveal 類開關都計一次（每頁一次）---
  var revealed = false;
  document.addEventListener("click", function (e) {
    if (revealed) return;
    var t = e.target;
    var sum = t.closest && t.closest("summary, .reveal-btn, .show-answer, [data-reveal]");
    if (sum) {
      revealed = true;
      ev("question_reveal");
    }
  }, true);

  // --- 深讀：捲到 90% ---
  var scrolled = false;
  window.addEventListener("scroll", function () {
    if (scrolled) return;
    var doc = document.documentElement;
    var max = (doc.scrollHeight - window.innerHeight);
    if (max > 0 && (window.scrollY / max) >= 0.9) {
      scrolled = true;
      ev("scroll_90");
    }
  }, { passive: true });

  // --- quiz 完成（quiz 系統 dispatch 嘅自訂事件）---
  document.addEventListener("quiz:complete", function (e) {
    ev("quiz_complete", { score: (e.detail && e.detail.score) || "" });
  });

  // --- 分享掣：任何 share 意圖連結／按鈕 ---
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t.closest) return;
    var s = t.closest("[data-share], a[href*='wa.me/'], a[href*='t.me/share'], a[href*='facebook.com/sharer'], a[href*='twitter.com/intent']");
    if (s) {
      var net = s.getAttribute("data-share") || "other";
      ev("share_click", { network: net });
    }
  }, true);

  // --- 複製連結 ---
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t.closest) return;
    var c = t.closest("[data-copy-link]");
    if (c) {
      var url = c.getAttribute("data-copy-link") || location.href;
      var done = function () { ev("copy_link"); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (err) {}
        document.body.removeChild(ta);
        done();
      }
    }
  }, true);
})();
