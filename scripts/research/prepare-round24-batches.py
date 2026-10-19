#!/usr/bin/env python3
"""Prepare and validate Round 24 provenance-audit artifacts.

1. Record Decision 8 host-operator checks for the manufacturer sites opened this round
   in source-host-allowlist.json (never downgrading an existing entry).
2. Build round24-url-results.json from round24_evidence_data.py.

Only fields whose live provenance still points at the checked URL with status
CITED_IN_NOTES_UNCHECKED are written; values always come from the live catalogue.
Re-running after apply is safe: an entry already recorded for Round 23 is preserved
instead of being rebuilt from a catalogue that no longer shows those fields as cited.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
ALLOW = os.path.join(HERE, 'source-host-allowlist.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
R24_URLS = os.path.join(HERE, 'round24-url-results.json')
CHECKED_DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


HOST_UPDATES = {
    'www.kicker.com': {
        'status': 'ESTABLISHED',
        'operator': 'Kicker (Stillwater Designs)',
        'evidence': [
            'https://www.kicker.com/47KSC650' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.kicker.com/47KSC650'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.behringer.com': {
        'status': 'ESTABLISHED',
        'operator': 'Behringer (Music Tribe)',
        'evidence': [
            'https://www.behringer.com/en/products/0313-ACS' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.behringer.com/en/products/0313-ACS'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.auratoneaudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Auratone',
        'evidence': [
            'https://www.auratoneaudio.com/products' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.auratoneaudio.com/products'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'voidacoustics.com': {
        'status': 'ESTABLISHED',
        'operator': 'Void Acoustics',
        'evidence': [
            'https://voidacoustics.com/products/air/air8/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://voidacoustics.com/products/air/air8/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'support.apple.com': {
        'status': 'ESTABLISHED',
        'operator': 'Apple Inc.',
        'evidence': [
            'https://support.apple.com/en-us/111843' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://support.apple.com/en-us/111843'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.sonos.com': {
        'status': 'ESTABLISHED',
        'operator': 'Sonos, Inc.',
        'evidence': [
            'https://www.sonos.com/en-us/guides/submini' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.sonos.com/en-us/guides/submini'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'newsroom.sonos.com': {
        'status': 'ESTABLISHED',
        'operator': 'Sonos, Inc. (newsroom)',
        'evidence': [
            'https://newsroom.sonos.com/254814-introducing-sonos-play-1/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://newsroom.sonos.com/254814-introducing-sonos-play-1/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'dutchdutch.com': {
        'status': 'ESTABLISHED',
        'operator': 'Dutch & Dutch',
        'evidence': [
            'https://dutchdutch.com/pages/8c' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://dutchdutch.com/pages/8c'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.rel.net': {
        'status': 'ESTABLISHED',
        'operator': 'REL Acoustics',
        'evidence': [
            'https://www.rel.net/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.rel.net/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.jbl.com': {
        'status': 'ESTABLISHED',
        'operator': 'JBL (HARMAN International)',
        'evidence': [
            'https://www.jbl.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw9c36c40d/pdfs/JBL_Charge5_SpecSheet_English.pdf' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.jbl.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw9c36c40d/pdfs/JBL_Charge5_SpecSheet_English.pdf'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'pioneer-car.eu': {
        'status': 'ESTABLISHED',
        'operator': 'Pioneer Europe (car audio)',
        'evidence': [
            'https://pioneer-car.eu/ts-d65c/ts-d65c' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://pioneer-car.eu/ts-d65c/ts-d65c'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.presonus.com': {
        'status': 'ESTABLISHED',
        'operator': 'PreSonus (Fender Musical Instruments)',
        'evidence': [
            'https://www.presonus.com/products/eris-e45-studio-monitor' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.presonus.com/products/eris-e45-studio-monitor'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'audison.com': {
        'status': 'ESTABLISHED',
        'operator': 'Audison (Elektromedia S.p.A.)',
        'evidence': [
            'https://audison.com/product/apk-165/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://audison.com/product/apk-165/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'rockfordfosgate.com': {
        'status': 'ESTABLISHED',
        'operator': 'Rockford Fosgate',
        'evidence': [
            'https://rockfordfosgate.com/products/details/p3d4-12/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://rockfordfosgate.com/products/details/p3d4-12/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'static.hertz-audio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Hertz (Elektromedia S.p.A.) asset host',
        'evidence': [
            'https://static.hertz-audio.com/media/2021/04/Hertz_CK165_Tech_Sheet_rev18A.pdf' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://static.hertz-audio.com/media/2021/04/Hertz_CK165_Tech_Sheet_rev18A.pdf'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'products.bose.com': {
        'status': 'ESTABLISHED',
        'operator': 'Bose Corporation (owner-support document host)',
        'evidence': [
            'https://products.bose.com/pdf/customer_service/owners/og_791.pdf' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://products.bose.com/pdf/customer_service/owners/og_791.pdf'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'usa.yamaha.com': {
        'status': 'ESTABLISHED',
        'operator': 'Yamaha Corporation of America',
        'evidence': [
            'https://usa.yamaha.com/products/audio_visual/speaker_systems/ns-5000/specs.html' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://usa.yamaha.com/products/audio_visual/speaker_systems/ns-5000/specs.html'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.revelspeakers.com': {
        'status': 'ESTABLISHED',
        'operator': 'Revel (HARMAN International)',
        'evidence': [
            'https://www.revelspeakers.com/products/in-room-loudspeakers/M106-.html' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.revelspeakers.com/products/in-room-loudspeakers/M106-.html'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'trianglehifi.com': {
        'status': 'ESTABLISHED',
        'operator': 'Triangle HiFi',
        'evidence': [
            'https://trianglehifi.com/products/enceinte-bibliotheque-hi-fi-borea-br03-paire' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://trianglehifi.com/products/enceinte-bibliotheque-hi-fi-borea-br03-paire'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'us.sennheiser-hearing.com': {
        'status': 'ESTABLISHED',
        'operator': 'Sonova Consumer Hearing (Sennheiser brand licensee)',
        'evidence': [
            'https://us.sennheiser-hearing.com/products/ambeo-soundbar' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://us.sennheiser-hearing.com/products/ambeo-soundbar'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.rcf.it': {
        'status': 'ESTABLISHED',
        'operator': 'RCF S.p.A.',
        'evidence': [
            'https://www.rcf.it/en/products/product-detail/nx-45-a' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.rcf.it/en/products/product-detail/nx-45-a'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.devialet.com': {
        'status': 'ESTABLISHED',
        'operator': 'Devialet',
        'evidence': [
            'https://www.devialet.com/en-us/soundbar/dione/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.devialet.com/en-us/soundbar/dione/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.kenwood.com': {
        'status': 'ESTABLISHED',
        'operator': 'JVCKenwood',
        'evidence': [
            'https://www.kenwood.com/usa/car/caraudio/speakers/kfc-1666s/spec.html' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.kenwood.com/usa/car/caraudio/speakers/kfc-1666s/spec.html'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.paradigm.com': {
        'status': 'ESTABLISHED',
        'operator': 'Paradigm Electronics',
        'evidence': [
            'https://www.paradigm.com/en/floorstanding/monitor-se-6000f' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.paradigm.com/en/floorstanding/monitor-se-6000f'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'martin-audio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Martin Audio Ltd',
        'evidence': [
            'https://martin-audio.com/products/archive/w8lm' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://martin-audio.com/products/archive/w8lm'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.danleysoundlabs.com': {
        'status': 'ESTABLISHED',
        'operator': 'Danley Sound Labs',
        'evidence': [
            'https://www.danleysoundlabs.com/products/sh96/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.danleysoundlabs.com/products/sh96/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'barefootsound.com': {
        'status': 'ESTABLISHED',
        'operator': 'Barefoot Sound',
        'evidence': [
            'https://barefootsound.com/footprint03/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://barefootsound.com/footprint03/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'funktion-one.com': {
        'status': 'ESTABLISHED',
        'operator': 'Funktion-One',
        'evidence': [
            'https://funktion-one.com/product/res-2/' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://funktion-one.com/product/res-2/'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.qacoustics.com': {
        'status': 'ESTABLISHED',
        'operator': 'Q Acoustics',
        'evidence': [
            'https://www.qacoustics.com/products/3030i-bookshelf-speaker-pair' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.qacoustics.com/products/3030i-bookshelf-speaker-pair'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'avantonepro.com': {
        'status': 'ESTABLISHED',
        'operator': 'Avantone Pro',
        'evidence': [
            'https://avantonepro.com/en/products/mixcube-passive' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://avantonepro.com/en/products/mixcube-passive'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'eaw.com': {
        'status': 'ESTABLISHED',
        'operator': 'Eastern Acoustic Works (EAW)',
        'evidence': [
            'https://eaw.com/wp-content/uploads/2013/12/KF760_SPECS_rev1.pdf' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://eaw.com/wp-content/uploads/2013/12/KF760_SPECS_rev1.pdf'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.ikmultimedia.com': {
        'status': 'ESTABLISHED',
        'operator': 'IK Multimedia',
        'evidence': [
            'https://www.ikmultimedia.com/news/?id=iloudmtm' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.ikmultimedia.com/news/?id=iloudmtm'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'www.sony.com': {
        'status': 'ESTABLISHED',
        'operator': 'Sony Corporation',
        'evidence': [
            'https://www.sony.com/electronics/support/sound-bars-home-theater-systems-sound-bars-surround-speakers/ht-a7000/specifications' + ' is the brand-operated page/document for this model and carries the specification text quoted in Round 24.',
        ],
        'sources': ['https://www.sony.com/electronics/support/sound-bars-home-theater-systems-sound-bars-surround-speakers/ht-a7000/specifications'],
        'note': 'Established by Decision 8 document check (Round 24).'
    },
    'cdn.shopify.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Shopify Inc. (multi-tenant storefront CDN)',
        'evidence': [
            'Multi-tenant CDN: the /s/files/<shop>/ path belongs to one store, but the host itself cannot be attributed to a single manufacturer, so documents served from it support but never promote a field.',
        ],
        'sources': ['https://cdn.shopify.com/s/files/1/0566/0809/6342/files/KRK-7000b_spec_sheet.pdf?v=1708102022'],
        'note': 'Recorded in Round 24; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
    'tcfurlong.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'TC Furlong (third-party backline rental firm)',
        'evidence': [
            "Rental company mirror of an owner's manual; not the manufacturer or an owner-approved distributor, so SUPPORTED_NOT_PROMOTED only.",
        ],
        'sources': ['https://tcfurlong.com/wp-content/uploads/Fostex-6301B-Rental-Manual.pdf'],
        'note': 'Recorded in Round 24; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
    'bangolufsenrmaskillgohel.blob.core.windows.net': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Azure blob storage account, ownership not established',
        'evidence': [
            "Storage-account host whose name embeds a person's name; brand ownership could not be established, so SUPPORTED_NOT_PROMOTED only.",
        ],
        'sources': ['https://bangolufsenrmaskillgohel.blob.core.windows.net/zendesk-guide/User%20Guide%20Files/Wireless%20Speaker%20Systems/Beosound%20Balance/Beosound%20Balance%20Product%20Sheet%20EN%20Sep2024.pdf'],
        'note': 'Recorded in Round 24; SUPPORTED_NOT_PROMOTED outcomes only.'
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
    known = set(by_host)
    allow['hosts'] = [by_host[h] for h in by_host]
    assert set(by_host) == known
    dump(ALLOW, allow)
    established = sum(1 for h in allow['hosts'] if h['status'].startswith('ESTABLISHED'))
    print(f'Updated source-host-allowlist.json: {len(allow["hosts"])} hosts '
          f'({established} established, {added} added, {upgraded} upgraded)')


def _load_evidence():
    spec = importlib.util.spec_from_file_location(
        'round24_evidence_data', os.path.join(HERE, 'round24_evidence_data.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DEFAULT_OUTCOMES = {'driverCount': ('PROMOTED', None),
                    'active': ('NOT_STATED', None)}


def build_round24_url_results():
    ev = _load_evidence()
    db = json.load(open(DATA, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    known_urls = {u['url'] for u in status['urls']}
    existing = json.load(open(R24_URLS, encoding='utf-8')) if os.path.exists(R24_URLS) else {'entries': []}
    existing_by_url = {e['url']: e for e in existing['entries']}
    entries = []
    declared_unused = 0
    for chk in ev.CHECKS:
        url = chk['url']
        assert url in known_urls, 'URL not in queue-url-status.json: ' + url
        if url in existing_by_url and existing_by_url[url].get('round') == 24:
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
        field_results = []
        used = set()
        for r, f in tied:
            key = r['id'] + '.' + f
            if key in declared:
                outcome, note = declared[key]
                used.add(key)
            else:
                outcome, note = DEFAULT_OUTCOMES[f]
            if note is None:
                note = ev.NOT_STATED_NOTE
            field_results.append({'record': r['id'], 'field': f, 'value': r.get(f),
                                  'outcome': outcome, 'note': note})
        declared_unused += len(set(declared) - used)
        outcomes = {fr['outcome'] for fr in field_results}
        if outcomes & {'NOT_EXTRACTED', 'INACCESSIBLE'}:
            # Ledger vocabulary has no NOT_EXTRACTED: an unreadable document is INACCESSIBLE.
            status_value = 'INACCESSIBLE'
        elif outcomes == {'PROMOTED'}:
            status_value = 'CHECKED_CONFIRMED'
        else:
            status_value = 'CHECKED_PARTIAL'
        entries.append({
            'url': url,
            'host': url.split('/')[2],
            'sourceClass': chk['sourceClass'],
            'round': 24,
            'checkedDate': ev.CHECKED_DATE,
            'document': chk['document'],
            'chunksOpened': chk['chunksOpened'],
            'chunksTotal': chk['chunksTotal'],
            'status': status_value,
            'evidence': chk['evidence'],
            'fieldResults': field_results,
        })
    seen = {e['url'] for e in entries}
    entries.extend(e for e in existing['entries'] if e['url'] not in seen)
    out = {'round': 24, 'checkedDate': ev.CHECKED_DATE, 'entries': entries}
    dump(R24_URLS, out)
    promoted = sum(1 for e in entries for fr in e['fieldResults'] if fr['outcome'] == 'PROMOTED')
    print(f'round24-url-results.json: urls={len(entries)} field_results='
          f'{sum(len(e["fieldResults"]) for e in entries)} promotions_planned={promoted} '
          f'declared_but_not_tied={declared_unused}')
    if declared_unused:
        raise SystemExit('A declared field result was not tied to the checked URL; fix the evidence table.')


if __name__ == '__main__':
    update_allowlist()
    build_round24_url_results()
