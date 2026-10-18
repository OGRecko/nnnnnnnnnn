// Regenerates THIRD-PARTY-NOTICES.md and public/third-party-notices.html from package-lock.json.
// Licenses come from the lockfile entry, falling back to the installed package.json. Nothing here is hand-maintained.
import fs from 'node:fs';
import path from 'node:path';
const root = process.cwd();
const lock = JSON.parse(fs.readFileSync(path.join(root, 'package-lock.json'), 'utf8'));
// Licenses missing from package metadata, resolved from public package/repository docs (listed in the notices footer).
const RESOLVED = { 'limiter@1.1.5': 'MIT', 'png-js@1.1.0': 'MIT', 'webgl-constants@1.1.1': 'MIT' };
const rows = new Map();
for (const [k, v] of Object.entries(lock.packages || {})) {
  if (!k || !v?.version) continue;
  let name = v.name || (k.includes('node_modules/') ? k.split('node_modules/').pop() : null);
  if (!name) continue;
  let license = v.license;
  if (!license) {
    try { license = JSON.parse(fs.readFileSync(path.join(root, k, 'package.json'), 'utf8')).license; } catch { /* not installed */ }
  }
  if (license && typeof license === 'object') license = license.type;
  rows.set(`${name}@${v.version}`, { name, version: v.version, license: license || RESOLVED[`${name}@${v.version}`] || 'UNKNOWN' });
}
const sorted = [...rows.values()].sort((a, b) => a.name.localeCompare(b.name) || a.version.localeCompare(b.version, undefined, { numeric: true }));
const unknown = sorted.filter((r) => r.license === 'UNKNOWN');
const today = new Date().toISOString().slice(0, 10);

const mdPath = path.join(root, 'THIRD-PARTY-NOTICES.md');
const oldMd = fs.readFileSync(mdPath, 'utf8');
const tableEnd = oldMd.lastIndexOf('\n| ');
const tail = tableEnd >= 0 ? oldMd.slice(oldMd.indexOf('\n', tableEnd + 1)) : '\n';
const md = ['# Cavity Audio — Third-party notices', '',
  `Generated from \`package-lock.json\` on ${today} by \`scripts/generate-third-party-notices.mjs\`. This is an inventory, not a replacement for the license text shipped with each dependency.`, '',
  '| Package | Version | License |', '|---|---|---|',
  ...sorted.map((r) => '| `' + r.name.replaceAll('`', '') + '` | `' + r.version + '` | `' + r.license.replaceAll('`', '') + '` |')].join('\n') + tail;
fs.writeFileSync(mdPath, md);

const htmlPath = path.join(root, 'public/third-party-notices.html');
const oldHtml = fs.readFileSync(htmlPath, 'utf8');
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const body = sorted.map((r) => `<tr><td>${esc(r.name)}</td><td>${esc(r.version)}</td><td>${esc(r.license)}</td></tr>`).join('\n');
let html = oldHtml.replace(/<tbody>[\s\S]*<\/tbody>/, `<tbody>\n${body}\n</tbody>`);
html = html.replace(/<strong>Generated [^<]*<\/strong>/, `<strong>Generated ${today}.</strong>`);
fs.writeFileSync(htmlPath, html);
console.log(JSON.stringify({ packages: sorted.length, unknownLicense: unknown.map((r) => `${r.name}@${r.version}`) }));
