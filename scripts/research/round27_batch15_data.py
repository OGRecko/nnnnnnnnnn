#!/usr/bin/env python3
"""Round 27 batch 15 (2026-10-19): Bowers & Wilkins 800 Series Diamond - checked, not promotable.

Each check reads the model's own technical specification table (brochure or information sheet
published by B&W). All seven tables print a nominal impedance row and a "recommended amplifier
power into 8 ohm on unclipped programme" row, and none of them prints a passive/active
classification. The repository's own rule - asserted in `src/data/speakers.test.ts` for
bw-802d3 and legacy-bw-7 - is "do not infer passive/active classification from a
recommended-amplifier range", so the seven `active` gaps stay open. Recording the checks
closes the URLs without manufacturing a value from an implication.

`driverCount` is already resolved for all seven records, so no count is rewritten here.
"""
CHECKED_DATE = '2026-10-19'
ROUND = 27
D4 = 'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw0365a301/downloads/800_series_diamond_d4_brochure_low-res.pdf'
D3_802 = 'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw7f94b222/archive-manuals/802-d3-info-sheet.pdf'
D3_800 = 'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_apac_shared/default/dw49334432/archive-manuals/800-d3-info-sheet.pdf'

NO_CLASS = ('The specification table prints the load and recommended-amplifier-power rows but no '
            'passive/active classification; classifying from that implication is forbidden by '
            'repository rule.')

CHECKS = [
    {
        'url': D4,
        'sourceClass': 'MANUFACTURER',
        'document': 'Bowers & Wilkins 800 Series Diamond D4 brochure, technical specification table',
        'chunksOpened': [1],
        'chunksTotal': 2,
        'evidence': (
            'Per-model blocks of the specification table. 801 D4: "3-way vented-box system"; "1x ø25mm '
            '(1in) diamond dome high-frequency 1x ø150mm (6in) Continuum cone FST midrange 2x ø250mm (10in) '
            'Aerofoil cone bass units"; "8Ω (minimum 3.0Ω)"; "50W – 1000W into 8Ω on unclipped programme". '
            '802 D4: "2x ø200mm (8in)" bass, "8Ω (minimum 3.0Ω)", "50W – 500W into 8Ω". 803 D4: '
            '"1x ø130mm (5in)" midrange, "2x ø180mm (7in)" bass, "8Ω (minimum 3.0Ω)", "50W – 500W into '
            '8Ω". 804 D4: "1x ø130mm (5in)" midrange, "2x ø165mm (6.5in)" bass, "8Ω (minimum 3.0Ω)", '
            '"50W – 200W into 8Ω". 805 D4: "2-way vented-box system"; "1x ø25mm (1in) diamond dome '
            'high-frequency 1x ø165mm (6.5in) Continuum cone bass midrange"; "8Ω (minimum 4.6Ω)"; '
            '"50W – 120W into 8Ω on unclipped programme". No row names a passive or active design.'
        ),
        'results': [
            ('bowers-wilkins-801-d4.active', 'NOT_STATED', None, NO_CLASS),
            ('bowers-wilkins-802-d4.active', 'NOT_STATED', None, NO_CLASS),
            ('bw-803-d4.active', 'NOT_STATED', None, NO_CLASS),
            ('bowers-wilkins-804-d4.active', 'NOT_STATED', None, NO_CLASS),
            ('bw-805-d4.active', 'NOT_STATED', None, NO_CLASS),
        ],
    },
    {
        'url': D3_802,
        'sourceClass': 'MANUFACTURER',
        'document': 'Bowers & Wilkins 802 D3 information sheet, technical specifications',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            '"Description 3-way vented-box system"; "Drive units 1x ø25mm (1 in) diamond dome '
            'high-frequency 1x ø150mm (6 in) Continuum cone FST™ midrange 2x ø200mm (8 in) Aerofoil cone '
            'bass units"; "Nominal impedance 8Ω (minimum 3.0Ω)"; "Recommended amplifier 50W - 500W into '
            '8Ω on unclipped programme". No passive/active row.'
        ),
        'results': [('bw-802d3.active', 'NOT_STATED', None, NO_CLASS)],
    },
    {
        'url': D3_800,
        'sourceClass': 'MANUFACTURER',
        'document': 'Bowers & Wilkins 800 D3 information sheet, technical specifications',
        'chunksOpened': [0],
        'chunksTotal': 1,
        'evidence': (
            '"Description 3-way vented-box system"; "Drive units 1x ø25mm (1 in) diamond dome '
            'high-frequency 1x ø150mm (6 in) Continuum cone FST™ midrange 2x ø250mm (10 in) Aerofoil cone '
            'bass units"; "Nominal impedance 8Ω (minimum 3.0Ω)"; "Recommended amplifier 50W - 1000W into '
            '8Ω on unclipped programme". No passive/active row.'
        ),
        'results': [('legacy-bw-7.active', 'NOT_STATED', None, NO_CLASS)],
    },
]
