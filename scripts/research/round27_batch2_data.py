#!/usr/bin/env python3
"""Round 27 batch 2 (2026-10-19): queue URLs opened after the dispute batch.

Each outcome below was decided from the whole document (or from the section that
carries the specification table); quotations are verbatim.
"""

CHECKED_DATE = '2026-10-19'
ROUND = 27

CHECKS = [
    {
        'url': 'https://assets.klipsch.com/product-specsheets/RF-7-III_Spec-Sheet-v01.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'Klipsch RF-7 III floorstanding speaker spec sheet, v01 (single-page PDF)',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            'Specifications: "HIGH FREQUENCY DRIVERS 1.75\\" (4.45cm) titanium diaphragm compression driver"; '
            '"LOW FREQUENCY DRIVERS Two 10\\" (25.4cm) Cerametallic cone woofers"; "SENSITIVITY 100 dB @ 2.83V / 1M"; '
            '"POWER HANDLING 250W / 1000W peak"; "INPUTS Dual binding posts / bi-wire / bi-amp". Two woofers plus '
            'one compression driver = 3 transducers. The sheet never states passive, active, powered or built-in '
            'amplification; it publishes a peak power handling rating and passive-cabinet input terminals only, '
            'which is not an explicit classification statement.'
        ),
        'results': [
            ('legacy-klip-6.driverCount', 'PROMOTED',
             'The sheet lists two 10-inch Cerametallic woofers and one 1.75-inch titanium compression driver: '
             '3 transducers, matching the stored value.'),
            ('legacy-klip-6.active', 'NOT_STATED',
             'The sheet gives power handling, sensitivity and binding-post/bi-amp inputs but never writes '
             'passive/active, powered or built-in amplification. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://jblpro.com/en-US/site_elements/4430-and-4435-information',
        'sourceClass': 'MANUFACTURER',
        'document': 'JBL 4430 / 4435 Bi-Radial Studio Monitors information sheet (3 chunks)',
        'chunksOpened': [0],
        'chunksTotal': 3,
        'evidence': (
            'The sheet separates "Single Amplification" and "Biamplification" maximum power input rows, gives '
            '"Recommended Amplifier Power", and states "A switch located adjacent to the connection terminals '
            'allows the monitor to be biamplified. A special crossover card is available for the JBL Model 5235 '
            'electronic frequency dividing network". It never uses the words passive, active, powered or '
            'built-in amplification for either model. Driver complement: 4430 "uses a single 380 mm (15 in) low '
            'frequency driver"; 4435 "uses a pair of 380 mm (15 in) low frequency drivers"; both use one '
            'compression driver on the Bi-Radial horn.'
        ),
        'results': [
            ('jbl-4430.active', 'NOT_STATED',
             'The sheet describes single-amplification and biamplification wiring and a recommended amplifier '
             'power but never states passive/active or built-in amplification. Field stays unverified.'),
            ('legacy-jbl-6.active', 'NOT_STATED',
             'Same document, same finding: biamplification and external amplifier power are described, but no '
             'explicit passive/active classification appears. Field stays unverified.'),
        ],
    },
    {
        'url': 'https://www.dali-speakers.com/media/5320/oberon-manual.pdf',
        'sourceClass': 'MANUFACTURER',
        'document': 'DALI OBERON owner manual (6 chunks; English, Danish, Chinese and Japanese sections retrieved)',
        'chunksOpened': [0, 4],
        'chunksTotal': 6,
        'evidence': (
            'The manual refers to "TABLE 1" for carton contents (speakers per carton, grilles, pads) and to '
            '"TABLE 2" for "10.0 TECHNICAL SPECIFICATIONS", stating "I tabel 2 finder du de mest almindelige '
            'specifikationer for højttalerserien". The retrieved text contains neither Table 2 nor any per-model '
            'driver complement, driver size or count; the specification table is not present in the extracted '
            'text of the pages retrieved (sections 1.0-10.0 in four languages are prose only). No driver count '
            'can be read from this document, so none is recorded.'
        ),
        'results': [
            ('dali-oberon-3.driverCount', 'NOT_EXTRACTED',
             'The manual points to "Table 2" for technical specifications, but that table is not present in the '
             'retrieved text, so no driver count can be read. Value left unchanged.'),
            ('dali-oberon-5.driverCount', 'NOT_EXTRACTED',
             'Table 2 is not present in the retrieved text of the manual; no driver count can be read. Value '
             'left unchanged.'),
            ('dali-oberon7.driverCount', 'NOT_EXTRACTED',
             'Table 2 is not present in the retrieved text of the manual; no driver count can be read. Value '
             'left unchanged.'),
        ],
    },
]
