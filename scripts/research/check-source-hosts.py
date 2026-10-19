#!/usr/bin/env python3
"""Report verified provenance sources whose host is not registered in the source-host allowlist.

The allowlist (source-host-allowlist.json) records, per host, whether the host is the
manufacturer (ESTABLISHED), serves manufacturer documents without being the manufacturer
(ESTABLISHED_FOR_LINKED_DOCUMENTS), or is explicitly not the manufacturer (NOT_MANUFACTURER).
A field whose status is a verified one should trace back to a host that has been classified;
otherwise the provenance label rests on a host nobody has adjudicated.

This is a reporting tool, not a gate: it prints the gap and exits 0. Pass --strict to exit 1
when any verified source host is unregistered (useful once the backlog below is cleared).
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
ALLOWLIST = os.path.join(HERE, 'source-host-allowlist.json')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')

VERIFIED = {
    'MANUFACTURER_VERIFIED',
    'MEASUREMENT_VERIFIED',
    'REPUTABLE_DATABASE_VERIFIED',
    'THIRD_PARTY_VERIFIED',
}


def host_of(url):
    try:
        return url.split('/')[2].lower()
    except IndexError:
        return ''


def main(argv):
    allow = {h['host'].lower(): h for h in json.load(open(ALLOWLIST, encoding='utf-8'))['hosts']}
    db = json.load(open(DATA, encoding='utf-8'))

    counts = collections.Counter()
    example = {}
    for record in db:
        for field, value in record.items():
            if not isinstance(value, dict):
                continue
            source = value.get('source')
            if not isinstance(source, str) or not source.startswith('http'):
                continue
            if value.get('status') not in VERIFIED:
                continue
            host = host_of(source)
            counts[host] += 1
            example.setdefault(host, (record['id'], field, source))

    missing = {h: c for h, c in counts.items() if h not in allow}
    registered = len(counts) - len(missing)
    print(f'verified-source hosts={len(counts)} registered={registered} unregistered={len(missing)}')
    for host, count in sorted(missing.items(), key=lambda kv: (-kv[1], kv[0])):
        record, field, source = example[host]
        print(f'  {count:4d}  {host:38s} e.g. {record}.{field} {source[:70]}')
    if missing and '--strict' in argv:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
