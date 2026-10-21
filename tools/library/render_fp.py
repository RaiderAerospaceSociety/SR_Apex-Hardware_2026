#!/usr/bin/env python3
"""render_fp.py <footprint.kicad_mod> <out_prefix> [model_z_rotation_override]
Places the footprint on a blank board and writes <out_prefix>_top.png and <out_prefix>_tilt.png
via kicad-cli 3D render. Model paths using ${KIPRJMOD}/../../libraries resolve to the repo libraries."""
import sys, re, os, subprocess, hashlib
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KCLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
TPL=REPO+'/templates/apex-template-2026/apex-template-2026.kicad_pcb'
import tempfile
SCR=os.path.join(tempfile.gettempdir(),'apex_render_fp')
fp, outp = sys.argv[1], sys.argv[2]
rot = sys.argv[3] if len(sys.argv) > 3 else None
tag = hashlib.md5((fp+outp).encode()).hexdigest()[:8]
root = f'{SCR}/render/{tag}'; os.makedirs(root+'/a/b', exist_ok=True)
link = root+'/libraries'
if not os.path.islink(link): os.symlink(REPO+'/libraries', link)
lines = open(TPL).read().split('\n')
cut = next(i for i,l in enumerate(lines) if re.match(r'\t\((footprint|gr_|segment|via|zone|group|embedded_fonts|generated|net )', l))
f = open(fp).read()
f0 = f  # measure extents before injecting placement
name = re.match(r'\(footprint "([^"]+)"', f).group(1)
f = f.replace(f'(footprint "{name}"', f'(footprint "APEX_FOOTPRINTS:{name}"', 1)
f = f.replace('(layer "F.Cu")', '(layer "F.Cu")\n\t(at 100 100)', 1)
if rot is not None:
    f = re.sub(r'\(rotate\s*\(xyz ([-\d.]+) ([-\d.]+) [-\d.]+\)', lambda m: f'(rotate (xyz {m.group(1)} {m.group(2)} {rot})', f)
xs = [float(v) for v in re.findall(r'\(at ([-\d.]+) [-\d.]+',f0)] + [float(v) for v in re.findall(r'\((?:start|end|center) ([-\d.]+)',f0)]
ys = [float(v) for v in re.findall(r'\((?:start|end|center) [-\d.]+ ([-\d.]+)',f0)]
r = max([abs(v) for v in xs+ys] + [2]) + 1.0
edge = '\n'.join(f'(gr_line (start {100+a} {100+b}) (end {100+c} {100+d}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts"))'
                 for a,b,c,d in [(-r,-r,r,-r),(r,-r,r,r),(r,r,-r,r),(-r,r,-r,-r)])
pcb = f'{root}/a/b/r.kicad_pcb'
open(pcb,'w').write('\n'.join(lines[:cut])+'\n'+f+'\n'+edge+'\n)\n')
for view, extra in [('top', []), ('tilt', ['--rotate', '-40,0,25'])]:
    out = f'{outp}_{view}.png'
    res = subprocess.run([KCLI,'pcb','render','-o',out,'-w','800','-h','800','--zoom','1.2','--quality','high',*extra,pcb], capture_output=True, text=True)
    print(view, 'OK' if os.path.exists(out) else 'FAILED', res.stdout.strip().splitlines()[-1:] , res.stderr.strip()[-300:])
