import re,glob,os,sys
import os
R=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'libraries')
t=open(R+'/symbols/APEX_Symbols.kicad_sym').read()
blocks=re.split(r'\n(?=\t\(symbol ")',t)[1:]
fps={os.path.basename(f)[:-10]:open(f).read() for f in glob.glob(R+'/footprints/APEX_FOOTPRINTS.pretty/*.kicad_mod')}
prob=[]
for b in blocks:
    n=re.match(r'\t\(symbol "([^"]+)"',b).group(1)
    p=dict(re.findall(r'\(property "([^"]+)" "([^"]*)"',b))
    fp=p.get('Footprint','')
    if fp:
        lib,_,name=fp.partition(':')
        if lib!='APEX_FOOTPRINTS' or name not in fps: prob.append(f'{n}: Footprint {fp!r} not in APEX_FOOTPRINTS'); continue
        fl=re.search(r'\(property "LCSC" "([^"]*)"',fps[name]); fl=fl.group(1) if fl else None
        if (p.get('LCSC') or '')!=(fl or ''): prob.append(f'{n}: LCSC sym={p.get("LCSC")!r} fp={fl!r}')
        pads=set(re.findall(r'\(pad "([^"]+)"',fps[name])); pins=set(re.findall(r'\(number "([^"]+)"',b))
        if pins-pads: prob.append(f'{n}: pins not on footprint {sorted(pins-pads)[:8]}')
    if 'LCSC' not in p and '(power' not in b and not n.startswith(('Test-','M3_')): prob.append(f'{n}: no LCSC property')
    if re.search(r'\(pin power_out[^\n]*\n[^\n]*\n[^\n]*\n\s*\(name "GND',b): prob.append(f'{n}: GND pin power_out')
for name,f in fps.items():
    for m in re.findall(r'\(model "([^"]+)"',f):
        if not m.startswith('${KIPRJMOD}/../../libraries/3dmodels/'): prob.append(f'fp {name}: non-standard model path {m}')
        elif not os.path.exists(R+'/3dmodels/'+m.split('/3dmodels/')[1]): prob.append(f'fp {name}: model missing {m}')
    if not re.search(r'\(model ',f): prob.append(f'fp {name}: no 3D model')
    if not re.search(r'\(property "LCSC"',f): prob.append(f'fp {name}: no LCSC property')
print(len(blocks),'symbols,',len(fps),'footprints'); print('\n'.join(prob) or 'no problems')
