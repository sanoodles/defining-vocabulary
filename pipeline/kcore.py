import json, collections, sys
lang=sys.argv[1]
d=json.load(open(f"{lang}_graph.json")); graph={k:set(v) for k,v in d["graph"].items()}; rank=d["rank"]
nodes=set(graph)
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
            for w in graph[u]:
                if w in alive: outdeg[w]-=1
mx=max(core.values())
print(f"out-degree core numbers: 0 .. {mx}   ({mx+1} distinct levels)")
dist=collections.Counter(core.values())
print(f"\n{'core':>5}{'words':>9}{'share':>8}  examples (most frequent first)")
for c in sorted(dist, reverse=True)[:14]:
    ws=sorted((w for w in core if core[w]==c), key=lambda w: rank[w])
    print(f"{c:>5}{dist[c]:>9,}{100*dist[c]/len(core):>7.1f}%  {' '.join(ws[:7])}")
print(f"{'...':>5}")
for c in sorted(dist)[:3]:
    ws=sorted((w for w in core if core[w]==c), key=lambda w: rank[w])
    print(f"{c:>5}{dist[c]:>9,}{100*dist[c]/len(core):>7.1f}%  {' '.join(ws[:7])}")
json.dump(core, open(f"{lang}_core.json","w"))
