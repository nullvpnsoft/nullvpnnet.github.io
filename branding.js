/* branding.js — theme-color & theme-state sync (r54: first-party edition).
 *
 * r54 CHANGE — the runtime design-token sync with the cabinet backend was
 * removed. It pointed at the DEV cabinet (cdn-dev.nullvpn.net), leaked every
 * visitor's IP to a third-party host on every page view, and in practice was
 * a no-op (the DEV palette it returned equals the tokens bundled in
 * style.css, so applyColors set identical values). The PROD cabinet serves a
 * DIFFERENT operator palette whose accent would also fail the r46 white-text
 * AA contrast work if auto-applied. The marketing site's palette is now
 * fully site-owned; if palette sync is ever wanted again it must be
 * re-designed: point at PROD, and only apply after contrast validation.
 *
 * What remains (and why this file still exists):
 *   1. <meta name="theme-color"> follows the manual light/dark toggle
 *      (data-theme on <html>) so mobile browser chrome matches the page.
 *   2. aria-pressed on the light/dark buttons stays in step (r51) — the
 *      visible .active class is sighted-only state; screen readers need
 *      aria-pressed. One central sync covers every page's inline setTheme
 *      copies without touching them.
 *   3. r56: wraps the global setTheme with a View Transitions circular
 *      reveal (progressive enhancement; reduced-motion + no-API safe).
 *
 * Failure modes are silent by design: any error leaves the static tokens.
 */
(function () {
  'use strict';

  function applyThemeColor() {
    var metas = document.querySelectorAll('meta[name="theme-color"]');
    if (!metas.length) return;
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    var value = dark ? '#0a0f1a' : '#f7e7ce';
    // r54: the static second meta carried media="(prefers-color-scheme: dark)",
    // which kept winning over the manual toggle for OS-dark users (toggle to
    // light -> page light, browser chrome stayed dark). Normalize: every meta
    // follows data-theme, media qualifiers dropped.
    for (var i = 0; i < metas.length; i++) {
      metas[i].removeAttribute('media');
      metas[i].setAttribute('content', value);
    }
  }

  // Keep theme-color in step with the site's manual light/dark toggle.
  // setTheme() flips data-theme on <html>; we observe attribute changes so no
  // per-page JS edits are needed.
  try {
    var observer = new MutationObserver(function () { applyThemeColor(); syncThemePressed(); });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  } catch (_) { /* very old browsers: theme-color just stays static */ }

  // r51: keep aria-pressed on the light/dark buttons in step with data-theme.
  function syncThemePressed() {
    try {
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      var lightBtn = document.getElementById('themeLight');
      var darkBtn = document.getElementById('themeDark');
      if (lightBtn) lightBtn.setAttribute('aria-pressed', String(!dark));
      if (darkBtn) darkBtn.setAttribute('aria-pressed', String(dark));
    } catch (_) { /* never break the page over state sync */ }
  }
  syncThemePressed();
  applyThemeColor();

  // r54 hygiene: drop the orphaned palette cache the removed sync used to
  // write (nullvpn.branding.v1) from returning visitors' localStorage.
  try { localStorage.removeItem('nullvpn.branding.v1'); } catch (_) {}

  // r56: theme flips animate as a circular reveal growing from the click
  // point (View Transitions API). The 14 per-page inline setTheme copies stay
  // untouched: this defer script runs after them, and onclick="setTheme(...)"
  // resolves window.setTheme at CALL time, so wrapping the global here covers
  // every page from one place. Guards: reduced-motion users and browsers
  // without the API keep the instant flip; keyboard/synthetic clicks
  // (e.detail === 0) don't move the origin — a stale pointer coordinate or
  // the viewport center is used instead.
  try {
    var origSetTheme = window.setTheme;
    if (typeof origSetTheme === 'function' && document.startViewTransition) {
      var lastPt = { x: -1, y: -1 };
      document.addEventListener('click', function (e) {
        if (e && e.detail > 0 && typeof e.clientX === 'number') {
          lastPt.x = e.clientX; lastPt.y = e.clientY;
        }
      }, true);
      window.setTheme = function (theme) {
        var reduced = window.matchMedia &&
          matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reduced) { origSetTheme(theme); return; }
        var x = lastPt.x, y = lastPt.y;
        if (x < 0) { x = window.innerWidth / 2; y = window.innerHeight / 2; }
        var vt = document.startViewTransition(function () { origSetTheme(theme); });
        if (vt && vt.ready && document.documentElement.animate) {
          vt.ready.then(function () {
            var r = Math.hypot(
              Math.max(x, window.innerWidth - x),
              Math.max(y, window.innerHeight - y)
            );
            document.documentElement.animate(
              { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)',
                           'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
              { duration: 400, easing: 'ease-in-out',
                pseudoElement: '::view-transition-new(root)' }
            );
          }).catch(function () { /* reveal is cosmetic; flip already happened */ });
        }
      };
    }
  } catch (_) { /* theme flips stay instant */ }
})();
