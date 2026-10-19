# Cavity Audio — Final Release Verification

**Audit date:** 2026-10-19  
**Product:** Cavity Audio 1.0.0  
**Release constraints:** free/public/no login/no payment; 50,000,000 FDTD grid-cell ceiling; 1–16 sources; 1–64 receivers.

## Verdict

# NOT RELEASE READY

The source/data gates are prepared and current documentation is generated from the authoritative source. External runtime, Windows signing, cloud credentials, and legal approval remain release-owner responsibilities and are not represented as completed by this source archive.

## Speaker database

- Records: 657
- Unique IDs: 657
- Unique brand/model pairs: 657
- PARTIALLY_VERIFIED: 657
- UNVERIFIED: 0
- UNAVAILABLE: 0
- Source-backed fields: sensitivity 305; power 416; impedance 355; resonant frequency 18; voice-coil size 63; woofer size 589; frequency-response limits 561.
- Response models: 657; 531 are modeled from published response limits, 102 use the generic reference path, and 24 use source-backed response-point datasets.
- Source-backed response-point datasets: 24 (measurement 0, manufacturer 24, reputable database 0).
- Embedded polar/CLF/GLL speaker directivity datasets: 0.
- Unsupported information remains unavailable rather than guessed.

## Open gates

- Directivity fidelity: **FAIL**. A pattern specified as 30 dB front-to-rear measured 20.02 dB aimed forward and -21.17 dB aimed backward (omnidirectional baseline -0.01 dB; tolerance +/-3 dB). Reproduce: `npm run validate:directivity`. See DIRECTIVITY-IMPORT.md.

## Scientific/data honesty

- Published bandwidth limits are not presented as measured response curves.
- No laboratory measurement is claimed without measurement provenance.
- Generic/reference speaker models are labeled as modeled.
- Speaker-specific polar/directivity behavior is not fabricated; imported polar data is the user's own. The solver fits an equivalent source to it and reproduces its direction and its low-order shape, but a 30 dB pattern comes back about 20 dB deep on the release-gate grid (see DIRECTIVITY-IMPORT.md and Open gates).
- Physical scatter is not modeled.
- 2.83 V/1 m sensitivity is normalized to the 1 W/1 m DSP reference only when nominal impedance is known.

## Implemented production safeguards

- Cloud Run, Cloud Tasks, Storage lifecycle, and Cloud Monitoring provisioning scripts are included.
- Production deployment requires configured release/cloud resources.
- Windows production release requires a signed Authenticode installer.
- Privacy, Terms, license, and third-party notice assets are included.
- Speaker data gaps and source provenance are generated from the current database.

## External requirements

- Owner/legal approval of the shipped license, Privacy Policy, and Terms is still required.
- GCP/Firebase resources, secrets, notification email, and IAM must be configured in the production project.
- Windows signing credentials/certificate must be configured on the Windows release runner.
- Clean Node 22.23.3+ <23 installation and the complete runtime release gate must be executed in a supported environment.

## Release rule

This source archive must not be described as a fully runtime-verified Windows production release until the external requirements above produce release evidence.
