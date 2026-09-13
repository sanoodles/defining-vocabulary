import json, re, sys, collections

W = "/home/itf/repos/word-bands/apps/web/data"
ranked = json.load(open(f"{W}/word-bands.pt.json"))["ranked"]
index  = {w.lower(): i+1 for i, w in enumerate(ranked)}          # word -> rank
forms  = json.load(open(f"{W}/forms.pt.json"))                    # inflected -> base
forms  = {k.lower(): v.lower() for k, v in forms.items()}
print(f"indexed words {len(index):,}   form map {len(forms):,}")

# Glosses that describe an inflection rather than a meaning.
INFL = re.compile(r"\b(primeira|segunda|terceira) pessoa\b|\b(feminino|masculino|plural|singular) de\b"
                  r"|\bpartic[ií]pio\b|\bger[uú]ndio\b|\bflex[aã]o\b|\bforma (feminina|masculina|plural|verbal)\b"
                  r"|\bdo verbo\b|\bimperativo de\b|\bsuperlativo (absoluto )?sint[eé]tico de\b", re.I)
TOK = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*", re.UNICODE)

def resolve(t):
    t = t.lower()
    if t in index: return t
    b = forms.get(t)
    return b if b and b in index else None

defof = collections.defaultdict(set)
have_entry = set(); kept = dropped = 0
for line in open("pt.jsonl", encoding="utf-8"):
    e = json.loads(line)
    w = (e.get("word") or "").lower()
    if w not in index: continue
    have_entry.add(w)
    for s in e.get("senses", []):
        for g in (s.get("glosses") or []):
            if not g: continue
            if INFL.search(g): dropped += 1; continue
            kept += 1
            for t in TOK.findall(g):
                u = resolve(t)
                if u and u != w: defof[w].add(u)

defined = {w for w in defof if defof[w]}
print(f"headwords matched {len(have_entry):,} ({100*len(have_entry)//len(index)}% of the list)")
print(f"glosses kept {kept:,}  inflection glosses dropped {dropped:,}")
print(f"words with at least one usable edge {len(defined):,}")

out = collections.Counter()
for v, us in defof.items():
    for u in us: out[u] += 1

# Peel only over words we actually have a definition for. The rest have no level.
nodes = set(defined)
outdeg = {u: sum(1 for v in nodes if u in defof[v]) for u in nodes}
# faster: recount restricted to nodes
outdeg = collections.Counter()
for v in nodes:
    for u in defof[v]:
        if u in nodes: outdeg[u] += 1
for u in nodes: outdeg.setdefault(u, 0)

alive = set(nodes); strata = []
while True:
    f = [u for u in alive if outdeg[u] == 0]
    if not f: break
    strata.append(f)
    for u in f:
        alive.discard(u)
        for w in defof[u]:
            if w in alive: outdeg[w] -= 1

print(f"\nPEEL: {len(strata)} rounds -> {len(strata)+1} levels")
json.dump({"strata": [sorted(s) for s in strata], "kernel": sorted(alive),
           "no_level": sorted(set(index) - nodes)}, open("pt_peel.json","w"))
tot = len(nodes)
print(f"{'level':>6}{'words':>9}{'share':>8}  examples (by frequency rank)")
def show(lbl, ws):
    ws = sorted(ws, key=lambda w: index[w])
    print(f"{lbl:>6}{len(ws):>9,}{100*len(ws)/tot:>7.1f}%  {' '.join(ws[:8])}")
show("1", alive)
for i, s in enumerate(reversed(strata), 2):
    show(str(i), s)

# --- why the peel stalls: edge density ---
E = sum(len(defof[v] & nodes) for v in nodes)
print(f"\nedges {E:,} over {len(nodes):,} nodes -> mean out-degree {E/len(nodes):.1f}")
od = sorted((sum(1 for v in nodes if False),))  # placeholder
