# Cavity Audio — Privacy Policy

**Last updated: October 4, 2026**

Cavity Audio does not require an account, login, payment, or advertising profile. This policy describes information processed when using the hosted service and the local desktop application.

## Hosted simulations

A hosted simulation may process the inputs required to perform the job, including room dimensions and materials, source and receiver coordinates, speaker selections, project names supplied by the user, job status, and generated simulation artifacts.

Hosted jobs use a temporary capability token. The server stores only a SHA-256 hash of that token. The raw capability token is returned to the browser so the browser can authorize access to that job.

## Operational data

The hosted service may process timestamps, request outcomes, rate-limit events, authentication failures, and other technical/security events needed to operate and protect the service. Application logging is designed to redact tokens, credentials, cookies, authorization headers, private keys, and raw IP addresses.

## Error reports

When the app hits an unexpected error, the page sends a short error report to the service it is running from (the hosted service, or the local server inside the desktop app, in which case the report never leaves your device). A report contains only the error message, the script location, and the stack trace, with URL query strings and fragments removed. It does not contain project data, speaker or room inputs, user-entered text, cookies, or identifiers. Before a report is logged, the server redacts tokens, credentials, IP addresses (IPv4 and IPv6), e-mail addresses, and operating-system account names in file paths. At most five reports are sent per page load.

You can opt out at any time: reporting is disabled when your browser sends Do Not Track or Global Privacy Control, or when you run `localStorage.setItem('cavity.errorReporting', 'off')` in the browser console. The preference is stored per browser profile.

## Retention

Hosted simulation records and generated artifacts are intended to be temporary. The current application configuration uses a 24-hour retention period with an object-storage lifecycle rule as a secondary cleanup safeguard. Local desktop project data remains on the device unless the user exports or shares it.

## Third-party infrastructure

The hosted deployment may use Google Firebase/Firestore, Google Cloud Run, Google Cloud Storage, and Google Cloud Tasks. Their own terms and privacy documentation apply to infrastructure processing they perform.

## Local application

The desktop application is designed to operate locally and does not require cloud credentials or a user account for local simulations.

## User choices

Do not submit personal or confidential information to a hosted simulation unless you are comfortable with the service processing it as described above. Use the local desktop application when local-only processing is required.

## Changes

This notice must be updated before changing the categories of information processed, retention period, or infrastructure providers.

> **Owner/legal review required before public release. This document is informational and is not legal advice.**
