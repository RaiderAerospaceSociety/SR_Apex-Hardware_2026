# Build a simplified, dimensionally accurate STEP of Same Sky UJ20-C-H-G-SMT-5-P16-TR
# from the datasheet mechanical drawing (rev 1.01, 09/12/2024, p.2) and PCB layout (p.3).
# Model coordinates = KiCad footprint coordinates with Y flipped (model Y = -footprint y),
# Z up, Z=0 = PCB top surface. So the footprint needs offset 0, rotate 0.
import sys
import cadquery as cq

out = sys.argv[1]

W = 8.94          # body/shell width (p.2 top view)
D = 7.35          # body depth (p.2 top view)
H = 3.16          # shell height (p.2 side view); centred on CH=1.63 -> z 0.05..3.21
CH = 1.63         # opening centre height above PCB
FRONT = 3.965     # footprint y of the front face (flush with product/PCB edge)
REAR = FRONT - D  # -3.385
OW, OH = 8.34, 2.56   # receptacle opening (USB-C standard, p.2 front view)
CAV = 4.80        # cavity depth to tongue root (section A-A)
TW, TT, TL = 6.69, 0.70, 4.45  # tongue width, thickness, length (section A-A)
HOUS = 1.0        # rear plastic housing band length


def my(y):  # footprint y -> model y
    return -y


def stadium(w, h, y0, y1):
    """Stadium (obround) prism, profile in XZ centred at (0, CH), spanning footprint y0..y1."""
    length = abs(y1 - y0)
    s = (cq.Workplane("XZ", origin=(0, my(y0), CH))
         .slot2D(w, h, 0).extrude(length))  # XZ normal is -Y in model -> +footprint y... check below
    return s


def prism_fp(y_from, y_to, w, h):
    # Build along model Y explicitly to avoid workplane-normal ambiguity.
    ya, yb = sorted((my(y_from), my(y_to)))
    s = (cq.Workplane("XZ").slot2D(w, h, 0).extrude(-(yb - ya))  # XZ normal = -Y; negative extrude -> +Y
         .translate((0, ya, CH)))
    return s


# Shell: full stadium from front to start of rear housing band
shell = prism_fp(FRONT, REAR + HOUS, W, H)
cavity = prism_fp(FRONT + 0.01, FRONT - CAV, OW, OH)
shell = shell.cut(cavity)

# Rear plastic housing band (black)
housing = prism_fp(REAR + HOUS, REAR, W, H)
# Tongue (black plastic) inside the cavity, from root back towards the front
ty0, ty1 = FRONT - CAV, FRONT - CAV + TL
tongue = (cq.Workplane("XY").box(TW, abs(ty1 - ty0) + 0.05, TT)
          .translate((0, my((ty0 + ty1) / 2), CH)))
# Contact strips on tongue (gold), simplified: 12 per side at 0.5 pitch
contacts = None
for i in range(12):
    x = -2.75 + 0.5 * i
    for zs in (+1, -1):
        c = (cq.Workplane("XY").box(0.25, TL - 0.8, 0.03)
             .translate((x, my((ty0 + ty1) / 2 + 0.3), CH + zs * (TT / 2 + 0.015))))
        contacts = c if contacts is None else contacts.union(c)
# Locating pegs (plastic), dia 0.6, 0.68 below PCB (p.2 side view)
pegs = None
for x in (-2.89, 2.89):
    p = (cq.Workplane("XY").circle(0.30).extrude(0.68 + 0.10)
         .translate((x, my(-2.315), -0.68)))
    pegs = p if pegs is None else pegs.union(p)
housing = housing.union(pegs).union(tongue)

# Shell SMT tabs: 1.2 x 1.0 feet at x 4.47..5.67, footprint y -3.315..-2.315 and 0.615..1.615
TABT = 0.20
tabs = None
for sx in (-1, 1):
    for yc in (-2.815, 1.115):
        foot = (cq.Workplane("XY").box(1.20 + 0.25, 1.0, TABT)
                .translate((sx * (4.47 + 0.60 - 0.125), my(yc), TABT / 2)))
        leg = (cq.Workplane("XY").box(TABT, 1.0, CH)
               .translate((sx * (4.47 - TABT / 2 - 0.05), my(yc), CH / 2)))
        t = foot.union(leg)
        tabs = t if tabs is None else tabs.union(t)
shell = shell.union(tabs)

# 16 SMD signal leads, 0.20 wide (p.2), 0.5 pitch inner, paired 0.25 apart under the 0.6 pads
xs = [0.25, 0.75, 1.25, 1.75, 2.275, 2.525, 3.075, 3.325]
xs = sorted([-x for x in xs] + xs)
LT = 0.15
leads = None
for x in xs:
    foot = (cq.Workplane("XY").box(0.20, 0.70, LT)
            .translate((x, my(-3.45), LT / 2)))   # fp y -3.66 .. -2.91 area
    riser = (cq.Workplane("XY").box(0.20, LT, 0.55)
             .translate((x, my(REAR - LT / 2), 0.55 / 2)))
    l = foot.union(riser)
    leads = l if leads is None else leads.union(l)

asm = cq.Assembly(name="UJ20-C-H-G-SMT-5-P16")
asm.add(shell, name="shell", color=cq.Color(0.78, 0.78, 0.80))
asm.add(housing, name="housing", color=cq.Color(0.08, 0.08, 0.08))
asm.add(contacts, name="contacts", color=cq.Color(0.86, 0.70, 0.25))
asm.add(leads, name="leads", color=cq.Color(0.86, 0.70, 0.25))
asm.save(out, exportType="STEP")

bb = cq.Workplane().add([shell.val(), housing.val(), leads.val()]).combine().val().BoundingBox()
print("bbox model X %.3f..%.3f  Y %.3f..%.3f  Z %.3f..%.3f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
print("=> footprint y %.3f..%.3f" % (-bb.ymax, -bb.ymin))
