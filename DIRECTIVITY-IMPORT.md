# Importing loudspeaker directivity (polar) data

**Status: experimental. Read "Known limitation" before relying on directional results.**

Cavity Audio lets you import your own polar data for a source (right sidebar, under the speaker). It is stored with the project and sent to the room solver. It is **your data**: it is labelled "imported by you, not verified by Cavity Audio" and is never presented as manufacturer or catalog data. No catalog speaker has built-in directivity data; without an import, a source is **omnidirectional** and the app says so ("Not available: omnidirectional assumed").

## Measured accuracy (release gate: `npm run validate:directivity`)

The solver does not spread the source over an in-phase cluster. It fits an **equivalent source**: a small shell of
monopole nodes carrying complex weights (amplitude *and* phase), solved by regularised least squares at each octave-band
centre. The phase is realised by injecting a 90-degree-advanced copy of the band excitation, so the nodes radiate a real
phase-differenced pattern.

Measured with `npm run validate:directivity` (14 m room, receivers well outside the source shell, pattern specified as
30 dB down at the rear, dataset covering every octave band the solver injects):

| Case | Measured front-minus-rear | Specified |
|---|---|---|
| Omnidirectional baseline | -0.01 dB | 0 dB |
| Aimed forward | +20.02 dB | +30 dB |
| Aimed backward | -21.17 dB | -30 dB |

The polarity and the shape are now correct: aiming the source 180 degrees mirrors the result, and a 14 dB
cardioid pattern is reproduced to within about 1 dB. A 30 dB pattern is reproduced to about 20 dB, so the release gate
still fails its +/-3 dB tolerance and the feature remains **Experimental**. The measured limitation is the *depth* of a
very sharp pattern on an FDTD grid, not its direction.

Why the gap remains: the pattern is fitted at the band centre and the same weights are used across the octave, so the
deepest part of a 30 dB pattern is shallower away from the centre; and octave bands above roughly `c/(3*dx)` (about
830 Hz at the gate's 13.7 cm cells) cannot carry a spatial pattern at all, so those bands keep the earlier
amplitude-cluster approximation. The solver reports how many bands carry directivity, and both limits are stated here
rather than hidden.

`npm run validate:directivity` exits non-zero until the measured result is inside tolerance; it is deliberately not part
of `npm test` and is listed as an open FAIL in the final verdict. Do not treat room results for directional sources as
validated.

## Formats
Supported: **CSV** (long or wide) and **JSON**.

Refused with a clear message, never guessed at:
- `.cf1` / `.cf2` / `.clf` (Common Loudspeaker Format): CLF2 is a binary, access-controlled format (it has a fixed byte signature, which is also detected inside renamed files). Not implemented.
- `.gll`: proprietary. Not implemented.
- `.ulf`, `.sofa`, `.xhn`: not supported yet.
- Any other binary file, ZIP archive, or non-UTF-8 file.

If your tool produced one of the refused formats, export the polar data as CSV or JSON from that tool.

### CSV, long format (one row per direction and frequency)
```
# brand: Example
# model: Example 8
azimuth_deg,elevation_deg,frequency_hz,magnitude_db
0,0,1000,90.0
30,0,1000,89.2
...
```
### CSV, wide format (one row per direction, one column per frequency)
```
azimuth_deg,elevation_deg,250,1000,4000
0,0,90.0,90.0,90.0
30,0,89.8,89.2,87.5
```
- Delimiter: comma, semicolon or tab (auto-detected). With semicolons or tabs a decimal comma is accepted (`89,2`).
- Header aliases: `azimuth|az`, `elevation|el`, `frequency|freq|f`, `magnitude|level|spl|db|gain`. Units such as `_deg`, `(deg)`, `_hz`, `_db` are ignored. Wide-format frequency headers may be `250`, `250 Hz`, `1k`, `4 kHz`.
- `theta` / `phi` / `polar` headers are **refused**: their conventions differ between tools and guessing would rotate the pattern.
- Lines starting with `#` are comments; `# brand:` and `# model:` set labels.
- Every number must be a plain decimal. `NaN`, `Infinity`, hex, formulas and units inside cells are rejected, with the line and column.

### JSON
Either `{"frequencies":[...],"points":{"az,el":[dB per frequency],...},"angularResolution":30}` or `"points":[{"azimuth":0,"elevation":0,"magnitude":[...]}, ...]`. A `.json` file name is always parsed as JSON.

## Conventions
- **Azimuth 0° is the speaker's forward (on-axis) direction**; positive azimuth rotates toward the speaker's local +X axis (+Y forward, +Z up). Azimuth is wrapped to [0°, 360°), so -30° equals 330°, and a repeated 360° row that matches 0° is merged.
- **Elevation** is -90° to +90°, positive up.
- **Magnitudes are normalised per frequency to the on-axis sample** (0°, 0°), so the file's absolute SPL and sensitivity are not read. The file **must contain an on-axis sample**.
- Every direction needs a value at every frequency. Conflicting duplicates (more than 0.1 dB apart) are an error.

## Limits (shared by the importer, project loader and solver API)
At most 16 frequencies, 4096 directions (a 5° full-sphere grid is 2,664; a 3° grid is not accepted), frequencies up to 24000 Hz, and normalised magnitudes between -120 and 30 dB. Files are limited to 5 MB. Everything accepted is re-validated by the same function the solver uses, so an imported file cannot be accepted here and rejected later.

## Which frequencies are used
Data is passed to a simulated octave band (125 Hz to 8 kHz) only when a supplied frequency lies within half an octave of it. Other bands stay omnidirectional. The panel lists the covered and uncovered bands.

## Aiming
Imported data only makes sense if the source can be aimed, so a source can be rotated. Axes are the room's **X (length)** and **Y (width)**, the same as the Source X/Y position fields. **0° faces toward higher Y**; positive angles turn toward lower X (90° faces lower X, 180° lower Y, 270° higher X). **Tilt up** raises the on-axis direction toward the ceiling. Orientation is saved with the project and sent to the solver.

## Fixed in this version
The solver previously applied polar data on the wrong axes: the grid's vertical axis was treated as "forward", so a level speaker's pattern pointed at the ceiling, and the pitch and roll angles were swapped. Both are fixed and covered by analytic tests (`server/solverDirectivity.orientation.test.ts`). The fidelity limitation above is separate and is not fixed.
