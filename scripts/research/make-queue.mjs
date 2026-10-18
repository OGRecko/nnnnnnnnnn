// Regenerates RESEARCH-QUEUE.md from the dataset (see that file's header).
import fs from 'node:fs';
import path from 'node:path';
const d = JSON.parse(fs.readFileSync('src/data/speakers.json', 'utf8'));
// Field-level queue: every record is PARTIALLY_VERIFIED, so filtering on overallStatus
// would always produce zero. Derive the queue from the provenance inventory instead.
const inv = JSON.parse(fs.readFileSync(path.join('scripts/research/field-provenance-inventory.json'), 'utf8')).entries;
const backlogStates = new Set(['CITED_IN_NOTES_UNCHECKED', 'UNSOURCED', 'NO_PROVENANCE']);
const backlogIds = new Set(inv.filter((e) => e.location === 'LIVE' && backlogStates.has(e.storedStatus)).map((e) => e.speakerId));
const todo = d.filter((s) => backlogIds.has(s.id));
const by = {};
for (const s of todo) (by[s.brand] ??= []).push(s);
const brands = Object.entries(by).sort((a, b) => b[1].length - a[1].length);
let o = '# Speaker research queue (generated from src/data/speakers.json)\n\nGenerated, not hand-edited. Regenerate with: node scripts/research/make-queue.mjs\n\n';
o += `Records still needing research: **${todo.length}** of ${d.length} (${todo.filter((s) => s.overallStatus === 'UNVERIFIED').length} UNVERIFIED, ${todo.filter((s) => s.overallStatus === 'UNAVAILABLE').length} UNAVAILABLE) across ${brands.length} brands.\n\n`;
o += 'Rules for every entry: exact model + revision; manufacturer page/manual/datasheet fetched (not a search snippet); populated fields carry their URL; anything unpublished stays N/A. Some discontinued or legacy models will have NO online manufacturer data and must stay UNVERIFIED.\n\n| Brand | Remaining | Models |\n|---|---|---|\n';
for (const [b, l] of brands) o += `| ${b} | ${l.length} | ${l.map((s) => `${s.model} (\`${s.id}\`)`).join('; ')} |\n`;
fs.writeFileSync('scripts/research/RESEARCH-QUEUE.md', o);
console.log(todo.length, 'records,', brands.length, 'brands');
