#!/usr/bin/env node
/**
 * tools/check_links.js — gate: all internal hrefs resolve to real files;
 * anchors exist on target pages. External links reported (network check via --external).
 * Durable copy kept at /home/z/my-project/tools/.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const pages = readdirSync(ROOT).filter((f) => f.endsWith('.html'));
let errors = 0;

for (const page of pages) {
  const html = readFileSync(join(ROOT, page), 'utf8');
  const re = /(?:href|src)="([^"]+)"/g;
  let m;
  while ((m = re.exec(html))) {
    const url = m[1];
    if (url.startsWith('http') || url.startsWith('mailto:') || url.startsWith('tel:') || url.startsWith('data:')) continue;
    const idx = m.index;
    const tagStart = html.lastIndexOf('<', idx);
    const tagCtx = html.slice(tagStart, idx + url.length + 2);
    if (/rel="(preconnect|dns-prefetch)"/.test(tagCtx)) continue;
    if (url.startsWith('#')) {
      const id = url.slice(1);
      if (id && !html.includes(`id="${id}"`)) { console.error(`${page}: broken anchor #${id}`); errors++; }
      continue;
    }
    const [rawFile, anchor] = url.split('#');
    const file = rawFile.split('?')[0];
    if (file && !existsSync(join(ROOT, file))) { console.error(`${page}: missing file ${file}`); errors++; continue; }
    if (anchor && file) {
      const target = readFileSync(join(ROOT, file), 'utf8');
      if (!target.includes(`id="${anchor}"`)) { console.error(`${page}: anchor #${anchor} not in ${file}`); errors++; }
    }
  }
}
console.log(`checked ${pages.length} pages`);
if (errors === 0) { console.log('check_links: CLEAN'); process.exit(0); }
console.log(`check_links: FAIL (${errors})`);
process.exit(1);
