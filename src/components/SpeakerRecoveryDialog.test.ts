import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { SpeakerRecoveryView } from './SpeakerRecoveryDialog';
import type { UnresolvedSpeakerRef } from '../lib/speakerRecovery';

let passed = 0;
function check(name: string, fn: () => void) { try { fn(); passed++; console.log(`  PASS  ${name}`); } catch (e: any) { console.error(`  FAIL  ${name}\n        ${e?.stack ?? e}`); process.exitCode = 1; } }
console.log('\n=== SpeakerRecoveryDialog (server-rendered markup) ===\n');

const archivedRef: UnresolvedSpeakerRef = { sourceId: 'a', sourceNumber: 1, speakerId: 'legacy-jbl-5', status: 'archived', savedBrand: 'JBL', savedModel: 'Old 5',
  archived: { brand: 'JBL', model: '4311 Studio Monitor', reason: 'Duplicate of jbl-4311.', archivedDate: '2026-10-12' }, suggestedReplacementId: 'jbl-4311' };
const unknownRef: UnresolvedSpeakerRef = { sourceId: 'b', sourceNumber: 2, speakerId: 'typo-id', status: 'unknown' };
const noop = () => {};
const render = (o: Partial<React.ComponentProps<typeof SpeakerRecoveryView>> = {}) => renderToStaticMarkup(React.createElement(SpeakerRecoveryView, { unresolved: [archivedRef, unknownRef], choices: {}, onChoose: noop, onSubmit: noop, onCancel: noop, ...o }));

check('it is a labelled, described, modal dialog and the label/description ids point at real elements', () => {
  const h = render(); assert.match(h, /role="dialog"/); assert.match(h, /aria-modal="true"/);
  const labelled = /aria-labelledby="([^"]+)"/.exec(h)![1], described = /aria-describedby="([^"]+)"/.exec(h)![1];
  assert.ok(h.includes(`id="${labelled}"`) && h.includes(`id="${described}"`)); assert.match(h, /<h2[^>]*data-autofocus/);
});

check('each affected source is its own fieldset with a legend naming the saved speaker and its position', () => {
  const h = render(); assert.equal((h.match(/<fieldset/g) ?? []).length, 2); assert.match(h, /<legend[^>]*>Source 1: JBL Old 5/); assert.match(h, /Source 2: Unknown speaker/);
});

check('archived and never-in-catalog are clearly different messages, and the archive reason and date are shown', () => {
  const h = render(); assert.match(h, /Archived\.<\/strong> This speaker was removed from the catalog on 2026-10-12/); assert.match(h, /Duplicate of jbl-4311\./);
  assert.match(h, /Not in the catalog\.<\/strong> The ID &quot;typo-id&quot; was never a catalog speaker/);
});

check('a redirect from the archive is presented as a suggestion only, with an explicit button', () => {
  const h = render(); assert.match(h, /only a suggestion; nothing is replaced until you choose it/); assert.match(h, /Use [^<]+4311[^<]*<\/button>/);
  assert.equal((h.match(/only a suggestion/g) ?? []).length, 1, 'no suggestion for the unknown ID');
});

check('search is an accessible combobox + listbox of live speakers', () => {
  const h = render(); assert.match(h, /type="search"/); assert.match(h, /role="combobox"/); assert.match(h, /aria-controls="[^"]+"/); assert.match(h, /role="listbox"/); assert.match(h, /role="option"/);
  assert.ok((h.match(/role="option"/g) ?? []).length >= 2);
});

check('open button is disabled and the status says how many are missing until EVERY source has a choice', () => {
  const h = render(); assert.match(h, /Choose a replacement for 2 more sources/); assert.match(h, /<button[^>]*disabled=""[^>]*aria-disabled="true"[^>]*>Open with replacements/);
  const one = render({ choices: { a: 'jbl-4311' } }); assert.match(one, /Choose a replacement for 1 more source</); assert.match(one, /disabled=""/);
  assert.match(one, /Replacement: <strong>JBL /, 'the chosen speaker is displayed with a Change button'); assert.match(one, />Change</);
  const all = render({ choices: { a: 'jbl-4311', b: 'jbl-l100' } }); assert.match(all, /2 replacements chosen/); assert.doesNotMatch(all, /<button[^>]*disabled=""[^>]*>Open with replacements/);
});

check('Cancel is always available and says the project will not be opened', () => { assert.match(render(), />Cancel, don&#x27;t open</); });

check('errors are announced through an assertive live region; with no error the region is present but visually hidden', () => {
  assert.match(render({ error: 'Choose a replacement for source 2.' }), /role="alert"[^>]*aria-live="assertive"[^>]*>Choose a replacement for source 2\./);
  assert.match(render(), /role="alert"[^>]*class="sr-only"/);
});

check('the copy states the safety guarantees: file unchanged, nothing automatic, history recorded on save', () => {
  const h = render(); assert.match(h, /Your file is not changed/); assert.match(h, /Nothing is replaced automatically/); assert.match(h, /recorded in the project once you save it/);
});

check('hostile text from a saved file is escaped, never injected as markup', () => {
  const evil: UnresolvedSpeakerRef = { ...unknownRef, speakerId: '"><img src=x onerror=alert(1)>', savedBrand: '<script>alert(1)</script>', savedModel: '<b onmouseover=x>' };
  const h = render({ unresolved: [evil] }); assert.doesNotMatch(h, /<script>alert/); assert.doesNotMatch(h, /<img src=x/); assert.doesNotMatch(h, /<b onmouseover/);
  assert.match(h, /&lt;script&gt;/);
});

check('both themes render with readable, distinct palettes, and the panel is scrollable on small screens', () => {
  const d = render({ theme: 'dark' }), l = render({ theme: 'light' }); assert.notEqual(d, l); assert.match(d, /bg-\[#16181c\]/); assert.match(l, /bg-white/); assert.match(d, /max-h-\[90vh\] overflow-y-auto/);
});

check('singular wording: one source, one replacement', () => {
  const h = render({ unresolved: [archivedRef], choices: { a: 'jbl-4311' } }); assert.match(h, /1 replacement chosen/); assert.doesNotMatch(h, /1 replacements/);
});

console.log(`\n=== ${passed} passed ===`);
