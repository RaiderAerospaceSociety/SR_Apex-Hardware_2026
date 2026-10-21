# APEX KiCad library workflow

This library is the source for APEX V2 symbols and footprints. The APEX V1 KiCad project under `/Users/loganrohlfs/Documents/KiCad/APEX-2026` is the visual style reference. Its original `symbols/LR_Sensor.kicad_sym` and `footprints/LR_Sensor.pretty` libraries are still on disk and should be consulted before drawing a new part. Use the exact package option when checking a footprint; confirm what any ordering suffix means from the manufacturer.

For each new part:

1. Save the manufacturer's product page, current datasheet revision, package drawing, and recommended PCB land pattern in a part note. Check whether the manufacturer links a CAD model and compare it with the datasheet.
2. Make a pin table with every pad number, exact datasheet name, electrical role, and any required connection or allowed no-connect state. Check the table against the package pin-one marker.
3. Add one symbol to `symbols/APEX_Symbols.kicad_sym`. Use the V1 conventions: a pale filled rectangle with no visible outline, reference and value at the upper left and right corners, supply pins at the top, grounds at the bottom, serial pins at the left, and interrupts and reserved pins at the right. Use a **50 mil (1.27 mm) base grid** for the body and every pin connection, **150 mil (3.81 mm) between neighboring pins**, and **100 mil (2.54 mm) pin length**. Use a 300 mil gap to separate pin groups. As a general rule, not a requirement: put power on top, ground on the bottom, inputs on the left (for example I2C/SPI), and outputs on the right (for example interrupts and switch nodes). Keep all pin numbers visible. Widen a symbol if full multifunction pin names would overlap. Assign electrical pin types for KiCad ERC using the industry convention: supply and ground pins on ICs are `power_in`. Only a regulator's output is `power_out`, and only power symbols and `PWR_FLAG` drive a net. Large unique symbols such as MCUs keep their original layout. Generic parts (R, C, L, LED, diodes, connectors) use generic symbols and set `LCSC` on each placed part; specific parts carry `LCSC` on both the symbol and the footprint.
4. Import the manufacturer CAD footprint when available, then compare **pad geometry and numbering** to the datasheet. If it is unavailable or unsuitable, draw the manufacturer's recommended land pattern and record the source. Match V1's footprint annotations: reference outside the body on F.SilkS, hidden value on F.Fab, top and bottom silkscreen edges, a pin-one mark, fab outline, and courtyard. Cosmetic changes must not change copper dimensions without a documented reason.
5. Set the symbol's `Footprint` and `Datasheet` properties. Export both assets with `kicad-cli` to confirm they parse and inspect the resulting drawings. Check symbol pin numbers and footprint pad numbers as sets, then check pin-one orientation and all dimensions against the datasheet. Review the footprint in KiCad before sending a board to fabrication.

The project template registers these libraries through `sym-lib-table` and `fp-lib-table`. New projects should copy those two tables with paths adjusted for their directory.

## ADXL375

