#!/usr/bin/env python3
"""Round 29 batch 31 (2026-10-19): no-provenance nulls probed against their own cited sources.

Only `electro-voice-ekx-15p` yields explicit field-level evidence. Everything else is recorded as an
outcome (NOT_STATED / INACCESSIBLE / NO_SPEC_TABLE), never as a value, and never with a provenance
object: the brief forbids "meaningless provenance objects" for unknown fields.
"""
DATE = '2026-10-19'
ROUND = 29

EV_EKX = 'https://www.electrovoice.com/product/ekx-15p'

PROMOTIONS = [
    {
        'record': 'electro-voice-ekx-15p',
        'field': 'driverCount',
        'value': 2,
        'source': EV_EKX,
        'note': ('Round 29 (2026-10-19): Electro-Voice EKX 15P product page — "The EKX 15P pairs an '
                 'EV-engineered EVS-15M 15-inch woofer and a DH-1M 1-inch titanium compression driver"; '
                 'headline reads "Powered 15\\" 2-Way Loudspeaker". Two transducers.'),
        'notesAppend': (' Round 29 (2026-10-19): driverCount 2 and active true taken from the EKX 15P '
                        'product page ("Powered 15\\" 2-Way Loudspeaker"; EVS-15M woofer + DH-1M '
                        'compression driver).'),
    },
    {
        'record': 'electro-voice-ekx-15p',
        'field': 'active',
        'value': True,
        'source': EV_EKX,
        'note': ('Round 29 (2026-10-19): Electro-Voice EKX 15P page — "Powered 15\\" 2-Way Loudspeaker" '
                 'and "1,500 W Class-D amp" inside the cabinet; explicit powered statement.'),
        'notesAppend': '',
    },
]

ASSESSMENTS = [
    {
        'record': 'atc-scm19', 'field': 'active', 'url': 'https://atc.audio/hi-fi/loudspeakers/entry-series/scm19/',
        'status': 'CHECKED_PARTIAL', 'outcome': 'NOT_STATED',
        'evidence': ('ATC SCM19 specification lists "Recommended Power Amplifier: 75 to 300 Watts" and '
                     '"Connectors: Binding Posts/4mm Plugs, bi-wire", plus a separate SCM19A model. The '
                     'SCM19 page never states passive or powered; an amplifier recommendation is not an '
                     'explicit passive statement, so the field stays unknown.'),
    },
    {
        'record': 'wilson-watt-puppy', 'field': 'active',
        'url': 'https://www.wilsonaudio.com/products/watt-puppy/watt-puppy-series-8',
        'status': 'CHECKED_CONFIRMED', 'outcome': 'NOT_STATED',
        'evidence': ('Wilson WATT/Puppy Series 8 technical specifications give enclosure type, drivers, '
                     'sensitivity, impedance and "Minimum Amplifier Power 7 Watts per channel" but no '
                     'passive/active/powered statement. Not promoted.'),
    },
    {
        'record': 'polk-rti-a7', 'field': 'active',
        'url': 'https://www.polkaudio.com/en-us/product/archive/archive-built-in-speakers/rti-a7',
        'status': 'INACCESSIBLE', 'outcome': 'INACCESSIBLE',
        'evidence': ('Polk archive URL now renders "Sorry, we\'ve got our wires crossed." — the product '
                     'archive page is gone and carries no specification text.'),
    },
    {
        'record': 'dutch-and-dutch-8c', 'field': 'driverCount',
        'url': 'https://dutchdutch.com/products/8c', 'status': 'CHECKED_PARTIAL',
        'outcome': 'NO_SPEC_TABLE',
        'evidence': ('The 8c storefront page is a configuration/purchase page (finish, stands, cables) and '
                     'has no driver table; https://dutchdutch.com/8c/ returns 404. No driver count '
                     'statement was found on the pages reachable today.'),
    },
    {
        'record': 'eV-sx300', 'field': 'active', 'url': 'https://www.electrovoice.com/product/sx300',
        'status': 'INACCESSIBLE', 'outcome': 'INACCESSIBLE',
        'evidence': ('electrovoice.com/product/sx300 returns an empty shell with only the site search '
                     'chrome; no product content is served.'),
    },
    {
        'record': 'eV-sx300', 'field': 'driverCount', 'url': 'https://www.electrovoice.com/product/sx300',
        'status': 'INACCESSIBLE', 'outcome': 'INACCESSIBLE',
        'evidence': 'Same empty shell: no driver information served.',
    },
    {
        'record': 'eV-eliminator', 'field': 'active', 'url': 'https://www.electrovoice.com/product/eliminator',
        'status': 'INACCESSIBLE', 'outcome': 'INACCESSIBLE',
        'evidence': 'electrovoice.com/product/eliminator returns an empty shell with no product content.',
    },
    {
        'record': 'eV-eliminator', 'field': 'driverCount',
        'url': 'https://www.electrovoice.com/product/eliminator',
        'status': 'INACCESSIBLE', 'outcome': 'INACCESSIBLE',
        'evidence': 'Same empty shell: no driver information served.',
    },
]
