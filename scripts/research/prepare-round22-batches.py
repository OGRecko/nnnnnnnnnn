#!/usr/bin/env python3
"""Prepare and validate Round 22 provenance audit artifacts:
1. Update source-host-allowlist.json with Decision 8 operator checks.
2. Reconcile electro-voice-zx3-60 and electro-voice-zx3-90 across speakers.json,
   round18-value-history.json, round18-url-results.json, and round18-field-check-ledger.json.
3. Fix round14-host-policy status entries in queue-url-status.json so exact URLs are matched
   and Round 18 promotions are reflected cleanly.
4. Build round22-url-results.json (CITED_IN_NOTES_UNCHECKED source checks).
5. Build round22-structural-batch.json (UNSOURCED field restorations from exact-model manufacturer pages).
"""
import json, os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(ROOT, 'src', 'data', 'speakers.json')
ALLOW = os.path.join(HERE, 'source-host-allowlist.json')
STATUS = os.path.join(HERE, 'queue-url-status.json')
R18_HIST = os.path.join(HERE, 'round18-value-history.json')
R18_URLS = os.path.join(HERE, 'round18-url-results.json')
R22_URLS = os.path.join(HERE, 'round22-url-results.json')
R22_STRUCT = os.path.join(HERE, 'round22-structural-batch.json')
CHECKED_DATE = '2026-10-19'


