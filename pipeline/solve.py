import colorsys
def srgb(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    h=h.lstrip("#"); r,g,b=(int(h[i:i+2],16) for i in (0,2,4))
    return .2126*srgb(r)+.7152*srgb(g)+.0722*srgb(b)
def cr(a,b):
    x,y=lum(a),lum(b); x,y=max(x,y),min(x,y); return (x+.05)/(y+.05)
def hex_hsl(h,s,l):
    r,g,b=colorsys.hls_to_rgb(h/360,l,s); return "#%02X%02X%02X"%(round(r*255),round(g*255),round(b*255))
def solve(h,s,bg,target,darker=True):
    lo,hi=(0.0,1.0)
    for _ in range(60):
        mid=(lo+hi)/2; c=cr(hex_hsl(h,s,mid),bg)
        if darker:
            if c>target: lo=mid
            else: hi=mid
        else:
            if c>target: hi=mid
            else: lo=mid
    return hex_hsl(h,s,(lo+hi)/2)

L_TRACK="#EDF2F1"; D_TRACK="#182524"
print("LIGHT tokens (solved against surface-2, the worst-case ground)")
lt={}
for name,h,s,t in [("muted",176,.11,9.5),("faint",176,.13,7.15),("accent",177,.78,7.6)]:
    lt[name]=solve(h,s,L_TRACK,t,darker=True)
    print(f"  --{name:<7}{lt[name]}   surface2 {cr(lt[name],L_TRACK):.2f}  bg {cr(lt[name],'#F4F7F7'):.2f}  white {cr(lt[name],'#FFFFFF'):.2f}")
print("DARK tokens")
dk={}
for name,h,s,t in [("muted",172,.14,9.5),("faint",172,.12,7.15),("accent",172,.62,8.5)]:
    dk[name]=solve(h,s,D_TRACK,t,darker=False)
    print(f"  --{name:<7}{dk[name]}   surface2 {cr(dk[name],D_TRACK):.2f}  bg {cr(dk[name],'#0C1413'):.2f}")

print("\nRAMP — 7 steps, every one >= 3.0 against its track")
import math
def ramp(track,darker,hue=176):
    out=[]
    for i in range(7):
        t=13.0*math.pow(3.15/13.0,i/6)          # geometric, 13.0 -> 3.15
        s=.80-.42*(i/6)
        out.append(solve(hue,s,track,t,darker=darker))
    return out
RL=ramp(L_TRACK,True); RD=ramp(D_TRACK,False)
for i,(a,b) in enumerate(zip(RL,RD),1):
    print(f"  L{i}  light {a} {cr(a,L_TRACK):5.2f}   dark {b} {cr(b,D_TRACK):5.2f}")
print("\n  --l1..l7 light:", " ".join(RL))
print("  --l1..l7 dark: ", " ".join(RD))
print("\nbutton check — pressed segment is accent ground with --bg text")
print(f"  light {cr(lt['accent'],'#F4F7F7'):.2f}   dark {cr(dk['accent'],'#04211F'):.2f}")
