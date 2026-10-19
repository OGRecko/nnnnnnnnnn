#!/usr/bin/env python3
"""Prepare and validate Round 23 provenance-audit artifacts.

1. Record Decision 8 host-operator checks for the manufacturer sites opened this round
   in source-host-allowlist.json (never downgrading an existing entry).
2. Build round23-url-results.json from round23_evidence_data.py.

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
R23_URLS = os.path.join(HERE, 'round23-url-results.json')
CHECKED_DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


HOST_UPDATES = {
    'www.marshall.com': {
        'status': 'ESTABLISHED',
        'operator': 'Marshall (official Marshall brand site, web store and support site)',
        'evidence': [
            'https://www.marshall.com/us/en/product/1960a-4x12-angled-cabinet?pid=1007269 is the official Marshall product page for the 1960A and carries the model specification table; cabinet manuals are served from assets.ctfassets.net (Marshall "Cabs Safety Leaflet").',
            'https://www.marshall.com/us/en/support/amps/support-for-1960av-4x12-angled-cabinet is Marshall\'s own support article tree for the 1960AV and repeats the model product details.'
        ],
        'sources': [
            'https://www.marshall.com/us/en/product/1960a-4x12-angled-cabinet?pid=1007269',
            'https://www.marshall.com/us/en/support/amps/support-for-1960av-4x12-angled-cabinet'
        ],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.svsound.com': {
        'status': 'ESTABLISHED',
        'operator': 'SVS (SVSound, official brand site and direct web store)',
        'evidence': [
            'https://www.svsound.com/products/pb-2000-pro is SVS\'s own product page and store listing for the PB-2000 Pro, with SVS product imagery and the SVS Subwoofer Control App described in the product copy.'
        ],
        'sources': ['https://www.svsound.com/products/pb-2000-pro'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.polkaudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Polk Audio (HARMAN International)',
        'evidence': [
            'https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/reserve-r200/300029.html is the official Polk product page; its checkout block links "Terms of Sale & Privacy Policy" to https://www.harman.com/privacy-policy-statement/, identifying the HARMAN-operated storefront.'
        ],
        'sources': ['https://www.polkaudio.com/en-us/product/home-speakers/bookshelf/reserve-r200/300029.html'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.revelspeakers.com': {
        'status': 'ESTABLISHED',
        'operator': 'Revel Speakers (HARMAN International)',
        'evidence': [
            'https://www.revelspeakers.com/products/in-room-loudspeakers/F206-.html serves the Performa3 F206 from /on/demandware.static/-/Sites-masterCatalog_Harman/... (HARMAN catalogue path) and carries the Revel dealer locator and Revel owner\'s manual PDFs.'
        ],
        'sources': ['https://www.revelspeakers.com/products/in-room-loudspeakers/F206-.html'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.krkmusic.com': {
        'status': 'ESTABLISHED',
        'operator': 'KRK Systems (official KRK web store)',
        'evidence': [
            'https://www.krkmusic.com/products/rokit-8-generation-4-powered-studio-monitor-black is KRK\'s own store listing; the page cart link points at shop.krksys.com and the product downloads are KRK manuals/brochures hosted on the KRK Shopify CDN.'
        ],
        'sources': ['https://www.krkmusic.com/products/rokit-8-generation-4-powered-studio-monitor-black'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.qacoustics.com': {
        'status': 'ESTABLISHED',
        'operator': 'Q Acoustics (official brand store)',
        'evidence': [
            'https://www.qacoustics.com/products/3020i-bookshelf-speaker-pair is the Q Acoustics brand store listing ("QAcoustics" vendor page) carrying the model copy and Q Acoustics support/warranty links.'
        ],
        'sources': ['https://www.qacoustics.com/products/3020i-bookshelf-speaker-pair'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.monitoraudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Monitor Audio Ltd (official product site)',
        'evidence': [
            'https://www.monitoraudio.com/en/us/product-ranges/creator-series/c3m/ is Monitor Audio\'s own product site ("British Design | Performance Loudspeakers | Experts Since 1972") with the model specification and downloads sections.'
        ],
        'sources': ['https://www.monitoraudio.com/en/us/product-ranges/creator-series/c3m/'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'orangeamps.com': {
        'status': 'ESTABLISHED',
        'operator': 'Orange Music Electronic Co Ltd',
        'evidence': [
            'https://orangeamps.com/en-us/products/ppc412 page title reads "Orange PPC412 speaker cabinet ... – Orange Music Electronic Co Ltd"; the store cart is hosted at storeusa.orangeamps.com.'
        ],
        'sources': ['https://orangeamps.com/en-us/products/ppc412'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'legacy.mesaboogie.com': {
        'status': 'ESTABLISHED',
        'operator': 'MESA/Boogie (MESA Engineering, Petaluma CA)',
        'evidence': [
            'https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/fillmore-series/2x12-fillmore.html is MESA/Boogie\'s official legacy catalogue page; the copy states "ALL MESA® ENCLOSURES ... Made in Petaluma, California" and product imagery is served from mesa-boogie.imgix.net.'
        ],
        'sources': ['https://legacy.mesaboogie.com/cabinets--simulators/guitar-cabinets--simulators/fillmore-series/2x12-fillmore.html'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'voxamps.com': {
        'status': 'ESTABLISHED',
        'operator': 'VOX (Korg) — official VOX Amps site',
        'evidence': [
            'https://voxamps.com/product/v212c-extension-cabinet/ is VOX\'s official product page, linking the VOX web shop (voxampshop.com), the VOX dealer locator and VOX owner\'s manual PDFs.'
        ],
        'sources': ['https://voxamps.com/product/v212c-extension-cabinet/'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.sonusfaber.com': {
        'status': 'ESTABLISHED',
        'operator': 'Sonus faber S.r.l., Arcugnano (Vicenza), Italy',
        'evidence': [
            'https://www.sonusfaber.com/en/products/lumina-ii/tech-specs footer reads "Sonus faber S.r.l. Via Antonio Meucci, 10 36057 – Arcugnano (Vicenza) Italy" and hosts the Lumina technical specifications and owner\'s manual links.'
        ],
        'sources': ['https://www.sonusfaber.com/en/products/lumina-ii/tech-specs'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.wilsonaudio.com': {
        'status': 'ESTABLISHED',
        'operator': 'Wilson Audio Specialties (official product site)',
        'evidence': [
            'https://www.wilsonaudio.com/products/watt-puppy/watt-puppy-series-8 is Wilson Audio\'s product page for the WATT/Puppy Series 8 and links the Series 8 manual PDF hosted on wilsonaudio.com.'
        ],
        'sources': ['https://www.wilsonaudio.com/products/watt-puppy/watt-puppy-series-8'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.psbspeakers.com': {
        'status': 'ESTABLISHED',
        'operator': 'PSB Speakers (official brand site and store)',
        'evidence': [
            'https://www.psbspeakers.com/products/synchrony-t600-tower is PSB\'s own store listing for the Synchrony T600, with PSB data sheet / owner\'s manual downloads and support links to support.psbspeakers.com.'
        ],
        'sources': ['https://www.psbspeakers.com/products/synchrony-t600-tower'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'global.jbl.com': {
        'status': 'ESTABLISHED',
        'operator': 'JBL (HARMAN International)',
        'evidence': [
            'https://global.jbl.com/JBLL100CLASSICUAM.html serves JBL L100 Classic (item JBLL100CLASSICUAM) from /on/demandware.static/-/Sites-masterCatalog_Harman/..., HARMAN\'s catalogue, alongside the JBL Specialty Audio dealer locator.'
        ],
        'sources': ['https://global.jbl.com/JBLL100CLASSICUAM.html'],
        'note': 'Established by Decision 8 document check (Round 23).'
    },
    'www.stereophile.com': {
        'status': 'NOT_MANUFACTURER',
        'operator': 'Stereophile (hi-fi review publication)',
        'evidence': [
            'https://www.stereophile.com/content/kef-ls50-anniversary-model-loudspeaker-specifications is a review-magazine "Specifications" sidebar that reports manufacturer data; it is a third-party publication, not a manufacturer document, so it can support but never promote a field.'
        ],
        'sources': ['https://www.stereophile.com/content/kef-ls50-anniversary-model-loudspeaker-specifications'],
        'note': 'Recorded as a third-party publication in Round 23; SUPPORTED_NOT_PROMOTED outcomes only.'
    },
}

STATUS_UPGRADES = {
    'www.jbl.com': {
        'status': 'ESTABLISHED',
        'operator': 'JBL (HARMAN International)',
        'evidence': [
            'https://www.jbl.com/HDI-3800.html serves JBL HDI-3800 (item JBLHDI3800GRO) from /on/demandware.static/-/Sites-masterCatalog_Harman/..., HARMAN\'s catalogue, and carries the JBL Specialty Audio dealer locator.'
        ],
        'sources': ['https://www.jbl.com/HDI-3800.html'],
        'note': 'Upgraded from BRAND_DOMAIN_UNVERIFIED after the Round 23 document check identified the HARMAN-operated catalogue path.'
    }
}


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
        'round23_evidence_data', os.path.join(HERE, 'round23_evidence_data.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DEFAULT_OUTCOMES = {'driverCount': ('PROMOTED', None),
                    'active': ('NOT_STATED', None)}


def build_round23_url_results():
    ev = _load_evidence()
    db = json.load(open(DATA, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    known_urls = {u['url'] for u in status['urls']}
    existing = json.load(open(R23_URLS, encoding='utf-8')) if os.path.exists(R23_URLS) else {'entries': []}
    existing_by_url = {e['url']: e for e in existing['entries']}
    entries = []
    declared_unused = 0
    for chk in ev.CHECKS:
        url = chk['url']
        assert url in known_urls, 'URL not in queue-url-status.json: ' + url
        if url in existing_by_url and existing_by_url[url].get('round') == 23:
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
            'round': 23,
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
    out = {'round': 23, 'checkedDate': ev.CHECKED_DATE, 'entries': entries}
    dump(R23_URLS, out)
    promoted = sum(1 for e in entries for fr in e['fieldResults'] if fr['outcome'] == 'PROMOTED')
    print(f'round23-url-results.json: urls={len(entries)} field_results='
          f'{sum(len(e["fieldResults"]) for e in entries)} promotions_planned={promoted} '
          f'declared_but_not_tied={declared_unused}')
    if declared_unused:
        raise SystemExit('A declared field result was not tied to the checked URL; fix the evidence table.')


if __name__ == '__main__':
    update_allowlist()
    build_round23_url_results()
