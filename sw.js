// Offline cache for the IFDSM question bank.
// Bump VERSION whenever you change index.html so devices pick up the update.
const VERSION = "ifdsm-qb-v1";
const ASSETS = ["./", "index.html", "manifest.webmanifest",
  "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
// Network first for the page (so updates arrive), cache fallback when offline.
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) {
    // Google Fonts: try network, then cache; the page falls back to system fonts if neither works.
    e.respondWith(caches.open(VERSION).then((c) => fetch(req).then((r) => { c.put(req, r.clone()); return r; })
      .catch(() => c.match(req))));
    return;
  }
  e.respondWith(fetch(req).then((r) => { const copy = r.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); return r; })
    .catch(() => caches.match(req).then((m) => m || caches.match("index.html"))));
});
