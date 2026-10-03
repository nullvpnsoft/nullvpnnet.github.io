#!/usr/bin/env node
/**
 * tools/check_html_i18n.js — gate: every data-i18n key used in any HTML page
 * must exist in T (i18n.js) for all 7 locales; T itself must be complete.
 * Durable copy kept at /home/z/my-project/tools/ (sandbox wipes /home/z between
 * sessions; /home/z/my-project persists).
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const LOCALES = ['en', 'ru', 'fa', 'ar', 'es', 'ne', 'fr'];

const i18nSrc = readFileSync(join(ROOT, 'i18n.js'), 'utf8');
const tStart = i18nSrc.indexOf('const T = {');
if (tStart < 0) { console.error('FATAL: T not found'); process.exit(1); }
let depth = 0, i = tStart + 'const T = {'.length - 1, end = -1;
for (; i < i18nSrc.length; i++) {
  const c = i18nSrc[i];
  if (c === '{') depth++;
  else if (c === '}') { depth--; if (depth === 0) { end = i; break; } }
}
if (end < 0) { console.error('FATAL: T terminator not found'); process.exit(1); }
const tBody = i18nSrc.slice(tStart, end + 1);

const keys = new Set();
const keyRe = /\n  "([A-Za-z0-9._-]+)": \{/g;
let m;
while ((m = keyRe.exec(tBody))) keys.add(m[1]);

const missing = {};
for (const l of LOCALES) missing[l] = new Set();
for (const key of keys) {
  const kStart = tBody.indexOf(`"${key}": {`);
  const kEnd = tBody.indexOf('\n  },', kStart);
  const block = tBody.slice(kStart, kEnd);
  for (const l of LOCALES) {
    if (!new RegExp(`\\b${l}: `).test(block)) missing[l].add(key);
  }
}

const pages = readdirSync(ROOT).filter((f) => f.endsWith('.html'));
let pageErrors = 0;
let usages = 0;
for (const page of pages) {
  const html = readFileSync(join(ROOT, page), 'utf8');
  const re = /data-i18n(?:-attr|-html)?="([^"]+)"/g;
  let mm;
  while ((mm = re.exec(html))) {
    usages++;
    const k = mm[1];
    if (!keys.has(k)) { console.error(`${page}: MISSING KEY IN T: ${k}`); pageErrors++; }
  }
}

let missingTotal = 0;
for (const l of LOCALES) {
  const real = [...missing[l]];
  if (real.length) { console.error(`T: ${real.length} keys missing ${l} value`); missingTotal += real.length; }
}

console.log(`T: ${keys.size} keys × ${LOCALES.length} locales`);
console.log(`pages: ${pages.length}, data-i18n usages: ${usages}`);
if (pageErrors === 0 && missingTotal === 0) { console.log('check_html_i18n: CLEAN'); process.exit(0); }
console.log(`check_html_i18n: FAIL (${pageErrors} page errors, ${missingTotal} missing values)`);
process.exit(1);
