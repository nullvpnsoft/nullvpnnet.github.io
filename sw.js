/* nullvpn.net service worker — r58
 * Strategies:
 *   - Navigations (HTML): network-first with cache fallback (fresh deploys always
 *     win; cache only bridges offline gaps).
 *   - Same-origin static assets: cache-first (cache busters vNN make versions
 *     unique, so a bumped ?v= is a brand-new cache entry — never stale).
 *   - Cross-origin (GitHub API, t.me, …): untouched.
 * Precache (r45): versioned assets (style.css / i18n.js) are discovered from
 * the live root HTML at install time instead of being hardcoded — the old
 * hardcoded list had silently drifted 3 deploys behind the busters (v11/v16
 * vs live v20/v14), leaving a first-visit-offline user with an unstyled shell.
 * Offline page (r55): uncached navigations now fall back to /offline.html
 * (branded, self-localizing) instead of silently serving the homepage.
 * r58 storage hygiene: (1) activate prunes stale VERSIONED entries — a bump
 * leaves the old ?v= behind in the same cache (name never changes), which
 * accumulated ~400KB of dead i18n/style per round for returning visitors;
 * (2) '/branding.js' dropped from PRECACHE — pages request branding.js?v=N,
 * so the unversioned entry was cached but never matched (discovery from live
 * HTML already handles the versioned URL).
 * r64: self-hosted font subsets precached (168K total) — a first-visit-offline
 *   user now gets the brand typography instead of a system-font flash.
 * CACHE bumped v2→v3 to purge stale shells cached under the old name.
 * r97: navigations are cached under their PATHNAME only and fallback matching
 *   uses ignoreSearch — deep links like /faq.html?q=refund now resolve from
 *   cache offline instead of hitting the offline page, and query variants
 *   (?cat=, ?q=) stop duplicating full HTML entries in the cache.
 * r103: network-first now means it. fetch(req) ran in default cache mode, so
 *   the browser HTTP cache (GitHub Pages max-age=600) answered BEFORE the
 *   network — returning visitors saw stale page HTML for up to 10 minutes
 *   after every deploy (observed live in r101). cache:'reload' forces the
 *   fetch to bypass the HTTP cache; the offline path is untouched (a failed
 *   reload still lands in the catch -> cache fallback). CACHE bumped
 *   v3->v4 to purge the legacy pre-r97 query-variant navigation entries
 *   (6 pricing variants observed) that pruneStaleVersions never touches
 *   (it only prunes versioned ?v= entries).
 */
const CACHE = 'nullvpn-v4';
const PRECACHE = [
  '/',
  '/index.html',
  '/offline.html',
  '/favicon.png',
  '/apple-touch-icon.png',
  '/favicon.ico',
  '/site.webmanifest',
  // r64: font subsets (stable filenames, no busters — cache-first matches)
  '/fonts/manrope-var-latin.woff2',
  '/fonts/manrope-var-latin-ext.woff2',
  '/fonts/manrope-var-cyrillic.woff2',
  '/fonts/outfit-var-latin.woff2',
  '/fonts/outfit-var-latin-ext.woff2',
  '/fonts/ibmplexmono-400-latin.woff2',
  '/fonts/ibmplexmono-400-cyrillic.woff2',
  '/fonts/ibmplexmono-500-latin.woff2',
  '/fonts/ibmplexmono-500-cyrillic.woff2',
];

async function precache() {
  const c = await caches.open(CACHE);
  const urls = new Set(PRECACHE);
  try {
    const r = await fetch('/', { cache: 'no-store' });
    if (r.ok) {
      const found = (await r.clone().text()).match(/(?:style\.css|i18n\.js|branding\.js)\?v=\d+/g) || [];
      found.forEach((u) => urls.add(u));
      await c.put('/', r);
      urls.delete('/'); // fresh copy already cached; don't refetch
    }
  } catch (_) { /* offline install: best-effort shell below */ }
  // Individual puts: one bad URL must never fail the whole install.
  await Promise.allSettled([...urls].map((u) => c.add(u)));
}

self.addEventListener('install', (e) => {
  e.waitUntil(precache().then(() => self.skipWaiting()));
});

// r58: bumping a buster leaves the previous ?v= entry in the SAME cache (the
// cache name only changes on deliberate major bumps like v2→v3). Old i18n.js
// and style.css copies are dead weight (~400KB per round for daily visitors).
// Keep the highest ?v= per pathname; never touch unversioned entries (HTML,
// icons) or non-numeric params (e.g. /faq.html?cat=pay navigations).
async function pruneStaleVersions() {
  const c = await caches.open(CACHE);
  const keys = await c.keys();
  const byPath = new Map();
  for (const k of keys) {
    const u = new URL(k.url);
    const v = u.searchParams.get('v');
    if (v === null || !/^\d+$/.test(v)) continue;
    if (!byPath.has(u.pathname)) byPath.set(u.pathname, []);
    byPath.get(u.pathname).push({ v: Number(v), key: k });
  }
  const dels = [];
  for (const list of byPath.values()) {
    const max = Math.max.apply(null, list.map((x) => x.v));
    list.forEach((x) => { if (x.v < max) dels.push(c.delete(x.key)); });
  }
  await Promise.all(dels);
  return dels.length;
}

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(pruneStaleVersions)
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return; // external: pass through

  const isNav = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  if (isNav) {
    e.respondWith(
      /* r103: cache:'reload' — bypass the browser HTTP cache (GH Pages
       * max-age=600) so a deploy is visible to returning visitors on their
       * very next load, not ten minutes later. */
      fetch(req, { cache: 'reload' })
        .then((resp) => {
          // r70: mirror the asset branch's guard — only cache OK responses.
          // Caching 404 navigations (typos, removed pages) bloated the cache
          // and could serve a stale error page offline for a URL that may
          // exist later. Failed responses simply fall through uncached.
          // r97: store under the PATHNAME only — static hosting serves one
          // document per path, so /faq.html?q=x and /faq.html are the same
          // entry; no query-variant duplicates, and ignoreSearch below hits.
          if (resp.ok && resp.type === 'basic') {
            const copy = resp.clone();
            const clean = new URL(req.url);
            clean.search = '';
            clean.hash = '';
            caches.open(CACHE).then((c) => c.put(new Request(clean.href), copy));
          }
          return resp;
        })
        .catch(() =>
          // r55: dedicated offline page for navigations that were never cached.
          // Falls back to the homepage only if offline.html itself is missing
          // (e.g. a user whose old SW installed before the precache existed).
          // r97: ignoreSearch lets a deep-linked navigation (?cat=, ?q=)
          // resolve from the cached bare pathname while offline.
          caches.match(req, { ignoreSearch: true })
            .then((m) => m || caches.match('/offline.html'))
            .then((m) => m || caches.match('/index.html'))
        )
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(
      (m) =>
        m ||
        fetch(req).then((resp) => {
          if (resp.ok && resp.type === 'basic') {
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(req, copy));
          }
          return resp;
        })
    )
  );
});
