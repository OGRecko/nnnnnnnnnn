#!/usr/bin/env python3
"""Round 29 batch 53 companion: record the URL-level assessment behind the structural writes.

`apply-structural-batch.py` only writes speakers.json and its history. This records the same four
decisions against the source URLs in `queue-url-status.json` (creating the Yamaha entry) so the
provenance queue and the ledger see them.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = os.path.join(HERE, 'queue-url-status.json')
LEDGER = os.path.join(HERE, 'provenance-source-ledger.json')

DATE = '2026-10-19'
ROUND = 29

YAM = 'https://www.yamaha.com/yamahavgn/Documents/ProAudio/ns10ms.pdf'
KRP = 'https://assets.klipsch.com/product-manuals/Reference-Premiere-Speakers-Manual-v03.pdf'
KREF = 'https://assets.klipsch.com/product-manuals/Reference-Speakers-2018-Manual-v02.pdf'

CONNECT = ('"Using 16-12 gauge speaker wire, connect the RED \\"positive\\" (+) terminal of the LEFT speaker '
           'to the RED \\"positive\\" (+) terminal of your amplifier\'s LEFT channel."')

ENTRIES = {
    YAM: {
        'status': 'CHECKED_CONFIRMED', 'chunksOpened': [0], 'chunksTotal': 1,
        'document': "Yamaha NS-10M STUDIO Monitor Speaker System owner's manual",
        'evidence': ('"Congratulations on your purchase of a Yamaha NS-10M STUDIO Monitor Speaker System!"; '
                     'SPECIFICATIONS "Components | LF: JA1801 (18 cm cone)  HF: JA0518A (3.5 cm soft dome)"; '
                     'CONNECTION "BEFORE MAKING SPEAKER CONNECTIONS, MAKE SURE YOUR POWER AMPLIFIER IS '
                     'TURNED OFF!"'),
        'fieldResults': [
            {'record': 'yamaha-ns10m', 'field': 'driverCount', 'value': 2, 'outcome': 'PROMOTED',
             'note': 'Round 29: components table lists LF JA1801 (18 cm cone) and HF JA0518A (3.5 cm soft dome).'},
            {'record': 'yamaha-ns10m', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
             'note': 'Round 29: connection chapter wires the speaker to an external power amplifier and '
                     'describes no mains inlet.'},
        ],
    },
    KRP: {
        'fieldResults': [
            {'record': 'klipsch-rp8000f', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
             'note': 'Round 29: RP-8000F is on the cover model list and the connection chapter wires it to '
                     'an external amplifier; no mains inlet described.'},
        ],
    },
    KREF: {
        'fieldResults': [
            {'record': 'klipsch-r51m', 'field': 'active', 'value': False, 'outcome': 'PROMOTED',
             'note': 'Round 29: R-51M is on the cover model list and the connection chapter wires it to an '
                     'external amplifier; no mains inlet described.'},
        ],
    },
}

HOSTS = {YAM: 'www.yamaha.com'}


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def main():
    status = json.load(open(STATUS, encoding='utf-8'))
    by_url = {u['url']: u for u in status['urls']}
    added = merged = 0
    for url, spec in ENTRIES.items():
        old = by_url.get(url)
        if old is None:
            by_url[url] = {
                'url': url, 'round': ROUND, 'status': spec['status'],
                'chunksOpened': spec['chunksOpened'], 'chunksTotal': spec['chunksTotal'],
                'checkedDate': DATE, 'sourceClass': 'MANUFACTURER',
                'document': spec['document'], 'evidence': spec['evidence'],
                'fieldResults': list(spec['fieldResults']), 'history': [],
            }
            status['urls'].append(by_url[url])
            added += 1
            continue
        cur = {f"{f['record']}.{f['field']}": f for f in old.get('fieldResults', [])}
        for f in spec['fieldResults']:
            cur[f"{f['record']}.{f['field']}"] = f
        old['fieldResults'] = list(cur.values())
        by_url[url] = old
        merged += 1
    status['urls'] = [by_url[u['url']] for u in status['urls']]
    dump(STATUS, status)

    ledger = json.load(open(LEDGER, encoding='utf-8'))
    have = {s.get('url') for s in ledger['sources']}
    if YAM not in have:
        spec = ENTRIES[YAM]
        ledger['sources'].append({
            'url': YAM, 'host': HOSTS[YAM], 'document': spec['document'],
            'status': spec['status'], 'openedDate': DATE,
            'chunksOpened': spec['chunksOpened'], 'chunksTotal': spec['chunksTotal'],
            'sourceClass': 'MANUFACTURER', 'coverage': spec['evidence'],
            'decisions': [{'id': f['record'], 'field': f['field'], 'value': f['value'],
                           'result': 'CONFIRMED', 'decision': 'MANUFACTURER_VERIFIED',
                           'evidence': f['note']} for f in spec['fieldResults']],
            'queueItemsResolved': len(spec['fieldResults']),
        })
    dump(LEDGER, ledger)
    print(f'batch53 companion: urls_added={added} urls_merged={merged} entries={len(status["urls"])}')


if __name__ == '__main__':
    main()
