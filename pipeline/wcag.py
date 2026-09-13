"""Contrast check. Reads the tokens out of page_template.html, so it cannot drift
from the palette the page actually ships."""
import pathlib, re

CSS = (pathlib.Path(__file__).parent / "page_template.html").read_text(encoding="utf-8")

def block(selector):
    i = CSS.index(selector + "{")
    body = CSS[i + len(selector) + 1 : CSS.index("}", i)]
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})", body))

LIGHT = block(":root")
DARK = block(':root[data-theme="dark"]')

def srgb(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    h=h.lstrip("#"); r,g,b=(int(h[i:i+2],16) for i in (0,2,4))
    return .2126*srgb(r)+.7152*srgb(g)+.0722*srgb(b)
def cr(a,b):
    x,y=lum(a),lum(b); x,y=max(x,y),min(x,y)
    return (x+.05)/(y+.05)

bad = 0
for name, T in (("LIGHT", LIGHT), ("DARK", DARK)):
    print(f"\n=== {name} — text contrast (AAA needs 7.0 for body text) ===")
    for fg in ("text","muted","faint","accent"):
        row=[]
        for bgk in ("bg","surface","surface-2"):
            v=cr(T[fg],T[bgk]); bad += v < 7
            row.append(f"{bgk}:{v:5.2f}{'' if v>=7 else '  FAIL'}")
        print(f"  {fg:<8}" + "   ".join(row))

print("\n=== ramp vs its track (AA non-text needs 3.0) ===")
for i in range(1, 8):
    a, b = cr(LIGHT[f"l{i}"], LIGHT["surface-2"]), cr(DARK[f"l{i}"], DARK["surface-2"])
    bad += (a < 3) + (b < 3)
    print(f"  L{i}  light {a:5.2f}{'' if a>=3 else '  FAIL'}   dark {b:5.2f}{'' if b>=3 else '  FAIL'}")

print(f"\n{'all pass' if not bad else str(bad) + ' FAILING pairs'}")
raise SystemExit(1 if bad else 0)
