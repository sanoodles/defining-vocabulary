import json, re, collections
W="/home/itf/repos/eigenlex/apps/web/data"
ranked=json.load(open(f"{W}/word-bands.pt.json"))["ranked"]
index={w.lower():i+1 for i,w in enumerate(ranked)}
forms={k.lower():v.lower() for k,v in json.load(open(f"{W}/forms.pt.json")).items()}
INFL=re.compile(r"\b(primeira|segunda|terceira) pessoa\b|\b(feminino|masculino|plural|singular) de\b"
                r"|\bpartic[ií]pio\b|\bger[uú]ndio\b|\bflex[aã]o\b|\bforma (feminina|masculina|plural|verbal)\b"
                r"|\bdo verbo\b|\bimperativo de\b|\bsuperlativo (absoluto )?sint[eé]tico de\b",re.I)
TOK=re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*",re.UNICODE)
def resolve(t):
    t=t.lower()
    if t in index: return t
    b=forms.get(t)
    return b if b and b in index else None
defof=collections.defaultdict(set)
for line in open("pt.jsonl",encoding="utf-8"):
    e=json.loads(line); w=(e.get("word") or "").lower()
    if w not in index: continue
    for s in e.get("senses",[]):
        for g in (s.get("glosses") or []):
            if not g or INFL.search(g): continue
            for t in TOK.findall(g):
                u=resolve(t)
                if u and u!=w: defof[w].add(u)
nodes={w for w in defof if defof[w]}
graph={v:sorted(defof[v]&nodes) for v in nodes}
json.dump({"graph":graph,"rank":{w:index[w] for w in index}},open("pt_graph.json","w"))
E=sum(len(x) for x in graph.values())
print(f"nodes {len(nodes):,}  edges {E:,}  mean out-degree {E/len(nodes):.1f}")
