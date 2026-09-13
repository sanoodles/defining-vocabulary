import json, re, collections, math, statistics
W="/home/itf/repos/eigenlex/apps/web/data"
ranked=json.load(open(f"{W}/word-bands.pt.json"))["ranked"]
index={w.lower():i+1 for i,w in enumerate(ranked)}
forms={k.lower():v.lower() for k,v in json.load(open(f"{W}/forms.pt.json")).items()}
INFL=re.compile(r"\b(primeira|segunda|terceira) pessoa\b|\b(feminino|masculino|plural|singular) de\b"
                r"|\bpartic[ií]pio\b|\bger[uú]ndio\b|\bflex[aã]o\b|\bforma (feminina|masculina|plural|verbal)\b"
                r"|\bdo verbo\b|\bimperativo de\b|\bsuperlativo (absoluto )?sint[eé]tico de\b",re.I)
TOK=re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*",re.UNICODE)

# entries: (word, pos, [glosses])
ENTRIES=[]
for line in open("pt.jsonl",encoding="utf-8"):
    e=json.loads(line); w=(e.get("word") or "").lower()
    if w not in index: continue
    gs=[g for s in e.get("senses",[]) for g in (s.get("glosses") or []) if g and not INFL.search(g)]
    if gs: ENTRIES.append((w,e.get("pos","?"),gs))
print(f"usable entries {len(ENTRIES):,}")

def run(name, allowed):
    keep={w for w,p,_ in ENTRIES if allowed is None or p in allowed}
    def resolve(t):
        t=t.lower()
        if t in index and t in keep: return t
        b=forms.get(t)
        return b if b and b in index and b in keep else None
    defof=collections.defaultdict(set)
    for w,p,gs in ENTRIES:
        if allowed is not None and p not in allowed: continue
        for g in gs:
            for t in TOK.findall(g):
                u=resolve(t)
                if u and u!=w: defof[w].add(u)
    nodes={w for w in defof if defof[w]}
    graph={v:defof[v]&nodes for v in nodes}
    E=sum(len(x) for x in graph.values())
    outdeg=collections.Counter()
    for v in nodes:
        for u in graph[v]: outdeg[u]+=1
    for u in nodes: outdeg.setdefault(u,0)
    alive=set(nodes); core={}; k=0
    while alive:
        k+=1
        while True:
            f=[u for u in alive if outdeg[u]<k]
            if not f: break
            for u in f:
                alive.discard(u); core[u]=k-1
                for w2 in graph[u]:
                    if w2 in alive: outdeg[w2]-=1
    mx=max(core.values()); dist=collections.Counter(core.values())
    ws=list(core)
    xs=[math.log(index[w]) for w in ws]; ys=[core[w] for w in ws]
    mxx,myy=statistics.mean(xs),statistics.mean(ys)
    r=sum((a-b)*(c-d) for a,b,c,d in zip(xs,[mxx]*len(xs),ys,[myy]*len(ys)))/math.sqrt(
        sum((a-mxx)**2 for a in xs)*sum((b-myy)**2 for b in ys))
    print(f"\n=== {name} ===")
    print(f"nodes {len(nodes):,}  edges {E:,}  mean out-degree {E/len(nodes):.1f}  levels {mx+1}  r(core,log rank) {r:.3f}")
    for c in range(mx,-1,-1):
        s=sorted((w for w in core if core[w]==c), key=lambda w: index[w])
        print(f"  L{mx-c+1} {dist[c]:>6,} {100*dist[c]/len(core):>5.1f}%  {' '.join(s[:8])}")
    band=[w for w in ws if 2000<=index[w]<6000]
    by=collections.defaultdict(list)
    for w in band: by[core[w]].append(w)
    print("  -- ranks 2,000-6,000 only --")
    for c in sorted(by,reverse=True):
        print(f"  L{mx-c+1} {len(by[c]):>6,}       {' '.join(sorted(by[c],key=lambda w:index[w])[:8])}")
    return core

CONTENT4={"noun","adj","verb","adv"}
CONTENT3={"noun","adj","verb"}
run("A · all parts of speech (current baseline)", None)
c4=run("B · noun + adj + verb + adv", CONTENT4)
c3=run("C · noun + adj + verb", CONTENT3)
json.dump(c4, open("pt_core_content4.json","w"))
json.dump(c3, open("pt_core_content3.json","w"))