- Device: ADXL375BCCZ, 14-terminal LGA, Analog Devices package CC-14-1. `-RL` and `-RL7` are reel options for the same package.
- Primary source: [Analog Devices ADXL375 datasheet, Rev. B](https://www.analog.com/media/en/technical-documentation/data-sheets/adxl375.pdf), Table 5 (pin functions), Figure 3 (top-view numbering), Figure 38 (recommended PCB land pattern), and Figure 40 (package outline).
- CAD reference: [Analog Devices product page](https://www.analog.com/en/products/adxl375.html) links the Ultra Librarian symbol, footprint, and 3D model. The V1 ADXL375 symbol and footprint provide the APEX appearance reference.
- Symbol: `APEX_Symbols:ADXL375`; assigned nominal footprint: `APEX_FOOTPRINTS:ADXL375_LGA_CC-14-1_ADI`. The library also contains `-L` and `-M` variants; do not substitute either without checking its pad dimensions.
- The assigned footprint's copper was left as provided in the new library. Its land geometry differs from ADI Figure 38, so compare the two during PCB review before fabrication. The changes here only move the reference text, hide the value on F.Fab, and set the symbol's footprint link.
- Pin 3 is `RESERVED` and may connect to VS or remain open. Pin 11 is `RESERVED` and may connect to ground or remain open. Pin 10 is internally unconnected. Keep pins 3 and 11 separate from the supply and ground pins in the schematic; do not treat the two reserved pins as interchangeable.

The V1 project has an ADXL375 STEP model. It has not yet been copied into the V2 library or verified against the new footprint.

## TPS62825

- Device: TPS62825DMQR, TI DMQ0006A (VSON-HR, 6 pins, 1.5 mm × 1.5 mm, 0.5 mm pitch). `DMQT` is the 250-piece reel of the same package. The `A`, `18`, and `33` variants use the same package and pinout but have different behavior or fixed outputs; check the datasheet before substituting one.
- Primary source: [TI TPS6282x datasheet, SLVSEF9I (March 2024)](https://www.ti.com/lit/ds/symlink/tps62825.pdf), Table 5-1 (pin functions), DMQ0006A package outline, and the example board layout and stencil (TI drawing 4222645/E).
- LCSC / JLCPCB: [C2650334](https://www.lcsc.com/product-detail/DC-DC-Converters_Texas-Instruments_C2650334.html). It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P). Its symbol was redrawn in APEX style, and its footprint was replaced (see below).
- Symbol: `APEX_Symbols:TPS62825`. VIN is on top, GND on the bottom, EN and FB on the left, and SW and PG on the right. Pins are spaced 150 mil apart with 100 mil pin length on the 50 mil grid. PG is open-drain (`open_collector` in KiCad).
- Footprint: `APEX_FOOTPRINTS:TPS62825_DMQ0006A_TI`, drawn from TI's example land pattern. Pads 1–3 are 0.60 × 0.25 mm at x = −0.65 mm. Pads 4–6 are 1.00 × 0.20 mm at x = +0.45 mm. Pitch is 0.5 mm, corners have R0.05, and the paste apertures are 1:1 with the pads, as in TI's stencil example. The DEV-G2-NANO footprint put its pads at the same positions but made them larger (0.70 × 0.35 and 1.10 × 0.30 mm) with a −0.05 mm mask margin. The LCSC/EasyEDA footprint put both pad columns at ±0.58 mm, which does not match TI. Neither was used.
- 3D model: `3dmodels/TPS62825.step`, the LCSC/EasyEDA model for C2650334. It is 1.50 × 1.50 × 0.89 mm with its origin at the package center. The footprint rotates it 90° about Z, which a KiCad render confirmed puts the model's pin-one dot at pad 1. The model's leads were checked against the DMQ0006A outline: three short 0.25 mm leads on the pin 1–3 side and three long 0.20 mm leads on the pin 4–6 side. The model has an LCEDA logo on its top face.

# Parts ported from DEV-G2-NANO (October 2026)

The parts below were brought over from the open-source [DEV-G2-NANO](../../DEV-G2-NANO) project (CERN-OHL-P) and checked against their manufacturer data. The validation scripts used are in `tools/library/`: `check_sym.py` checks pins, grid and spacing; `render_fp.py` renders a footprint with its 3D model; `check_library.py` checks the whole library.

## TPS62086

- Device: TPS62086RLTR, a 3 A synchronous buck converter with a fixed 3.3 V output and a 2.5 V to 6 V input, in TI package RLT0007A (VSON-HR, 7 pins, 2.0 mm × 2.0 mm, no exposed pad). `RLTT` is the 250-piece reel of the same package. TPS62085 (adjustable) and TPS62087 (1.8 V) share the package and pinout. The DEV-G2-NANO brief called this package "SOT-583-8", which is wrong: TPS62086 comes only in RLT.
- Primary source: [TI TPS6208x datasheet, SLVSB70C (January 2021)](https://www.ti.com/lit/ds/symlink/tps62086.pdf), which covers:
  - §5 Device Options (RLT = 3.3 V fixed)
  - Figure 6-1 and Table 6-1 (pinout and pin functions)
  - the RLT0007A package outline, example board layout and example stencil (TI drawing 4220429/A)
- LCSC / JLCPCB: [C2071344](https://www.lcsc.com/product-detail/C2071344.html). LCSC's own datasheet file, `2410121901_Texas-Instruments-TPS62086RLTR_C2071344.pdf`, confirms it, and easyeda2kicad returns the matching VSON-7 2×2 part. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P). The symbol was redrawn in APEX style. The footprint keeps DEV's pad centres, but the copper, mask and paste were reworked to TI's pattern (see below).
- Symbol: `APEX_Symbols:TPS62086`. Its layout follows `TPS62825`: body ±10.16 × ±6.35 mm, 150 mil pin pitch, 100 mil pins on the 50 mil grid.
  - VIN (7) is on top and GND (5) on the bottom, both `power_in`.
  - EN (1) and FB (3) are on the left, both `input`. On this fixed-output part, FB must be tied to VOUT.
  - SW (6, `power_out`), VOS (4, `input`, output sense taken at the output capacitor) and PG (2, `open_collector`, open-drain) are on the right.
  - The DEV symbol had every pin `unspecified` and no properties.
- Footprint: `APEX_FOOTPRINTS:TPS62086_RLT0007A_TI`, drawn from TI's example land pattern and stencil. The origin is the package centre.
  - Pads 1–4: 0.60 × 0.25 mm at x = −0.9 mm, 0.5 mm pitch, non-solder-mask-defined (NSMD). Pad 1 is rectangular and pads 2–4 have rounded ends. Paste is reduced to 0.21 mm wide.
  - Pads 5–7 (GND, SW, VIN): solder-mask defined, per TI, at x = +0.45 mm with 0.6 mm pitch. The copper is 1.64 × 0.44 mm and a −0.07 mm mask margin gives a 1.50 × 0.30 mm opening (0.07 mm metal under the mask all round).
  - Paste on pads 5–7: two 0.65 × 0.30 mm apertures per pad, at x = 0.025 and 0.875 mm (TI stencil, 0.125 mm thick, 85 % coverage).
  - Pads 5–7 carry a local 0.15 mm clearance, because their copper-to-copper gap is 0.16 mm.
  - Comparison with DEV-G2-NANO: the pad centres were the same. Its pads 5–7 used 1.7 × 0.5 mm copper, leaving only a 0.1 mm gap, with paste over the whole pad, and pads 1–4 had a +0.1 mm mask expansion, above TI's 0.07 mm maximum. All three were corrected.
  - The LCSC/EasyEDA footprint uses the mask-opening sizes as copper and is shifted 0.225 mm in x from the package centre, so it was not used. KiCad has no stock footprint for this package.
- 3D model: `3dmodels/TPS62086.step`, the LCSC/EasyEDA model for C2071344, measuring 2.0 × 2.0 × 1.0 mm with its origin at the package centre.
  - Its leads were checked against the RLT0007A outline: four 0.25 mm leads at 0.5 mm pitch and three 0.30 × 1.3 mm leads at 0.6 mm pitch.
  - The footprint rotates it 90° about Z. A KiCad render confirmed that this puts the model's pin-1 dot next to pad 1 and the short leads over pads 1–4.
  - The model has an EasyEDA "VSON-7 / LCEDA" marking on its top face.

### Open issues
1. Pads 5–7 have a local 0.15 mm clearance override, because TI's SMD land pattern leaves 0.16 mm between the copper of VIN, SW and GND, below the 0.2 mm Default net-class clearance. The board minimum is 0.1 mm and JLCPCB can build 0.15 mm. Accept the override, or switch to NSMD 1.5 × 0.3 mm copper, which departs from TI.
2. The 3D model is the EasyEDA one. Its dimensions are correct, but it carries LCEDA branding. Replace it with TI's Ultra Librarian STEP (login required) if wanted.

## LM66200

- Device: TI LM66200, a 1.6 V to 5.5 V, 2.5 A dual ideal diode with automatic switchover. It has integrated N-FETs, an active-low enable (~ON) and an open-drain status output (ST). Orderable part: LM66200DRLR, package DRL0008A (SOT-5X3 / SOT-583, 8 pin, 2.1 x 1.2 mm body, 1.6 mm lead span, 0.5 mm pitch, 0.6 mm max height).
- Primary source: [TI LM66200 datasheet, SLVSG04, Nov 2021](https://www.ti.com/lit/ds/symlink/lm66200.pdf).
  - Section 5: Figure 5-1 and Table 5-1, pin functions.
  - Section 7.3.3: ST is an open drain output and needs a pull-up.
  - Package drawing 4224486/G: Package Outline p.18, Example Board Layout p.19, Example Stencil p.20.
- LCSC: [C3235556](https://www.lcsc.com/product-detail/C3235556.html) (LM66200DRLR). JLCPCB lists the same number, re-confirmed as LM66200DRLR SOT-583 on 2026-10-21. Set on both the symbol and the footprint.
- Origin: DEV-G2-NANO `project_symbols:LM66200` / `project_footprints:LM66200` (CERN-OHL-P).
  - The symbol was redrawn from scratch. The DEV symbol had an empty Value, every pin typed `unspecified`, stacked hidden duplicate pins, and ~ON on a separate unit.
  - The footprint copper was kept and the annotations were restyled.

### Symbol
`APEX_Symbols:LM66200` is a single unit.
- Body: (-7.62, 6.35) to (7.62, -10.16). GND pins 1 and 5 are at x = -1.27 and 2.54 on the bottom edge, 150 mil apart. Their vertical names sit between the ~ON and ST labels without overlapping.
- Pins: 100 mil long on a 150 mil pitch, with a 300 mil gap before the control pins. Everything is on the 50 mil grid.
- Footprint `APEX_FOOTPRINTS:LM66200_DRL0008A_TI`. `ki_fp_filters` is `LM66200_DRL0008A_TI`.

| Pin | Name | Type | Side |
|---|---|---|---|
| 3 | VIN1 | power_in | left |
| 6 | VIN2 | power_in | left |
| 4 | ~{ON} | input | left (after the gap) |
| 2 | VOUT | power_out | right |
| 7 | VOUT | passive | right |
| 8 | ST | open_collector | right (after the gap) |
| 1 | GND | power_in | bottom |
| 5 | GND | power_in | bottom |

- Duplicate pins are listed separately, as ADXL375 does.
- Only VOUT pin 2 is `power_out`. Pin 7 is `passive` so the electrical rules check does not report two power outputs on one net.
- Inputs are on the left and the output is on the right, so the power path reads from left to right.
- Review results:
  - Pins and types were re-checked against Table 5-1 and Section 7.3.3.
  - Gap-fill re-review (2026-10-21) of the merged `APEX_Symbols:LM66200`:
    - `check_sym.py` with the footprint reports no issues. The pin set equals the pad set (1 to 8). All pins are 100 mil long and on the 50 mil grid, with 150 mil pitch and a 300 mil group gap.
    - Datasheet, Description and LCSC are identical on the symbol and the footprint.
    - The SVG export shows no overlapping text.

### Footprint
`APEX_FOOTPRINTS:LM66200_DRL0008A_TI`
- Copper: 8 roundrect pads, 0.67 x 0.3 mm with R0.05 corners, at x = ±0.74 (rows 1.48 mm apart centre to centre) and y = ±0.25 / ±0.75. This is TI's land pattern 4224486/G.
  - Paste is 1:1 with the pads, per the stencil drawing. There is no exposed pad.
  - Pads 1 to 4 run down the left side and 5 to 8 up the right side, with pin 1 at top-left.

| Source | Pad | Row c-c | Verdict |
|---|---|---|---|
| TI 4224486/G | 0.67 x 0.3, R0.05 | 1.48 | reference |
| DEV-G2-NANO | 0.67 x 0.3, rr 0.1667 | 1.48 | identical, kept |
| KiCad `SOT-583-8` | 0.67 x 0.3 | 1.48 | identical |
| EasyEDA C3235556 | 0.28 x 0.68 rect | 1.28 | wrong span, not used |

- Annotations, restyled to APEX:
  - Silk bars at y = ±1.15 (0.15 wide), 0.175 mm clear of copper.
  - Pin-1 dot r0.1 at (-0.95, -1.2), above pad 1: 0.2 mm clear of copper, 0.175 mm clear of the top bar, and inside the courtyard.
    - The interrupted re-run moved the dot here from (-1.35, -0.75), where it sat on the courtyard line. This review re-verified the new position and kept it.
  - Fab body outline 1.2 x 2.1 with a pin-1 chamfer, and `${REFERENCE}` on F.Fab.
  - Courtyard ±1.35 x ±1.4, 0.05 wide.
- `descr` corrected: the DEV footprint pointed to `tps62933.pdf`.
- The footprint Description now matches the symbol. It previously called the part an "OR-ing controller", but the LM66200 has integrated FETs.

### 3D model
`LM66200.step` is the LCSC/EasyEDA STEP for C3235556 (`SOT-583-8_L2.1-W1.2-P0.50-LS1.6-BL`). TI's STEP needs an Ultra Librarian login, so it was not used.
- Size: 2.1 x 1.6 x 0.56 mm, which matches the TI drawing.
- Placement: rotate (0 0 90), offset (0 0 0), linked as `${KIPRJMOD}/../../libraries/3dmodels/LM66200.step`.
- Checked with top and tilted KiCad renders from the fixed `tools/library/render_fp.py` (re-run 2026-10-21): the pin-1 dimple sits over pad 1 at top-left and all 8 leads are centred on their pads.

### Open issues
- The 3D model comes from EasyEDA, not TI. KiCad's stock `SOT-583-8.step` has the same geometry and could replace it.
- VIN1 and VIN2 are `power_in`, so each input net needs a driver (a PWR_FLAG or a regulator output) to pass the electrical rules check. VOUT pin 7 is `passive` on purpose.
- When updating the DEV-G2-NANO schematic, re-check the wiring: the old symbol had stacked hidden pins and ~ON on a separate unit, so the pin positions have changed.

## TPD3S044

- Device: TPD3S044DBVR, a TI USB host-port 1.5 A current-limited load switch with 2-channel D+/D- IEC 61000-4-2 ESD protection. Package: TI DBV0006A (SOT-23-6, 2.9 mm × 1.6 mm, 0.95 mm pitch, 1.45 mm max height). The TPD3S014 (0.5 A, marking SII) uses the same package and pinout.
- Primary source: [TI TPD3S014/TPD3S044 datasheet, SLVSCP4B (Aug 2015)](https://www.ti.com/lit/ds/symlink/tpd3s044.pdf). Relevant sections:
  - Section 5: device comparison (TPD3S044 is 1.5 A, marking SIJ).
  - Section 6, p.3: pin configuration and functions.
  - Section 7.3: VIN range 4.5–5.5 V.
  - DBV0006A package outline, example board layout and stencil (TI drawing 4214840/G, pp.28–30).
- LCSC / JLCPCB: [C2155670](https://www.lcsc.com/product-detail/USB-ICs_Texas-Instruments-TPD3S044DBVR_C2155670.html) (TPD3S044DBVR, JLCPCB extended part). It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: DEV-G2-NANO (CERN-OHL-P) had only a footprint for this part. It had no symbol and was not placed in its schematic. The symbol here is new, drawn from the datasheet, and the footprint was redrawn (see below).
- Symbol: `APEX_Symbols:TPD3S044`. IN (pin 3, `power_in`) is on top and GND (pin 2, `power_in`) on the bottom. EN (pin 1, `input`) is on the left. Below EN, after a 300 mil gap, D1 and D2 (pins 5 and 6) sit on the left as `passive` ESD clamp nodes, since the device never drives them. OUT (pin 4, `power_out`) is on the right. Pins are spaced 150 mil apart with 100 mil pin length on the 50 mil grid. The device has no fault pin.
- Footprint: `APEX_FOOTPRINTS:TPD3S044_DBV0006A_TI`, drawn from TI's example land pattern (4214840/G, p.29).
  - Pads: six 1.1 × 0.6 mm roundrect pads with R0.05 corners. Pads 1–3 are at x = −1.3 mm and pads 4–6 at x = +1.3 mm. Pitch is 0.95 mm, and the paste apertures are 1:1 with the pads, as in TI's stencil example.
  - Silkscreen: body-edge lines clear the copper by 0.225 mm, and the pin-1 dot clears it by 0.3 mm.
  - Courtyard: ±2.1 × ±1.8 mm.
  - Comparison with other sources:
    - The DEV-G2-NANO footprint is identical to KiCad's stock SOT-23-6: 1.325 × 0.6 mm pads at x = ±1.1375 mm, extending 0.275 mm further under the body than TI's pattern. It was replaced; pad numbering and orientation are unchanged.
    - The LCSC/EasyEDA footprint uses smaller pads (0.53 × 1.07 mm at ±1.15 mm) and was not used.
- 3D model: `3dmodels/TPD3S044.step`, the LCSC/EasyEDA generic SOT-23-6 model for C2155670.
  - Size: 2.9 × 1.6 × 1.5 mm body with a 2.8 mm lead span, which matches the DBV0006A nominal dimensions.
  - Alignment: rotation and offset are 0. A KiCad render confirmed that the model's pin-1 dimple sits over pad 1 and the leads are centered on the pads.
  - Cosmetic: the top face carries "SOT-23-6" and LCEDA text.

### Open issues
- The footprint copper differs from DEV-G2-NANO: it follows TI's DBV0006A land pattern instead of the stock IPC SOT-23-6 pattern. Confirm this is acceptable.
- The part is not placed in the DEV-G2-NANO schematic. It was ported only so the library is complete.
- The 3D model is a generic SOT-23-6 with LCEDA markings. TI's own STEP file is behind the Ultra Librarian login.

## BAT54C

- Device: Nexperia BAT54C,215. It is a dual Schottky barrier diode with a common cathode (30 V, 200 mA, VF ≤ 800 mV at 100 mA) in SOT23 (TO-236AB): 3 pins, 2.9 × 1.3 mm body, 1.9 mm pitch.
- Primary source: [Nexperia BAT54C product data sheet (1 July 2022)](https://assets.nexperia.com/documents/data-sheet/BAT54C.pdf). The relevant parts are:
  - Sec. 5, Table 2 (pinning): 1 = A1, 2 = A2, 3 = K1/K2 common cathode.
  - Sec. 4 and Sec. 8 (ratings and characteristics).
  - Fig. 5 (SOT23 outline).
  - Sec. 13, Fig. 6 (reflow soldering footprint `sot023_fr`).
  - A mirror of the datasheet is at https://www.lcsc.com/datasheet/C37704.pdf.
- LCSC / JLCPCB: [C37704](https://www.lcsc.com/product-detail/C37704.html), a JLCPCB "Preferred Extended" part. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: the DEV-G2-NANO project (CERN-OHL-P). That project placed the stock `Diode:BAT54C` symbol with a footprint copied from the KiCad stock SOT-23. Here the symbol was redrawn in APEX/V1 style and the footprint was redrawn to Nexperia's land pattern.
- Symbol: `APEX_Symbols:BAT54C`, Ref `D`.
  - Drawn like the V1 `DIO_MBR0540T3G` Schottky glyph: two Schottky diodes facing each other, cathodes joined at a junction dot.
  - Pins: A1 (pin 1) on the left, A2 (pin 2) on the right, K (pin 3) at the bottom.
  - All pins are `passive` and 100 mil long, on the 50 mil grid. Pin names are hidden and pin numbers are shown.
  - `ki_fp_filters` is `BAT54C_SOT23*`.
- Footprint: `APEX_FOOTPRINTS:BAT54C_SOT23_Nexperia`, built to Nexperia Fig. 6.
  - Pads: three 0.7 × 0.6 mm lands (0.7 along the row axis), R 15 %. Pad 1 is at (−1.0, −0.95), pad 2 at (−1.0, +0.95) and pad 3 at (+1.0, 0).
  - Spacing: 1.9 mm pitch, 2.0 mm between pad rows.
  - Paste is 0.6 × 0.5 mm (`solder_paste_margin −0.05`), as in Fig. 6.
  - Silk: top and bottom edges plus right-side stubs, with a pin-1 dot. Every silk element is at least 0.22 mm from copper.
  - Fab: body outline with a pin-1 chamfer. Courtyard: ±1.6 × ±1.75 mm.
  - Deviation from DEV-G2-NANO: its footprint (the KiCad stock IPC SOT-23) uses 1.475 mm-long pads at x = ±0.9375 mm, which reach 0.45 mm under the body.
  - Deviation from LCSC/EasyEDA: that footprint uses 1.07 mm pads at x = ±1.24 mm and is rotated 180°.
  - Neither of those was used.
- 3D model: `3dmodels/BAT54C.step`, a byte-identical copy of the KiCad stock `Package_TO_SOT_SMD.3dshapes/SOT-23.step` (CC-BY-SA 4.0 with the design exception).
  - The footprint applies offset 0 and rotation 0.
  - Its 2.9 × 1.3 mm body matches Nexperia Fig. 5.
  - A KiCad top render confirmed that the model's pin-1 dot is next to pad 1 and that all three leads land on their pads.

### Open issues
- The Nexperia reflow lands are 0.7 mm long. The KiCad/IPC stock pads are 1.475 mm long. This footprint follows the datasheet; switch to the stock pads if you want larger toe fillets or easier hand rework.
- No BAT54C is a JLCPCB Basic part. C37704 is Preferred Extended, so it should not add a loading fee for Economic assembly.
  - The cheaper same-pinout alternative is C2135 (JSCJ), which has a higher VF: 1 V at 100 mA.
  - Other alternatives: C14308 (onsemi BAT54CLT1G), C134405 (Diodes BAT54C-7-F) and C49991 (LRC LBAT54CLT1G).
- The Datasheet URL `https://assets.nexperia.com/documents/data-sheet/BAT54C.pdf` follows Nexperia's standard path, but their CDN returns HTTP 403 to scripted requests, so it could not be fetched to confirm. The LCSC mirror above does work.

## LSM6DSV

- Device: ST LSM6DSV (orderable LSM6DSVTR, tape and reel). It is a 6-axis IMU with an accelerometer and a gyroscope, in a 14-lead LGA-14L package (2.5 x 3.0 x 0.86 mm max). This is the plain LSM6DSV used by DEV-G2-NANO (`user-io.kicad_sch`). It is not the LSM6DSV16X or LSM6DSV32X.
- Primary source: [ST LSM6DSV datasheet DS13476 Rev 5](https://www.st.com/resource/en/datasheet/lsm6dsv.pdf). Sections used:
  - Figure 4: pin connections, bottom view.
  - Section 3.1, Figure 5 and Table 2: connection modes 1/2/3 and pin description.
  - Table 9: serial interface pins. CS low selects SPI; CS high selects I2C/I3C.
  - Tables 17 and 18: I2C master and aux SPI pins.
  - Section 19.1, Figure 31: LGA-14L package outline.
  - Land size follows ST TN0018 (LGA soldering guidance).
- LCSC: [C5267399](https://www.lcsc.com/product-detail/C5267399.html), LSM6DSVTR. Confirmed from the LCSC/EasyEDA part data. The same number is set on both the symbol and the footprint.
- Origin: DEV-G2-NANO `project_symbols:LSM6DSV` / `project_footprints:LSM6DSV` (CERN-OHL-P). The custom 3D model was not available.
- Symbol: `APEX_Symbols:LSM6DSV`, restyled to match the APEX sensor symbols (ICM-45686, BMP581, ADXL375).
  - Body 25.4 x 27.94 mm, pins 100 mil long at a 150 mil pitch.
  - Top: VDD (8) and VDDIO (5). Bottom: GND (6) and GND (7), listed separately.
  - Left (host interface): `~{CS}` (12), SCL (13, clock input), SDA (14, bidirectional), SDO/SA0 (1, bidirectional).
  - Right: INT1 (4) is an output. INT2 (9) is bidirectional because it doubles as the DEN input.
  - Right, after a 300 mil gap (aux/OIS group): OCS_Aux (10) is an input. SCx (3), SDx (2) and SDO_Aux (11) are bidirectional. In mode 1 these pins are tied to VDDIO or GND, so they are not typed as outputs.
  - Footprint `APEX_FOOTPRINTS:LSM6DSV_LGA-14L_ST`; `ki_fp_filters` `LSM6DSV*LGA*`.
- Footprint: `APEX_FOOTPRINTS:LSM6DSV_LGA-14L_ST`.
  - Pad centers come from ST Figure 31: 0.5 mm pitch, and each package pad's outer edge is 0.1 mm inside the body edge.
    - Side pad centers: x = ±1.1625, y = ±0.25 and ±0.75.
    - Top/bottom pad centers: y = ±0.9125, x = 0 and ±0.5.
  - Land size is the package pad (0.475 x 0.25) plus 0.1 mm per TN0018, so 0.575 x 0.35, as roundrect with rratio 0.2.
  - Pin numbering is Figure 4 (bottom view) mirrored to top view: pin 1 at top-left, pins 1-4 down the left side, 5-7 along the bottom, 8-11 up the right side, and 12-14 along the top from right to left.
  - Silk: top and bottom lines are 0.175 mm clear of copper. The pin-1 dot is 0.2 mm from pad 1.
  - Courtyard: ±1.9 x ±1.55, which encloses the pin-1 dot.
  - Comparison with other sources:
    - DEV-G2-NANO: 0.6 x 0.3 lands, with centers 0.0125 mm inward of ST. Not kept.
    - KiCad stock `LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y`: same centers, with lands 0.05 mm longer.
    - EasyEDA: pads pushed about 0.1 mm outward. Rejected.
- 3D model: `LSM6DSV.step`, the LCSC/EasyEDA STEP for C5267399 (ST offers no directly downloadable STEP).
  - It is placed with offset 0 and rotation 0.
  - Measured body is 3.0 x 2.5 mm, and pad geometry matches Figure 31.
  - Pin 1 alignment: the model's chamfered pad 1 and its top pin-1 dot are at top-left. In the KiCad 3D render the top dot lines up with the silk pin-1 dot.

### Open issues

- The pin names follow the ST datasheet: SDA, SDO/SA0, VDDIO, OCS_Aux and `~{CS}`. Pin types are now real types; the DEV symbol used `unspecified`, with names such as SDI/SDO/VDD_IO/OCS_AUX. DEV schematic nets still connect, because KiCad matches by pin number. Re-run ERC after updating the symbol from the library.
- The 3D model is 0.921 mm tall; the datasheet gives 0.86 max. Its top surface shows "LGA14" and an LCEDA/EasyEDA logo. Both are cosmetic.
- Paste is 1:1 with the lands at 0.5 mm pitch. Review the stencil apertures if paste volume turns out to be a problem.
- The footprint Description and descr give a height of 0.83 mm (typical). The package maximum is 0.86 mm.

## LIS2MDL

- **Device:** STMicroelectronics LIS2MDL, an ultra-low-power 3-axis digital magnetometer (±50 gauss, I2C/SPI). The package is LGA-12, 2.0 x 2.0 x 0.7 mm, pitch 0.5 mm. The orderable MPN is LIS2MDLTR (tape and reel).
- **Primary source:** [ST LIS2MDL datasheet, DocID030621 Rev 5](https://www.st.com/resource/en/datasheet/lis2mdl.pdf). st.com was unreachable, so the text was read from the identical 41-page copy on the Mikroe mirror. References used:
  - Section 1.2, Figure 2 (pin connections, bottom view) and Table 2 (pin description), p.7–8.
  - Figure 5 (electrical connections, C1 = 220 nF), p.19.
  - Section 5.1 (land pattern deferred to ST TN0018), p.21.
  - Figure 9 (LGA-12 package outline), p.37.
- **LCSC:** [C919695](https://www.lcsc.com/product-detail/C919695.html) (LIS2MDLTR, also on [JLCPCB](https://jlcpcb.com/partdetail/Stmicroelectronics-LIS2MDLTR/C919695) as an extended part). The same number is set on both the symbol and the footprint.
- **Origin:** ported from DEV-G2-NANO (`project_symbols:LIS2MDL` / `project_footprints:LIS2MDL`, CERN-OHL-P). The symbol was restyled and the footprint rebuilt. DEV-G2-NANO's 3D model was not available.

### Symbol (`APEX_Symbols:LIS2MDL`)
- Footprint `APEX_FOOTPRINTS:LIS2MDL_LGA-12_ST`. Datasheet, Description and LCSC are set, and are identical on the symbol and the footprint (LCSC C919695 re-verified as LIS2MDLTR, LGA-12). ki_fp_filters is `LIS2MDL_LGA-12_ST* LGA*2x2mm*P0.5mm*`.
- **Layout:**
  - Top: VDD (9) and VDD_IO (10), both `power_in`.
  - Bottom: GND (6) and GND (8), `power_in`, listed separately rather than stacked, as in BMP581 and ADXL375. NC (2, 11, 12) form a separate group typed `no_connect`.
  - Left: SCL/SPC (1, `input`), SDA/SDI/SDO (4, `bidirectional`), CS (3, `input`).
  - Right: INT/DRDY/SDO (7, `output`, push-pull), then C1 (5, `passive`) in its own group. C1 takes a 220 nF low-ESR capacitor to GND placed next to pins 5 and 6.
- **Style:** body 1000 x 900 mil. Pins are 100 mil long at 150 mil pitch, with 300 mil gaps between groups, all on the 50 mil grid. `check_sym.py` reports no issues, and the 12 pins match the 12 pads.
- **Names:** taken from Table 2. Vdd/Vdd_IO are uppercased to VDD/VDD_IO to follow the APEX convention. CS is not overbarred because the datasheet calls it "CS" (1 = I2C, 0 = SPI).
- **Changes from DEV-G2-NANO:** that symbol had every pin typed `unspecified`, pins 200 mil long, GND pin 8 hidden and stacked on pin 6, and pins 2, 11 and 12 missing.

### Footprint (`LIS2MDL_LGA-12_ST`)
- **Pads:** 12 rectangular SMD pads, numbered counter-clockwise in the top view (Fig. 9 bottom view mirrored):
  - 1–4 down the left side at x = -0.7625, y = -0.75 / -0.25 / 0.25 / 0.75.
  - 5 and 6 along the bottom at y = +0.7625, x = -0.25 / +0.25.
  - 7–10 up the right side.
  - 11 (x = +0.25) and 12 (x = -0.25) along the top.
- **Land size:** side pads are 0.375 x 0.35 mm and top/bottom pads are 0.35 x 0.375 mm. Each is the 0.275 x 0.25 mm terminal plus 0.1 mm, following ST TN0018 (applies because terminal spacing is over 200 µm). The gap between pads is 0.15 mm.
- **Comparison:**
  - The KiCad stock `Package_LGA:LGA-12_2x2mm_P0.5mm` has identical copper.
  - DEV-G2-NANO used the same pad sizes, but its centers were at ±0.75 instead of ±0.7625 (12.5 µm further in). Its pads 2, 11 and 12 had no numbers; they are numbered now.
  - The EasyEDA footprint was rejected: it uses 0.30 x 0.30 lands with no TN0018 oversize, and its numbering is rotated 90°.
- **Annotations:**
  - Silkscreen: an outline at ±1.2 mm, width 0.15, 0.175 mm clear of copper. The pin-1 dot is at (-1.5, -0.75), 0.45 mm from pad 1.
  - Fab: the 2.0 x 2.0 mm body with a pin-1 chamfer, plus `${REFERENCE}`.
  - Courtyard: ±1.3 mm, width 0.05, 0.35 mm from the pads.
  - REF** is on F.SilkS and Value is hidden on F.Fab. Datasheet, Description and LCSC are hidden properties.

### 3D model (`LIS2MDL.step`)
- **Source:** the LCSC/EasyEDA STEP for C919695 (`VLGA-12_L2.0-W2.0-P0.50-BL`, from `easyeda2kicad`). ST's STEP could not be downloaded. The KiCad stock LGA-12 model was rejected because it is 1.045 mm tall.
- **Link:** `${KIPRJMOD}/../../libraries/3dmodels/LIS2MDL.step`, with no offset and no rotation.
- **Size:** the body is 2.0 x 2.0 mm and stands 0.71 mm above the board.
- **Alignment:** a kicad-cli 3D render (top and tilted) shows the model's pin-1 dot at the top-left, on pad 1, matching the F.Fab chamfer and the silkscreen dot. The review pass re-checked all 12 pins against Table 2 and the copper against the KiCad stock LGA-12 2x2 footprint (identical).

### Open issues
- **3D model below the board.** It is the EasyEDA one: it has an "LCEDA EasyEDA" logo on top, and its terminal and substrate solids extend from z = 0 down to z = -0.24, hidden inside the board. The visible height above the board is correct, so this only matters visually. Replace it with ST's STEP if one becomes available.
- **TN0018 not read directly.** The land rule comes from secondary sources. It exactly matches the KiCad stock LGA-12 2x2 footprint.
- **NC pin types.** Pins 2, 11 and 12 are typed `no_connect`. The datasheet allows tying them to Vdd, Vdd_IO or GND; if a board does that, change them to `passive` to avoid ERC errors.
- **LCSC stock.** Stock for C919695 is inconsistent between sources: LCSC showed about 4k, EasyEDA showed 0. Confirm availability before ordering.
- **Pin placement differs from other sensors.** Power is on top and ground on the bottom, following the style rule. The existing APEX sensors (BMP581, ADXL375) put all pins on the sides. Decide whether sensors should be consistent with each other.
- **Silkscreen dot outside the courtyard.** The pin-1 dot sits slightly outside the courtyard, the same as in the TPS62825 reference.

## MIMXRT1171DVMAB

- **Device/package:** NXP i.MX RT1171 crossover MCU (Cortex-M7 at 1 GHz, 2 MB SRAM), consumer grade.
  - Package: 289-ball MAPBGA (LFBGA289), NXP SOT1534-4 / case 98ASA01216D.
  - 14 x 14 mm, 1.37 mm nominal height, 17 x 17 balls at 0.8 mm pitch.
  - Rows A..U, skipping I, O and Q.
- **Primary sources:**
  - NXP IMXRT1170BCEC data sheet, Rev. 1, 05/2025. The cover lists MIMXRT1171DVMAB. Ball assignments come from Section 6.1.2, Table 112 (supplies) and Table 113 (functional). LDO output rails are in Section 4.2.3, Tables 19–21.
    - Link: https://www.nxp.com/docs/en/data-sheet/IMXRT1170BCEC.pdf
  - NXP "SOT1534-4 Package information" (8 Oct 2019):
    - Fig. 1 / Table 1: outline.
    - Fig. 2: solder mask opening, 289X dia 0.44.
    - Fig. 3: solderable pad, 289X dia 0.34.
- **LCSC:** [C44999792](https://jlcpcb.com/partdetail/C44999792). JLCPCB lists it as MIMXRT1171DVMAB, NXP, BGA289; re-checked 2026-10-21.
  - Alternative: C1020278 is MIMXRT1171DVMAA, the older silicon revision in the same package.
- **Origin:** DEV-G2-NANO (`project_lib`), CERN-OHL-P.
- **Symbol (`MIMXRT1171DVMAB`):**
  - Copied from DEV-G2-NANO as is (large MCU, not restyled). It has 4 units and 289 pins; duplicate supply balls are stacked as hidden pins.
  - Every one of the 289 ball/name pairs was checked by script against BCEC Tables 112/113: 0 mismatches.
  - Its pin set equals the footprint's pad set.
  - `check_sym.py` reports 5.08 mm pins and non-150 mil spacing. These are expected, because the symbol was not restyled.
  - Every pin is currently `unspecified`. Supply pin types should be corrected (see Open issues).
- **Footprint (`MIMXRT1171DVMAB_BGA`):**
  - Copper is unchanged from the DEV-G2-NANO / commit 2d5b2e4 version: 289 pads, identical positions, sizes and numbering, verified by script.
    - Round SMD pads, dia 0.34, with `solder_mask_margin` 0.05, which gives a 0.44 NSMD opening. This matches NXP SOT1534-4 Fig. 2/3 exactly.
    - Ball A1 is at (-6.4, -6.4) and U17 at (6.4, 6.4). All pads are on the 0.8 grid with the correct row letter and column.
  - EasyEDA C1020278 has the same positions but 0.32 mm pads with no NSMD margin, so it was not used.
  - Graphics:
    - F.SilkS outline at ±7.2 (≥0.58 mm from copper), with a pin-1 dot at (-7.6, -7.6).
    - F.Fab body at ±7.0 with a 1 mm A1 chamfer.
    - F.CrtYd at ±7.35, width 0.05.
    - REF** on silk, Value hidden on F.Fab, `${REFERENCE}` on F.Fab.
  - Properties: Datasheet = BCEC URL, Description, LCSC C44999792.
- **3D model:** `libraries/3dmodels/MIMXRT1171DVMAB.step`.
  - Source: the EasyEDA/LCSC STEP for C1020278 ("MAPBGA-289_L14.0-W14.0-R17-C17-P0.80-TL.step"). NXP does not publish a STEP without a login.
  - Extents, measured from the STEP points: X/Y -7.0..7.0 (14.0 mm, matches the body); Z -0.57..0.76 (1.33 mm, against 1.37 mm nominal).
  - Placement: offset (0, 0, 0.57), rotation 0. Referenced as `${KIPRJMOD}/../../libraries/3dmodels/MIMXRT1171DVMAB.step`.
  - Alignment: the `render_fp.py` top and tilt renders (2026-10-21) show the body filling the silk outline. The A1 dimple is top-left, over pad A1 and the silk pin-1 dot, and the balls sit on the board.

### Open issues
- **Symbol properties in APEX_Symbols.kicad_sym** (the orchestrator must apply these; this unit did not edit the file):
  - LCSC: `C44999798` is MIMXRT1176DVMAB, the wrong part. Change it to `C44999792`.
  - Datasheet: change `IMXRT1170BIEC.pdf` (industrial grade) to `https://www.nxp.com/docs/en/data-sheet/IMXRT1170BCEC.pdf`.
  - Description: change "DEV-G2-NANO Microcontroller" to the footprint description.
- **Pin electrical types:** every pin is `unspecified`, so ERC cannot check the supplies. The proposed retype is in the orchestrator actions:
  - Visible supply and ground pins become `power_in`.
  - Visible pins of on-chip regulator outputs become `power_out`.
  - Hidden stacked duplicates become `passive`. This avoids power_out/power_out conflicts and any implicit hidden-power-pin nets.
  - The schematic then needs PWR_FLAGs on rails that only regulators or passives drive.
  - GPIO and other signal pins stay `unspecified` (optional cleanup).
- **Symbol text overlap:** the Reference ("U1", at 18.796, 4.572) and Value (at 18.796, 2.032), size 1.27, overlap the top pin numbers of unit A. They are cosmetic, but should move above the pin row.
- **Source design** (DEV-G2-NANO, for the user's information): NVCC_SNVS is tied to VDD_SNVS_ANA, and VDD_MIPI_1P0/1P8 are left mostly unconnected. Review this when reusing the circuit.
- **3D model:** EasyEDA's generic MAPBGA-289 (1.33 mm tall), not an NXP model.

## MKL26Z128VFM4

- Device: NXP (Freescale) Kinetis KL26 MKL26Z128VFM4. It is an Arm Cortex-M0+ running at 48 MHz, with 128 KB flash, 16 KB SRAM and USB FS OTG, rated −40 to 105 °C. The package is a 32-pin QFN (FM suffix), 5 × 5 × 0.9 mm with 0.5 mm pitch and an exposed pad, per NXP drawing 98ASA00473D Rev B (SOT617-17). DEV-G2-NANO uses it as the DAPLink debug-probe MCU.
- Primary source: [NXP KL26 Sub-Family data sheet, KL26P64M48SF5 Rev 5 (08/2014)](https://www.nxp.com/docs/en/data-sheet/KL26P64M48SF5.pdf), §5.1 "KL26 Signal Multiplexing and Pin Assignments" (32 QFN column, pp. 48–51) and §4.1 "Obtaining package dimensions". The package outline is [98ASA00473D](https://cache.nxp.com/docs/en/package-information/98ASA00473D.pdf) (Fig. 1 outline, Fig. 2 Detail G, Fig. 3 notes). nxp.com blocks scripted downloads, so the pin table was checked against the identical PJRC mirror of the data sheet.
- LCSC / JLCPCB: [C1338088](https://www.lcsc.com/product-detail/NXP-MCU_NXP-Semicon-MKL26Z128VFM4_C1338088.html). This is the exact MPN in QFN-32-EP (5x5) and an extended JLCPCB part. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P), `project_symbols:MKL26Z128VFM4` and `project_footprints:MKL26Z128VFM4`.
- Symbol: `APEX_Symbols:MKL26Z128VFM4`. This large MCU symbol was copied **as is, not restyled**. It keeps DEV-G2-NANO's 100 mil pins, 100 mil pitch and DAPLink net-hint text (SWD, UART, BOOT_MODE, RESET).
  - It has two units: "Main Symbol" holds the used pins plus power, and "Unused Pins" holds the pins DAPLink reserves or leaves unused.
  - Only these properties were changed: Footprint, Datasheet, Description, LCSC, `ki_keywords`, and `ki_fp_filters` (now `MKL26Z128VFM4_QFN32_NXP`).
  - All 32 pins plus EPAD (33) match the data sheet's 32 QFN column.
  - Electrical types: VDD, VDDA, VREGIN, VSS, VSSA and EPAD are `power_in`; VOUT33, the output of the internal USB regulator, is `power_out`; all GPIO is `bidirectional`.
  - Pin 16 (the second VSS) is a hidden `passive` pin stacked on pin 2.
- Footprint: `APEX_FOOTPRINTS:MKL26Z128VFM4_QFN32_NXP`.
  - NXP publishes no recommended land pattern for 98ASA00473D, so the copper was checked against the package dimensions instead: b = 0.18–0.30, L = 0.30–0.50, and EP 3.50–3.70 (3.60 nominal).
  - The copper is identical to DEV-G2-NANO's, which is the KiCad stock `QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm`. The 32 signal pads are 0.875 × 0.25 mm roundrect at ±2.4375 mm. The EP is a 3.45 × 3.45 mm land with 9 paste squares of 0.83 mm (about 52 % coverage). The EP-to-pad gap is 0.275 mm.
  - Pads are numbered counter-clockwise from the top of the left side, and pad 33 is the EP.
  - The LCSC/EasyEDA footprint was rejected. Its pads sit 0.1 mm further out, its EP has 100 % paste, and it is drawn rotated 90°.
  - Silkscreen is corner brackets with 0.2 mm clearance to copper, plus a pin-1 dot at (−3, −3). The courtyard is ±3.15 mm.
- 3D model: `3dmodels/MKL26Z128.step`, the LCSC/EasyEDA model for C1338088. NXP publishes no STEP. The model is 5.0 × 5.0 × 0.91 mm with a 3.6 mm EP, which matches the drawing.
  - The footprint rotates it 90° about Z with no offset. A KiCad 3D render confirmed that the model's pin-1 dot sits at pad 1 and its leads land on the pads.
  - The model has an LCEDA logo on its top face.

### Open issues
- The pin-33 (EPAD) net is not stated in the data sheet text. The symbol keeps DEV-G2-NANO's `power_in` EPAD, which is assumed to tie to VSS/GND.
- Pins 20, 22 and 24–27 keep the shorter DEV-G2-NANO names, for example `PTC1` instead of the data sheet's `PTC1/LLWU_P6/RTC_CLKIN`. They were left unchanged because the symbol is not being restyled.
- The symbol does not follow APEX style (100 mil pins and pitch), which the spec allows for large MCUs. Unit 2's Reference and Value text sits far from its pins, as in the original.
- NXP gives no land pattern, so the footprint was verified only against package dimensions. The EP land (3.45 mm) is slightly smaller than the package EP minimum (3.50 mm), which is normal practice.
- The EP has no thermal vias, as on DEV-G2-NANO. Add vias on the board if the EP should tie to the ground plane.
- The 3D model carries an EasyEDA/LCEDA logo. JLCPCB stock for C1338088 was not checked.

## RTMC-G2-4IQ48

- **Device:** Theta Machines RTMC-G2 real-time closed-loop motion controller IC (4 motor A/B output channels, 4 quadrature encoder A/B inputs with shared Z/limit-switch inputs, SPI host interface, crystal oscillator, on-chip buck for VDD_CORE). Package: LQFP-48, 7x7 mm body, 0.5 mm pitch, no exposed pad (JEDEC MS-026 BBC).
- **Primary source:** none public. Theta Machines publishes no datasheet, pinout or package drawing (thetamachines.com and github.com/theta-machines/theta-docs checked; theta-docs covers only the ETH4K boards and the RTMC-C-ETH500P36 API). Pin names and types come from the DEV-G2-NANO symbol, checked against the DEV-G2-NANO netlist connectivity. Datasheet property on symbol and footprint points to https://www.thetamachines.com/.
- **LCSC:** none. Not stocked at LCSC/JLCPCB; the part is sold by Theta Machines. `LCSC` is present but empty on both symbol and footprint.
- **Origin:** DEV-G2-NANO `project_symbols:RTMC-G2-4IQ48` and `project_footprints:RTMC-G2-4IQ48` (Theta Machines, CERN-OHL-P).
- **Symbol:** copied as-is (large/unique-symbol rule): 200 mil pins, 100 mil pitch, six GND and six VDD pins stacked (pins 6/7 visible, the rest hidden power_in). Changes vs source: Reference/Value moved to the upper-left/upper-right above the body at size 1.524; Footprint `APEX_FOOTPRINTS:RTMC-G2-4IQ48_LQFP-48_ThetaMachines`, Datasheet, Description, empty LCSC, `ki_keywords` and `ki_fp_filters` (`RTMC-G2-4IQ48*`) added; pin 48 `RESET_N` changed from `unspecified` to `input` (driven by an MCU GPIO with pull-up). `BUCK_SW` (42) is power_out; `BUCK_IN` (41), `BUCK_GND` (43), `VDD_CORE` (44) are power_in; `FAULT_OUT` (23) is open_collector.
- **Footprint:** `RTMC-G2-4IQ48_LQFP-48_ThetaMachines`. Copper kept from DEV-G2-NANO (pad-by-pad identical: 48 rect pads 1.5 x 0.3 mm, 0.5 mm pitch, centres at ±4.20 mm; DEV wrote them as 0.3 x 1.5 rotated, same geometry). Numbering CCW from pin 1 top-left: 1-12 left, 13-24 bottom, 25-36 right, 37-48 top. No manufacturer land pattern exists; compared with KiCad stock `Package_QFP:LQFP-48_7x7mm_P0.5mm` (1.475 x 0.3 roundrect at ±4.1625, < 0.05 mm per edge difference) and JEDEC MS-026 lead geometry (~0.45 mm toe, ~0.3 mm heel). APEX annotations added: silk corner ticks and pin-1 dot (≥0.185 mm from copper), F.Fab 7x7 body with 1 mm pin-1 chamfer, `${REFERENCE}` on F.Fab, stepped courtyard (pads +0.25 at ±5.2, body +0.25 at ±3.75).
- **3D model:** `LQFP-48_7x7mm_P0.5mm.step`, byte-identical copy of the KiCad stock `Package_QFP.3dshapes` model (the one DEV referenced), at `${KIPRJMOD}/../../libraries/3dmodels/LQFP-48_7x7mm_P0.5mm.step`, offset 0, rotation 0. render_fp.py top/tilt views: pin-1 dimple at the top-left over pad 1 and the silk dot, leads on the pads.
- **Validation:** check_sym: pin set == pad set (48/48). Its pin-length and pitch warnings are expected (symbol not restyled). Symbol and footprint SVGs inspected.

### Open issues
- No public datasheet: confirm pin functions and types with Theta Machines, in particular the M*_A/B output function, `UPDATE` (pin 13) as bidirectional, and `INTER` (pin 47) as push-pull output (change to open_collector if it is open-drain).
- Active-low names `RESET_N` and `CS_N` kept from the source rather than renamed to `~{RESET}`/`~{CS}`; rename if strict APEX naming is wanted.
- `BUCK_GND` (43) is a separate visible pin and must be tied to GND. `VDD_CORE` (power_in) is fed from `BUCK_SW` through an inductor, so ERC needs a PWR_FLAG on the VDD_CORE net.
- No manufacturer land pattern or package drawing; copper is generic LQFP-48 7x7 from DEV-G2-NANO. Re-check if Theta Machines publishes a drawing.
- No LCSC part: the IC must be bought from Theta Machines and consigned to the assembler or hand-placed.
- On DEV-G2-NANO only axes 1-3 are wired; M4/E4 and all Z/LS pins are unconnected (add no-connect flags in schematics that do the same).

## MAYA-W166

- Device: u-blox MAYA-W166-00B, a host-based Wi-Fi 4 (802.11a/b/g/n, dual-band) and Bluetooth 5.2 module built on the NXP IW416. It has an internal PCB antenna and comes in an 86-pin LGA, 10.4 × 14.3 × 1.8 mm (DS Sec. 1 Table 1), on a 1.10 mm grid. The host interfaces are SDIO 3.0 for Wi-Fi and a 4-wire UART for Bluetooth. MAYA-W160, MAYA-W161 and MAYA-W166-01B have the same pinout and copper, but they have antenna pins or U.FL connectors and no internal antenna.
- Primary sources:
  - [u-blox MAYA-W1 data sheet UBX-21006380 R09](https://content.u-blox.com/sites/default/files/documents/MAYA-W1_DataSheet_UBX-21006380.pdf): Sec. 3.1 Fig. 13 and Table 16 (pin assignment, top view), Sec. 2.1 Tables 3–4 (CONFIG strap pins), Sec. 6.1 Fig. 14 and Table 30 (footprint and RF keep-out), Sec. 6.2.1 Fig. 15 (mechanical).
  - [MAYA-W1 system integration manual UBX-21010495 R09](https://content.u-blox.com/sites/default/files/documents/MAYA-W1_SIM_UBX-21010495.pdf): sec. 3.7 (NSMD pads, stencil equal to copper) and sec. 2.2.3 (antenna placement).
- LCSC / JLCPCB: [C5441012](https://www.lcsc.com/product-detail/C5441012.html). This is an exact MPN match for MAYA-W166-00B; LCSC lists the package as "LGA-76", which is wrong because the part has 86 pins. It is an extended part and was out of stock when checked in 2026-10. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P). The symbol was copied without restyling because it is a module. The footprint copper was kept, and the rest of the footprint was rebuilt.
- Symbol: `APEX_Symbols:MAYA-W166-00B` has two units. The geometry, pin names and unit B annotation text are unchanged from DEV-G2-NANO: 5.08 mm pins on a 2.54 mm pitch with 1.27 mm text, so the symbol does not follow APEX style. All pins are on the 50 mil grid.
  - Unit A (main): power pins 1V8, VIO, VIO_SD and 3V3 are on top, and GND is on the bottom. The left side has the SDIO, WLAN control, UART, BT control, PDn and CONFIG[1:0] pins.
  - Unit B: pins that are unused on the -00B variant. RF_ANT0/1 and RF_CNTL3_P are absent or must be left floating on -00B. Also on unit B are PCM/I2S, WCI-2 coexistence, GPIO[2]/JTAG_TDI and SLP_CLK_IN.
  - The source had every pin as `passive`. Pin types now follow the Table 16 I/O column:
    - Supplies and GND: `power_in`.
    - SD_CLK, UART_SIN, UART_CTSn, PDn, WCI_SIN and SLP_CLK_IN: `input`.
    - UART_SOUT, UART_RTSn and WCI_SOUT: `output`.
    - The remaining signal pins are I/O in the data sheet and are `bidirectional`.
    - RF_ANT0/1: `passive`.
  - 22 GND pins and 2 3V3 pins are stacked. Only the visible pin of each stack (A1 GND, A7 3V3) is `power_in`. The hidden duplicates are `passive`, so they don't create implicit global nets.
  - The 28 NC/"Reserved" pads have no symbol pins, as in the source and per Table 16: B9, C1, C2, C4, C5, C8, C9, D1, D2, D7, D9, E1, E2, F1, F2, G1–G5, H1–H3, J1, J2, J4, J5 and K5.
  - Pin names match the data sheet (`PDn`, `UART_CTSn`, `UART_RTSn`), not `~{}` notation.
  - Every pin number, name and type was re-checked against Table 16.
- Footprint: `APEX_FOOTPRINTS:MAYA-W166_LGA86_u-blox`.
  - Copper: 86 square 0.60 × 0.60 mm pads (Table 30), on a 1.10 mm pitch.
    - Rows A–M follow Fig. 13/14 (top view). A1 is bottom-right at (4.4, 6.6), and the antenna end (rows L/M) is toward −y.
    - Row L pads sit at y = −4.8 and row M at y = −6.3. Pins 4/5 of rows E–J sit at x = ±0.55.
    - The masks are NSMD (board default expansion), with paste 1:1, per SIM sec. 3.7.
    - All 86 pad positions were checked numerically against Fig. 14. The DEV-G2-NANO copper was identical and was kept. The LCSC/EasyEDA footprint agrees once rotated 90°. KiCad's stock library has no MAYA footprint.
  - Added an RF keep-out rule area on all copper layers, from Fig. 14. It blocks tracks, vias and pour. Its extent is x ±4.1 for y −3.6…−6.0, x ±3.0 for y −6.0…−6.8, and full width out to the module edge at y −6.95.
  - Markings:
    - Silk: a body outline 0.11 mm outside the body (≥0.4 mm from copper) and a pin-1 dot beside A1.
    - Fab: an outline with an A1 chamfer.
    - Courtyard: the body plus 0.25 mm, with a small notch that takes in the pin-1 dot.
  - Changes from DEV-G2-NANO: added the keep-out, pin-1 mark, fab chamfer and properties; fixed the model path.
- 3D model: `3dmodels/MAYA-W166.step`, from u-blox's official [3D-Step-Models-Library](https://github.com/u-blox/3D-Step-Models-Library) (`SHO/MAYA-W166.step`). EasyEDA has no model for this part.
  - The model origin is the module's lower-left corner. The footprint applies an offset of (−5.2, −7.35, 0) with no rotation.
  - In a KiCad top render the model fits the silk outline. The antenna area with its passives is at the L/M end, and the u-blox logo is at the bottom-right of the shield, as in Fig. 15.
  - The model has no pads or pin-1 mark on its underside. Its orientation was checked from the antenna end and the logo position, which put A1 bottom-right as Fig. 13 shows.

- Final review (2026-10-21), staged symbol re-checked against the DEV-G2-NANO source:
  - All 58 pins are present in both units, with identical numbers, names, positions, orientations and lengths. The 6 graphic items (body and unit B notes) are unchanged.
  - Only the pin electrical types and the properties changed. Each type was re-checked against the Table 16 I/O column (R09, pp. 21–24).
  - `check_sym.py` with the footprint: the only reported issues are the inherited 5.08 mm pin length and 2.54 mm pitch, plus the 28 NC pads. All pins are on the 50 mil grid.
  - Exported SVGs were inspected: no overlapping text.
  - The footprint SVG and `render_fp.py` top/tilt renders were inspected. The model fills the silk outline, the antenna is at the L/M end, the u-blox logo is bottom-right, and the pin-1 dot sits beside A1 (bottom-right).
  - LCSC was re-confirmed with the JLCPCB component API: C5441012 = MAYA-W166-00B, U-BLOX, extended/shop part, stock 0.

### Open issues
- **Board placement:** the data sheet hatching continues past the module edge on the antenna side, but how far is not dimensioned. The rule area stops at the module outline. Place the module at the board edge with the antenna facing out. Keep all copper layers clear out to the edge, with at least 10 mm of ground plane on each side and no tall parts within 10 mm of the antenna (SIM sec. 2.2.3).
- **Keep-out permissions:** the keep-out allows pads and footprints, because the row L/M GND pads touch its boundary. Decide whether it should block other footprints too.
- **Variant-specific footprint:** the keep-out makes this footprint specific to MAYA-W166-00B. W160, W161 and W166-01B would need a copy without the keep-out.
- **LCSC availability:** C5441012 was out of stock and is an extended part with the wrong "LGA-76" package label. Check availability before planning JLCPCB assembly, or plan to consign the part.
- **Symbol style:** the symbol is deliberately not in APEX style (module, copied as is). Restyle it only if you want it to.
- **ERC on unused inputs:** PDn (internal 10 kΩ pull-up, may float), WCI_SIN, SLP_CLK_IN and the unit B pins need no-connect flags when left floating, or ERC will flag them.
- **Pad check:** `check_sym.py` reports a pin/pad mismatch for the 28 NC pads. This is intentional.
- **Regenerating the footprint:** the courtyard notch was hand-edited into the .kicad_mod. Edit the footprint by hand; it was not generated from a script.
- **Lifecycle:** the R09 data sheet lists MAYA-W166-00B-00 as "Mass production", but a web search snippet of the u-blox product page reportedly marks it as no longer available. Distributors (DigiKey: Active, 20-week lead time) are inconsistent. Confirm the lifecycle before committing to it.

## MAX-M10S

- Device: u-blox MAX-M10S-00B standard-precision GNSS module (M10 platform), 18-pad LCC, 9.7 x 10.1 x 2.5 mm, 1.1 mm pitch.
- Primary sources: [u-blox MAX-M10S data sheet UBX-20035208 R08](https://content.u-blox.com/sites/default/files/MAX-M10S_DataSheet_UBX-20035208.pdf), section 3.1 Figure 2 / Table 10 (pin assignment), section 3.2 Table 11 (pin state), section 6 Table 21 (mechanical); MAX-M10S integration manual UBX-20053088 R05, section 4.4.1 Figure 30 / Table 44 (copper and solder mask) and Figure 31 / Table 45 (paste mask).
- LCSC: [C4153167](https://www.lcsc.com/product-detail/C4153167.html) (MAX-M10S-00B, LCC-18 9.7x10.1, JLCPCB assembly part). Set on both the symbol and the footprint. Alternative: [C24834155](https://www.lcsc.com/product-detail/C24834155.html), the newer MAX-M10S-00B-01 (ROM SPG 5.10), with the same pinout and footprint.
- Origin: the user's V1 library (`LR_RF:MAX-M10S-00B` symbol, `LR_RF.pretty/MAX-M10S-00B` footprint, `LR_RF.3dshapes/MAX-M10S-00B.step`). Not part of DEV-G2-NANO.
- Symbol: `APEX_Symbols:MAX-M10S`, Value `MAX-M10S-00B`, footprint `APEX_FOOTPRINTS:MAX-M10S_LCC18_u-blox`. Restyled to the APEX IC layout (150 mil pitch, 100 mil pins, 50 mil grid). Supplies VCC/V_IO/V_BCKP on top; GND pins 1, 10 and 12 on the bottom, listed separately; RF_IN, UART RX, I2C and control inputs (EXTINT, ~{RESET}, ~{SAFEBOOT}, VIO_SEL) on the left; VCC_RF (power_out), LNA_EN, TXD and TIMEPULSE on the right. All 18 pins match Table 10. Changes from V1: RF_IN is passive instead of bidirectional; ~{SAFEBOOT} is input instead of power_in; "Timepulse" is renamed TIMEPULSE; Datasheet, Description and LCSC are filled in.
- Footprint: `APEX_FOOTPRINTS:MAX-M10S_LCC18_u-blox`. The copper matches IM Table 44: pads are 1.8 mm long (1.0 mm inside and 0.8 mm outside the 9.7 mm body edge, centered at x = ±4.75); they are 0.8 mm wide, or 0.7 mm at the corners (pads 1, 9, 10, 18); the pitch is 1.1 mm. The solder mask is the same size as the copper. The paste follows IM Table 45 and is drawn as separate F.Paste T-polygons, not as pad paste: outer 1.4 mm x pad width, reaching x = ±6.25 (T = 12.5); inner 0.9 mm x 0.6 mm (0.5 mm on the corners), reaching x = ±3.95 (S = 7.9). The paste deliberately extends 0.6 mm beyond the copper on the outer side, as u-blox recommends to wet the castellations, with a 150 µm stencil. Pins 1–9 run down the left side and 10–18 run up the right side (counter-clockwise from the top). The V1 copper and paste already matched and were kept. Deviations from V1: the V1 all-layer keep-out under the module is removed, because IM section 4.4 asks for GND on L1/L2 under the module with no signals there. The fab outline is the nominal 9.7 x 10.1 mm with a pin-1 chamfer. The courtyard is ±6.5 x ±5.8, which is u-blox's 11.1 x 10.1 mm keep-out area plus margin. Silk runs along the top and bottom edges at y = ±5.45, and the pin-1 dot is above pad 1.
- 3D model: `libraries/3dmodels/MAX-M10S-00B.step`, copied from the user's V1 library (a SolidWorks export). It is linked as `${KIPRJMOD}/../../libraries/3dmodels/MAX-M10S-00B.step` with rotation (-90, 0, 0) and no offset. Its size is 9.7 x 10.1 mm plus a 0.3 mm de-paneling tab, which matches DS Table 21. A KiCad 3D render (top and tilted) shows the castellations on all 18 pads, the pin-1 dot at pad 1, and the tab at the pin-9/10 end.
- Review (link agent): `check_sym.py` with the footprint reports no issues, and the 18 pins match the 18 pads. The pin names and directions match DS Table 10. The pad and paste dimensions match IM Tables 44/45. The model alignment was re-rendered and confirmed. No fixes were needed.

### Open issues
- Pin 15 VIO_SEL: tie it to GND for a 1.8 V V_IO, or leave it open for 3.3 V. Choose this deliberately in the schematic.
- SAFEBOOT_N (pin 18) is connected inside the module to TIMEPULSE (pin 4) through 1 kΩ (DS footnote 15). Leave it open, or bring it to a test pad for firmware recovery; never drive it while TIMEPULSE is in use.
- RF_IN needs a 50 Ω microstrip/CPWG to the antenna. VCC_RF and LNA_EN are only needed for an active antenna or an external LNA.
- The paste T-shapes extend 0.6 mm past the copper. If the assembler's DFM tool flags paste outside the pads, that is intentional per u-blox IM Figure 31.
- The STEP file contains one stray construction point about 18 mm along its height axis. The rendered geometry is correct, so this only affects the bounding box.
- If C4153167 is out of stock, C24834155 (MAX-M10S-00B-01) can replace it directly.

## W25Q64JW

- Device: Winbond W25Q64JWUUIQ, a 64 Mbit 1.8 V (1.7–1.95 V) serial NOR flash with Standard, Dual and Quad SPI. Package code UU is the 8-pad USON, 4 mm × 3 mm × 0.55 mm with 0.8 mm pitch. The `Q` suffix means QE=1 is fixed, so /WP and /HOLD work as IO2 and IO3 by default. Other W25Q64JW package codes (SS, ZP, ZE, XG) have the same 8-pin assignment but different packages.
- Primary source: [Winbond W25Q64JW datasheet, Rev E (March 10, 2021)](https://www.winbond.com/resource-files/W25Q64JW%20RevE%2003102021%20Plus.pdf). Used sections: 3.2, Figure 1b (pad assignments); 3.3 (pin description table); 4.6 (hardware /RESET exists only on the SOIC-16 and TFBGA packages); 10.4, p. 69 (UU package outline and dimensions); 11 (ordering code). The pin table and the UU drawing are the same in Rev D (April 2020).
- LCSC / JLCPCB: [C6604692](https://www.lcsc.com/product-detail/NOR-FLASH_Winbond-Elec-W25Q64JWUUIQ_C6604692.html). The EasyEDA data for this number names W25Q64JWUUIQ with a Winbond UU footprint. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: DEV-G2-NANO (CERN-OHL-P) placed the stock `Memory_Flash:W25Q32JVSS` symbol with value W25Q64JWUUIQ and its own `W25Q64JWUUIQ` footprint. The APEX symbol is new and drawn from the datasheet. The footprint was redrawn (see below).
- Symbol: `APEX_Symbols:W25Q64JW`. VCC (8) is on top and GND (4) on the bottom, both `power_in`. The host-driven inputs are on the left: `~{CS}` (1) and `CLK` (6) as `input`, and `DI/IO0` (5) as `bidirectional`. `DO/IO1` (2), `~{WP}/IO2` (3) and `~{HOLD}/IO3` (7) are on the right, all `bidirectional`. Pin 7 is not named /RESET because the USON package has no hardware reset. Pins are 150 mil apart with 100 mil pin length on the 50 mil grid. The body is 30.48 mm × 20.32 mm, wide enough that the VCC pin number clears the Reference and Value text. The exposed metal has no symbol pin.
- Footprint: `APEX_FOOTPRINTS:W25Q64JW_USON8_Winbond`. Winbond publishes no land pattern for UU, so the copper uses IPC-7351 nominal sizes. This gives the same copper as the KiCad stock `Winbond_USON-8-2EP_3x4mm_P0.8mm_EP0.2x0.8mm`.
  - Orientation: KiCad standard, with pin 1 at the top left. Pads 1–4 run down the left side and pads 5–8 run up the right side.
  - Signal pads: 1.05 × 0.30 mm at x = ±1.35 mm with 0.8 mm pitch. That gives a 0.375 mm toe and 0.075 mm heel past the 0.60 mm lead.
  - Center metal: two unnumbered 0.20 × 0.80 mm pads at y = ±0.8 mm, matching the two center metal bars. The datasheet says this metal is not connected inside the part and may float or go to GND. It also says to keep exposed vias out from under it.
  - Paste: 1:1 with the pads.
  - Silkscreen and pin-1 dot: top and bottom silk lines are at least 0.67 mm from copper. The pin-1 dot sits outside the body corner, 0.32 mm from pad 1 and inside the courtyard.
  - Courtyard: ±2.15 × ±2.25 mm.
  - Footprints not used:
    - DEV-G2-NANO's footprint was rotated 90° and its pads were exactly the lead size (0.30 × 0.60 mm), with no toe extension for a solder fillet.
    - The EasyEDA footprint's pads are 0.40 mm wide, more than the 0.35 mm maximum lead width.
- 3D model: `3dmodels/W25Q64JW.step` is the LCSC/EasyEDA model for C6604692. It is a generic GigaDevice GD25Q32 USON-8 body with an LCEDA logo on top; no Winbond STEP was available.
  - Size: the bounding box is 3.0 × 4.0 × 0.55 mm, and the leads are 0.6 mm long and 0.30 mm wide. The origin is at the package center.
  - Placement: offset 0 and rotation 0. A KiCad render confirmed that the model's pin-1 dot sits over pad 1 and its leads sit over all eight pads.

### Open issues
- The copper is IPC-7351 nominal, not a manufacturer land pattern, because Winbond publishes none for UU. Review it before fabrication.
- The center metal pads are unnumbered, so they float, which the datasheet allows. To tie them to GND, number them "4" (or add an `EP` pin to the symbol) and keep exposed vias out from under them.
- This footprint is rotated 90° from the DEV-G2-NANO footprint. Swapping it into that board means rotating the part again.
- The 3D model is a generic GigaDevice USON-8 body with an EasyEDA logo, not a Winbond model.
- Value is `W25Q64JW` (symbol name, following the library convention). The DEV-G2-NANO schematic used `W25Q64JWUUIQ`. Set the full MPN per placement if the BOM needs it.

## UJ20-C-H-G-SMT-5-P16

- **Device:** Same Sky (formerly CUI Devices) UJ20-C-H-G-SMT-5-P16-TR. USB 2.0 Type-C receptacle, 16 contacts on 12 signal pads, horizontal, top mount. It has 4 SMT shell tabs and 2 NPTH locating pegs, and is rated 5 A / 48 V.
- **Primary source:** [datasheet rev 1.01 (09/12/2024)](https://www.sameskydevices.com/product/resource/uj20-c-h-g-smt-5-p16-tr.pdf)
  - p.1: specifications.
  - p.2: mechanical drawing. The body is 8.94 x 7.35 mm, and 11.34 mm wide across the shell tabs.
  - p.3: "PIN CONNECTIONS" table and "Recommended PCB Layout, Top View" (PCB tolerance ±0.05 mm).
- **LCSC:** [C45082768](https://www.lcsc.com/product-detail/C45082768.html) is UJ20-C-H-G-SMT-5-P16-TR, a JLCPCB extended part. It was confirmed against the JLCPCB parts API response (componentCode C45082768 maps to componentModelEn UJ20-C-H-G-SMT-5-P16-TR). The symbol and the footprint carry the same number.
  - These siblings are **not** equivalent because their shells or tabs differ: C45082766 (-1-P16), C45343181 (-2-P16), C45082769 (-P16, oval PTH shell tabs) and C7407133 (UJ20-C-H-G-SMT-TR).
- **Origin:** DEV-G2-NANO `project_symbols:USB-C` / `project_footprints:UJ20-C-H-G-SMT-5-P16` (CERN-OHL-P). The symbol was restyled to APEX and the footprint annotations were rebuilt.

### Symbol `UJ20-C-H-G-SMT-5-P16`
- Reference `J`. Value is the MPN without `-TR`.
- Footprint `APEX_FOOTPRINTS:UJ20-C-H-G-SMT-5-P16_SameSky`, with Datasheet, Description and LCSC filled in.
- 13 pins. Each pin number matches a footprint pad name exactly (`check_sym.py`: pin set == pad set).

| Pad | Name | Type | Side |
|---|---|---|---|
| A4_B9, B4_A9 | VBUS | passive | left, top group |
| A5 / B5 | CC1 / CC2 | bidirectional | left |
| A8 / B8 | SBU1 / SBU2 | bidirectional | left |
| A6, B6 | D+ | bidirectional | right |
| A7, B7 | D- | bidirectional | right |
| A1_B12, B1_A12 | GND | passive | bottom |
| S1 | SHIELD | passive | bottom (all 4 shell tabs) |

- I checked the pin table against datasheet p.3. A1/A12/B1/B12 are GND, A4/A9/B4/B9 are VBUS, A5 is CC1, B5 is CC2, A6/B6 are Dp, A7/B7 are Dn, A8 is SBU1 and B8 is SBU2.
- The data pins use the `D+`/`D-` convention (as in DEV-G2-NANO and the KiCad stock symbol) instead of the datasheet's Dp1/Dn1/Dp2/Dn2. The A/B pad number tells the two sides apart.
- SBU1/SBU2 were added. The DEV-G2-NANO symbol left them out, although its footprint has the pads.
- Pin types follow the usual connector convention (as in the KiCad stock USB-C symbols): VBUS, GND and SHIELD are `passive`, and CC, D± and SBU are `bidirectional`.
- **Deviations from the APEX style:**
  - The VBUS, GND and SHIELD pins are 300 mil long instead of 100 mil. Their merged pad numbers (`A4_B9` and similar) are about 6 mm long and would otherwise overlap the pin names.
  - VBUS sits at the top of the left side, not on the top edge, so its long numbers stay clear of the Reference/Value row.
  - Everything else is on the 50 mil grid, with 150 mil pitch and 300 mil group gaps. The body is 1500 x 1300 mil.

### Footprint `UJ20-C-H-G-SMT-5-P16_SameSky`
- **Copper source:** datasheet p.3 Recommended PCB Layout. The DEV-G2-NANO copper is identical to it and was kept. I re-checked every dimension against the drawing during review. The origin is the centre of the 7.93 mm pad-to-edge span.
  - **12 signal pads,** each 1.15 mm long, centred at y = -3.39 (spanning -3.965 to -2.815). Left to right, viewed from the top with the mouth toward +Y: A1_B12, A4_B9, B8, A5, B7, A6, A7, B6, A8, B5, B4_A9, B1_A12. This is the standard Type-C order, the same as the p.3 labels and the KiCad stock HRO footprint.
  - **Pad widths:** the four outer pads are 0.60 mm wide, with 6.40 / 4.80 mm centre-to-centre spacing. The inner eight are 0.30 mm wide at 0.50 mm pitch.
  - **Shell pads:** 4 pads named `S1`, 1.5 x 1.5 mm, at x = ±5.12 (10.24 mm c-c) and y = -2.815 / +1.115 (3.93 mm c-c).
  - **Pegs:** 2 NPTH holes, Ø0.65 mm, at x = ±2.89 (5.78 mm c-c), y = -2.315, which is 0.50 mm below the upper shell pad line.
  - **Product edge** at y = +3.965, 2.85 mm in front of the lower shell pads, marked "PCB edge" on F.Fab.
  - **Pad numbering** keeps the DEV-G2-NANO merged names (A1_B12, A4_B9, B4_A9, B1_A12, S1 x4).
  - p.3 shows 3.92 mm for one spacing and 3.93 mm for another that should match. 3.93 mm is used, as in DEV-G2-NANO; the difference is within the ±0.05 mm tolerance.
- **Annotations:**
  - REF on F.SilkS above the pads.
  - Value hidden on F.Fab, and `${REFERENCE}` on F.Fab.
  - Fab body (8.94 x 7.35 mm) with an A1 chamfer and the shell-tab outlines.
  - Silk side lines broken around the shell pads, ≥0.15 mm clear of copper.
  - A1 pin-1 dot on silk, 0.285 mm from the pad.
  - Courtyard ±6.15 x ±4.25 mm, width 0.05. It extends 0.285 mm past the board edge.
- There is no EasyEDA footprint for C45082768, and no KiCad stock footprint for this part.
- **Review fixes:**
  - Removed the silk front line at y = 3.89. It sat on the product/board edge and would be clipped or flagged by the silk-to-edge check. The side silk lines now end at y = 3.4.
  - Enlarged the pin-1 dot from r = 0.10 to r = 0.15 at (-3.2, -4.4), still 0.285 mm from copper.

### 3D model
- **File:** `libraries/3dmodels/UJ20-C-H-G-SMT-5-P16.step`, referenced as `${KIPRJMOD}/../../libraries/3dmodels/UJ20-C-H-G-SMT-5-P16.step`. The footprint transform is now offset (0, 0, 0), rotate (0, 0, 0), scale 1. It replaces the unverified DEV-G2-NANO transform (0, -4, 1.62 / -90, 0, 0), which was meant for Same Sky's own STEP.
- **Source:** this is **not** the manufacturer model. It is a simplified model built with CadQuery from datasheet rev 1.01 (09/12/2024). It uses p.2 (top/front/side views and section A-A) and p.3 (recommended layout). The generator script is `tools/library/build_uj20_step.py`.
  - The Same Sky STEP needs you to accept their CAD terms, and nobody accepted them on your behalf.
  - LCSC/EasyEDA has no model for C45082768, and KiCad has no stock model.
- **Dimensions, re-checked against p.2 in review:**
  - Body: 8.94 wide x 7.35 deep.
  - Shell: 3.16 high, top at 3.21, opening centre CH = 1.63.
  - Opening: 8.34 x 2.56. Tongue: 6.69 wide, 0.70 thick, 4.45 long. Cavity: 4.80 deep.
  - Shell tabs: 11.34 mm across, at 2.85 / 3.93 from the front face.
  - Pegs: 5.78 c-c, 0.68 below the board.
  - Leads: 16 x 0.20 wide, at the p.2 bottom-view lead spacing.
  - STEP point extents are X ±5.67, footprint y -3.80 to +3.975 and Z -0.68 to 3.21. The extra 0.01 mm at the front is a cut overshoot of the opening only.
- **Alignment check:** in review I re-ran `render_fp.py` (top and tilt). All 16 leads land on the 12 signal pads, with the pairs on the four 0.6 mm pads. The four tab feet sit on the S1 pads and the pegs are at the NPTH holes. The opening faces +y, so the front face is flush with the Fab "PCB edge" line at y = +3.965. A1 and the pin-1 dot are on the -x side.
- **Copper:** the only change to the footprint (git diff) is the model offset/rotate. Pads, holes, silk and courtyard are unchanged.

### Open issues

- **Merged pad numbers:** the footprint keeps the DEV-G2-NANO names (A1_B12, A4_B9, ...), so DEV boards port directly.
  - If you would rather have separate datasheet numbers (stacked `A1` + `B12` pads, as the KiCad stock footprints do), the symbol pins must be renumbered to match.
  - With short numbers, the VBUS/GND/SHIELD pins could go back to 100 mil and VBUS could move to the top edge.
- **VBUS/GND pin type:** they are `passive` (the connector convention). The APEX "power_in for supplies/GND" rule targets ICs. Change them to `power_in` if you prefer, but that causes ERC "not driven" errors unless the nets carry a PWR_FLAG.
- **Board edge:** place the footprint so the board edge falls on the Fab "PCB edge" line. The courtyard extends 0.285 mm past it.
- **Stock:** C45082768 is low stock (67 on 2026-10-16). Check availability before ordering.
- The model is an approximation. The envelope, opening, tabs, leads and pegs follow the drawing. The internal contacts, the shell embossing/latch windows and the lead forms are simplified.
- If you later download Same Sky's official STEP by accepting their terms, it can replace this file. The transform must then be re-checked with a render, since their file uses a different origin and orientation.

## PTS815

- Device: C&K PTS815 SJM 250 SMTR LFS (`PTS815SJM250SMTRLFS`). It is a microminiature top-actuated tactile switch: SPST-NO, 180 gf, 12 VDC / 50 mA, 4.2 × 3.2 × 2.5 mm body with J-bend SMT leads, supplied on tape and reel. The SJK (250 gf) and SJG (400 gf) variants have the same package and pinout.
- Primary source: [C&K PTS815 Series datasheet (4 Apr 22)](https://www.ckswitches.com/media/2728/pts815.pdf).
  - Page B-43: How To Order and the force options.
  - Page B-44: package outline, CIRCUIT DIAGRAM (terminals 1–2 common, 3–4 common, switch between the pairs) and P.C.B LAND DIMENSION.
  - The ckswitches.com link blocks automated downloads. The identical file was read from the [RS mirror](https://docs.rs-online.com/25f5/A700000009339342.pdf).
- LCSC / JLCPCB: [C2689510](https://www.lcsc.com/product-detail/C2689510.html). The LCSC page lists it as C&K PTS815SJM250SMTRLFS, SMD-4P 4.2x3.2mm. It is stored as the `LCSC` property on both the symbol and the footprint.
- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P).
  - DEV placed the stock `Switch:SW_Push` with Value `PTS815` and the project footprint `PTS815`.
  - Here the symbol is a dedicated APEX part, and the footprint is rebuilt. DEV's copper is kept and its pad-numbering bug is fixed (see below).
- Symbol: `APEX_Symbols:PTS815`.
  - It is a 2-pin pushbutton in the V1 style: dark-red graphics, both pins `passive`, 100 mil pins on the 50 mil grid, pin numbers visible and pin names hidden.
  - Pin 1 = datasheet terminals 1 and 2 (common). Pin 2 = terminals 3 and 4 (common).
  - The Reference is at the upper left. The Value is centred below the switch, as on the V1 R/C symbols, because at the upper right it collided with the Reference on such a compact symbol.
  - `ki_fp_filters` is `PTS815*`.
- Footprint: `APEX_FOOTPRINTS:PTS815_4.2x3.2mm_CK`, built from the datasheet land pattern.
  - Copper: four 1.0 × 0.7 mm rectangular pads at x = ±2.25 mm, y = ±1.075 mm (3.5 mm inner and 5.5 mm outer span, 2.15 mm row pitch).
  - Pad numbering is 1/1/2/2: top-left and top-right are datasheet pins 1 and 2, and bottom-left and bottom-right are datasheet pins 3 and 4. This matches the 2-pin symbol, as KiCad's stock `SW_SPST_PTS810` does.
  - DEV-G2-NANO's copper was identical, but its bottom-left pad had an empty pad number, so that lead was never connected to the net. It is now numbered 2.
  - The LCSC/EasyEDA footprint (1.05 × 0.65 mm at x = ±2.08 mm) does not match the datasheet and was not used. KiCad has no stock PTS815 footprint.
  - Silk: top and bottom edges plus short side ticks, 0.20 mm clear of copper. The pin-1 dot is 0.25 mm left of pad 1.
  - Fab: 4.2 × 3.2 mm body with a pin-1 chamfer, plus the 3.0 × 2.2 mm actuator.
  - Courtyard: ±3.3 × ±1.95 mm.
- 3D model: `3dmodels/PTS815.step`, the LCSC/EasyEDA model for C2689510 (`KEY-SMD_4P-L4.2-W3.25-P2.15-TL`).
  - Its origin is 1.5 mm above the seating plane, so the footprint uses offset z = +1.5 mm with no rotation.
  - Top, tilt and side KiCad renders show the leads on the four pads, the body inside the silk, and an overall height of about 2.5 mm.
  - The part is 2-fold symmetric, so its orientation makes no electrical difference.
  - Lead-tip span is about 4.76 mm, against the datasheet's 4.6 ± 0.2 mm.

### Open issues
- Force variant: DEV-G2-NANO only recorded "PTS815". SJM (180 gf, C2689510) was chosen. If 250 gf (SJK) or 400 gf (SJG) is wanted, change the Description and LCSC on the symbol and footprint; nobody looked up LCSC numbers for those variants.
- Symbol Value placement differs from the IC rule: it is centred below the switch instead of at the upper right. Accept or adjust.
- The 3D model is EasyEDA's, not C&K's (the C&K site blocks automated downloads). Its lead span is at the top of the tolerance. Swap in the C&K STEP if you download it by hand.
- Any board built from DEV-G2-NANO's footprint has one unconnected switch lead (the unnumbered bottom-left pad). That is harmless electrically because the bottom-right pad is internally common with it.
- If the symbol is ever made 4-pin, renumber the footprint pads 1/2/3/4 (top-left, top-right, bottom-left, bottom-right).
- No KiCad DRC was run on the footprint. Clearances were checked by hand from the coordinates.

## Pin headers, test points and IO banks

- Devices: generic single-row 2.54 mm straight through-hole male pin headers (1x02, 1x04, 1x30); a 3-pad SMD probe/pogo test-point cluster; and the two board-specific DEV-G2-NANO IO bank symbols that sit on the 1x30 headers.
- Primary source: there is no manufacturer datasheet for these. Header copper follows KiCad stock `Connector_PinHeader_2.54mm:PinHeader_1x0N_P2.54mm_Vertical` (KLC generator `connector/pin_header_socket`). The IO bank pinout comes from DEV-G2-NANO `kicad/user-io.kicad_sch`, checked against a netlist exported from the DEV-G2-NANO project.
- LCSC / JLCPCB: the parts are generic, so `LCSC` is present but empty on every symbol and footprint and is set per placed part. Candidates:
  - 1x02: [C124375](https://www.lcsc.com/product-detail/C124375.html) (Ckmtw B-2100S02P-A110). C36717 is an unverified alternative.
  - 1x04: [C124378](https://www.lcsc.com/product-detail/C124378.html) (Ckmtw B-2100S04P-A110), confirmed on LCSC and JLCPCB.
  - 1x30: no exact 1x30 part confirmed. [C2337](https://www.lcsc.com/product-detail/C2337.html) (BOOMELE 1x40 breakaway header) can be cut to 30.
- Origin: DEV-G2-NANO (CERN-OHL-P): `project_symbols:IO_Bank_Upper` / `IO_Bank_Lower` and `project_footprints:Header-1x02`, `Header-1x04`, `Header-1x30`, `TestPoints-3`. In DEV-G2-NANO, J1 (Lower Bank) and J2 (Upper Bank) use `Header-1x30`, J4 ("HIC SWD", stock `Conn_01x03`) uses `TestPoints-3`, and J5 ("RTC Battery", stock `Conn_01x02`) uses `Header-1x02`. `Header-1x04` is not placed on the DEV board.

### Symbols
- `APEX_Symbols:IO_Bank_Lower` and `APEX_Symbols:IO_Bank_Upper` are board-specific, so they were copied as they are and not restyled. Each has 30 `passive` pins (`Pin_1`..`Pin_30`, names hidden), 2.54 mm pitch, 3.81 mm pins and a 2.54 x 76.2 mm body. Footprint is `APEX_FOOTPRINTS:PinHeader_1x30_P2.54mm`, `ki_fp_filters` is `PinHeader_1x30_P2.54mm*`, Datasheet is empty, and `LCSC` is empty.
- Supply pins, drawn on the right side (all other pins are IO on the left), confirmed from the DEV netlist:
  - IO_Bank_Lower (J1): pin 9 = GND, pin 20 = +3V3.
  - IO_Bank_Upper (J2): pin 11 = GND, pin 22 = +3V3, pin 30 = V_IN.
- Fixed from the source: IO_Bank_Upper's Value said `IO_Bank_Lower`. It now reads `IO_Bank_Upper`.
- check_sym: 30/30 pins match the 30 pads of `PinHeader_1x30_P2.54mm`. It flags the 3.81 mm pin length and 100 mil pitch; both are deliberate (copied as-is, and the pitch matches the header).
- Link/review pass (2026-10-19): a fresh `kicad-cli sch export netlist` of DEV-G2-NANO again gives J1-9 = GND, J1-20 = +3V3, J2-11 = GND, J2-22 = +3V3, J2-30 = V_IN, so the right-side pins match. The Value field sits below the body, as in the DEV original, and was left there.
- The 1x02/1x04/test-point footprints have no APEX symbol; use the stock `Connector_Generic:Conn_01x0N` symbols as DEV-G2-NANO does.

### Footprints
- `APEX_FOOTPRINTS:PinHeader_1x02_P2.54mm`, `PinHeader_1x04_P2.54mm`, `PinHeader_1x30_P2.54mm`: 1.7 mm pads with a 1.0 mm drill, pad 1 at the origin and pads going down +Y at 2.54 mm. Pad positions and sizes match both DEV-G2-NANO and KiCad stock. EasyEDA's 1.1 mm drill (C124378) was not used; the 0.64 mm square pin (0.91 mm diagonal) fits 1.0 mm.
  - Deviation from DEV-G2-NANO: pad 1 is square (stock convention); DEV's pads are all round.
  - Silk: stock-style outline at ±1.38 mm (0.15 mm), open around pad 1, with an L-shaped pin-1 corner. Minimum silk-to-copper clearance is 0.345 mm. DEV's 1x30 had no silk.
  - Fab: 2.54 mm body with a 0.635 mm pin-1 chamfer. Courtyard: ±1.8 mm around the body (KiCad connector convention).
- `APEX_FOOTPRINTS:TestPoints_1x03`: copper copied exactly from DEV `TestPoints-3`. It has three 1.0 mm round pads (F.Cu and F.Mask, no paste) on a 1.5 mm equilateral triangle: pad 1 (0.75, 0.433), pad 2 (-0.75, 0.433), pad 3 (0, -0.866). The numbering is unchanged, so the J4 pin map is preserved.
  - Silk: a ring of r = 1.6 mm (0.159 mm clear of copper) and a pin-1 dot outside the ring next to pad 1. Courtyard: a circle of r = 2.1 mm.
  - Attributes are `smd exclude_from_pos_files exclude_from_bom`; DEV-G2-NANO had only `smd`.
- All four footprints export cleanly with kicad-cli. There are no duplicate UUIDs in APEX_FOOTPRINTS.pretty.

### 3D models
- `3dmodels/PinHeader_1x02_P2.54mm.step`, `PinHeader_1x04_P2.54mm.step` and `PinHeader_1x30_P2.54mm.step` are byte-identical copies (checked with `cmp`) of the KiCad 10 stock `Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x{02,04,30}_P2.54mm_Vertical.step`.
- They are referenced as `${KIPRJMOD}/../../libraries/3dmodels/...` with zero offset and rotation, the same as the stock footprint. render_fp.py renders (1x04 and 1x30) show the pins on the pads, with the body inside the silk outline.
- `TestPoints_1x03` has no model (bare pads).

### Open issues
- Pad 1 on the headers is square, while DEV-G2-NANO's are round. Revert to round if you want to match DEV exactly.
- `TestPoints_1x03` is excluded from the BOM and position files. Remove those attributes if J4 should be listed (for example as a pogo-fixture reference).
- No exact 1x30 LCSC part is confirmed. Choose one at order time (C2337 1x40 cut to length is the usual choice). C36717 (1x02 alternative) is unverified.
- The LCSC header datasheet PDFs could not be downloaded, so the pin cross-section was not checked against a datasheet. The 1.0 mm drill is the KiCad/industry default.
- DEV-G2-NANO places both 1x30 headers on the bottom side, so their new silk outline will print on B.SilkS.
- The IO bank GND/+3V3/V_IN pins are `passive` (normal for a connector). ERC will need a PWR_FLAG on any net powered only through these headers.
- In the DEV schematic, the placed Values were renamed to "Lower Bank" / "Upper Bank". The library Value equals the symbol name.
- `PinHeader_1x04_P2.54mm` is not used on the DEV-G2-NANO board; it was ported because the task listed it.

## Inductors (SDCL1V4018, DFE201610E, L_1008)

- Origin: carried over from the open-source DEV-G2-NANO project (CERN-OHL-P). The DEV schematics give values only, with no MPNs. L2 is 4.7 µH on `project_footprints:SDCL1V4018`. L3 and L4 are 470 nH on `project_footprints:L_0806` and sit on the TPS62825/TPS62086 buck outputs (all in power.kicad_sch). L1 is 10 µH on stock `L_1008_2520Metric` (user-io.kicad_sch).
- Symbol: the generic `APEX_Symbols:L` from the Generic-Passives unit. Its `ki_fp_filters` (`L_* DFE201610E* SDCL1V4018*`) already matches all three footprints. Its pins 1 and 2 match pads 1 and 2 of each footprint (check_sym: the pin set equals the pad set). Because L is generic, `LCSC` is set on each placed part. The two specific footprints below also carry it.
- All three footprints have two roundrect pads (ratio 0.1), pad 1 at −X. Each has silkscreen lines on the top and bottom edges, a Fab body rectangle, a 0.05 mm courtyard at least 0.25 mm outside the pads and body, and hidden Datasheet, Description and LCSC properties. Following the V1 passive style (`LR_Passive_SMD`), these non-polar parts have no pin-1 mark.

### SDCL1V4018 (4.7 µH)

- Device: Eaton (Bussmann) SDCL1V4018-4R7M-R, a semi-shielded power inductor, 4.0 × 4.0 × 1.85 mm max. Ratings: 4.7 µH ±20%, Irms 1.75 A, Isat 2.0 A, DCR 88 mΩ nominal (102 mΩ max).
- Primary source: [Eaton Technical Data ELX1032 (April 2021)](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-sdcl1v40-semi-shielded-smt-power-inductor-data-sheet-elx1032-en.pdf). Page 2 has the ratings table. Page 3 has the SDCL1V4018 dimensions and pad layout: a = 1.3, b = 4.3, c = 3.7 mm. It also says "traces or vias underneath the inductor is not recommended".
- LCSC / JLCPCB: [C17218852](https://www.lcsc.com/product-detail/C17218852.html). I re-verified it on the LCSC page during review: EATON SDCL1V4018-4R7M-R, 4.7 µH, 4 × 4 mm.
- Footprint: `APEX_FOOTPRINTS:SDCL1V4018_4.0x4.0mm_Eaton`.
  - Pads are 1.5 × 3.7 mm at x = ±1.4 mm, derived from the datasheet values. I re-checked the derivation in review.
  - The DEV-G2-NANO copper is identical, so it was kept. EasyEDA has no CAD for this part, and KiCad stock has no SDCL footprint.
  - Silkscreen lines sit at y = ±2.2, 0.275 mm clear of copper. The courtyard is ±2.4 mm.
- 3D model: `3dmodels/SDCL1V4018.step` is a **stand-in**. It is KiCad stock `L_Bourns-SRN4018.step`, the same semi-shielded 4 × 4 × 1.8 mm shape with terminals on ±X. Neither Eaton nor LCSC offered a STEP. Offset and rotation are 0. The top and tilt renders show the terminals on pads 1 and 2.

### DFE201610E (470 nH, ×2)

- Device: Murata DFE201610E-R47M=P2, a metal-alloy power inductor in 0806 (2016 metric), 2.0 × 1.6 × 1.0 mm max. Ratings: 0.47 µH ±20%, Isat 4.8 A, Itemp 3.6 A, DCR 32 mΩ max. DEV gave no MPN, so the footprint agent chose this part.
- Primary source: Murata inductor catalog O05E (Jan 25 2019). Page 15 has the dimensions. Page 139, "Standard Land Dimensions" for DFE201610E, gives a = 0.8, b = 2.4, c = 1.8 mm. [Product page](https://www.murata.com/en-us/products/productdetail?partno=DFE201610E-R47M%3DP2).
- LCSC / JLCPCB: [C269773](https://www.lcsc.com/product-detail/C269773.html). I re-verified it on the LCSC page during review: muRata DFE201610E-R47M=P2, 470 nH, 0806. LCSC lists these alternatives: DFE201610R-H-R47M=P2 (C882981), Chilisin EHEI201608A-R47M-Q7DG (C5727767), and Cybermax CMLO201610SR47MTT (C55200332).
- Footprint: `APEX_FOOTPRINTS:DFE201610E_0806_Murata`.
  - Pads are 0.8 × 1.8 mm at x = ±0.8 mm, per Murata.
  - The DEV-G2-NANO `L_0806` copper is identical, so it was kept.
  - The EasyEDA footprint for C269773 (pads 1.2 × 1.8 at ±1.0) does not match Murata, so it was rejected.
  - Silkscreen lines sit at y = ±1.15, 0.175 mm clear of copper. The courtyard is ±1.45 × ±1.25 mm.
- 3D model: `3dmodels/DFE201610E.step` comes from LCSC/EasyEDA (`L0806_L2.0-W1.6-H1.0`). Its origin is at mid-height, so the footprint offsets it z = +0.475 mm, with rotation 0. The tilt render shows it seated on the board with its terminals over the pads. The DEV project had referenced the wrong-size stock L_0805 model.

### L_1008 (10 µH, generic)

- Device: a generic 1008 (2520 metric) SMD inductor. DEV gave no MPN, so `LCSC` and `Datasheet` are empty, and LCSC is set on each placed part.
- Footprint: `APEX_FOOTPRINTS:L_1008`. Its copper is identical to KiCad stock `Inductor_SMD:L_1008_2520Metric` (IPC-7351 nominal): pads 1.25 × 2.2 mm at x = ±1.075 mm. Silkscreen lines sit at y = ±1.35, 0.175 mm clear of copper. The courtyard is ±1.95 × ±1.45 mm.
- 3D model: `3dmodels/L_1008.step`, copied from the stock `L_1008_2520Metric.step`. Offset and rotation are 0, and a render confirmed the alignment.

### Open issues

- **SDCL1V4018 3D model** is a Bourns SRN4018 stand-in. Replace it with Eaton's STEP if one can be downloaded. The link is on the Eaton SKU page and needs a browser.
- **SDCL1V4018 variant:** the DEV footprint description names SDCL1V4018-2R2M-R-1 (2.2 µH, Isat 3.0 A), but the schematic value is 4.7 µH. These notes follow the schematic: -4R7M-R, Isat only 2.0 A. Check the current and the value for L2's circuit.
- **470 nH choice:** confirm that DFE201610E-R47M=P2 (Isat 4.8 A, Itemp 3.6 A) suits both regulators, especially TPS62086 at 3 A, against TI's recommended-inductor tables.
- **10 µH 1008** is still generic. Choose a specific part (and check its current rating and land pattern) before ordering.
- **No pin-1 silk marker** on these non-polar inductors. This follows the V1 passive style but deviates from the spec's general pin-1 rule.

## Crystals (XTAL_3215, XTAL_3225)

Generic SMD crystal footprints. They are used by the generic `Crystal` (2-pin) and `Crystal_GND24` (4-pin) symbols from the Generic-Passives unit, through `ki_fp_filters` `XTAL_3215*` and `XTAL_3225*`. The `LCSC` property is present but empty on both footprints and symbols, because it is set per placed part (frequency and CL vary).

- **Origin:** DEV-G2-NANO `project_footprints:Crystal-2-Pin` (32.768 kHz) and `Crystal-4-Pin` (8/16/24 MHz), CERN-OHL-P. I did not keep the DEV copper (see deviations below).
- **Symbols:** generic, from the Generic-Passives unit. All pins are `passive`. `Crystal` has pins 1 and 2. `Crystal_GND24` has pins 1 and 3 for the crystal and pins 2 and 4 for GND (lid). I checked both with `check_sym.py`: the pin set equals the pad set.

### XTAL_3215 (2-pad, 3.2 x 1.5 mm, 32.768 kHz)
- **Primary source:** Epson FC-135R / FC-135 datasheet, page 1, "Footprint (Recommended)" (https://download.epsondevice.com/td/pdf/brief/FC-135_en.pdf). It gives 1.0 x 1.8 mm pads at a 2.5 mm centre-to-centre pitch, and a 3.2 x 1.5 x 0.9 mm body.
- **Copper:** pad 1 at (-1.25, 0) and pad 2 at (+1.25, 0), rect 1.0 x 1.8 mm. This matches the datasheet exactly. It is also identical to KiCad stock `Crystal_SMD_3215-2Pin_3.2x1.5mm` (which has pad 1 at +X) and to EasyEDA C32346 (pad 1 at -X).
- **Deviation from DEV:** the DEV pads were 1.1 x 1.9 mm with pad 1 at +X. I used the datasheet size and put pad 1 at -X. The part is unpolarized, so this has no electrical effect.
- **Silk:** top and bottom bars, 0.225 mm from copper. There is no pin-1 mark because the part is unpolarized.
- **Fab:** body rectangle, 3.2 x 1.5 mm.
- **Courtyard:** ±2.0 x ±1.15 mm (pads + 0.25 mm).
- **Suggested LCSC:** [C32346](https://www.lcsc.com/product-detail/C32346.html), Epson Q13FC13500004, 12.5 pF, ±20 ppm (JLC basic part).

### XTAL_3225 (4-pad, 3.2 x 2.5 mm, 8/16/24 MHz)
- **Pinout:** numbered counter-clockwise from the bottom-left in top view (1 BL, 2 BR, 3 TR, 4 TL). Pads 1 and 3 are the crystal; pads 2 and 4 are GND (lid). This is the standard SMD3225-4P pinout (Epson FA-238 / TSX-3225 internal-connection figure, YXC, KiCad stock).
- **Copper:** 1.4 x 1.2 mm rect pads at (±1.1, ±0.85), so the pitch is 2.2 x 1.7 mm. This is identical to KiCad stock `Crystal_SMD_3225-4Pin_3.2x2.5mm` (TXC 7M land; stock uses roundrect) and to EasyEDA C13738 (YXC X322516MLB4SI).
- **Deviation from the datasheet:** Epson FA-238 "Footprint (Recommended)" (TSX-3225 datasheet, page 1, https://download.epsondevice.com/td/pdf/brief/TSX-3225_en.pdf) uses the same 1.4 x 1.2 mm pads but a 1.6 mm Y pitch (centre to centre). I kept the TXC/YXC/KiCad 1.7 mm pitch because the suggested parts are YXC.
- **Deviation from DEV:** the DEV pads were off-centre by 0.1 mm in x (pads 2 and 3 at x = +1.2) and used y = ±0.9. I did not keep that.
- **Silk:** an L along the left and bottom edges with its corner at the pin-1 corner, 0.175 mm from copper.
- **Fab:** body outline with a chamfer at the pin-1 corner.
- **Courtyard:** ±2.2 x ±1.85 mm, enlarged so it encloses the silk.
- **Suggested LCSC (per frequency):**
  - 8 MHz: [C2682775](https://www.lcsc.com/product-detail/C2682775.html), YXC X32258MOB4SI, 12 pF. Alternative: C2682774, X32258MSB4SI, 20 pF.
  - 16 MHz: [C13738](https://www.lcsc.com/product-detail/C13738.html), YXC X322516MLB4SI, 9 pF.
  - 24 MHz: [C70590](https://www.lcsc.com/product-detail/C70590.html), YXC X322524MOB4SI, 12 pF.
  - C9006 is 25 MHz, not 24 MHz. C115962 (8 MHz) is a 5032 package. Do not use either.

### 3D models
- `XTAL_3215.step` and `XTAL_3225.step` are byte-identical copies of KiCad stock `Crystal_SMD_3215-2Pin_3.2x1.5mm.step` and `Crystal_SMD_3225-4Pin_3.2x2.5mm.step`.
- Both are referenced as `${KIPRJMOD}/../../libraries/3dmodels/<Name>.step`, with offset 0 and rotation 0.
- I checked the renders (top and tilt views). Both bodies are centred, the terminals sit on the pads, and the body sizes are 3.2 x 1.5 mm and 3.2 x 2.5 mm. Both models are symmetric, so pin 1 cannot be distinguished on the model.

### Open issues
- The DEV-G2-NANO schematics give no MPN or load capacitance for Y1 (8 MHz), Y2 (16 MHz), Y3 (24 MHz) or Y4 (32.768 kHz). Check the CL of each LCSC pick above against the board's load capacitors and the MCU/PHY oscillator requirements before ordering.
- XTAL_3225 uses the 1.7 mm Y pitch from TXC/YXC/KiCad, not the 1.6 mm pitch in Epson FA-238. If an Epson TSX-3225 is chosen, reconsider this. The footprint's Datasheet field links the Epson TSX-3225 PDF because the YXC datasheet could not be downloaded (the link served HTML).
- XTAL_3215 has pad 1 on the left, while DEV and stock have it on the right. This is harmless for an unpolarized crystal, but it is mirrored relative to the DEV layout.

## Generic passives, diodes, crystals, switch (symbols)

Generic symbols, not tied to any MPN: `R`, `C`, `C_Polarized`, `L`, `FB`, `D`, `D_Schottky`, `D_Zener`, `D_TVS`, `D_TVS_Bidir`, `LED`, `D_Schottky_x2_KCom`, `Crystal`, `Crystal_GND24`, `SW_Push`. They replace the KiCad stock symbols used in DEV-G2-NANO (`Device:R_Small_US`, `C_Small`, `L_Small`, `FerriteBead_Small`, `LED`, `Crystal_Small`, `project_symbols:Crystal_GND24_Small`, `Switch:SW_Push`).

- **Primary source:** none (generic). The drawings follow the user's V1 library `APEX-2026/symbols/LR_Passive_SMD.kicad_sym` (R, C, C_Polarized, L, FB geometry; pin ends at ±3.81) and `LR_Power-Components.kicad_sym` (`DIO_MBR0540T3G` diode body and Schottky hooks).
- **LCSC:** property present and empty on every symbol; it is set per placed part.
- **Origin:** new drawings. DEV-G2-NANO (CERN-OHL-P) was used only to find which generic symbols were needed.
- **Footprint / Datasheet:** empty. Footprints are selected through `ki_fp_filters` (table below).
- **Footprint, 3D model:** none in this unit. The matching footprints come from the Generic-RC-FP (R_/C_), Generic-LDF-FP (L_/FB_/LED_/D_), Inductors, Crystals, BAT54C and PTS815 units.

### Symbol summary (all pins `passive`, text 1.27, Reference/Value visible)
| Symbol | Ref | Pins | Pin ends (mm) | ki_fp_filters |
|---|---|---|---|---|
| R | R | 1, 2 | ±3.81 | `R_*` |
| C | C | 1, 2 | ±3.81 | `C_*` |
| C_Polarized | C | 1 = +, 2 = - | + at -3.81 | `C_* CP_*` |
| L | L | 1, 2 | ±3.81 | `L_* DFE201610E* SDCL1V4018*` |
| FB | FB | 1, 2 | ±3.81 | `FB_* L_0402* L_0603*` |
| LED | D | 1 = K, 2 = A | K +3.81, A -3.81 | `LED_*` |
| D, D_Schottky, D_Zener, D_TVS | D | 1 = K, 2 = A | K +3.81, A -3.81 | `D_SOD* D_SMA* D_SMB* D_SMF* D_0402* D_0603*` |
| D_TVS_Bidir | D | 1 = A1, 2 = A2 | ±5.08 | same as D |
| D_Schottky_x2_KCom | D | 1 = A1, 2 = A2, 3 = K | A1 -6.35, A2 +6.35, K (0, +3.81) | `D_SOT23* SOT?23* BAT54C*` |
| Crystal | Y | 1, 2 | ±3.81 | `XTAL_3215*` |
| Crystal_GND24 | Y | 1, 3 = crystal; 2 (top), 4 (bottom) = GND | 1/3 ±5.08; 2/4 (0, ±5.08) | `XTAL_3225*` |
| SW_Push | SW | 1, 2 | ±5.08 | `SW_* PTS815*` |

- Diode pin 1 = cathode (KiCad/IPC convention), anode drawn on the left, cathode bar on the right.
- `D_Schottky_x2_KCom` follows the BAT54C SOT-23 pinout (Nexperia BAT54 series data sheet: 1 = anode 1, 2 = anode 2, 3 = common cathode). Pin set equals the pad set of `BAT54C_SOT23_Nexperia` (check_sym.py).
- `Crystal` vs `XTAL_3215` (1/2), `Crystal_GND24` vs `XTAL_3225` (1-4, pads 2/4 = lid) and `SW_Push` vs `PTS815_4.2x3.2mm_CK` (1,1,2,2) were checked with check_sym.py: pin set equals pad set.

### Deviations from the IC-style spec (intentional, V1 compact style)
- Reference centred above and Value centred below at size 1.27 (not corner placement at 1.524).
- Pin lengths follow the V1 drawings: 3.175 (C, FB, diode/LED K pin), 2.794 (C_Polarized "-"), 1.27 (L). check_sym.py reports these as "length != 2.54"; every pin connection point is still on the 50 mil grid.
- Pin names are defined but hidden (`pin_names hide`); polarity is shown graphically ("+" mark and filled negative plate on C_Polarized, triangle/bar on diodes). Pin numbers are visible.
- R uses the V1 rectangle, not the US zigzag `R_Small_US` from DEV-G2-NANO.
- V1's explicit dark-red stroke colour was dropped so the symbols follow the schematic theme.
- V1 used `bidirectional` pins on C_Polarized, L and FB; all are `passive` here.

### Review (link and review pass)
- Exported all 15 symbols to SVG/PNG and inspected them: no text/graphic overlaps; L pin numbers sit tight against the coil ends because of the 1.27 mm V1 pin length (cosmetic only).
- Text sizes (1.27 everywhere), reference designators (R/C/L/FB/D/Y/SW) and Value visibility are consistent across all symbols.
- Second pass: re-ran check_sym.py on all 15 symbols (only the expected V1 pin-length notes on C, C_Polarized, L, FB and the diode/LED K pin); pin set equals pad set for `R` vs `R_0402`, `L` vs `L_1008`, `D_Schottky_x2_KCom` vs `BAT54C_SOT23_Nexperia`, `Crystal` vs `XTAL_3215`, `Crystal_GND24` vs `XTAL_3225` (pads 1/3 crystal, 2/4 lid, matching the Crystals unit) and `SW_Push` vs `PTS815_4.2x3.2mm_CK`.
- Changed `ki_fp_filters`: `L` now also matches `DFE201610E*` and `SDCL1V4018*` (the Inductors unit footprints are used with the generic L symbol); `FB` also matches `L_0402*`/`L_0603*` (DEV-G2-NANO placed its ferrite bead on an `L_0402` footprint).

### Open issues
- Generic-LDF-FP footprints (FB_, LED_, D_*) were not yet in the library at review time (only `L_1008` was present). Confirm their names match the filters (`FB_*`, `LED_*`, `D_SOD*`, `D_SMA*`, ...) and that every LED and diode footprint has pad 1 = cathode. The V1 `DIO_MBR0540T3G` symbol used pin 1 = anode, so any V1-derived diode footprint would be reversed.
- D_TVS (unidirectional) has no single standard drawing; here both bar ends bend toward the cathode, to differ from D_Zener (Z-shaped bar). Some datasheets draw a TVS identical to a Zener. Confirm which you want.
- Pin numbers are visible on R, C, L and FB (as in V1). Hide them if you prefer a cleaner schematic.
- Datasheet is empty on all generic symbols (no single source). Set `~` if you want KiCad's "no datasheet" convention.
- `D_Schottky_x2_KCom` overlaps the specific `BAT54C` symbol from the BAT54C unit. Keep one, or keep both (generic for alternates such as BAT54CW/BAS40-04).

## Generic connectors and test point

- **Symbols:** `Conn_01x01` to `Conn_01x10`, `Conn_01x30`, `Conn_02x05`, `TestPoint`.
- **Purpose:** these replace KiCad stock `Connector_Generic:Conn_01xNN` and the V1 `LR_Power:TP`. DEV-G2-NANO uses `Conn_01x02`, and `Conn_01x03` with the `TestPoints-3` footprint.
- **Primary source:** none, because these are generic parts. The style follows V1 `LR_Power.kicad_sym:TP` (dark-red filled circle, r = 0.635) and the stock `Connector_Generic` drawing (a body with one pin stub per contact).
- **LCSC:** none. The `LCSC`, `Footprint` and `Datasheet` properties exist but are empty; set them on each placed part (SPEC, generic parts).
- **Origin:** written new for APEX. It replaces the stock symbols used by DEV-G2-NANO (CERN-OHL-P). No geometry was copied.

### Symbol
| Symbol | Pins | Name | Type | Position |
|---|---|---|---|---|
| Conn_01xNN | 1..N | Pin_1..Pin_N (hidden) | passive | Left side, x = -3.81. Pin 1 at the top, 2.54 mm pitch |
| Conn_02x05 | 1,3,5,7,9 / 2,4,6,8,10 | Pin_n (hidden) | passive | Odd pins on the left, even pins on the right, as on the 10-pin ARM Cortex SWD header |
| TestPoint | 1 | 1 (name and number hidden) | passive | Connects at (-2.54, 0). Circle centred at (0.635, 0) |

- **Pin pitch:** 100 mil (2.54 mm), not 150 mil, on purpose. Symbol pin order matches the physical header 1:1, and `Conn_01x30` stays about 76 mm tall. `check_sym.py` reports only this spacing deviation.
- **Grid and pin length:** all pins and body corners are on the 50 mil grid, and every pin is 100 mil long. That includes TestPoint: V1 used 1.905 mm, so the circle was moved to keep the pin end on grid.
- **TestPoint pin type:** passive. V1 used bidirectional; passive avoids ERC conflicts on power nets.
- **Text:** Reference at the upper left (`left bottom`, 1.524). Value sits below the body (`left top`, 1.524), because the 100–200 mil body leaves no room at the upper right. The TestPoint Value is hidden.
- **ki_fp_filters:**
  - Conn_01xNN: `PinHeader_1xNN_* TestPoints_1xNN* Connector*:*_1xNN_*`
  - Conn_02x05: `PinHeader_2x05_* *2x05*P1.27mm* Connector*:*_2x05_*`
  - TestPoint: `TestPoint_* TP_* TestPoints_1x01*`
- **Matching APEX footprints:** `PinHeader_1x02_P2.54mm`, `PinHeader_1x04_P2.54mm`, `PinHeader_1x30_P2.54mm` and `TestPoints_1x03` match their `Conn_01xNN`. Their pad sets equal the symbol pin sets (checked with `check_sym.py`).

### Footprint / 3D model
- No footprint or 3D model belongs to this unit. The pin-header and test-point footprints and their models come from other units.

### Review (link and review pass)
- Re-ran `check_sym.py` on all symbols. The only flag is the intentional 100 mil spacing.
- Checked pin and pad sets against `PinHeader_1x02/1x04/1x30_P2.54mm` and `TestPoints_1x03`. They match.
- Re-exported `Conn_01x01`, `Conn_01x05`, `Conn_01x30`, `Conn_02x05` and `TestPoint` to SVG and PNG and inspected them. Pins, numbers and text do not overlap.
- Fix: the TestPoint filter changed from `TestPoint*` to `TestPoint_*`. The old filter also matched the 3-pad `TestPoints_1x03` for a 1-pin symbol.

### Open issues
- No APEX footprint exists yet for a 2x05 1.27 mm SWD header or a single test-point pad. The filters use the expected names (`PinHeader_2x05_*`, `*2x05*P1.27mm*`, `TestPoint_*`). Update them if the footprints get different names.
- The DEV-G2-NANO `TestPoints-3` (a 3-pad pogo cluster) maps to `Conn_01x03` with `APEX_FOOTPRINTS:TestPoints_1x03`, not to three `TestPoint` symbols. Confirm this mapping.
- These symbols use a 100 mil pin pitch, not the SPEC's 150 mil IC pitch. Confirm this is acceptable for generic connectors.

## Power symbols (GND, AGND, PGND, +1V0, +1V2, +1V8, +3V3, +5V, VBUS, VBAT, VIN, V_RAIL, PWR_FLAG)

- Device/package: schematic-only virtual symbols (`(power global)`), no physical part. Footprint, Datasheet and LCSC are not applicable: Footprint and Datasheet are empty, and there is no LCSC property (the symbols are excluded from the BOM and the board, like the KiCad stock `power:` library).
- Purpose: replaces the KiCad stock `power:` symbols used by DEV-G2-NANO: `power:GND` x56 and `power:+1V0` x54. The `+1V0` instances have their Value edited to `+1V8` (18), `+3V3` (17), `+5V` (6), `V_{BUCK}` (3), `V_{DCDC_ANA}` (3), `V_{DCDC_DIG}` (3), `V_{IN}` (2) and `V_{USB}` (2). DEV-G2-NANO uses no PWR_FLAG.
- Style source: the user's V1 `LR_Power.kicad_sym` (GND/AGND/PGND, +3V3/+5V/+VBAT drawings). The header flags (`pin_numbers hide`, `pin_names offset 0 hide`, `ki_keywords`) and PWR_FLAG come from the KiCad 10 stock `power.kicad_sym`.
- Origin: written fresh. No DEV-G2-NANO (CERN-OHL-P) geometry was used.

### Symbol summary
| Symbol | Ref | Pin | Type | Drawing |
|---|---|---|---|---|
| GND, AGND, PGND | #PWR | 1, hidden, len 0, at (0,0) | power_in | V1 ground: stem 0 to -1.27, bars 2.54/1.27/0.254 wide at -1.27/-1.905/-2.54, dark red 132,0,0; Value at (0,-3.81) |
| +1V0, +1V2, +1V8, +3V3, +5V, VBUS, VBAT, VIN | #PWR | 1, hidden, len 0 | power_in | V1 rail: stem 0 to 1.27, filled dark-red triangle up to 2.54; Value at (0,3.81) |
| V_RAIL | #PWR | 1, hidden, len 0 | power_in | Same as the rails. **Edit the Value** to any net name (e.g. `V_{DCDC_DIG}`); KiCad 10 names the global net from the Value field |
| PWR_FLAG | #FLG | 1, len 0, rot 90 | power_out | Stock diamond flag; in_bom/on_board yes, same as stock |

- Every symbol except PWR_FLAG has `in_bom no` and `on_board no`. PWR_FLAG matches stock.
- Each symbol has a Description and `ki_keywords`.
- None of the names collide with symbols already in `APEX_Symbols.kicad_sym`.

### Footprint / 3D model
- None. These are virtual symbols.

### Decisions
- V1 draws the third ground bar as a zero-radius circle "dot". It is replaced here with a 0.254 mm bar so it renders reliably. Apart from that, the drawing matches V1.
- AGND and PGND use the same drawing as GND, as V1 does. Only the Value text tells them apart.
- Pins have length 0 at the origin, following the V1 and stock power convention. check_sym.py reports `length 0 != 2.54` and a missing LCSC for every symbol. Both are expected for power symbols and were not changed.
- Rail names: `VBAT` is used instead of V1's `+VBAT`, and `VBUS` and `VIN` were added.

### Validation (link/review pass, 2026-10-21, on the regenerated staged file)
- Structure check of all 13 symbols against the stock KiCad 10 `power.kicad_sym`: each has `(power global)`, `pin_numbers hide`, `pin_names offset 0 hide`, exactly one pin at (0,0) with length 0. Rails and grounds use a hidden `power_in` pin named like the net, Reference `#PWR` (hidden), and Value = net name (visible). PWR_FLAG is byte-identical to the stock symbol (`power_out`, rot 90, Reference `#FLG`).
- Drawings compared with V1 `LR_Power.kicad_sym`: the rail triangle and stem match V1 `+3V3_1` exactly. The ground stem and bars match V1 GND/AGND/PGND, except that the V1 zero-radius dot is drawn as a 0.254 mm bar.
- check_sym.py: 1 pin each, of the expected type. The only findings are `length 0 != 2.54` and missing LCSC, both expected for power symbols.
- SVG export works for all 13 symbols. PNGs of GND, +3V3, V_RAIL and PWR_FLAG were inspected and render as intended.
- A test schematic was built in which 7 resistors tie +3V3/GND, V_RAIL(Value `V_{DCDC_DIG}`)/GND, V_RAIL(Value `V_{BUCK}`)/AGND, +1V8/PGND, VBUS/VBAT, VIN/+5V and +1V0/+1V2.
  - `kicad-cli sch export netlist` gives exactly 13 nets: +1V0, +1V2, +1V8, +3V3, +5V, AGND, GND (R1.2 and R2.2), PGND, VBAT, VBUS, VIN, `V_{BUCK}` and `V_{DCDC_DIG}`. Net names come from the power symbol Value, so V_RAIL works with an edited Value, and two V_RAIL instances with different Values stay separate nets.
  - ERC with a PWR_FLAG on each net, plus a local sym-lib-table: 0 errors and 0 warnings.
  - ERC without flags (`pwrtest_noflag.kicad_sch`): 13 `power_pin_not_driven` errors, one per net, which confirms the pins are `power_in`.
- The symbols are NOT yet in `REPO/libraries/symbols/APEX_Symbols.kicad_sym`. The orchestrator must merge all 13; none collide with names already there.

### Open issues
- AGND and PGND look identical to GND, as in V1. If they should look different, they need a distinct drawing (for example a stock-style AGND triangle or a chassis/PGND variant).
- Schematic port mapping: `power:GND` becomes `GND`. `power:+1V0` with Value `+1V8`, `+3V3` or `+5V` becomes the named symbol. The other `power:+1V0` instances (`V_{BUCK}`, `V_{DCDC_ANA}`, `V_{DCDC_DIG}`, `V_{IN}`, `V_{USB}`) become `V_RAIL` with the instance Value kept. Note that `V_{IN}` and `VIN` are different net names; keep `V_{IN}` via V_RAIL unless you want to rename the net.
- `VBAT` is spelled without V1's `+` prefix. Confirm this is the naming you want.

## Generic R / C footprints (R_0201 … R_1206, C_0201 … C_1206)

- **Symbols:** none in this unit. The generic `R` and `C` symbols (unit Generic-Passives) carry an empty `Footprint`, empty `LCSC`, and `ki_fp_filters` `R_*` / `C_*`, which match these footprint names. `check_sym.py` confirms symbol pins {1,2} equal the footprint pad set (the 0201 paste-only pads are unnumbered and ignored).
- **Primary source:** IPC-7351B nominal land patterns (no single manufacturer datasheet for generic parts); LCSC is set per placed part, not on the footprint.

- **Device/package:** generic 2-terminal chip resistors and MLCCs, EIA 0201/0402/0603/0805/1206 (metric 0603/1005/1608/2012/3216).
- **Files:** `libraries/footprints/APEX_FOOTPRINTS.pretty/{R,C}_{0201,0402,0603,0805,1206}.kicad_mod` (10 files).
- **Land-pattern source:** IPC-7351 nominal (density level B), as implemented in the KiCad stock `Resistor_SMD` / `Capacitor_SMD` footprints (`{R,C}_<size>_<metric>Metric`, KiCad 10.0.3). The body sizes come from IPC-SM-782 pp. 72 and 76 (the R/C chip tables), with Vishay CRCW0201 for 0201. These are generic parts, so there is no single manufacturer datasheet.
- **Origin:** APEX V1 `LR_Passive_SMD.pretty` (user's own library). DEV-G2-NANO (CERN-OHL-P) uses the KiCad stock footprints directly (`Resistor_SMD:R_0201_0603Metric`, `Capacitor_SMD:C_0201/0402/0603…`) and has no custom R/C footprint.
- **Pads:** 2 pads, numbered `1` (left, −X) and `2` (right, +X), roundrect. The 0201 also has two unnumbered F.Paste-only pads (0.318×0.36 at ±0.345), the same as stock: the paste is reduced and pushed outward to limit tombstoning. Its copper pads are F.Cu+F.Mask only.

### Copper comparison (pad centre ±X, pad W×H, mm)
| Footprint | APEX (new) | V1 LR_Passive_SMD | KiCad stock | DEV-G2-NANO |
|---|---|---|---|---|
| R_0201 / C_0201 | ±0.32, 0.46×0.40 (+paste 0.318×0.36 @±0.345) | identical | identical | uses stock |
| R_0402 | ±0.51, 0.54×0.64 | identical | identical | (not used) |
| C_0402 | ±0.48, 0.56×0.62 | identical | identical | uses stock |
| R_0603 | ±0.825, 0.80×0.95 | identical | identical | (not used) |
| C_0603 | ±0.775, 0.90×0.95 | identical | identical | uses stock |
| R_0805 | ±0.9125, 1.025×1.40 | identical | identical | — |
| C_0805 | ±0.95, 1.00×1.45 | identical | identical | — |
| R_1206 | ±1.4625, 1.125×1.75 | identical | identical | — |
| C_1206 | ±1.475, 1.15×1.80 | identical | identical | — |

The V1 copper equals the stock IPC-7351 nominal copper exactly (same corner-radius ratios too), so the copper is kept unchanged. I did not use EasyEDA footprints because the parts are generic.

### Annotation changes vs V1 (APEX style)
- **Silk:** V1 used a full box at 0.153 width that sat only about 0.09–0.10 mm from the pads. It is now top and bottom lines only (width 0.15) spanning the body length, at y = pad_h/2 + 0.225 (rounded up to 0.01), so the line edge is ≥0.15 mm from copper (measured 0.155 mm on every size).
- **Courtyard:** V1 and stock use 0.15 mm (0201–0402) or 0.25 mm margins. It is now an `fp_rect` with ≥0.25 mm around pads and body, rounded up to 0.05. 0201: ±0.80×±0.45; 0402: ±1.05×±0.60; 0603: ±1.50×±0.75; R_0805: ±1.70×±0.95; C_0805: ±1.70×±1.00; 1206: ±2.30×±1.15.
- **Text and properties:** REF** is on F.SilkS above the courtyard (size 1, thickness 0.15). Value is on F.Fab, hidden. `${REFERENCE}` is on F.Fab, scaled to the body (0.15/0.25/0.4/0.5/0.8). Properties: Datasheet empty, Description "Generic resistor/capacitor, <size> SMD", LCSC **empty** (hidden, F.SilkS 1/0.1), plus descr and tags.
- **Fab:** body rectangle (stock body dims). There is no pin-1 chamfer and no silk pin-1 dot because R/C are non-polarized (same as V1 and stock). See open issues.

### 3D models
- Source: the KiCad stock (10.0.3) `Resistor_SMD.3dshapes` / `Capacitor_SMD.3dshapes` `{R,C}_<size>_<metric>Metric.step`, copied into `libraries/3dmodels/` (10 files). Each footprint links `${KIPRJMOD}/../../libraries/3dmodels/<t>_<size>_<metric>Metric.step`.
- Offset 0, rotation 0, scale 1, the same as the stock footprints. The renders show the bodies centred on the pads with terminations over pads 1 and 2 for all 10 sizes. Polarity is irrelevant.

### JLCPCB part numbers for DEV-G2-NANO values
Checked 2026-10-19 with the JLCPCB parts-search API (`selectSmtComponentList`, filtered by package and value). **JLCPCB has no 0201 Basic parts at all** (a Basic-library search returns no 0201 package), and none of the 0201 candidates carries the "Preferred Extended" flag. Every 0201 part is therefore Extended. The table gives the highest-stock suitable one, with alternatives.

| Size | Value | LCSC | MPN | Rating | Library | Alternatives |
|---|---|---|---|---|---|---|
| R 0201 | 10k | C473048 | UNI-ROYAL 0201WMF1002TEE | 1%, 50 mW | Extended | C106225 (Yageo RC0201FR-0710KL) |
| R 0201 | 17.8k | C474125 | UNI-ROYAL 0201WMF1782TEE | 1% | Extended | C469664 (Yageo RC0201FR-0717K8L), C166323 |
| R 0201 | 2.2k | C473508 | UNI-ROYAL 0201WMF2201TEE | 1% | Extended | C142018 (Yageo RC0201FR-072K2L) |
| R 0201 | 5.1k | C270344 | UNI-ROYAL 0201WMF5101TEE | 1% | Extended | C274341 (Yageo RC0201FR-075K1L), C473460 (5%) |
| C 0201 | 100nF | C307380 | Samsung CL03A104KO3NNNC | 16V X5R 10% | Extended | C76939 (Murata GRM033R61E104KE14D, 25V), C66938 (6.3V) |
| C 0201 | 1uF | C76929 | Murata GRM033R60J105KEA2D | 6.3V X5R 10% | Extended | C87143 (Taiyo JMK063ABJ105MP-F, 6.3V), C2846675 (FH, 10V) |
| C 0201 | 2.2uF | C386031 | Taiyo Yuden LDK063BBJ225MPLF | 10V X5R 20% | Extended | C77762 (Samsung CL03A225MQ3CRNC, 6.3V), C319184 (Murata, 10V) |
| C 0201 | 220nF | C701263 | Murata GRM033R61E224KE01D | 25V X5R 10% | Extended | C76936 (Murata, 10V), C76932 (6.3V) |
| C 0402 | 10uF | C15525 | Samsung CL05A106MQ5NUNC | 6.3V X5R 20% | **Basic** | C315248 (Samsung CL05A106MP5NUNC, 10V, Extended) |
| C 0402 | 15pF | C1548 | FH 0402CG150J500NT | 50V C0G 5% | **Basic** | C106997 (Yageo, Extended) |
| C 0402 | 4.7uF | C23733 | Samsung CL05A475MP5NRNC | 10V X5R 20% | **Basic** | C368809 (10%, Extended) |
| C 0603 | 22uF | C59461 | Samsung CL10A226MQ8NRNC | 6.3V X5R 20% | **Basic** | C86295 (Samsung CL10A226MP8NUNE, 10V, Extended) |

LCSC product pages use the form `https://www.lcsc.com/product-detail/<C-number>.html`. The JLC API records `lcscGoodsUrl` for each part.

### Review (link & review agent)
- Pad position, size and layers diffed line-by-line against KiCad 10.0.3 stock `{R,C}_<size>_<metric>Metric` for all 10 sizes: identical (only the roundrect ratio is written with 4 decimals instead of 6 on 0805/1206, a negligible <0.0001 difference).
- All 10 STEP files are byte-identical to the KiCad 10.0.3 stock models; model paths use `${KIPRJMOD}/../../libraries/3dmodels/`, offset/rotation 0. Renders checked: body centred, terminations on pads.
- UUIDs are unique across the whole `APEX_FOOTPRINTS.pretty`.
- SVG exports of C_0201, C_0805 and R_1206 checked: silk is clear of copper, and the courtyard encloses pads and body.

### Open issues
- No JLCPCB Basic parts exist in 0201. All 8 of DEV-G2-NANO's 0201 values are Extended, which adds a loading fee per unique part (8 extra). Changing to 0402 Basic parts (for example C1525 100nF, C25744 10k) would avoid that if board space allows.
- DEV-G2-NANO gives no voltage ratings. Check the 6.3V picks (C 0201 1uF C76929, C 0402 10uF C15525 Basic, C 0603 22uF C59461 Basic) against the rail voltages. On a 5V USB/VBUS rail, use the 10V alternative.
- Courtyards are now larger than stock/V1 (0.25 mm margin per spec instead of the 0.15 mm used by stock 0201/0402). Dense 0201 decoupling that was placed against the stock courtyards may raise courtyard-overlap DRC warnings.
- The silk lines extend slightly beyond the courtyard in y on 0201 (0.505 vs 0.45) and on 0805 (≈0.05 mm). This is acceptable under the spec, but 0201 silk is often dropped on dense boards, so decide whether to keep it.
- No pin-1 marker or fab chamfer on these non-polarized parts (spec rule written for ICs). Add them if the user wants strict uniformity.

## Generic L / FB / LED / diode / SOT-23 footprints

- **Footprints** (`APEX_FOOTPRINTS.pretty`):
  - Inductors and beads: `L_0402`, `L_0603`, `L_0805`, `FB_0402`, `FB_0603`
  - LEDs: `LED_0402`, `LED_0603`, `LED_0805`
  - Diodes: `D_SOD-123`, `D_SOD-323`, `D_SOD-523`, `D_SMA` (DO-214AC)
  - Transistor/dual-diode package: `SOT-23`
  - `L_1008` is owned by the Inductors unit and is not part of this unit.
- **Origin:** generic packages used by DEV-G2-NANO (CERN-OHL-P). Because the parts are not specific, the copper is IPC-7351 nominal, taken from the KiCad 10 stock libraries:
  - `Inductor_SMD:L_*_Metric`
  - `LED_SMD:LED_*_Metric`
  - `Diode_SMD:D_SOD-123/323/523`, `D_SMA`
  - `Package_TO_SOT_SMD:SOT-23`
- **Copper:** pad size and position match stock exactly. This was checked numerically against the stock `.kicad_mod` for all 13 footprints.
  - `FB_0402` and `FB_0603` use the stock `L_0402` and `L_0603` copper.
  - Pads are roundrect, ratio 0.25. `D_SMA` keeps the stock ratio of 0.1389.
  - The stock `D_SOD-523` pads are rotated 180°. The rotation was dropped because the pads are symmetric, so the geometry is identical.
- **Style:** follows the APEX `R_0402`/`C_0402` style.
  - `REF**` on F.SilkS at 1/0.15. Value hidden on F.Fab. `${REFERENCE}` on F.Fab.
  - Datasheet and Description are hidden. `LCSC` is empty and hidden on F.SilkS at 1/0.1, because the LCSC number is set per placed part.
  - Every file has fresh UUIDs.
- **Pin 1 / polarity:**
  - **LED_\* and D_\*:** pad 1 is the **cathode**, at −X. This matches the generic `LED`, `D`, `D_Schottky`, `D_Zener` and `D_TVS` symbols, where pin 1 = K and pin 2 = A. `D_TVS_Bidir` uses A1/A2.
    - Silk: a bracket closed on the cathode side.
    - Fab: a body outline with a chamfer at the pad-1 corner, plus a cathode band line.
  - **L_\* and FB_\*:** non-polar. The silk is the top and bottom edge lines only.
  - **SOT-23:** stock numbering. Pins 1 and 2 are on −X and pin 3 is on +X, the same as `BAT54C_SOT23_Nexperia`.
    - Silk: a pin-1 dot. Fab: a chamfer at pin 1.
    - With `D_Schottky_x2_KCom` (1 = A1, 2 = A2, 3 = K) this gives the BAT54C pinout.
- **Clearances** (measured):
  - Silk to copper is at least 0.150 mm on every footprint. The minimum is 0.150 mm on the 0603 and LED_0805 parts, 0.155 mm on the 0402 parts, 0.175 mm on the diodes and L_0805, and 0.225 mm on SOT-23.
  - The courtyard (0.05 width) is at least 0.25 mm outside the pads and body, on a 0.05 grid, and it encloses the silk.
- **3D models:** KiCad 10 stock STEP files. Each copy in `libraries/3dmodels/` is byte-identical to the stock file.
  - Files: `L_0402/0603/0805_*Metric.step`, `LED_0402/0603/0805_*Metric.step`, `D_SOD-123.step`, `D_SOD-323.step`, `D_SOD-523.step`, `D_SMA.step`, `SOT-23.step`.
  - Linked as `${KIPRJMOD}/../../libraries/3dmodels/<name>.step`, with offset and rotation 0 (the same as the stock footprints).
  - `FB_*` reuse the `L_*` models.
  - Renders (`render_fp.py`) confirm the alignment:
    - The cathode band sits on pad 1 and on the silk-bracket side for SOD-123, SOD-323, SOD-523 and SMA.
    - The SOT-23 model's pin-1 dot sits at pad 1.
    - The LED, L and FB bodies are centred on their pads.
- **Symbol filters** (`APEX_Symbols.kicad_sym`): all generic symbols match the new footprints, so no edits are needed.
  - `L`: `L_* ...`
  - `FB`: `FB_* L_0402* L_0603*`
  - `LED`: `LED_*`
  - `D`, `D_Schottky`, `D_Zener`, `D_TVS`, `D_TVS_Bidir`: `D_SOD* D_SMA* ...`
  - `D_Schottky_x2_KCom`: `SOT?23*`
  - `check_sym.py` reports matching pin and pad sets for every symbol/footprint pair.
- **Suggested JLCPCB parts** for DEV-G2-NANO values. Each was verified on its LCSC page:
  - Red 0603 LED: [C2286](https://www.lcsc.com/product-detail/C2286.html), Hubei KENTO KT-0603R. Basic part; use `LED_0603`.
  - 120R@100MHz bead, 0402: [C89458](https://www.lcsc.com/product-detail/Ferrite-Beads-And-Chips_TDK_MMZ1005F121ET000_120R-25_C89458.html), TDK MMZ1005F121ET000. Extended part; 200 mA, 1.5 Ω max; use `FB_0402`.
  - 120R@100MHz bead, Basic alternative: [C14709](https://www.lcsc.com/product-detail/C14709.html), Murata BLM18PG121SN1D. 0603, 2 A, 50 mΩ; use `FB_0603`.

### Open issues
- **0402 bead decision:** use Basic C14709 and move to `FB_0603`, or accept Extended C89458 on `FB_0402`. DEV-G2-NANO used an MMZ1005 120R bead.
- **10 uH 1008 inductor (L1):** no Basic or Preferred-Extended 1008 part exists, and no LCSC number was verified, so the field is left empty. The Basic 10 uH parts, C1035 (0603) and C1046 (0805), are multilayer parts rated only 3 mA and 15 mA. They suit signal-level current only.
- **Cosmetic:** `FB_*` show a chip-inductor 3D body. The stock LED models have no top-side cathode mark, so orientation is shown by the silk bracket and fab band only.
- **Not this unit:** the generic L, FB and D symbols use compact V1 pin lengths (1.27 and 3.175 mm), which `check_sym.py` flags against 2.54 mm. The spec allows this for generic 2-pin parts. No action is needed.

# Inter-board connectors (added by the user, completed 2026-10-21)

## Samtec Tiger Eye TFM / SFM (1.27 mm 2x20 board-to-board)

- Devices: a mating stacking pair, 1.27 mm pitch, 2x20 = 40 positions, vertical SMT, both with `-A` alignment pins.
  - `TFM-120-22-L-D-A`: male terminal strip, lead style -22, -L plating.
  - `SFM-120-02-L-D-A`: female socket strip, lead style -02, -L plating. The "X" in the user's part name `SFM-120-02-X-D-A` is the plating code, and the real part is **L**. Samtec offers SFM only in -F and -L. The user's model file name and the LCSC listing both use -L.
- Stack height: 9.86 mm (0.388 in) fully mated, 10.24 mm (0.403 in) max, from the Samtec "XFM Mated Views" document, Table 1 (SFM -02 with TFM -22).
- Primary sources (Samtec):
  - [TFM print, Rev GB](https://suddendocs.samtec.com/prints/tfm-1xx-xx-xxx-d-xxx-x-xx-mkt.pdf)
  - [TFM footprint, Rev Q](https://suddendocs.samtec.com/prints/tfm-1xx-x2-xxx-d-xx-footprint.pdf)
  - [SFM print, Rev EB](https://suddendocs.samtec.com/prints/sfm-1xx-xx-xxx-d-xxx-x-xx-mkt.pdf)
  - [SFM/SFC footprint, Rev K](https://suddendocs.samtec.com/prints/sfm-dv%20&%20sfc-dv%20footprint.pdf)
  - [XFM mated views](https://suddendocs.samtec.com/prints/xfm%20mated%20document.pdf)
  - The older `...-d-xxx-mkt.pdf` prints (TFM Rev FQ, SFM Rev DV) are superseded. Symbol and footprint Datasheet fields both point to the newer `-x-xx-` URLs.
- LCSC:
  - SFM-120-02-L-D-A: [C3322789](https://www.lcsc.com/product-detail/Female-Headers_Samtec-SFM-120-02-L-D-A_C3322789.html). It is the exact part number but was out of stock when checked.
  - TFM-120-22-L-D-A: not listed at LCSC or JLCPCB, so the field is empty. Buy it from Samtec, DigiKey or Arrow.
- Origin: the user's own APEX symbols, footprints and models. This pair is not from DEV-G2-NANO.
- Symbols: `APEX_Symbols:TFM-120-22-L-D-A` and `APEX_Symbols:SFM-120-02-X-D-A`.
  - Geometry and pins are the user's connector style and were not changed: 2.54 mm pitch, 5.08 mm pins, odd pins on the left, even pins on the right, Reference J, all pins passive. This was verified byte-identical to the originals.
  - Properties added: Datasheet, Description, LCSC, ki_keywords, and ki_fp_filters (`SAMTEC_TFM-120-22-*-D-A`, `SAMTEC_SFM-120-02-*-D-A`).
  - The Footprint fields link to `APEX_FOOTPRINTS:SAMTEC_TFM-120-22-L-D-A` and `APEX_FOOTPRINTS:SAMTEC_SFM-120-02-X-D-A`.
  - Datasheet, Description and LCSC are identical on each symbol and its footprint.
  - `check_sym.py` reports pin set == pad set (01..40) for both, with no mounting pads. The alignment holes are unnumbered NPTH. Its only flags are the 5.08 mm pin length and 2.54 mm pitch, which are the intended connector style.
- Footprints: the user's copper was kept. Samtec land patterns were used as the reference.
  - TFM: pad 01 is at (-12.065, +1.715), bottom-left, with odd pads on the +y row. The alignment holes are 1.42 mm NPTH at ±13.655 mm.
  - SFM: pad 01 is at (+12.065, +1.365), bottom-right. This is the mirror of the TFM, as on Samtec's drawing.
  - Mating: when the SFM board is flipped onto the TFM, SFM pin n lands on TFM pin n and the polarization keys agree, so both symbols use the same net-to-pin mapping.
  - Annotation changes:
    - Fab outline with a pin-1 chamfer, and `${REFERENCE}` on F.Fab.
    - Value hidden on F.Fab.
    - The duplicated TFM fab lines were cleaned up.
    - Silkscreen and courtyard were not touched; they pass the ≥0.15 mm silkscreen and ≥0.25 mm courtyard rules.
  - Copper deviations from Samtec are listed under Open issues.
- 3D models: the user's Samtec STEP files, `TFM-120-22-L-D-A.stp` and `SFM-120-02-L-D-A.stp`, referenced as `${KIPRJMOD}/../../libraries/3dmodels/...`.
  - `render_fp.py` top views show both bodies centred, the leads on the pads, and the alignment posts on the NPTH holes.
  - The TFM polarization notch sits at the +x/−y corner. The SFM key sits at the −x/−y corner, which coincides with the TFM notch when the SFM board is mirrored.

### Open issues
- **Rename SFM-120-02-X-D-A to SFM-120-02-L-D-A?** The symbol name, Value and footprint name still contain "X", so the BOM Value will read "-X-". Renaming requires changing the symbol name, the Value, the footprint file, and the symbol Footprint field together. The ki_fp_filter already matches either name.
- **TFM pad length:** the pads are 0.74 x 2.79 mm, and Samtec Rev Q specifies 0.74 x 2.92 mm with the same ±1.715 mm centres. The gap between rows is 0.64 mm instead of 0.51 mm. Copper was left unchanged; lengthen the pads to match Samtec if desired.
- **SFM alignment holes:** they are 1.42 mm NPTH, and Samtec Rev K specifies 1.35 mm (0.053 in). The 1.42 mm value looks copied from the TFM. Copper was left unchanged.
- **TFM -L plating:** the TFM print says 15 µin gold for -L, while the catalog says 10 µin. The Description avoids stating a thickness.
- **TFM LCSC:** none exists, so the part must be sourced outside JLCPCB, or a consigned part used for assembly.
- **Cosmetic:** the TFM symbol Reference is at x = -8.12, slightly off the 1.27 mm grid (the SFM uses -7.62). The silkscreen pin-1 dots sit just outside the courtyard, which breaks no rule.
- **Extra symbol fields:** the user's PARTREV, STANDARD, MAXIMUM_PACKAGE_HEIGHT and MANUFACTURER fields were left as they were. SFM PARTREV "Q" does not match the current SFM print (Rev EB). Consider deleting or updating it.

## EHF-120-01-L-D

- **Device:** Samtec EHF-120-01-L-D. It is a 1.27 mm (0.050 in) pitch, 2x20 (40-position) shrouded IDC header with ejector latches, through-hole, vertical. "-L" means 10 µin gold in the contact area with a matte tin tail.
- **Mates with:** Samtec FFSD-20-D IDC ribbon cable assemblies and FFTP. It does not fit FFSD cables built with the -SR strain-relief option (catalog note F-226).
- **Primary sources:**
  - Samtec print EHF-1XX-01-X-D-XX-XX-XX-X-XX Rev AM, sheet 1 (body 39.88 x 6.67 mm); sheet 3, Fig 8 (ejector application view). https://suddendocs.samtec.com/prints/ehf-1xx-01-x-d-xx-xx-xx-x-xx-mkt.pdf (Datasheet on both the symbol and the footprint).
  - Samtec "Recommended PCB layout for EHF-1XX-01-X-D-XX-XX-XX" Rev A, through-hole option: https://suddendocs.samtec.com/prints/ehf-1xx-01-x-d-xx-xx-xx-footprint.pdf
  - Catalog: https://suddendocs.samtec.com/catalog_english/ehf.pdf
- **LCSC:** none. LCSC/JLCPCB do not stock the through-hole part, so the property is empty on both the symbol and the footprint.
  - Buy it from DigiKey: https://www.digikey.com/en/products/detail/samtec-inc/EHF-120-01-L-D/1106570
  - LCSC lists only the surface-mount versions: -SM C7434808, -SM-LC C17693080, -SM-TR C17653183. These need a different footprint.
- **Origin:** the user's own footprint and 3D model; not DEV-G2-NANO. The symbol is new.
- **Symbol `EHF-120-01-L-D`:**
  - It copies the geometry of the user's `TFM-120-22-L-D-A`: body ±7.62 x -25.4..27.94; pins 5.08 mm long at x = ±12.7 on a 2.54 mm pitch.
  - Odd pins 01..39 are on the left and even pins 02..40 on the right, top to bottom. All pins are passive and the Reference is J.
  - Properties: Footprint `APEX_FOOTPRINTS:SAMTEC_EHF-120-01-L-D`, `ki_fp_filters` `SAMTEC_EHF-120-01-L-D*`, MANUFACTURER, STANDARD and `ki_keywords`.
  - `check_sym` flags pin length and 150 mil spacing. Both are expected because the connector style overrides the IC rules. The pin set matches the pad set exactly (01..40).
- **Footprint `SAMTEC_EHF-120-01-L-D`:**
  - The user's copper is unchanged and matches the Samtec layout: 0.71 mm PTH, 1.27 x 1.27 mm grid, 1.06 mm pads.
  - Pad 01 (square) is at (-12.065, +0.635), with the odd row on +Y and pad 02 directly above pad 01.
  - Added `descr`, `tags`, Datasheet, Description and an empty LCSC property. The Value is now hidden.
  - Rebuilt the F.Fab outline with a pin-1 chamfer and a key-slot notch, and added `${REFERENCE}`. Silk and courtyard were left as the user drew them.
  - Datasheet, Description and LCSC are now identical between the symbol and the footprint.
- **3D model:** `EHF-120-01-L-D.stp`, a Samtec/CADENAS STEP, referenced as `${KIPRJMOD}/../../libraries/3dmodels/EHF-120-01-L-D.stp` with rotation (-90, 0, 0) and offset 0.
  - Checked with a render_fp top and tilt render: the pins sit in the holes, and the shroud's molded pin-1 triangle and polarization key slot are both on the pad-01 (+Y, odd-row) side at the pad-01 end.
  - This is consistent with the symbol's odd/even split and the footprint's pin-1 marks.

### Open issues
- There is no LCSC part for the through-hole header, so it can't be assembled at JLC as is. If JLC assembly is needed, switch to EHF-120-01-L-D-SM (C7434808) and make a new surface-mount footprint.
- The courtyard (±20.19 mm) covers only the closed body. The ejectors reach about 1.8 mm further at each end when open (43.56 mm REF), so consider enlarging the courtyard or keeping tall parts clear.
- The silk pin-1 dot at (-20.59, 0.635) sits about 0.4 mm outside the courtyard. It is harmless and was left as the user drew it.
- `libraries/3dmodels/EHF-120-01-L-D.stp` has permissions 0600; consider `chmod 644` before committing.
- The symbol's Value and Reference placement and its 1.016 pin font follow the TFM style, not the IC-rule placement and sizes. This is intentional.

## EHT-120-01-L-D (Samtec 2.00 mm 2x20 shrouded IDC ejector header)

- **Device/package:** Samtec EHT-120-01-L-D. It is a 2.00 mm pitch, 2x20 (40-position) shrouded IDC ejector box header that mounts vertically through-hole. Posts are 0.50 mm square. "-L" plating means 10 µin (0.25 µm) gold on the post and matte tin on the tail. This is the variant without strain relief and with no position omitted.
- **Mating part:** Samtec TCSD 2.00 mm IDC/discrete socket cable assemblies (TCSD-20-D-xx.xx-01-x). An EC2-20 ejector cap is optional. EHT does not mate with TCMD; TCMD mates only the sibling ETMM series.
- **Primary source:** Samtec print EHT-1XX-01-XX-D-XX-XX-XX-X-XX-MKT rev BN, https://suddendocs.samtec.com/prints/eht-1xx-01-xx-d-xx-xx-xx-x-xx-mkt.pdf
  - Sheet 1, Fig 1: body 53.79 x 7.90 mm, row pitch 2.00 mm, 0.50 mm square tail.
  - Sheet 3: latch-open length 59.89 mm.
  - Catalog: https://suddendocs.samtec.com/catalog_english/eht.pdf (page F-226).
  - Through-hole size reference: https://www.samtec.com/support/pcb-hole-sizes/
- **LCSC:** none for the exact MPN, so the property is present and empty on both the symbol and the footprint. Buy from Samtec, Mouser or DigiKey. Listed variants that are not drop-in replacements:
  - C17251386: -S-D-RA (right-angle)
  - C17528950: -S-D-RA-40 (right-angle, pin 40 omitted)
  - C17594820: -S-D-21 (pin 21 omitted)
  - C17323678: -S-D-01 (pin 1 omitted, JLCPCB)
- **Origin:** the user supplied the footprint (a SnapEDA-style export) and the STEP model. This part does not come from DEV-G2-NANO.
- **Symbol `EHT-120-01-L-D`:** drawn in the same connector style as the user's TFM-120-22-L-D-A and SFM-120-02-X-D-A.
  - Body rectangle runs from (-7.62,-25.4) to (7.62,27.94).
  - Odd pins 1..39 are on the left at x=-12.7 and even pins 2..40 are on the right at x=12.7.
  - Pin pitch is 2.54 mm, pin length 5.08 mm, all pins passive, pin name = pin number. Reference is J.
  - Footprint is `APEX_FOOTPRINTS:CONN40_20-01-F-D-10_SAI`, with `ki_fp_filters` `CONN40_20-01-F-D-10_SAI*`.
  - Datasheet, Description and LCSC (empty) are identical on the symbol and the footprint.
  - `check_sym.py`: the pin set equals the pad set (1..40) with no mounting pads. It flags pin length and the 150 mil spacing, which is expected because connector style overrides those rules.
- **Footprint `CONN40_20-01-F-D-10_SAI`:** the user's copper is unchanged.
  - Pads are 1.27 mm round with a 0.762 mm drill on a 2.00 x 2.00 mm grid. Pad 1 is at the origin, odd pads are on y=0 and even pads on y=-2.
  - Changes:
    - Added descr, tags, Datasheet, Description and LCSC.
    - The tags said EHT-120-01-L-D-SR; they now say EHT-120-01-L-D, because the body and the model are the version without strain relief.
    - Moved REF** off the pads to (19,-6.1) and hid Value on F.Fab.
    - Redrew the fab outline to the Samtec body size, 53.79 x 7.90 mm, with a pin-1 chamfer.
    - The courtyard is now 0.05 mm wide and sits 0.25 mm outside the body (x -8.15..46.15, y -5.2..3.2).
  - Kept the user's silk outline and the pin-1 dot at (-8.91,0) on F.SilkS and B.SilkS.
- **3D model:** `libraries/3dmodels/eht-120-01-l-d.stp` (Samtec/TraceParts STEP), offset (19,1,0), rotate (-90,0,0).
  - `render_fp.py` top and zoom renders show all 40 posts centred on the pads.
  - The pin-1 end matches the silk pin-1 dot. The odd/even rows agree across symbol, footprint and model.

### Open issues
1. **Drill size:** the footprint uses a 0.762 mm drill, but Samtec recommends a 0.81 mm finished hole for a 0.50 mm square tail. The tail diagonal is about 0.71 mm, so the fit is tight once plating tolerance is added. I recommend 0.81 mm. The copper is the user's, so it was not changed.
2. **Pad 1 shape:** pad 1 is round like all the others, with no square or rectangular pin-1 pad. Pin 1 is marked only by the silk dot. Consider making pad 1 a rectangle (also the user's call).
3. **Suggested rename** (not done): `EHT-120-01-L-D_2x20_P2.00mm_Samtec`. If you rename, update the symbol's Footprint and `ki_fp_filters` at the same time.
4. **Strain relief:** confirm whether the -SR variant was intended, as the original tag suggests. It has the same hole pattern but a wider 9.40 mm body, so the fab outline and courtyard would change.
5. **No LCSC listing** for the exact MPN; it has to come from Samtec, Mouser or DigiKey.
6. **Latch clearance:** the latches open to 59.89 mm overall, about 3 mm past each end of the body. The courtyard covers only the closed body, so keep that zone clear.
7. **Grid noise:** pad coordinates are off the exact 2.000 mm grid by less than 5 µm (SnapEDA rounding). It is harmless and was left as is.

## 2045194031 (Molex Micro-Lock Plus 1.25, 2x20 RA SMT header)

- **Device:** Molex **2045194031** (204519-4031). It is a Micro-Lock Plus 1.25 mm-pitch wire-to-board PCB header: dual row (2x20, 40 circuits), right-angle, SMT, positive lock, low-halogen. The 204519 series is the low-halogen version of the 505448 series. DigiKey lists it as "1.25 MLP DUAL RA ASSY 40CKT G38" (900-2045194031-ND). It is active but not stocked there, with about a 23-week lead time.
  - "2045190002" is the Molex **sales drawing number** (2045190002-SD) for the 204519 family, not an orderable MPN. The footprint name comes from it.
- **Mating parts:**
  - Receptacle crimp housing **505432-4001**, LCSC [C519093](https://www.lcsc.com/product-detail/C519093.html).
  - Crimp terminals from the 505431 series:
    - 505431-1100 (Au, 26-30 AWG), LCSC [C505364](https://www.lcsc.com/product-detail/C505364.html).
    - 505431-1000 (tin), LCSC [C385112](https://www.lcsc.com/product-detail/C385112.html).
  - I found no off-the-shelf 40-circuit dual-row cable assembly; Molex's Micro-Lock Plus OTS cables are single row. Plan on custom crimped harnesses.
- **Primary source:** [Molex 2045194031 product page](https://www.molex.com/en-us/products/part-detail/2045194031) (sales drawing 2045190002-SD). molex.com could not be fetched, so the copper was checked against the sister-series drawing, Molex **5054480000 PSD rev B**, sheet 2, "Recommend PWB layout".
- **LCSC:** none for 2045194031. It is not on JLCPCB, and LCSC lists only 204519-1631 and 204519-3431, both out of stock. The `LCSC` property is empty on both the symbol and the footprint.
  - The layout-compatible, JLCPCB-assemblable alternative is **505448-4071**, LCSC [C17610759](https://www.lcsc.com/product-detail/C17610759.html).
- **Origin:** the user's own footprint and 3D model, added to APEX (not from DEV-G2-NANO). The symbol is new and drawn in the user's connector style.

### Symbol (`APEX_Symbols:2045194031`)
- **Style:** a copy of the user's `TFM-120-22-L-D-A` connector style:
  - body -7.62,-25.4 to 7.62,27.94
  - pins at x = ±12.7, 5.08 mm long, 2.54 mm pitch, all `passive`
  - pin font 1.016, Reference `J`
- **Pins:** odd pins 1-39 on the left and even pins 2-40 on the right, pin 1 at the top. Pin numbers are "1"-"40" to match the pad names. Pin names repeat the numbers.
- **Properties:**
  - Footprint `APEX_FOOTPRINTS:CONN_2045190002-SD_40P_MOL`, with ki_fp_filters `CONN_2045190002-SD*`.
  - Datasheet, Description and LCSC (empty) are identical on the symbol and the footprint.
  - MANUFACTURER is "Molex", and ki_keywords is set.
- **check_sym.py:** the 40 pins match pads 1-40. The only flags are the expected ones:
  - 5.08 mm pin length and 2.54 mm pitch, which the connector style overrides.
  - Pads 41/42 are not in the symbol; they are the intentional mounting tabs.

### Footprint (`CONN_2045190002-SD_40P_MOL`)
- **Copper:** the user's copper is unchanged.
  - 40 signal pads, 0.8382 x 2.0574 mm, at 1.25 mm pitch.
  - Two rows **directly opposite each other (not staggered)**, 7.4 mm apart. The odd row (1..39) is at y = +3.934, at the rear. The even row (2..40) is at y = -3.466, on the mating side. Pad 1 is at the bottom left (-11.875, 3.934).
  - Retention tabs 41/42 are 1.0922 x 4.953 mm at (±14.075, -1.341).
  - Pitch, span (23.75), row spacing and tab centres all match the Molex 505448 layout exactly.
  - Pads are about 0.04-0.1 mm oversize against Molex (0.8 x 2.0 signal, 1.0 x 4.85 tab), which looks like imperial rounding. That leaves a 0.41 mm gap between pads instead of 0.45. It is reported, not changed.
- **Edits by the footprint pass:**
  - Added `descr`/`tags`, Datasheet, Description and a hidden empty LCSC property.
  - Moved REF** outside the body to (0, -5.75).
  - Courtyard width 0.05, rounded to ±15.05 x (-4.75 .. +5.25).
- **Link pass:** the footprint Description was set to the same text as the symbol Description.

### 3D model (`MOLEX_ML-40.stp`)
- **Source:** Molex's own STEP (product "2045194031"), linked as `${KIPRJMOD}/../../libraries/3dmodels/MOLEX_ML-40.stp`, offset (-11.8, 6, 4.5), rotation z = -180.
  - The body sits on the board.
  - The mating opening faces -Y, over the even row.
  - The rear tails land on the odd pads, and the pin-1 end is at the silkscreen pin-1 dot.
  - The retention nails sit on pads 41/42.
  - Symbol pin 1 (top left) = pad 1 (bottom-left, rear row) = model pin 1. The odd/even split is consistent across symbol, footprint and model.

### Open issues
- **Variant.** Confirm that 2045194031 is intended. It is G38 plated, bulk packed and not stocked at DigiKey (about a 23-week lead time). For JLCPCB assembly, **505448-4071 (C17610759)** fits the same footprint.
- **Molex drawing not read.** 2045190002-SD itself could not be downloaded. The copper was verified against the 505448 sister-series layout, and the oversize pads (+0.04-0.1 mm) were left as drawn.
- **Pads 41/42.** They are numbered mechanical tabs with no symbol pin, so they get no net. If you want them on GND, or want a clean parity check, either add passive pins 41/42 to the symbol or rename the pads to "" or "MP".
- **Pin naming.** Pin numbers are "1".."40", while your Samtec symbols use "01". This is intentional, because they must match this footprint's pad names.
- **Annotations left as you drew them:**
  - A pin-1 dot on B.SilkS, which prints on the back of the board.
  - The Value on F.Fab is visible and overlaps `${REFERENCE}`.
  - The fab outline has no pin-1 chamfer and is only 0.0254 wide.
  - The F.SilkS pin-1 dot sits slightly outside the courtyard (x ≈ -16.4).

> LCSC numbers added afterwards by the sourcing research (2026-10-21; Samtec stock at LCSC is single digits, so recheck before ordering): TFM-120-22-L-D-A C17491812, EHF-120-01-L-D (through-hole) C7437447, EHT-120-01-L-D C17523594. SFM-120-02-L-D-A is C3322789 (0 in stock); SFM-120-02-L-D-TR C3323111 is the stocked alternative.
