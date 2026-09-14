"""Write the defining levels into word-bands as a committed artifact.

The app reads this positionally against `ranked`, so a rebuild of word-bands.pt.json
would silently shift every level onto the wrong word. `count` and `digest` are what make
that failure loud instead: the app's test re-derives both and refuses a mismatch.

Levels are D1-D7 here, not the core numbers pt_levels.json carries, because this file is
read by the app rather than by the pipeline. D = 7 - core.
"""
import hashlib, json, pathlib

W = pathlib.Path("/home/itf/repos/word-bands/apps/web/data")
ranked = json.load(open(W / "word-bands.pt.json"))["ranked"]
d = json.load(open("pt_levels.json"))
assert d["words"] == ranked, "pt_levels.json is not built against this word-bands.pt.json"

levels = "".join("-" if c == "-" else str(7 - int(c)) for c in d["cores"])
digest = hashlib.sha256("\n".join(ranked).encode("utf-8")).hexdigest()[:16]
out = {"lang": "pt", "count": len(ranked), "digest": digest, "levels": levels}
(W / "defining.pt.json").write_text(json.dumps(out), encoding="utf-8")

n = sum(1 for c in levels if c != "-")
print(f"defining.pt.json  {len(ranked):,} words, {n:,} levelled, digest {digest}")
for k in "1234567-":
    print(f"  {'none' if k=='-' else 'D'+k:>5} {levels.count(k):>7,}")
