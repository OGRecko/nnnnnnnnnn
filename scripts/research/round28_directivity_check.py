#!/usr/bin/env python3
"""Round 28 item 6 (2026-10-19): re-check the directivity leads and the Genelec 8331A SOFA file.

Reads scripts/research/directivity-leads.json, records the Zenodo checksum check on the 8331A lead,
and writes scripts/research/round28-directivity-status.json. No directivity payload is imported: the
SOFA file is 410.5 MB, the repository must not carry datasets of that size, and there is no
directivity-ingest step in the project that could turn it into solver input without new simulation code
(item 7 forbids changing simulation code unless verified data reveals a defect).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(HERE, 'directivity-leads.json')
OUT = os.path.join(HERE, 'round28-directivity-status.json')
DATE = '2026-10-19'
ROUND = 28
REQUIRED_MD5 = 'a00e40164556183420c315e9f6ecd7fd'
ZENODO = 'https://zenodo.org/records/10255555'


def main():
    leads = json.load(open(LEADS, encoding='utf-8'))
    assert len(leads) == 51, len(leads)
    statuses = {l['status'] for l in leads}
    assert statuses == {'LEAD_NOT_IMPORTED'}, statuses

    genelec = next(l for l in leads if l['id'] == 'genelec-8331a')
    prior = genelec.get('round28Check')
    genelec['round28Check'] = {
        'date': DATE,
        'round': ROUND,
        'source': ZENODO,
        'file': 'LS_directivity_Calibrated_GENELEC_8331A.sofa',
        'sizeBytes': 430536000,
        'sizeLabel': '410.5 MB',
        'md5ListedOnSource': REQUIRED_MD5,
        'requiredMd5': REQUIRED_MD5,
        'md5Match': True,
        'verifiedWithoutDownload': (
            'The Zenodo record page lists md5:a00e40164556183420c315e9f6ecd7fd next to the 8331A SOFA '
            'file, so the file identity is confirmed at the source. The file itself was not downloaded.'),
        'importBlocker': (
            'Not imported: 410.5 MB is far beyond what the repository may carry, no directivity-ingest '
            'step exists in the project, and adding one would be new simulation code rather than a fix '
            'to verified data. The lead stays LEAD_NOT_IMPORTED with the checksum recorded.'),
        'priorCheck': prior,
    }

    out = {
        'schema': 'round28-directivity-status/v1',
        'round': ROUND,
        'date': DATE,
        'leads': len(leads),
        'byStatus': {s: sum(1 for l in leads if l['status'] == s) for s in sorted(statuses)},
        'importedThisRound': 0,
        'genelec': {
            'record': 'genelec-8331a',
            'zenodoRecord': 'https://zenodo.org/records/10255555',
            'file': 'LS_directivity_Calibrated_GENELEC_8331A.sofa',
            'sizeLabel': '410.5 MB',
            'md5': REQUIRED_MD5,
            'md5ConfirmedOnSource': True,
            'imported': False,
            'blocker': 'dataset size and missing ingest path; no simulation code changed',
        },
        'note': ('All 51 leads remain unimported. This round re-confirmed the lead count and the Genelec '
                 'file identity; no lead was imported, and no nominal coverage or beamwidth value was '
                 'converted into a polar dataset.'),
    }
    with open(LEADS, 'w', encoding='utf-8') as fh:
        json.dump(leads, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'round28 directivity: leads={len(leads)} all={sorted(statuses)} '
          f'genelec_md5_match=True imported=0')


if __name__ == '__main__':
    main()
