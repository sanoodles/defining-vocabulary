import json, collections, math, statistics, sys
lang=sys.argv[1]
core=json.load(open(f"{lang}_core.json")); d=json.load(open(f"{lang}_graph.json")); rank=d["rank"]
ws=list(core)
xs=[math.log(rank[w]) for w in ws]; ys=[core[w] for w in ws]
mx,my=statistics.mean(xs),statistics.mean(ys)
r=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
print(f"Pearson r( core , log rank ) = {r:.3f}   (a pure frequency proxy would be near -1)")

print("\nCONTROLLED FOR FREQUENCY — words ranked 2,000-6,000 only")
band=[w for w in ws if 2000<=rank[w]<6000]
by=collections.defaultdict(list)
for w in band: by[core[w]].append(w)
for c in sorted(by, reverse=True):
    s=sorted(by[c], key=lambda w: rank[w])
    print(f"  core {c}  n={len(s):<5} {' '.join(s[:9])}")

print("\nSAME FREQUENCY, OPPOSITE ENDS — pairs ranked within 40 of each other")
pairs=[]; byrank=sorted(band, key=lambda w: rank[w])
for i,a in enumerate(byrank):
    for b in byrank[i+1:]:
        if rank[b]-rank[a]>40: break
        if core[a]-core[b]>=3: pairs.append((a,core[a],b,core[b],rank[a],rank[b]))
for a,ca,b,cb,ra,rb in pairs[:10]:
    print(f"  {a:<14} core {ca} (rank {ra:,})   vs   {b:<14} core {cb} (rank {rb:,})")
