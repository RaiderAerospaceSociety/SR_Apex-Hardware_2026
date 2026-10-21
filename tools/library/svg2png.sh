#!/bin/zsh
# svg2png.sh <file.svg> [px]  -> writes <file.svg>.png scaled so the drawing fills ~px pixels (default 900)
f=$1; px=${2:-900}; d=$(dirname $f)
python3 -I - "$f" "$px" <<'PY'
import re,sys
p,px=sys.argv[1],int(sys.argv[2]); t=open(p).read()
vb=re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"',t)
w,h=float(vb.group(3)),float(vb.group(4)); s=px/max(w,h)
t=re.sub(r'(<svg[^>]*?)\swidth="[^"]*"',r'\1',t,1); t=re.sub(r'(<svg[^>]*?)\sheight="[^"]*"',r'\1',t,1)
t=t.replace('<svg','<svg width="%dpx" height="%dpx"'%(w*s,h*s),1)
open(p,'w').write(t)
PY
qlmanage -t -s $px -o $d $f >/dev/null 2>&1; ls $f.png
