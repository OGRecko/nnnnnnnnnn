#!/usr/bin/env python3
"""Round 29: align queue rows with the MV host-policy demotions.

Rows recorded as PROMOTED for a field that is now CITED_IN_NOTES_UNCHECKED become
SUPPORTED_NOT_PROMOTED (the document still supports the value; the host cannot carry MV).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = os.path.join(HERE, 'queue-url-status.json')
REPORT = os.path.join(HERE, 'round29-mv-host-audit.json')
DATE = '2026-10-19'


def main():
    report = json.load(open(REPORT, encoding='utf-8'))
    wanted = {(r['record'], r['field']): r for r in report['rows']}
    status = json.load(open(STATUS, encoding='utf-8'))
    changed = 0
    for entry in status['urls']:
        for fr in entry.get('fieldResults', []):
            key = (fr.get('record'), fr.get('field'))
            row = wanted.get(key)
            if row is None or fr.get('outcome') == 'SUPPORTED_NOT_PROMOTED':
                continue
            if fr.get('outcome') != 'PROMOTED':
                continue
            fr['outcome'] = 'SUPPORTED_NOT_PROMOTED'
            fr['note'] = ((fr.get('note') or '').rstrip() +
                          f' Round 29 ({DATE}): host {row["host"]} is NOT_MANUFACTURER; status demoted to '
                          'CITED_IN_NOTES_UNCHECKED, value kept.').strip()
            changed += 1
    json.dump(status, open(STATUS, 'w'), indent=2, ensure_ascii=False)
    open(STATUS, 'a').write('\n')
    print(f'round29 queue rows aligned: changed={changed}')


if __name__ == '__main__':
    main()
