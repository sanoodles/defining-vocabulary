DEF = {
 "aardvark":"burrowing african mammal long snout",
 "anteater":"mammal eats ants long snout",
 "ant":"small insect that lives in groups",
 "insect":"small animal with six legs",
 "snout":"nose of an animal",
 "nose":"part of a face used to smell",
 "face":"front part of a head",
 "head":"top part of a body",
 "body":"whole physical thing of an animal",
 "mammal":"animal that feeds milk to its young",
 "milk":"white food made by a mammal",
 "animal":"living thing that moves and eats food",
 "food":"thing that animals eat",
 "eat":"to take food into the body",
 "thing":"object that exists",
 "object":"thing that can be touched",
 "part":"piece of a thing",
 "piece":"part of an object",
 "Bananenbrotrezept":"",          # in the word list, no dictionary entry
}
LEMMA={"eats":"eat","animals":"animal","ants":"ant","feeds":"feed","moves":"move"}

def peel(defs, lemma):
    words=set(defs)
    defof={v:{lemma.get(t,t) for t in d.split()} & words for v,d in defs.items()}
    out={u:0 for u in words}
    for v,ts in defof.items():
        for u in ts: out[u]+=1
    outdeg0=dict(out)
    alive, strata = set(words), []
    while True:
        f=sorted(u for u in alive if out[u]==0)
        if not f: break
        strata.append(f)
        for u in f:
            alive.discard(u)
            for w in defof[u]:
                if w in alive: out[w]-=1
    return strata, alive, outdeg0

strata, kernel, outdeg = peel(DEF, LEMMA)
LEVELS=len(strata)+1
def lvl_of(i): return len(strata)-i+2   # round i -> level; kernel is 1
print(f"PEEL — {LEVELS} levels out of {len(strata)} rounds")
print(f"  kernel        -> level 1 (most generic) : {' '.join(sorted(kernel))}")
for i,s in enumerate(strata,1):
    print(f"  round {i:<2}      -> level {lvl_of(i):<2}{chr(40)+'most specific'+chr(41) if i==1 else '':<16}: {chr(32).join(s)}")

print("\nOUT-DEGREE — how many words each helps define (a ranking, not a level)")
for w in ["thing","animal","food","body","milk","snout","aardvark"]:
    lvl = 1 if w in kernel else lvl_of(next(i for i,s in enumerate(strata,1) if w in s))
    print(f"  {w:<12} out-degree {outdeg[w]:<3} level {lvl}")

print("\nWITHOUT LEMMATISATION — the same peel, 'ants' never mapped to 'ant'")
s2,k2,_=peel(DEF, {})
for i,s in enumerate(s2,1):
    if "ant" in s: print(f"  'ant' now falls in round {i} of {len(s2)} (was round 2 of {len(strata)})")
print(f"  round 1 becomes: {' '.join(s2[0])}")
