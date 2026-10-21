#!/usr/bin/env python3
"""check_sym.py <lib.kicad_sym> <SymbolName> [footprint.kicad_mod]
Prints properties and pins, checks 50 mil grid, pin length, side spacing, and pin-vs-pad number sets."""
import re, sys
t = open(sys.argv[1]).read(); name = sys.argv[2]
i = t.index(f'\t(symbol "{name}"\n'); j = t.find('\n\t(symbol "', i+5); j = len(t) if j < 0 else j
blk = t[i:j]
props = dict(re.findall(r'\(property "([^"]+)" "([^"]*)"', blk))
for k in ['Reference','Value','Footprint','Datasheet','Description','LCSC']: print(f'{k:12}: {props.get(k,"<MISSING>")!r}')
pins = re.findall(r'\(pin (\w+) (\w+)\s*\(at ([-\d.]+) ([-\d.]+) (\d+)\)\s*\(length ([\d.]+)\)(.*?)\(name "([^"]*)".*?\(number "([^"]*)"', blk, re.S)
print(f'{len(pins)} pins')
grid = lambda v: abs(float(v)/1.27 - round(float(v)/1.27)) < 1e-6
bad = []
sides = {}
for typ, shape, x, y, rot, ln, mid, nm, num in pins:
    print(f'  {num:>4} {nm:20} {typ:15} at ({x},{y}) rot {rot} len {ln}{" HIDDEN" if "(hide yes)" in mid else ""}')
    if not (grid(x) and grid(y)): bad.append(f'pin {num} off 50mil grid')
    if ln != '2.54': bad.append(f'pin {num} length {ln} != 2.54')
    sides.setdefault(rot, []).append(float(y) if rot in ('0','180') else float(x))
for rot, v in sides.items():
    v = sorted(set(v)); sp = sorted(set(round(b-a,3) for a,b in zip(v,v[1:])))
    print(f'  side rot={rot}: spacings {sp}')
    if any(abs(s/3.81 - round(s/3.81)) > 1e-6 for s in sp): bad.append(f'side {rot} spacing not a multiple of 150 mil: {sp}')
if len(sys.argv) > 3:
    pads = set(re.findall(r'\(pad "([^"]*)"', open(sys.argv[3]).read())) - {''}
    nums = set(p[8] for p in pins)
    print('pads not in symbol:', sorted(pads-nums), '| pins not in footprint:', sorted(nums-pads))
    if pads != nums: bad.append('pin/pad number sets differ')
print('ISSUES:', bad if bad else 'none')
