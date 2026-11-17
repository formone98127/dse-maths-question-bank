/* ===== DSE Hub service worker — 網絡優先，斷線時使用快取 ===== */
"use strict";


<<<<<<< HEAD
<<<<<<< HEAD
const CACHE = "dsehub-v202611172310";
=======
const CACHE = "dsehub-v202611172310";
=======
const CACHE = "dsehub-v202611172310";
=======
const CACHE = "dsehub-v202611172310";
>>>>>>> e64f7c8 (2025 P1 圖：Q12a 幹葉圖行距／欄距／分隔線對齊原卷)
>>>>>>> aac36b6 (2025 P1 圖：Q12a 幹葉圖、Q12b 框線圖 100% 照原卷重排（欄距、虛線導引、鬚線不穿框、標籤貼軸）)
const SHELL = [
  "./",
  "./hub/",
  "./hub/style.css",
  "./hub/app.js",
  "./hub/data.js",
  "./data.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => Promise.allSettled(SHELL.map((url) => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  let url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (url.origin !== self.location.origin) return;

  // 試卷 PDF 直接由瀏覽器下載，不作離線快取
  if (/\.pdf$/i.test(url.pathname)) return;

  // 頁面導航：先連網，失敗時使用快取（離線仍可開啟）
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match("./hub/") || caches.match("./"))
        )
    );
    return;
  }

  // 靜態資源：網絡優先（更新即時可見），離線時使用快取
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res && res.ok && res.type === "basic") {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      })
      .catch(() => caches.match(req))
  );
});