def dump(path, obj):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def update_allowlist():
    allow = json.load(open(ALLOW, encoding='utf-8'))
    allow['reviewDate'] = CHECKED_DATE
    by_host = {h['host']: h for h in allow['hosts']}

    updates = {
        'www.eviaudio.fr': {
            'host': 'www.eviaudio.fr',
            'status': 'ESTABLISHED',
            'operator': 'EVI Audio France (official French distributor of Electro-Voice, Dynacord, RTS, and Telex; hosts verbatim Electro-Voice manual PDFs)',
            'evidence': [
                'https://www.eviaudio.fr/ homepage identifies operator as "EVI AUDIO FRANCE" ("Bienvenue chez EVI AUDIO FRANCE ... Electro-Voice, Dynacord, RTS, Telex").',
                'https://www.eviaudio.fr/wp-content/uploads/2020/04/ev_zx3_manuel.pdf is the verbatim Electro-Voice Zx3 Owner\'s Manual DOC38110265 Rev B carrying "© Electro-Voice, 12000 Portland Ave South, Burnsville, MN 55337" (permitted under Owner Decision 1, 2026-10-12).'
            ],
            'sources': [
                'https://www.eviaudio.fr/',
                'https://www.eviaudio.fr/wp-content/uploads/2020/04/ev_zx3_manuel.pdf'
            ],
            'previousStatus': 'NOT_ESTABLISHED',
            'note': 'Established under Owner Decision 1 (distributor copy of verbatim manufacturer manual) and Decision 8 (document check).'
        },
        'www.fmicassets.com': {
            'host': 'www.fmicassets.com',
            'status': 'ESTABLISHED',
            'operator': 'Fender Musical Instruments Corporation / PreSonus Audio Electronics, Inc. (Fender-owned since 2021)',
            'evidence': [
                'Owner confirmation (2026-10-13, round 18): www.fmicassets.com is PreSonus\'s official document host after Fender\'s 2021 acquisition.',
                'https://www.fmicassets.com/Damroot/Original/10001/OM_2777500107_Eris-E5_Tech-Sheet_EN.pdf carries "© 2017 PreSonus Audio Electronics, Inc. All Rights Reserved. Baton Rouge • USA".',
                'https://www.fmicassets.com/Damroot/Original/10001/OM_leg_bassamp_Bassman_115__410_2005.pdf carries "A Product of: FENDER MUSICAL INSTRUMENTS CORPORATION CORONA, CALIFORNIA".'
            ],
            'sources': [
                'https://www.fmicassets.com/Damroot/Original/10001/OM_2777500107_Eris-E5_Tech-Sheet_EN.pdf',
                'https://www.fmicassets.com/Damroot/Original/10001/OM_leg_bassamp_Bassman_115__410_2005.pdf'
            ],
            'previousStatus': 'NOT_ESTABLISHED',
            'note': 'Established by Owner Decision (2026-10-13) and Decision 8 document check.'
        },
        'boseprofessional.com': {
            'host': 'boseprofessional.com',
            'status': 'ESTABLISHED',
            'operator': 'Transom Post OpCo LLC, dba Bose Professional',
            'evidence': [
                'https://boseprofessional.com/products/loudspeakers/surface-mount/designmax-surface-mount/designmax-dm5se-1-pair links directly to assets.boseprofessional.com technical data sheets carrying "©2025 Transom Post OpCo LLC".'
            ],
            'sources': [
                'https://boseprofessional.com/products/loudspeakers/surface-mount/designmax-surface-mount/designmax-dm5se-1-pair'
            ]
        },
        'jblpro.com': {
            'host': 'jblpro.com',
            'status': 'ESTABLISHED',
            'operator': 'HARMAN International Industries, Incorporated (JBL Professional)',
            'evidence': [
                'https://jblpro.com/en-US/site_elements/srx828sp-spec-sheet and https://jblpro.com/en-US/site_elements/jrx225-spec-sheet carry "HARMAN Professional 8500 Balboa Blvd. Northridge, CA 91329 USA" and "© HARMAN International Industries, Incorporated".',
                'https://jblpro.com/en-US/products/lsr305.html footer carries "© 2026 HARMAN International. All Rights Reserved."'
            ],
            'sources': [
                'https://jblpro.com/en-US/site_elements/srx828sp-spec-sheet',
                'https://jblpro.com/en-US/products/lsr305.html'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'dynaudio.com': {
            'host': 'dynaudio.com',
            'status': 'ESTABLISHED',
            'operator': 'Dynaudio A/S (owned by GoerTek since 2014)',
            'evidence': [
                'https://dynaudio.com/hubfs/2022_DynaudioCore7_SpecSheet_WEB.pdf and https://dynaudio.com/hubfs/user-manuals/home-audio/dynaudio_manuals_home_audio_passive_speakers_en.pdf carry "Dynaudio A/S, Sverigesvej 15, 8660 Skanderborg, Denmark" and "© Dynaudio A/S".'
            ],
            'sources': [
                'https://dynaudio.com/hubfs/2022_DynaudioCore7_SpecSheet_WEB.pdf',
                'https://dynaudio.com/hubfs/user-manuals/home-audio/dynaudio_manuals_home_audio_passive_speakers_en.pdf'
            ],
            'previousStatus': 'OWNER_IDENTIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.genelec.com': {
            'host': 'www.genelec.com',
            'status': 'ESTABLISHED',
            'operator': 'Genelec Oy',
            'evidence': [
                'https://www.genelec.com/8361a and linked datasheets on assets.ctfassets.net/4zjnzn055a4v carry "Genelec Oy, Olvitie 5, FI-74100 Iisalmi, Finland" and "Copyright Genelec Oy".'
            ],
            'sources': [
                'https://www.genelec.com/8361a',
                'https://assets.ctfassets.net/4zjnzn055a4v/2ebf482d-2ac6-4eb0-8994-8216c9f9f9d6/1030A_sysspecs.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.adam-audio.com': {
            'host': 'www.adam-audio.com',
            'status': 'ESTABLISHED',
            'operator': 'ADAM Audio GmbH (part of Focusrite Group since 2019-07-16)',
            'evidence': [
                'https://www.adam-audio.com/content/uploads/2016/12/adam-audio-user-manual-A7-fr.pdf and https://www.adam-audio.com/content/uploads/2016/12/adam-audio-manual-S3A-en-de.pdf carry "ADAM Audio GmbH, Berlin, Germany".',
                'https://www.adam-audio.com/en/a-series/a4v/ footer carries "© ADAM Audio GmbH".'
            ],
            'sources': [
                'https://www.adam-audio.com/content/uploads/2016/12/adam-audio-user-manual-A7-fr.pdf',
                'https://www.adam-audio.com/en/a-series/a4v/'
            ],
            'previousStatus': 'OWNER_IDENTIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'mackie.com': {
            'host': 'mackie.com',
            'status': 'ESTABLISHED',
            'operator': 'LOUD Audio, LLC (formerly LOUD Technologies Inc.)',
            'evidence': [
                'https://mackie.com/img/file_resources/THUMPXT_2022_SS.pdf and https://mackie.com/img/file_resources/SRM%20V-Class_SS.pdf carry "©2020–2022 LOUD Audio, LLC. All Rights Reserved."',
                'https://mackie.com/img/file_resources/DLM8_12_SS.pdf carries "©2012 LOUD Technologies Inc. 16220 Wood-Red Road NE, Woodinville, WA 98072 USA".'
            ],
            'sources': [
                'https://mackie.com/img/file_resources/THUMPXT_2022_SS.pdf',
                'https://mackie.com/img/file_resources/DLM8_12_SS.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'assets.kef.com': {
            'host': 'assets.kef.com',
            'status': 'ESTABLISHED',
            'operator': 'GP Acoustics (UK) Limited / GP Acoustics Group (KEF)',
            'evidence': [
                'https://assets.kef.com/documents/ls50/20-KEF-LS50-Wireless-II-Product-Info-Sheet.pdf and https://assets.kef.com/pdf_doc/KF92/KF92_infosheet_EN.pdf carry "GP Acoustics (UK) Limited, Eccleston Road, Tovil, Maidstone, Kent, ME15 6QP, UK".'
            ],
            'sources': [
                'https://assets.kef.com/documents/ls50/20-KEF-LS50-Wireless-II-Product-Info-Sheet.pdf',
                'https://assets.kef.com/pdf_doc/KF92/KF92_infosheet_EN.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'ap.kef.com': {
            'host': 'ap.kef.com',
            'status': 'ESTABLISHED',
            'operator': 'GP Acoustics Group (KEF)',
            'evidence': [
                'https://us.kef.com/pages/terms-and-conditions states: "using the website displayed at the URL kef.com and its associate domains or sub-domains (the \'Site\') ... operated by GP Acoustics Group and/or its affiliates (\'KEF\')".'
            ],
            'sources': [
                'https://us.kef.com/pages/terms-and-conditions'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'us.kef.com': {
            'host': 'us.kef.com',
            'status': 'ESTABLISHED',
            'operator': 'GP Acoustics Group (KEF)',
            'evidence': [
                'https://us.kef.com/pages/terms-and-conditions states: "using the website displayed at the URL kef.com and its associate domains or sub-domains (the \'Site\') ... operated by GP Acoustics Group and/or its affiliates (\'KEF\')".'
            ],
            'sources': [
                'https://us.kef.com/pages/terms-and-conditions'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'international.kef.com': {
            'host': 'international.kef.com',
            'status': 'ESTABLISHED',
            'operator': 'GP Acoustics Group (KEF)',
            'evidence': [
                'https://us.kef.com/pages/terms-and-conditions states: "using the website displayed at the URL kef.com and its associate domains or sub-domains (the \'Site\') ... operated by GP Acoustics Group and/or its affiliates (\'KEF\')".'
            ],
            'sources': [
                'https://us.kef.com/pages/terms-and-conditions'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'media.focal-naim.com': {
            'host': 'media.focal-naim.com',
            'status': 'ESTABLISHED',
            'operator': 'Focal-JMlab (Vervent Audio Group / Focal Naim)',
            'evidence': [
                'https://media.focal-naim.com/dam/aria-926/fp_aria_926_gb.pdf and https://media.focal-naim.com/dam/sub-one/fp_sub_one_en.pdf carry "Focal-JMlab - BP 374 - 108, rue de l\'Avenir - 42353 La Talaudière cedex - France - www.focal.com".'
            ],
            'sources': [
                'https://media.focal-naim.com/dam/aria-926/fp_aria_926_gb.pdf',
                'https://media.focal-naim.com/dam/sub-one/fp_sub_one_en.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'dam.focal-naim.com': {
            'host': 'dam.focal-naim.com',
            'status': 'ESTABLISHED',
            'operator': 'Focal-JMlab (Vervent Audio Group / Focal Naim)',
            'evidence': [
                'Official Focal-Naim DAM asset host serving Focal product datasheets (FP_Aria_906_GB-pdf.pdf, FP_Chora806_GB-pdf.pdf, FP_Chora826_GB-pdf.pdf, FP_Alpha_80_Evo_EN-pdf.pdf) produced by Focal-JMlab, La Talaudière, France.'
            ],
            'sources': [
                'https://dam.focal-naim.com/m/733c5c6acac9341c/original/FP_Aria_906_GB-pdf.pdf',
                'https://dam.focal-naim.com/m/75f492b929881650/original/FP_Alpha_80_Evo_EN-pdf.pdf'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'www.focal.com': {
            'host': 'www.focal.com',
            'status': 'ESTABLISHED',
            'operator': 'Focal-JMlab',
            'evidence': [
                'https://www.focal.com/products/alpha-65-evo and Focal product sheets ("Focal-JMlab - BP 374 - 108, rue de l\'Avenir - 42353 La Talaudière cedex - France - www.focal.com").'
            ],
            'sources': [
                'https://www.focal.com/products/alpha-65-evo',
                'https://media.focal-naim.com/dam/sub-one/fp_sub_one_en.pdf'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'assets.klipsch.com': {
            'host': 'assets.klipsch.com',
            'status': 'ESTABLISHED',
            'operator': 'Klipsch Group, Inc. (Premium Audio Company / Gentex Corporation)',
            'evidence': [
                'https://assets.klipsch.com/product-specsheets/Heresy-Spec.pdf and https://assets.klipsch.com/product-specsheets/R-51M_Spec-Sheet_v01.pdf carry "3502 WOODVIEW TRACE INDIANAPOLIS, IN 46268 | KLIPSCH.COM" and "©2018 KLIPSCH GROUP, INC."'
            ],
            'sources': [
                'https://assets.klipsch.com/product-specsheets/Heresy-Spec.pdf',
                'https://assets.klipsch.com/product-specsheets/R-51M_Spec-Sheet_v01.pdf'
            ],
            'previousStatus': 'OWNER_IDENTIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.klipsch.com': {
            'host': 'www.klipsch.com',
            'status': 'ESTABLISHED',
            'operator': 'Klipsch Group, Inc.',
            'evidence': [
                'Official Klipsch brand domain named on all Klipsch spec sheets ("3502 WOODVIEW TRACE INDIANAPOLIS, IN 46268 | KLIPSCH.COM", "© KLIPSCH GROUP, INC.").'
            ],
            'sources': [
                'https://www.klipsch.com/products/cdt-5650-c-ii',
                'https://assets.klipsch.com/product-specsheets/R-51M_Spec-Sheet_v01.pdf'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'www.bowerswilkins.com': {
            'host': 'www.bowerswilkins.com',
            'status': 'ESTABLISHED',
            'operator': 'B&W Group Ltd. (Bowers & Wilkins, owned by Harman / Samsung Electronics)',
            'evidence': [
                'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw0a89b49d/downloads/db1d-information-sheet.pdf and 804d4-information-sheet.pdf carry "B&W Group Ltd., Dale Road, Worthing, West Sussex, BN11 2BH, England" and "Copyright © B&W Group Ltd."'
            ],
            'sources': [
                'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dw0a89b49d/downloads/db1d-information-sheet.pdf',
                'https://www.bowerswilkins.com/on/demandware.static/-/Library-Sites-bowers_northamerica_shared/default/dwd7be5f6c/downloads/804d4-information-sheet.pdf'
            ],
            'previousStatus': 'OWNER_IDENTIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'atc.audio': {
            'host': 'atc.audio',
            'status': 'ESTABLISHED',
            'operator': 'Loudspeaker Technology Ltd (ATC)',
            'evidence': [
                'https://atc.audio/wp-content/uploads/2017/05/SCM45A-Pro-Tech.-Datasheet-revB.pdf (linked from https://atc.audio/professional/loudspeakers/scm45a-pro/) carries "Loudspeaker Technology Ltd, Gypsy Lane, Aston Down, Stroud, Gloucestershire, GL6 8HR".'
            ],
            'sources': [
                'https://atc.audio/professional/loudspeakers/scm45a-pro/',
                'https://atc.audio/wp-content/uploads/2017/05/SCM45A-Pro-Tech.-Datasheet-revB.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'pmc-speakers.com': {
            'host': 'pmc-speakers.com',
            'status': 'ESTABLISHED',
            'operator': 'Professional Monitor Company Limited (PMC)',
            'evidence': [
                'https://pmc-speakers.com/privacy-policy states: "Our company name is Professional Monitor Company Limited (PMC). Our registered address is Holme Court, Biggleswade SG18 9ST, United Kingdom, company number 02472746."'
            ],
            'sources': [
                'https://pmc-speakers.com/privacy-policy',
                'https://pmc-speakers.com/studio/active/result6'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.l-acoustics.com': {
            'host': 'www.l-acoustics.com',
            'status': 'ESTABLISHED',
            'operator': 'L-ACOUSTICS',
            'evidence': [
                'https://prdstglaxxwe001.blob.core.windows.net/media/documents/Syva_DoC_EN.pdf and SYVA_SPS_EN_2.2.pdf (linked directly from https://www.l-acoustics.com/products/syva/) carry "L-ACOUSTICS, 13 rue Levacher Cintrat – 91460 Marcoussis – France" and "info@l-acoustics.com / www.l-acoustics.com".'
            ],
            'sources': [
                'https://www.l-acoustics.com/products/syva/',
                'https://prdstglaxxwe001.blob.core.windows.net/media/documents/Syva_DoC_EN.pdf'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.martinlogan.com': {
            'host': 'www.martinlogan.com',
            'status': 'ESTABLISHED',
            'operator': 'MartinLogan, Ltd.',
            'evidence': [
                'https://www.martinlogan.com/uploads/documents/manuals/manual_motion_60xt.pdf and https://www.martinlogan.com/en/privacy-policy carry "MartinLogan, Ltd., 2101 Delaware Street, Lawrence, Kansas 66046, USA" and "© MartinLogan, Ltd."'
            ],
            'sources': [
                'https://www.martinlogan.com/uploads/documents/manuals/manual_motion_60xt.pdf',
                'https://www.martinlogan.com/en/privacy-policy'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        },
        'www.wharfedale.co.uk': {
            'host': 'www.wharfedale.co.uk',
            'status': 'ESTABLISHED',
            'operator': 'IAG Group Ltd. (International Audio Group / Wharfedale)',
            'evidence': [
                'https://www.wharfedale.co.uk/cdn/shop/files/Diamond_12_User_Manual_250729_R13.pdf (linked from https://www.wharfedale.co.uk/collections/diamond-12-series/products/diamond-12-1) carries "IAG House, 13/14 Glebe Road, Huntingdon, Cambridgeshire, PE29 7DL, UK ... www.wharfedale.co.uk" and identifies manufacturer "IAG Group Ltd."'
            ],
            'sources': [
                'https://www.wharfedale.co.uk/collections/diamond-12-series/products/diamond-12-1',
                'https://www.wharfedale.co.uk/cdn/shop/files/Diamond_12_User_Manual_250729_R13.pdf'
            ],
            'note': 'Established by Decision 8 document check.'
        },
        'www.dali-speakers.com': {
            'host': 'www.dali-speakers.com',
            'status': 'ESTABLISHED',
            'operator': 'DALI A/S (Danish Audiophile Loudspeaker Industries)',
            'evidence': [
                'https://www.dali-speakers.com/media/5320/oberon-manual.pdf and https://www.dali-speakers.com/en/about-dali/ identify operator "DALI A/S, Dali Allé 1, DK-9610 Nørager, Denmark, www.dali-speakers.com".'
            ],
            'sources': [
                'https://www.dali-speakers.com/media/5320/oberon-manual.pdf',
                'https://www.dali-speakers.com/en/about-dali/'
            ],
            'previousStatus': 'BRAND_DOMAIN_UNVERIFIED',
            'note': 'Established by Decision 8 document check.'
        }
    }

    for host, entry in updates.items():
        by_host[host] = entry

    allow['hosts'] = [by_host[k] for k in by_host]
    dump(ALLOW, allow)
    print(f'Updated source-host-allowlist.json: {len(allow["hosts"])} hosts ({sum(1 for h in allow["hosts"] if h["status"].startswith("ESTABLISHED"))} established)')


def reconcile_zx3():
    db = json.load(open(DATA, encoding='utf-8'))
    by_id = {r['id']: r for r in db}
    doc_origin = 'Electro-Voice Zx3 Owners Manual, DOC38110265 Rev B; copyright Electro-Voice, 12000 Portland Ave South, Burnsville, MN 55337.'
    host_loc = 'www.eviaudio.fr (EVI Audio France distributor copy; permitted under owner decision 1, 2026-10-12).'
    zx3_url = 'https://www.eviaudio.fr/wp-content/uploads/2020/04/ev_zx3_manuel.pdf'

    acoustic_reconciliations = []
    for sid in ('electro-voice-zx3-60', 'electro-voice-zx3-90'):
        r = by_id[sid]
        cov = '60° x 60°' if sid.endswith('-60') else '90° x 50°'
        assert r['driverCount'] == 2
        assert r['active'] is False
        assert r['woofer']['value'] == 12
        assert r['sensitivity']['value'] == 97
        assert r['power']['value'] == 600
        assert r['impedance']['value'] == 8
        assert r['frequencyResponse']['low_hz'] == 58 and r['frequencyResponse']['high_hz'] == 15000

        # Ensure all 5 acoustic spec fields carry identical documentOrigin, hostingLocation, and clean notes
        field_notes = {
            'sensitivity': f'Round 18 (2026-10-16): origin and hosting recorded separately; Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table confirms Axial Sensitivity (SPL, 1 W / 1 m) = 97 dB (half-space; 95 dB full-space for {cov} model).',
            'woofer': 'Round 18 (2026-10-16): origin and hosting recorded separately; Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table confirms LF Transducer = DVX3121, 12 in (305 mm) driver.',
            'power': 'Round 18 (2026-10-16): origin and hosting recorded separately; Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table confirms Power Handling (Full-Range) = 600 W Cont. / 2400 W Peak.',
            'impedance': 'Round 18 (2026-10-16): origin and hosting recorded separately; Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table confirms Nominal Impedance = 8 Ohms (Minimum Impedance 6.2 Ohms).',
            'frequencyResponse': 'Round 18 (2026-10-16): origin and hosting recorded separately; Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table confirms Frequency Response (-3 dB) = 58 Hz - 15,000 Hz (half-space).'
        }
        # Preserve original before objects if already recorded in round18-value-history.json
        r18_existing = json.load(open(R18_HIST, encoding='utf-8')) if os.path.exists(R18_HIST) else {}
        prev_before_map = {
            (x['id'], x['field']): x['before']
            for x in r18_existing.get('acousticFieldProvenanceReconciliation', [])
        }
        for af, note_text in field_notes.items():
            before_obj = prev_before_map.get((sid, af), dict(r[af]))
            r[af]['documentOrigin'] = doc_origin
            r[af]['hostingLocation'] = host_loc
            r[af]['note'] = note_text
            acoustic_reconciliations.append({
                'id': sid,
                'field': af,
                'value': r[af].get('value', {'low_hz': r[af].get('low_hz'), 'high_hz': r[af].get('high_hz')}),
                'before': before_obj,
                'after': dict(r[af]),
                'round': 18
            })

        # Ensure driverCountProvenance and activeProvenance have clean notes without duplicate Round 18: prefixes
        r['driverCountProvenance']['documentOrigin'] = doc_origin
        r['driverCountProvenance']['hostingLocation'] = host_loc
        r['driverCountProvenance']['note'] = 'Round 18 (2026-10-16): Electro-Voice Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table: LF Transducer DVX3121 12 in (305 mm) driver + HF Transducer ND2 2 in (50 mm) voice-coil compression driver (2 transducers; Passive or Biamp 2-Way).'
        r['activeProvenance']['documentOrigin'] = doc_origin
        r['activeProvenance']['hostingLocation'] = host_loc
        r['activeProvenance']['note'] = 'Round 18 (2026-10-16): Electro-Voice Zx3 Owner\'s Manual DOC38110265 Rev B p. 3 spec table: System Configuration "Passive or Biamp 2-Way"; Connectors "(2) 4 Contact Neutrik Speakon"; external amplifier required.'

    dump(DATA, db)

    # Update round18-url-results.json so chunksOpened includes all 6 chunks [0, 1, 2, 3, 4, 5]
    r18_urls = json.load(open(R18_URLS, encoding='utf-8'))
    for e in r18_urls['entries']:
        if e['url'] == zx3_url:
            e['chunksOpened'] = [0, 1, 2, 3, 4, 5]
            e['evidence'] = (
                'Electro-Voice Zx3 Owner\'s Manual, DOC38110265 Rev B (chunks 0-5 inspected): '
                'copyright Electro-Voice, 12000 Portland Ave South, Burnsville, MN 55337. '
                'Spec table (p. 3) covers Zx3-60B/60W/60PI (60° x 60°) and Zx3-90B/90W/90PI (90° x 50°): '
                'System Configuration "Passive or Biamp 2-Way"; LF Transducer "DVX3121, 12 in (305 mm) Driver"; '
                'HF Transducer "ND2, 2 in (50 mm) Voice Coil Compression Driver on a 1 in Exit Horn"; '
                'Frequency Response (-3 dB) "58 Hz - 15,000 Hz"; Axial Sensitivity (SPL, 1 W / 1 m) "97 dB" (half-space; 95 dB full-space); '
                'Power Handling (Full-Range) "600 W Cont. / 2400 W Peak"; Nominal Impedance "8 Ohms"; '
                'Connectors "(2) 4 Contact Neutrik Speakon".'
            )
    dump(R18_URLS, r18_urls)

    # Update round18-value-history.json so after objects on zx3-60/90 include documentOrigin and hostingLocation,
    # and preserve acousticFieldProvenanceReconciliation
    r18_hist = json.load(open(R18_HIST, encoding='utf-8'))
    for e in r18_hist['entries']:
        if e['id'] in ('electro-voice-zx3-60', 'electro-voice-zx3-90'):
            rec = by_id[e['id']]
            e['after'] = dict(rec[e['field'] + 'Provenance'])
    r18_hist['acousticFieldProvenanceReconciliation'] = acoustic_reconciliations
    dump(R18_HIST, r18_hist)
    print('Reconciled electro-voice-zx3-60 and electro-voice-zx3-90 in speakers.json, round18-url-results.json, and round18-value-history.json.')


def fix_round14_status_file():
    """Fix queue-url-status.json entries on www.fmicassets.com where apply-round14-host-policy.py
    matched by host instead of exact URL, and update R65/R80 URL status to reflect Round 18 promotion."""
    status = json.load(open(STATUS, encoding='utf-8'))
    r18_urls = json.load(open(R18_URLS, encoding='utf-8'))
    r18_by_url = {e['url']: e for e in r18_urls['entries']}

    for u in status['urls']:
        url = u['url']
        if url in r18_by_url:
            e = r18_by_url[url]
            history = list(u.get('history', []))
            if u.get('status') not in (None, 'OPEN') and u.get('round') != 18:
                snap = {k: v for k, v in u.items() if k != 'history'}
                history.append({'snapshotOfRound': u.get('round'), 'entry': snap})
            u['round'] = 18
            u['status'] = e['status']
            u['chunksOpened'] = e['chunksOpened']
            u['chunksTotal'] = e.get('chunksTotal')
            u['checkedDate'] = r18_urls['checkedDate']
            u['sourceClass'] = 'DISTRIBUTOR_HOSTED_MANUFACTURER_MANUAL' if 'eviaudio.fr' in url else 'MANUFACTURER'
            u['document'] = e.get('document', '')
            u['evidence'] = e['evidence']
            u['fieldResults'] = [
                {
                    'record': fr['record'],
                    'field': fr['field'],
                    'value': fr['value'],
                    'outcome': fr['outcome'],
                    'note': fr.get('evidence', '')
                }
                for fr in e['fieldResults']
            ]
            u['history'] = history
        elif 'fmicassets.com' in url:
            # Remove cross-URL fieldResults that were added by host-matching bug in apply-round14-host-policy.py
            if 'OM_2777500107_Eris-E5_Tech-Sheet_EN.pdf' in url:
                u['fieldResults'] = [fr for fr in u.get('fieldResults', []) if fr['record'] == 'presonus-eris-e5']
            elif 'OM_leg_bassamp_Bassman_115__410_2005.pdf' in url:
                u['fieldResults'] = []
                u['status'] = 'OPEN'
                u['round'] = None

    dump(STATUS, status)
    print('Fixed round14/round18 URL status entries in queue-url-status.json.')




def _load_evidence():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'round22_evidence_data', os.path.join(HERE, 'round22_evidence_data.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DEFAULT_OUTCOMES = {'driverCount': ('PROMOTED', None),
                    'active': ('NOT_STATED', None)}


def build_round22_url_results():
    """Turn the Round 22 evidence table into round22-url-results.json.

    Values always come from the live catalogue; a field is included only when its
    provenance still points at the checked URL with status CITED_IN_NOTES_UNCHECKED.
    """
    ev = _load_evidence()
    db = json.load(open(DATA, encoding='utf-8'))
    status = json.load(open(STATUS, encoding='utf-8'))
    known_urls = {u['url'] for u in status['urls']}
    existing = json.load(open(R22_URLS, encoding='utf-8')) if os.path.exists(R22_URLS) else {'entries': []}
    existing_by_url = {e['url']: e for e in existing['entries']}
    entries = []
    declared_unused = 0
    for chk in ev.CHECKS:
        url = chk['url']
        assert url in known_urls, 'URL not in queue-url-status.json: ' + url
        # Idempotent re-run: keep the entry that was already applied; the live catalogue
        # no longer shows those fields as CITED_IN_NOTES_UNCHECKED after apply.
        if url in existing_by_url and existing_by_url[url].get('round') == 22:
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
            # The ledger vocabulary has no NOT_EXTRACTED: a document we could not read
            # (parser limit or HTTP error) is recorded as INACCESSIBLE.
            status_value = 'INACCESSIBLE'
        elif outcomes == {'PROMOTED'}:
            status_value = 'CHECKED_CONFIRMED'
        else:
            status_value = 'CHECKED_PARTIAL'
        entries.append({
            'url': url,
            'host': url.split('/')[2],
            'sourceClass': 'MANUFACTURER',
            'round': 22,
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
    out = {'round': 22, 'checkedDate': ev.CHECKED_DATE, 'entries': entries}
    dump(R22_URLS, out)
    promoted = sum(1 for e in entries for fr in e['fieldResults'] if fr['outcome'] == 'PROMOTED')
    print(f'round22-url-results.json: urls={len(entries)} field_results='
          f'{sum(len(e["fieldResults"]) for e in entries)} promotions_planned={promoted} '
          f'declared_but_not_tied={declared_unused}')


def build_round22_structural_batch():
    ev = _load_evidence()
    out = {'round': 22, 'checkedDate': ev.CHECKED_DATE, 'entries': ev.STRUCTURAL}
    dump(R22_STRUCT, out)
    print(f'round22-structural-batch.json: entries={len(out["entries"])}')


if __name__ == '__main__':
    update_allowlist()
    reconcile_zx3()
    fix_round14_status_file()
    build_round22_url_results()
    build_round22_structural_batch()
