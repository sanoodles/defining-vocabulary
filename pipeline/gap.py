import json, re, collections
W="/home/itf/repos/eigenlex/apps/web/data"
index={w.lower():i+1 for i,w in enumerate(json.load(open(f"{W}/word-bands.pt.json"))["ranked"])}
nolevel=set(json.load(open("pt_peel.json"))["no_level"])
INFL=re.compile(r"\b(primeira|segunda|terceira) pessoa\b|\b(feminino|masculino|plural|singular) de\b"
                r"|\bpartic[ií]pio\b|\bger[uú]ndio\b|\bflex[aã]o\b|\bforma (feminina|masculina|plural|verbal)\b"
                r"|\bdo verbo\b|\bimperativo de\b|\bsuperlativo (absoluto )?sint[eé]tico de\b",re.I)
seen=collections.defaultdict(lambda:[0,0])   # word -> [real glosses, inflection glosses]
for line in open("pt.jsonl",encoding="utf-8"):
    e=json.loads(line); w=(e.get("word") or "").lower()
    if w not in nolevel: continue
    for s in e.get("senses",[]):
        for g in (s.get("glosses") or []):
            if not g: continue
            seen[w][1 if INFL.search(g) else 0]+=1
infl_only=[w for w,(r,i) in seen.items() if i and not r]
real_but_lost=[w for w,(r,i) in seen.items() if r]
absent=[w for w in nolevel if w not in seen]
print(f"no level total          {len(nolevel):,}")
print(f"  inflection-only entry {len(infl_only):,}  <- recoverable: inherit the lemma's level")
print(f"  had a real gloss      {len(real_but_lost):,}  <- gloss resolved to no indexed word")
print(f"  no entry at all       {len(absent):,}")
for lbl,ws in (("inflection-only",infl_only),("no entry",absent)):
    s=sorted(ws,key=lambda w:index[w])[:10]
    print(f"  {lbl:<16}: {' '.join(s)}")
