#!/usr/bin/env python3
"""Prepare and validate Round 26 provenance-audit artifacts.

1. Record Decision 8 host-operator checks for the hosts opened this round in
   source-host-allowlist.json (never downgrading an existing entry).
2. Build round26-url-results.json from round26_evidence_data.py.

Only fields whose live provenance still points at the checked URL with status
CITED_IN_NOTES_UNCHECKED are written; values always come from the live catalogue.
Every tied field must be declared explicitly in the evidence table: there is no
default outcome, so a page that was opened for one field can never silently
"assess" another one.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
ALLOW = os.path.join(HERE, 'source-host-allowlist.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
R26_URLS = os.path.join(HERE, 'round26-url-results.json')
CHECKED_DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


HOST_UPDATES = {
    'www.sisme.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Sisme S.p.A. (Italian L-Acoustics distributor)',
        'evidence': [
            'https://www.sisme.com/media/3071/lacoustics-arcsii_ds.pdf is an L-Acoustics-branded ARCS II data sheet served from the distributor host; it carries the ARCS II specification table quoted in Round 26.',
        ],
        'sources': ['https://www.sisme.com/media/3071/lacoustics-arcsii_ds.pdf'],
        'note': 'Distributor host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'www.customsounds.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Custom Sounds (authorized JL Audio dealer)',
        'evidence': [
            'https://www.customsounds.com/uploads/docs/377c821058ecf356e1c0be4aa8bd69a2260bcc04.pdf is JL Audio\'s own 10W3v3 owner\'s manual, served verbatim by the dealer; it carries the text quoted in Round 26.',
        ],
        'sources': ['https://www.customsounds.com/uploads/docs/377c821058ecf356e1c0be4aa8bd69a2260bcc04.pdf'],
        'note': 'Authorized-dealer host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'tacotunes.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Taco Tunes (authorized JL Audio dealer)',
        'evidence': [
            'https://tacotunes.com/wp-content/uploads/2013/02/JL-Audio-C3-650-Component-Speakers-Manual.pdf is JL Audio\'s C3-650 owner\'s manual served verbatim by the dealer.',
        ],
        'sources': ['https://tacotunes.com/wp-content/uploads/2013/02/JL-Audio-C3-650-Component-Speakers-Manual.pdf'],
        'note': 'Authorized-dealer host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'www.bobscb.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': "Bob's Car Audio (authorized JL Audio dealer)",
        'evidence': [
            'https://www.bobscb.com/PDGManuals/C1-650_MAN.pdf is JL Audio\'s C1-650 owner\'s manual served verbatim by the dealer.',
        ],
        'sources': ['https://www.bobscb.com/PDGManuals/C1-650_MAN.pdf'],
        'note': 'Authorized-dealer host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'onlinecarstereo.blob.core.windows.net': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'OnlineCarStereo (authorized JL Audio dealer)',
        'evidence': [
            'https://onlinecarstereo.blob.core.windows.net/www/cms/2024/JL%20Audio/13612W3V32.pdf is JL Audio\'s 12W3v3 owner\'s manual served verbatim by the dealer.',
        ],
        'sources': ['https://onlinecarstereo.blob.core.windows.net/www/cms/2024/JL%20Audio/13612W3V32.pdf'],
        'note': 'Authorized-dealer host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'manualzz.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Manualzz (document aggregator)',
        'evidence': [
            'https://manualzz.com/doc/22701574/electro-voice-sentry500-data-sheet serves an Electro-Voice data sheet as extracted text; the URL is written without the www prefix in the queue.',
        ],
        'sources': ['https://manualzz.com/doc/22701574/electro-voice-sentry500-data-sheet'],
        'note': 'Aggregator host; support only.'
    },
    'manualmachine.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'ManualMachine (document aggregator)',
        'evidence': [
            'https://manualmachine.com/spendor/sp100/2351828-owners-manual/ serves the Spendor SP-100 owner\'s manual as page images plus extracted text.',
        ],
        'sources': ['https://manualmachine.com/spendor/sp100/2351828-owners-manual/'],
        'note': 'Aggregator host; support only.'
    },
    'manualsnet.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Manualsnet (document aggregator)',
        'evidence': [
            'https://manualsnet.com/kef/reference-series-model-ls3-5a serves the KEF LS3/5A installation manual text quoted in Round 26.',
        ],
        'sources': ['https://manualsnet.com/kef/reference-series-model-ls3-5a'],
        'note': 'Aggregator host; support only.'
    },
    'static1.squarespace.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Squarespace CDN (generic asset host; site owner not identified by the URL)',
        'evidence': [
            'https://static1.squarespace.com/static/5a6a2d73bff200e7e9dde1f9/t/5b5b68456d2a73ca7faa5fbd/1532717141711/LP-6+User%27s+Manual.pdf is the Kali Audio LP-6 manual, but the host is a generic CDN and the URL carries no brand domain.',
        ],
        'sources': ['https://static1.squarespace.com/static/5a6a2d73bff200e7e9dde1f9/t/5b5b68456d2a73ca7faa5fbd/1532717141711/LP-6+User%27s+Manual.pdf'],
        'note': 'Generic CDN; support only until brand-host ownership is established.'
    },
    'valueelectronics.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Value Electronics (authorized LG dealer)',
        'evidence': [
            'https://valueelectronics.com/wp-content/uploads/2024/04/LG-2024-S95TR_9.1.5_SoundBar_spec_sheet.pdf is LG\'s S95TR spec sheet served by the dealer.',
        ],
        'sources': ['https://valueelectronics.com/wp-content/uploads/2024/04/LG-2024-S95TR_9.1.5_SoundBar_spec_sheet.pdf'],
        'note': 'Dealer host; support only.'
    },
    'www.zzounds.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'zZounds (authorized Vox retailer)',
        'evidence': [
            'https://www.zzounds.com/item--VOXV212 is a retail product page carrying the V212BN spec block quoted in Round 26.',
        ],
        'sources': ['https://www.zzounds.com/item--VOXV212'],
        'note': 'Retailer host; support only.'
    },
    'www.svconline.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Sound & Video Contractor (trade press)',
        'evidence': [
            'https://www.svconline.com/products/meyer-sound-announces-mjf-212-high-power-stage-monitor-366663 reproduces a Meyer Sound product announcement.',
        ],
        'sources': ['https://www.svconline.com/products/meyer-sound-announces-mjf-212-high-power-stage-monitor-366663'],
        'note': 'Trade-press host; support only.'
    },
    'www.soundstagehifi.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'SoundStage! Hi-Fi (review publication)',
        'evidence': [
            'https://www.soundstagehifi.com/index.php/equipment-reviews/807-kef-reference-1-loudspeakers carries the review text quoted in Round 26.',
        ],
        'sources': ['https://www.soundstagehifi.com/index.php/equipment-reviews/807-kef-reference-1-loudspeakers'],
        'note': 'Review host; support only.'
    },
    'www.mono.no': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Mono AS (Norwegian Sonus faber dealer)',
        'evidence': [
            'https://www.mono.no/media/multicase/documents/sonus%20faber/produktark/sonus_faber_guarneri_evolution_produktblad.pdf is a Sonus faber Guarneri Evolution data sheet served by the dealer.',
        ],
        'sources': ['https://www.mono.no/media/multicase/documents/sonus%20faber/produktark/sonus_faber_guarneri_evolution_produktblad.pdf'],
        'note': 'Dealer host; support only.'
    },
}

STATUS_UPGRADES = {}


def update_allowlist():
    allow = json.load(open(ALLOW, encoding='utf-8'))
    allow['reviewDate'] = CHECKED_DATE
    by_host = {h['host']: h for h in allow['hosts']}
    added = upgraded = 0
    for host, upd in HOST_UPDATES.items():
        if host in by_host:
            continue
        entry = {'host': host}
        entry.update(upd)
        by_host[host] = entry
        added += 1
    for host, upd in STATUS_UPGRADES.items():
        entry = by_host.get(host)
        if entry is None:
            continue
        if entry.get('status') == upd['status']:
            continue
        entry['previousStatus'] = entry.get('status')
        entry.update(upd)
        upgraded += 1
    allow['hosts'] = [by_host[h] for h in by_host]
    dump(ALLOW, allow)
    established = sum(1 for h in allow['hosts'] if h['status'].startswith('ESTABLISHED'))
    print(f'Updated source-host-allowlist.json: {len(allow["hosts"])} hosts '
          f'({established} established, {added} added, {upgraded} upgraded)')


def _load_evidence():
    spec = importlib.util.spec_from_file_location(
        'round26_evidence_data', os.path.join(HERE, 'round26_evidence_data.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_round26_url_results():
    ev = _load_evidence()
    db = json.load(open(DATA, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    known_urls = {u['url'] for u in status['urls']}
    existing = json.load(open(R26_URLS, encoding='utf-8')) if os.path.exists(R26_URLS) else {'entries': []}
    existing_by_url = {e['url']: e for e in existing['entries']}
    entries = []
    for chk in ev.CHECKS:
        url = chk['url']
        assert url in known_urls, 'URL not in queue-url-status.json: ' + url
        if url in existing_by_url and existing_by_url[url].get('round') == 25:
            entries.append(existing_by_url[url])
            continue
        tied = []
        for r in db:
            for f in ('driverCount', 'active'):
                prov = r.get(f + 'Provenance') or {}
                if prov.get('status') == 'CITED_IN_NOTES_UNCHECKED' and prov.get('source') == url:
                    tied.append((r, f))
        if not tied:
            continue
        declared = {key: (outcome, note) for key, outcome, note in chk['results']}
        missing = sorted({r['id'] + '.' + f for r, f in tied} - set(declared))
        assert not missing, f'{url}: tied fields without an explicit outcome: {missing}'
        field_results = []
        for r, f in tied:
            key = r['id'] + '.' + f
            outcome, note = declared[key]
            if note is None:
                note = ev.NOT_STATED_NOTE
            field_results.append({'record': r['id'], 'field': f, 'value': r.get(f),
                                  'outcome': outcome, 'note': note})
        outcomes = {fr['outcome'] for fr in field_results}
        if outcomes & {'NOT_EXTRACTED', 'INACCESSIBLE'}:
            status_value = 'INACCESSIBLE'
        elif outcomes == {'PROMOTED'}:
            status_value = 'CHECKED_CONFIRMED'
        else:
            status_value = 'CHECKED_PARTIAL'
        entry = {
            'url': url,
            'host': url.split('/')[2],
            'sourceClass': chk['sourceClass'],
            'round': 25,
            'checkedDate': ev.CHECKED_DATE,
            'document': chk['document'],
            'chunksOpened': chk['chunksOpened'],
            'chunksTotal': chk['chunksTotal'],
            'status': status_value,
            'evidence': chk['evidence'],
            'fieldResults': field_results,
        }
        if chk.get('ownerDecision'):
            entry['ownerDecision'] = chk['ownerDecision']
        entries.append(entry)
    seen = {e['url'] for e in entries}
    entries.extend(e for e in existing['entries'] if e['url'] not in seen)
    out = {'round': 25, 'checkedDate': ev.CHECKED_DATE, 'entries': entries}
    dump(R26_URLS, out)
    promoted = sum(1 for e in entries for fr in e['fieldResults'] if fr['outcome'] == 'PROMOTED')
    print(f'round26-url-results.json: urls={len(entries)} field_results='
          f'{sum(len(e["fieldResults"]) for e in entries)} promotions_planned={promoted}')
    if not promoted:
        raise SystemExit('No promotions planned; check the evidence table.')


if __name__ == '__main__':
    update_allowlist()
    build_round26_url_results()
