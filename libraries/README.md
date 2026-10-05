# APEX KiCad library workflow

This library is the source for APEX V2 symbols and footprints. The APEX V1 KiCad project under `/Users/loganrohlfs/Documents/KiCad/APEX-2026` is the visual style reference. Its original `symbols/LR_Sensor.kicad_sym` and `footprints/LR_Sensor.pretty` libraries are still on disk and should be consulted before drawing a new part. Use the exact package option when checking a footprint; confirm what any ordering suffix means from the manufacturer.

For each new part:

1. Save the manufacturer's product page, current datasheet revision, package drawing, and recommended PCB land pattern in a part note. Check whether the manufacturer links a CAD model and compare it with the datasheet.
2. Make a pin table with every pad number, exact datasheet name, electrical role, and any required connection or allowed no-connect state. Check the table against the package pin-one marker.
3. Add one symbol to `symbols/APEX_Symbols.kicad_sym`. Use the V1 conventions: a pale filled rectangle with no visible outline, reference and value at the upper left and right corners, supply pins at the top, grounds at the bottom, serial pins at the left, and interrupts and reserved pins at the right. Use a **50 mil (1.27 mm) base grid** for the body and every pin connection; use 100 mil (2.54 mm) between neighboring pins where space permits. Keep all pin numbers visible. Widen a symbol if full multifunction pin names would overlap. Assign electrical pin types for KiCad ERC.
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
