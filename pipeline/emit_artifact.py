"""Write a language's defining levels into word-bands as a committed artifact.

    python3 pipeline/emit_artifact.py it

The app reads this positionally against `ranked`, so a rebuild of word-bands.<lang>.json
would silently shift every level onto the wrong word. `count` and `digest` are what make
that failure loud instead: the app's test re-derives both and refuses a mismatch.

Levels are D1-D7 here, not the core numbers <lang>_core.json carries, because this file is
read by the app rather than by the pipeline. D = 7 - core. The app shows exactly seven
levels, so a language whose graph peels into any other number is refused.
"""
import hashlib, json, pathlib, sys

lang = sys.argv[1]
W = pathlib.Path("/home/itf/repos/word-bands/apps/web/data")
ranked = json.load(open(W / f"word-bands.{lang}.json"))["ranked"]
rank = json.load(open(f"{lang}_graph.json"))["rank"]
assert rank == {w.lower(): i + 1 for i, w in enumerate(ranked)}, \
    f"{lang}_graph.json is not built against this word-bands.{lang}.json"
core = json.load(open(f"{lang}_core.json"))
top = max(core.values())
assert top == 6, f"{lang} peels into {top + 1} levels, and the app shows exactly 7"

levels = "".join(str(7 - core[w.lower()]) if w.lower() in core else "-" for w in ranked)
digest = hashlib.sha256("\n".join(ranked).encode("utf-8")).hexdigest()[:16]
out = {"lang": lang, "count": len(ranked), "digest": digest, "levels": levels}
(W / f"defining.{lang}.json").write_text(json.dumps(out), encoding="utf-8")

n = sum(1 for c in levels if c != "-")
print(f"defining.{lang}.json  {len(ranked):,} words, {n:,} levelled, digest {digest}")
for k in "1234567-":
    print(f"  {'none' if k=='-' else 'D'+k:>5} {levels.count(k):>7,}")
