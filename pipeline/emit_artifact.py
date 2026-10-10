"""Write a language's defining levels into wordbands as a committed artifact.

    python3 pipeline/emit_artifact.py it

The app reads this positionally against `ranked`, so a rebuild of wordbands.<lang>.json
would silently shift every level onto the wrong word. `count` and `digest` are what make
that failure loud instead: the app's test re-derives both and refuses a mismatch.

Levels are D1 to Dn here, not the core numbers <lang>_core.json carries, because this file
is read by the app rather than by the pipeline. n is how many levels the graph peels into,
and it differs by language. D = n - core. Each level is one base-36 digit, so D10 and past
still take one character and a language under ten levels reads as plain digits.
"""
import hashlib, json, pathlib, sys

lang = sys.argv[1]
W = pathlib.Path("/home/itf/repos/wordbands/apps/web/data")
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
ranked = json.load(open(W / f"wordbands.{lang}.json"))["ranked"]
rank = json.load(open(f"{lang}_graph.json"))["rank"]
assert rank == {w.lower(): i + 1 for i, w in enumerate(ranked)}, \
    f"{lang}_graph.json is not built against this wordbands.{lang}.json"
core = json.load(open(f"{lang}_core.json"))
n = max(core.values()) + 1
assert n < len(DIGITS), f"{lang} peels into {n} levels, more than one digit holds"

# The corpus writes both coeur and cœur, and the dictionary only the ligature, so a word
# spelled without it takes the level of its twin spelled with it.
UNLIGATE = str.maketrans({"œ": "oe", "æ": "ae"})
lower = [w.lower() for w in ranked]
twin = {w.translate(UNLIGATE): w for w in lower if w.translate(UNLIGATE) != w}
def core_of(w):
    w = w.lower()
    return core[twin[w]] if twin.get(w) in core else core.get(w)

levels = "".join("-" if (c := core_of(w)) is None else DIGITS[n - c] for w in ranked)
digest = hashlib.sha256("\n".join(ranked).encode("utf-8")).hexdigest()[:16]
out = {"lang": lang, "count": len(ranked), "digest": digest, "levels": levels}
(W / f"defining.{lang}.json").write_text(json.dumps(out), encoding="utf-8")

levelled = sum(1 for c in levels if c != "-")
print(f"defining.{lang}.json  {len(ranked):,} words, {levelled:,} levelled into {n} levels, digest {digest}")
for d in range(1, n + 1):
    print(f"  {'D' + str(d):>5} {levels.count(DIGITS[d]):>7,}")
print(f"  {'none':>5} {levels.count('-'):>7,}")
