"""What word-bands' filters let through, measured by a second dictionary.

The lemma list and the Wiktionary extract each flag thousands of ordinary words on their
own — the lemma list never headwords function words, Wiktionary calls michmech's feminine
lemmas inflections. Only words neither vouches for are junk. Prints the three tables in
word-bands' CLAUDE.md, under "Measuring what the gate misses".
"""
import json, re, collections

W = "/home/itf/repos/word-bands/apps/web/data"
GATE, FLOOR = 25000, 1000                      # DICT_GATE, NAME_RANK_FLOOR in build-bands.ts
WORD_OK = re.compile(r"^[^\W\d_]+(?:[-'’][^\W\d_]+)*$", re.UNICODE)

# build-bands.ts: `known(s) = isHeadword.has(s) || form2lemma.has(s)`, over `lemma<TAB>form`.
vouched = set()
for line in open(f"{W}/lemma-pt.txt", encoding="utf-8-sig", errors="replace"):
    p = line.replace("﻿", "").rstrip("\r\n").split("\t")
    if len(p) < 2: continue
    l, f = p[0].strip().lower(), p[1].strip().lower()
    if l and f and WORD_OK.match(l) and WORD_OK.match(f): vouched |= {l, f}
names = {l.strip().lower() for l in open(f"{W}/names.txt", encoding="utf-8") if l.strip()}

d = json.load(open("pt_levels.json"))
words, pos = d["words"], d["pos"]
no_entry = {i for i, p in enumerate(pos) if p == "?"}      # no Wiktionary entry
no_lemma = {i for i, w in enumerate(words) if w.lower() not in vouched}
cand = sorted(no_entry & no_lemma)

print(f"{'words':<26}{len(words):>7,}")
print(f"{'not in the lemma list':<26}{len(no_lemma):>7,}  {' '.join(words[i] for i in sorted(no_lemma)[:6])}")
print(f"{'no Wiktionary entry':<26}{len(no_entry):>7,}")
print(f"{'NEITHER':<26}{len(cand):>7,}")

win = lambda r: "1-1,000" if r <= FLOOR else "1,001-24,999" if r < GATE else "25,000+"
by = collections.Counter(win(i + 1) for i in cand)
print("\nwhere they sit")
for k in ("1-1,000", "1,001-24,999", "25,000+"): print(f"  {k:<24}{by[k]:>7,}")

print("\nagainst the gazetteer")
for label, hit in (("in names.txt", True), ("not in names.txt", False)):
    ws = [words[i] for i in cand if (words[i].lower() in names) == hit]
    print(f"  {label:<24}{len(ws):>7,}  {' '.join(ws[:14])}")
