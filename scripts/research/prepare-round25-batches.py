#!/usr/bin/env python3
"""Prepare and validate Round 25 provenance-audit artifacts.

1. Record Decision 8 host-operator checks for the hosts opened this round in
   source-host-allowlist.json (never downgrading an existing entry).
2. Build round25-url-results.json from round25_evidence_data.py.

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
R25_URLS = os.path.join(HERE, 'round25-url-results.json')
CHECKED_DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


HOST_UPDATES = {
    'data.yamaha.com': {
        'status': 'ESTABLISHED',
        'operator': 'Yamaha Corporation (document/asset host)',
        'evidence': [
            'https://data.yamaha.com/files/download/other_assets/3/325553/dxr-dxs_en_om_c0.pdf is the Yamaha DXR/DXS Owner\'s Manual served from Yamaha\'s own data.yamaha.com asset host and carries the specification table quoted in Round 25.',
        ],
        'sources': ['https://data.yamaha.com/files/download/other_assets/3/325553/dxr-dxs_en_om_c0.pdf'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.dbaudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'd&b audiotechnik GmbH',
        'evidence': [
            'https://www.dbaudio.com/assets/products/downloads/manuals-documentation/t-series/dbaudio-datasheet-t10-1.1-en.pdf is the d&b T10 data sheet on the brand-operated dbaudio.com site and carries the text quoted in Round 25.',
        ],
        'sources': ['https://www.dbaudio.com/assets/products/downloads/manuals-documentation/t-series/dbaudio-datasheet-t10-1.1-en.pdf'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.dasaudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'DAS Audio',
        'evidence': [
            'https://www.dasaudio.com/wp-content/uploads/2011/11/TECNOLOGIAS_AERO_12A_V1.pdf is the DAS Audio Aero 12A technical report on the brand site and carries the text quoted in Round 25.',
        ],
        'sources': ['https://www.dasaudio.com/wp-content/uploads/2011/11/TECNOLOGIAS_AERO_12A_V1.pdf'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'legacy.adamson.ai': {
        'status': 'ESTABLISHED',
        'operator': 'Adamson Systems Engineering (legacy support archive)',
        'evidence': [
            'https://legacy.adamson.ai/support/downloads-directory/e-series/e15/1-e15-technicaldata/file is the Adamson E-series E15 technical data sheet on Adamson\'s legacy support host.',
        ],
        'sources': ['https://legacy.adamson.ai/support/downloads-directory/e-series/e15/1-e15-technicaldata/file'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'magnepan.com': {
        'status': 'ESTABLISHED',
        'operator': 'Magnepan, Inc.',
        'evidence': [
            'https://magnepan.com/pages/manual-controller serves the Magnepan 1.7 owner\'s manual on the brand site and carries the model description quoted in Round 25.',
        ],
        'sources': ['https://magnepan.com/pages/manual-controller'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.fender.com': {
        'status': 'ESTABLISHED',
        'operator': 'Fender Musical Instruments Corporation',
        'evidence': [
            'https://www.fender.com/products/blues-junior-iv is the Fender product page for the Blues Junior IV and carries the specification block quoted in Round 25.',
        ],
        'sources': ['https://www.fender.com/products/blues-junior-iv'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.lg.com': {
        'status': 'ESTABLISHED',
        'operator': 'LG Electronics',
        'evidence': [
            'https://www.lg.com/ca_en/speakers/soundbars/s90tr/ is LG\'s own product page and its "All Spec" panel carries the speaker-count row quoted in Round 25.',
        ],
        'sources': ['https://www.lg.com/ca_en/speakers/soundbars/s90tr/'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.alpine-usa.com': {
        'status': 'ESTABLISHED',
        'operator': 'Alpine Electronics of America, Inc.',
        'evidence': [
            'https://www.alpine-usa.com/company/press/2017/alpine-electronics-now-shipping-x-series-speakers is an Alpine Electronics of America press release on the brand site listing the X-Series speaker models.',
        ],
        'sources': ['https://www.alpine-usa.com/company/press/2017/alpine-electronics-now-shipping-x-series-speakers'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.morelhifi.com': {
        'status': 'ESTABLISHED',
        'operator': 'Morel HiFi',
        'evidence': [
            'https://www.morelhifi.com/en/products/car-audio/reference-9/elate-carbon-16/elate-carbon-62-6-2-way-158 is the Morel Elate Carbon product page and carries the model/configuration table quoted in Round 25.',
        ],
        'sources': ['https://www.morelhifi.com/en/products/car-audio/reference-9/elate-carbon-16/elate-carbon-62-6-2-way-158'],
        'note': 'Established by Decision 8 document check (Round 25).'
    },
    'www.rockfordfosgate.com': {
        'status': 'ESTABLISHED',
        'operator': 'Rockford Fosgate',
        'evidence': [
            'https://www.rockfordfosgate.com/products/details/t1650-s/ is the brand-operated Rockford Fosgate product page (www host of the established rockfordfosgate.com domain).',
        ],
        'sources': ['https://www.rockfordfosgate.com/products/details/t1650-s/'],
        'note': 'www variant of the established rockfordfosgate.com host; recorded in Round 25.'
    },
    'www.manualslib.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'ManualsLib (document aggregator)',
        'evidence': [
            'Aggregator that hosts verbatim manufacturer owner\'s manuals. Round 25 promotions from this host rest on Owner Decision 1 (2026-10-12): a distributor/aggregator copy of an exact-model manufacturer manual counts as manufacturer-verified.',
        ],
        'sources': ['https://www.manualslib.com/manual/1412330/Kef-Blade.html?page=10'],
        'note': 'Aggregator host; only DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL entries carrying the owner-decision ID may promote.'
    },
    'www.soundonsound.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Sound On Sound Ltd (magazine)',
        'evidence': [
            'Review magazine; supports but never promotes a field (Round 25).',
        ],
        'sources': ['https://www.soundonsound.com/reviews/mackie-hr824'],
        'note': 'Recorded in Round 25; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
    'www.soundandvision.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Sound & Vision (magazine)',
        'evidence': [
            'Review magazine; supports but never promotes a field (Round 25).',
        ],
        'sources': ['https://www.soundandvision.com/content/pioneer-ex-series-surround-speaker-system-specifications'],
        'note': 'Recorded in Round 25; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
    'www.hifi-guide.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'hifi-guide.com (enthusiast loudspeaker database)',
        'evidence': [
            'Community database of loudspeaker specifications; supports but never promotes a field (Round 25).',
        ],
        'sources': ['https://www.hifi-guide.com/loudspeaker/bowers-wilkins-801-matrix/'],
        'note': 'Recorded in Round 25; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
    'www.radiomuseum.org': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Radiomuseum.org (collector catalogue)',
        'evidence': [
            'Collector-maintained equipment catalogue; supports but never promotes a field (Round 25).',
        ],
        'sources': ['https://www.radiomuseum.org/r/klh_compact_bookshelf_speaker_system_model_six_6.html?language_id=2'],
        'note': 'Recorded in Round 25; SUPPORTED_NOT_PROMOTED outcomes only.'
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
        'round25_evidence_data', os.path.join(HERE, 'round25_evidence_data.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_round25_url_results():
    ev = _load_evidence()
    db = json.load(open(DATA, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    known_urls = {u['url'] for u in status['urls']}
    existing = json.load(open(R25_URLS, encoding='utf-8')) if os.path.exists(R25_URLS) else {'entries': []}
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
    dump(R25_URLS, out)
    promoted = sum(1 for e in entries for fr in e['fieldResults'] if fr['outcome'] == 'PROMOTED')
    print(f'round25-url-results.json: urls={len(entries)} field_results='
          f'{sum(len(e["fieldResults"]) for e in entries)} promotions_planned={promoted}')
    if not promoted:
        raise SystemExit('No promotions planned; check the evidence table.')


if __name__ == '__main__':
    update_allowlist()
    build_round25_url_results()
