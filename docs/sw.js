/* ===== DSE Hub service worker â€” ç¶²çµ¡å„ªå…ˆï¼Œæ–·ç·šç”¨å¿«å– ===== */
"use strict";

const CACHE = "dsehub-v202611081433";
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

  // è©¦å· PDF ç›´æŽ¥ç”±ç€è¦½å™¨ä¸‹è¼‰ï¼Œå””ä½”é›¢ç·šå¿«å–
  if (/\.pdf$/i.test(url.pathname)) return;

  // é é¢å°Žè¦½ï¼šå…ˆä¸Šç¶²ï¼Œå¤±æ•—å…ˆç”¨å¿«å–ï¼ˆé›¢ç·šéƒ½é–‹å¾—è¿”ï¼‰
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

  // éœæ…‹è³‡æºï¼šç¶²çµ¡å„ªå…ˆï¼ˆæ›´æ–°å³è¦‹ï¼‰ï¼Œé›¢ç·šæ™‚ç”¨å¿«å–
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
