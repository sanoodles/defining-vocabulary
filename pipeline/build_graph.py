"""The definitional graph of one language: u -> v when u appears in v's definition.

    python3 pipeline/build_graph.py it

Reads that language's own Wiktionary, wiktextract-<lang>.jsonl.gz, and writes <lang>_graph.json.
"""
import json, re, collections, gzip, sys
lang=sys.argv[1]
W="/home/itf/repos/word-bands/apps/web/data"
ranked=json.load(open(f"{W}/word-bands.{lang}.json"))["ranked"]
index={w.lower():i+1 for i,w in enumerate(ranked)}
forms={k.lower():v.lower() for k,v in json.load(open(f"{W}/forms.{lang}.json")).items()}
# The word an elision stands for, so dell'acqua reads as della + acqua.
ELIDED={
    "pt":{"d":"de"},
    "it":{"l":"lo","d":"di","dell":"della","all":"alla","nell":"nella","sull":"sulla","dall":"dalla",
          "un":"una","c":"ci","s":"si","m":"mi","t":"ti","v":"vi","n":"ne","quest":"questa",
          "quell":"quella","tutt":"tutto","dov":"dove","com":"come","anch":"anche","qual":"quale",
          "po":"poco","nessun":"nessuna","buon":"buona","grand":"grande","sant":"santo","bell":"bella",
          "cos":"cosa"},
}.get(lang,{})
# Link labels the Italian extract leaves inside a definition: "casa ( approfondimento)".
LINKS={"it":re.compile(r"\(\s*(?:approfondimento|citazioni)\s*\)")}.get(lang)
TOK=re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*",re.UNICODE)
APOS=re.compile(r"['’]")
def resolve(t):
    t=t.lower()
    if t in index: return t
    b=forms.get(t)
    return b if b and b in index else None
def words(g):
    if LINKS: g=LINKS.sub(" ",g)
    for t in TOK.findall(g):
        u=resolve(t)
        if u or not APOS.search(t):
            yield u; continue
        *head,tail=APOS.split(t.lower())
        for p in head: yield resolve(ELIDED[p]) if p in ELIDED else resolve(p) if len(p)>1 else None
        yield resolve(tail) if len(tail)>1 else None
# Wiktextract marks an inflection's senses, and "plurale di casa" defines nothing.
def inflection(s): return bool(s.get("form_of") or s.get("alt_of") or {"form-of","alt-of"}&set(s.get("tags",[])))
defof=collections.defaultdict(set)
for line in gzip.open(f"wiktextract-{lang}.jsonl.gz","rt",encoding="utf-8"):
    e=json.loads(line); w=(e.get("word") or "").lower()
    if e.get("lang_code")!=lang or w not in index: continue
    for s in e.get("senses",[]):
        if inflection(s): continue
        for g in (s.get("glosses") or []):
            for u in words(g):
                if u and u!=w: defof[w].add(u)
nodes={w for w in defof if defof[w]}
graph={v:sorted(defof[v]&nodes) for v in nodes}
json.dump({"graph":graph,"rank":{w:index[w] for w in index}},open(f"{lang}_graph.json","w"))
E=sum(len(x) for x in graph.values())
print(f"nodes {len(nodes):,}  edges {E:,}  mean out-degree {E/len(nodes):.1f}")
