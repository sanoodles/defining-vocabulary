# Defining vocabulary

The pipeline behind wordbands' third band view, `defining`, alongside `freq` and `cefr`.
It emits the levels the app ships for all six of its languages. The page is a report on the
Portuguese levels.

## Open this first

**Published at <https://defining-vocabulary.vercel.app>** — Vercel project
`sanoodles-dev/defining-vocabulary`, deployed from `site/`. See **Deploying** below.

`defining-pt.html` — the same page as a local file, self-contained, no server needed.
All 35,827 indexed Portuguese words, their defining level, frequency rank and CEFR band.
Set the frequency window to 2,001–6,000 to see the levels separate at constant frequency.
Use the **word set** toggle to hide function words and dictionary metalanguage.
All three controls sit in one **Scope** bar, which governs the three views below it: the
distribution chart, the scatter and the columns. The frequency window also sets the
scatter's initial x range. Search filters the distribution and the columns; in the scatter
it dims non-matches instead of hiding them, so a match keeps its context — searching `mente`
shows the -mente adverbs absent from D1-D2 and piled into D5-D7.

The **frequency against defining level** scatter draws all 22,824 levelled words on canvas.
`ctrl`/`⌘`+wheel zooms, drag pans, shift+drag box-zooms, double-click resets, hover names
the word. Full screen is a button. A touch screen has none of those, so it gets its own set
— see **On a phone** below. Three choices worth knowing:

| Choice | Why |
| --- | --- |
| Zoom takes `ctrl`/`⌘`, a bare wheel does not | A bare wheel scrolls the page. A 710px canvas that swallows it traps the reader mid-page, so the chart only claims the wheel when the modifier is held, and an overlay names the key when it is not. `touch-action:pan-y` is the same fix for a vertical swipe. Trackpad pinch arrives as a ctrl wheel event, so it zooms for free |
| Stable jitter within each band | The defining level is 7 discrete values, so without it every word stacks on seven straight lines. The offset is hashed from the word, so points never move between renders |
| Square-root x axis, not log | Log gave ranks 1-1,000 two thirds of the width. Sqrt gives each CEFR band a roughly equal share (16/12/12/17/26/17%) |

Points are one ink colour, not the level ramp: the y position already encodes the level, and
the pale end of the ramp disappears against the ground. Colour is spent on search hits.

### Where the scope bar sits

A control belongs next to what it controls. These three govern a range 2,400px tall on a
laptop, so the bar sits at the top of that range and then follows the reader down it.

| Rule | Why |
| --- | --- |
| Directly above the distribution, below the explainer | The explainer governs nothing, and above it the bar is three screens from the first view it applies to |
| Sticks to the top across all three views | The loop is toggle, look, toggle again, and the columns are 1,700px below the search box |
| Releases at the end of the columns | `.governed` is the wrap holding the bar and the three views, so the range it sticks over is the range it applies to |
| Sticky only from 1440x620 | Stuck, one row of controls is 205px, 22% of a 950px viewport. Below 1440 they wrap to two or three rows — 268px at 1280, 360px at 1024, 483px at 400 — and a bar that size has no business following anyone. Below the gate it scrolls away like anything else |
| `scroll-padding-top` while sticky | Shift-tabbing upwards would otherwise put focus under the stuck bar |

The scatter clears the stuck bar at every viewport, and not by luck: the chart is
`min(90vh, 100vh - 240px)` tall, the bar is 205px, and 205 is less than 240.

## What the page explains

`Where the two numbers come from` sits between the figures and the scope bar, and answers
three questions: what the data sources are, how the frequency rank is worked out, and how
the defining level is worked out. The sources
table names all four inputs, and says which of them was already building the app.

One term per idea throughout, so a reader is never asked to guess that two words mean
the same thing:

| Idea | The word the page uses | Not |
| --- | --- | --- |
| An entry's explanatory text | definition | gloss |
| The 35,827 indexed words | word list | corpus, vocabulary |
| A step on the scale | level | step, band, stratum |
| A CEFR or frequency group | band | level |
| `u -> v` | link | edge |
| A word that has one | has a level | levelled |

## What the level means

An edge `u -> v` means *u appears in v's definition*. A word's level is its out-degree
core number: the largest k for which it still helps define k words that themselves
survive at k. D1 = core 6 = the core the dictionary explains everything else with.
D7 = core 0 = never used to define a word outside D7.

Most D7 words appear in no definition at all. The other 24% appear only in definitions of
other D7 words. The bottom level of Italian, French, Spanish and German splits the same way:
21–25% of its words appear only in definitions of other words at that level. In English it is
17% of D20.

What the peel finds is an **emergent defining vocabulary** — the uncontrolled-corpus
analogue of the Longman Defining Vocabulary or Ogden's Basic English, discovered from the
dictionary's own usage rather than fixed in advance by an editor.

**It is not a measure of how general a word's meaning is.** Three readings of the data
say so: `animal` is D2 while
`água` is D3, though one is a superordinate category and the other a substance; `planta`
is D3 beside `olho` and `boca`; and a quarter of D1 is `palavra oração expressar etc
pronome preposição`, the vocabulary of writing definitions rather than of naming things.
The axis is how often a definition reaches for a word, which correlates with generality
without being it.

The page states the same thing as rounds of peeling, which needs no graph vocabulary:
round k removes every word now used in fewer than k definitions, and a word's level is
8 minus the round it falls in.

### The worked example

`porco` is used in **94** definitions and `igual` in **92**, yet `porco` finishes three
levels lower. That is the shortest proof that this is not a popularity count. Words used in
85 to 100 definitions spread across four levels, D2 to D5.

| Round starts | Words still using `igual` | Words still using `porco` |
| --- | --- | --- |
| 1 | 92 | 94 |
| 2 | 65 | 44 |
| 3 | 42 | 12 -> falls to 2, out |
| 4 | 28 | — |
| 5 | 17 | — |
| 6 | 8 -> falls to 5, out | — |
| **Level** | **D2** | **D5** |

`porco` is used only by words more specific than itself (`presunto`, `javali`,
`toucinho`, `leitão`, `pocilga`), and 82 of its 94 users are gone before round 3. `igual`
is used at every level, including by `valor`, `diferente`, `semelhante` and `comparar`,
which survive and hold it up. Reproduce both columns by instrumenting the peel loop in
`pipeline/kcore.py` with a watch set.

Read it as how much the dictionary leans on a word, never as easy -> hard. `olá` and
`uau` are A1 vocabulary sitting at D7, because no definition is ever written in terms of
"hello". D7 is a fact about the dictionary, not about the word.

## Parts of speech

The toggle is a **display filter only**. Restricting the graph itself was tested and rejected:

| Variant | Edges | Mean out-degree | Levels | r vs log rank | D1 size |
| --- | --- | --- | --- | --- | --- |
| A · all parts of speech (shipped) | 308,617 | 13.5 | 7 | -0.591 | 51 |
| B · noun+adj+verb+adv | 254,554 | 11.3 | 5 | -0.576 | 1,531 |
| C · noun+adj+verb | 236,804 | 10.7 | 5 | -0.577 | 1,474 |
| D · function-word stoplist | 209,582 | 9.4 | 5 | -0.572 | 1,445 |

Every restricted variant produces the **same ordering** of content words and merges A's top
three levels into one. Function words appear in nearly every gloss, so they add a near-constant
to every out-degree: a constant cannot reorder anything, but it does raise the ceiling, and the
ceiling is what sets how many levels the k-core resolves.

POS filtering on headwords cannot remove function words from the graph anyway. Edges come from
gloss tokens, which are untagged, and every function word carries a marginal content entry
(`o` is also the noun "the letter O"; `a` carries seven tags including noun).

Known limit of the toggle: it keys on whether a word has any closed-class Wiktionary entry, so
`não` (tagged adv + intj + noun) reads as a content word and stays visible.

The table was measured on an earlier, smaller word list, so row A differs from the committed
graph under **Results**. `pipeline/variants.py` and `pipeline/variantD.py` measure it again,
against whatever list wordbands holds.

## Results

| File | Holds |
| --- | --- |
| `pt_levels.json` | `words` (frequency order), `cores` (one char, `-` = no level), `pos` (`c` content / `f` function / `m` metalanguage / `?` no entry) |
| `pt_core.json` | word -> out-degree core number, 32,750 entries |
| `pt_peel.json` | the naive 1-core peel: strata, kernel, no-level list |
| `pt_graph.json` | the definitional graph, 32,750 nodes / 429,758 edges |
| `pt_core_content4.json` `pt_core_content3.json` `pt_core_D.json` | the rejected variants, kept for comparison |
| `it_core.json` | word -> out-degree core number, 33,986 entries |
| `it_graph.json` | the definitional graph, 33,986 nodes / 498,800 edges |
| `fr_core.json` | word -> out-degree core number, 47,268 entries |
| `fr_graph.json` | the definitional graph, 47,268 nodes / 1,021,843 edges |
| `es_core.json` | word -> out-degree core number, 34,028 entries |
| `es_graph.json` | the definitional graph, 34,028 nodes / 724,560 edges |
| `de_core.json` | word -> out-degree core number, 39,093 entries |
| `de_graph.json` | the definitional graph, 39,093 nodes / 430,903 edges |
| `en_core.json` | word -> out-degree core number, 48,400 entries |
| `en_graph.json` | the definitional graph, 48,400 nodes / 1,269,463 edges |

## Numbers

| | Portuguese | Italian | French | Spanish | German | English |
| --- | --- | --- | --- | --- | --- | --- |
| Levels | 7, shares 0.2 / 1.7 / 3.4 / 6.6 / 14.4 / 25.6 / 48.0% | 7, shares 1.1 / 2.2 / 3.3 / 4.9 / 10.3 / 22.5 / 55.8% | 14, shares 0.2 / 0.7 / 0.9 / 1.0 / 1.3 / 1.2 / 1.5 / 2.1 / 3.0 / 3.8 / 5.5 / 8.9 / 19.9 / 50.1% | 11, shares 0.1 / 0.0 / 1.5 / 2.0 / 2.4 / 2.9 / 4.2 / 6.5 / 11.1 / 21.0 / 48.2% | 5, shares 0.9 / 4.5 / 9.2 / 23.2 / 62.2% | 20, shares 1.9 / 0.2 / 0.7 / 0.4 / 0.8 / 0.6 / 0.8 / 0.6 / 0.8 / 0.9 / 1.1 / 1.4 / 1.9 / 2.3 / 3.0 / 4.1 / 5.9 / 9.6 / 19.3 / 43.5% |
| Coverage | 32,750 of 44,352 = 74% | 33,986 of 41,422 = 82% | 47,304 of 48,566 = 97%, 36 of them through a ligature twin | 34,028 of 45,314 = 75% | 39,093 of 50,000 = 78% | 48,400 of 50,000 = 97% |
| Mean out-degree | 13.1 | 14.7 | 21.6 | 21.3 | 11.0 | 26.2 |
| Correlation with log frequency rank | -0.70 | -0.71 | -0.77 | -0.75 | -0.62 | -0.78 |

The naive 1-core peel does **not** work on Wiktionary: 61% kernel, empty middle.
Wiktionary has no controlled defining vocabulary, so the graph is too dense to peel.
The k-core generalisation is the fix and is what produced the levels above.

## Pipeline

Run in order from this directory. The first four take a language code, `pt`, `it`, `fr`,
`es`, `de` or `en`, and need that language's own Wiktionary extract first:

    curl -o wiktextract-pt.jsonl.gz https://kaikki.org/ptwiktionary/raw-wiktextract-data.jsonl.gz   # 36MB
    curl -o wiktextract-it.jsonl.gz https://kaikki.org/itwiktionary/raw-wiktextract-data.jsonl.gz   # 40MB
    curl -o wiktextract-fr.jsonl.gz https://kaikki.org/frwiktionary/raw-wiktextract-data.jsonl.gz   # 734MB
    curl -o wiktextract-es.jsonl.gz https://kaikki.org/eswiktionary/raw-wiktextract-data.jsonl.gz   # 103MB
    curl -o wiktextract-de.jsonl.gz https://kaikki.org/dewiktionary/raw-wiktextract-data.jsonl.gz   # 309MB
    curl -o wiktextract-en.jsonl.gz https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.jsonl.gz   # 523MB

Each file but the English one holds every language its Wiktionary defines, and
`build_graph.py` keeps the entries in the language itself. kaikki publishes no raw dump of
the English edition, since `kaikki.org/enwiktionary/` answers 404, so English takes the file
of the English edition's English entries. Run on the extracts below, the first three scripts
rebuild every committed `<lang>_graph.json` and `<lang>_core.json`, and every
`defining.<lang>.json` in wordbands, exactly. That was checked on 2026-10-20.

kaikki rebuilds each file at the same URL, so a new download is a later dump and moves
levels. The committed files come from these dumps. Write the new date here when replacing
one.

| Extract | kaikki built it on | Read from |
| --- | --- | --- |
| `wiktextract-pt.jsonl.gz` | 2026-09-22 | The commit that rebuilt Portuguese, `ba3e82a`. The file's gzip header carries no date |
| `wiktextract-it.jsonl.gz` | 2026-09-16 | The file's gzip header |
| `wiktextract-fr.jsonl.gz` | 2026-09-23 | The file's gzip header |
| `wiktextract-es.jsonl.gz` | 2026-10-02 | The file's gzip header |
| `wiktextract-de.jsonl.gz` | 2026-10-01 | The file's gzip header |
| `wiktextract-en.jsonl.gz` | 2026-10-03 | The file's gzip header |

The gzip header holds the time kaikki compressed the file. This prints it:

    date -ud @$(od -An -tu4 -j4 -N4 wiktextract-it.jsonl.gz | tr -d ' ') +%F

The other scripts are about the Portuguese page and read kaikki's Portuguese-only file,
which kaikki marks deprecated:

    curl -o pt.jsonl \
      'https://kaikki.org/ptwiktionary/Portugu%C3%AAs/kaikki.org-dictionary-Portugu%C3%AAs.jsonl'   # 339MB

| Script | Does |
| --- | --- |
| `pipeline/build_graph.py <lang>` | Parse glosses, resolve tokens through `forms.<lang>.json`, write `<lang>_graph.json` |
| `pipeline/kcore.py <lang>` | Out-degree core decomposition -> `<lang>_core.json` |
| `pipeline/emit_artifact.py <lang>` | Write `defining.<lang>.json` into wordbands, one base-36 digit per word |
| `pipeline/analyse.py <lang>` | Correlation with frequency, frequency-controlled samples |
| `pipeline/gap.py` | Split the no-level words by cause |
| `pipeline/peel_pt.py` | The naive 1-core peel, kept to show why it fails |
| `pipeline/peel2.py` | The toy dictionary demo of peeling and its traps |
| `pipeline/gate_gap.py` | What wordbands' filters let through, crossed with this extract. Needs no `pt.jsonl` |

Paths inside the scripts point at `apps/web/data/` in the wordbands repo, as an absolute
path in each of the seven — so moving that repo breaks them all until they are repointed.
`build_graph.py` and `emit_artifact.py` read `WORDBANDS_DATA` first, so the three that make
the levels can run against another checkout's `data/`, such as a worktree's:

    WORDBANDS_DATA=../wordbands-<topic>/apps/web/data python3 pipeline/build_graph.py it

## Italian

The same method, run on the Italian Wiktionary. It gives seven levels, as Portuguese does,
and they separate at constant frequency in the same way. Among the words ranked
2,000-6,000, D1 is the vocabulary of writing definitions (`definizione` `specifico`
`distinguere`) and D7 holds words no definition outside D7 uses (`sbirro` `bussare`
`arrivederci`). `scrittura` and `diffuso` are each used in 70 definitions, sit at ranks 2,806
and 3,730, and finish at D1 and D5. `ciao` is A1 vocabulary at D7, like `olá`.

`build_graph.py` needs three details for Italian:

| Detail | Why |
| --- | --- |
| An inflection is skipped by Wiktextract's own `form_of` marking | One filter serves every edition, with no per-language list of phrases like "plurale di" |
| An elided word is split off and spelled out | The tokenizer reads `dell'acqua` as one word. Whole, it resolves to nothing, and both `della` and `acqua` lose the link. Splitting adds 3.5% more links in Italian |
| Link labels are cut out of the definition | The Italian extract leaves `( approfondimento)` and `( citazioni)` inside 25 definitions. Kept, they raise five words a level each |

## French

The same method, run on the French Wiktionary. It peels into 14 levels, and 97% of the
list has one, as in English. Among the words ranked 2,000-6,000, D1 is again the
vocabulary of writing definitions (`marquer` `employer` `désigner` `verbe`) and
D14 holds words no definition outside D14 uses (`démissionner` `grand-chose` `pisser`).
`comparaison` and `canard` are each used in 45 definitions, sit at ranks 3,341 and 3,207,
and finish at D2 and D10. `demain` is A1 vocabulary at D14, like `olá` and `ciao`.

French needs two details of its own:

| Detail | Why |
| --- | --- |
| An elided word is split off and spelled out, as in Italian | `l'eau` and `qu'il` would otherwise lose `le` and `que`. It adds 1% more links and keeps 14 levels |
| A word spelled without the ligature takes its twin's level | The word list holds 43 words in both spellings, `coeur` and `cœur`, and the dictionary writes only `cœur`. `emit_artifact.py` gives `coeur` the level of `cœur`. Without it 36 words have no level, `oeil` at rank 281 and `coeur` at 613 among them |

## Spanish

The same method, run on the Spanish Wiktionary. It peels into 11 levels, and 75% of the
list has one, close to Portuguese. Among the words ranked 2,000-6,000, the top is again the
vocabulary of writing definitions (`verbo` at D1, `significado` `símbolo` `interpretar` at
D3) and D11 holds words no definition outside D11 uses (`ciertamente` `doler` `sofá`
`moto`). `seguida` and `hígado` are each used in 23 definitions, sit at ranks 3,369 and
4,151, and finish at D4 and D10. `hola` is A1 vocabulary at D11, like `olá`, `ciao` and
`demain`.

D2 holds 9 words, the fewest of any level in the six languages: `lo` `al` `otro` `alguno`
`indicar` `u` `determinar` `objeto` `expresar`.

Spanish needs two details of its own:

| Detail | Why |
| --- | --- |
| Maintenance notes are cut out of the definition | The extract leaves `[cita requerida]` inside 231 definitions and `[definición imprecisa]` inside 51. Kept, they are 466 links, and they hold `cita` two levels above where its own uses put it |
| A sense number is cut off the word it marks | The Spanish Wiktionary writes `llevar₁` to point at one sense of `llevar`, and the tokenizer reads the digit as a letter, so the word resolves to nothing. 1.9% of definitions carry one. The digits are cut only after a lowercase letter, so `CH₄` stays a formula rather than becoming the junk entry `ch` |

## German

The same method, run on the German Wiktionary. It peels into 5 levels, the fewest of the
six languages, and 78% of the list has one. Among the words ranked 2,000-6,000, D1 is
again the vocabulary of writing definitions (`Bezeichnung` `Eigenschaft` `Bestandteil`
`Merkmal`) and D5 holds words no definition outside D5 uses (`erwischen` `Champagner`
`schief`). `definiert` and `Furcht` are each used in 27 definitions, sit at ranks 4,172 and
4,750, and finish at D1 and D4. `hallo` is A1 vocabulary at D5, like `olá`, `ciao`,
`demain` and `hola`.

Both numbers come from the inputs, not from the method:

| Detail | Why |
| --- | --- |
| 5 levels, with 62% of the words that have one in D5 | German definitions link the fewest words, 11.0 a word against 13.1 to 26.2 in the other five. A sparser graph runs out of rounds sooner |
| 78% of the list has a level | 7,604 of the 10,907 words without one are entries in wordbands' list that the German Wiktionary files only as forms of another word, and a form defines nothing. The lemma list makes `gesagt` a headword of its own. Portuguese, Italian and Spanish have 690 to 1,529 such words. Nearly all the rest have no entry: names, English, and compounds such as `Sicherheitssystem`. The share falls with rarity: A1 to C2 run 96, 90, 85, 82, 79 and 74%, close to Italian's 96, 95, 90, 84, 79 and 79% |
| Nothing is cut out of the definitions | The German Wiktionary points a definition at a sense of its own headword with `[1]` or `^([1])`. The mark holds no word, and a headword written beside it is a self-link, which the graph drops |

## English

The same method, run on the English Wiktionary. It peels into 20 levels, the most of the six,
and 97% of the list has one, as in French. Among the words ranked 2,000-6,000, D1 holds words
definitions reach for (`manner` `proceed` `instance` `circumstance`) and D20 holds words no
definition outside D20 uses (`mum` `grandma` `gimme`). `resolve` and `bark` are each used in
66 definitions, sit at ranks 2,953 and 3,575, and finish at D1 and D13. `tomorrow` is A1
vocabulary at D20, like `olá`, `ciao`, `demain`, `hola` and `hallo`. `hello` is not at the
bottom: the English Wiktionary defines `hey`, `hiya` and `aloha` with it, so it sits at D17.

| Detail | Why |
| --- | --- |
| 20 levels | English definitions link the most words, 26.2 a word against 11.0 to 21.6 in the other five. A denser graph lasts more rounds |
| The levels follow frequency the most of the six | The correlation with log frequency rank is -0.78, against -0.62 to -0.77 elsewhere |
| Nothing is cut out of the definitions | Splitting a word at its apostrophe adds 0.3% of the links, nearly all of them a possessive's head: `one's` gives `one`. Contractions such as `don't` are too rare in definitions to matter |

## How many levels

A level is one round of the peel, and a dictionary whose definitions use more words peels
further. So each language has its own count, and the app reads it off the artifact.
`emit_artifact.py` writes one base-36 digit per word, so D10 and past still take one
character. On the September 2026 extracts, and the October ones for Spanish, German and
English:

| Language | Levels | Mean out-degree |
| --- | --- | --- |
| German | 5 | 11.0 |
| Portuguese | 7 | 13.1 |
| Italian | 7 | 14.7 |
| Spanish | 11 | 21.3 |
| French | 14 | 21.6 |
| English | 20 | 26.2 |

## What this says about the word list

Building the graph meant looking every one of the 35,827 Portuguese words up in Wiktionary.
11,719 of them are not in it at all. That is worth handing back, because wordbands built
the list and nothing had checked its first 25,000 words against a dictionary.

Being absent from one dictionary proves nothing, because each one drops ordinary words for
its own reasons:

| Dictionary | Has no entry for | Because |
| --- | --- | --- |
| Wiktionary | `boa` `má` `última` `certa` | It files them under `bom`, `mau`, `último`, `certo` |
| `lemma-pt.txt`, the list wordbands filters with | `que` `de` `com` `se` | It lists only words that inflect |

Being absent from **both** is the signal. 7,565 words are:

| Kind | Examples |
| --- | --- |
| People's names | `John` `Jack` `Sam` `Michael` `Charlie` `Frank` |
| English, left untranslated | `The` `of` `and` `New` `City` `Red` `Hey` |
| Misspellings | `näo` for `não`, `voce` for `você` |
| Abbreviations | `km` `srta` `fbi` `Mr` `St` |

Every one of the 7,565 sits in the first 25,000 words. wordbands does check a word against
a dictionary, but only from rank 25,000 onward, and past that rank the count is zero. So the
check works. It starts too late.

2,704 of them are already listed in `names.txt`, the file wordbands uses to drop personal
names. The filter had the word in hand and kept it anyway.

Some of the 7,565 are real words: `bem-vindos`, `directamente` and `Iorque` are ordinary
Portuguese. This is a list to review, not a list to delete.

`pipeline/gate_gap.py` prints all of it, and needs no `pt.jsonl`. The long version is in
wordbands' `CLAUDE.md`, under "Measuring what the gate misses".

## On a phone

The page works from 320px up, and one line in the head is what makes the rest of it
reachable. Without `<meta name="viewport" content="width=device-width">` a phone lays the
page out at 980px and scales the result down: every reflow rule below is dead, and 16px
body text arrives at about 6px. The AA reflow row in the table below was true of the CSS
and false of the device until that line existed.

| Below 700px | Why |
| --- | --- |
| Browse is a snapped swipe strip, one column at a time | Eight columns do not fit, and stacking them makes eight nested scrollers down a 2,200px section. The strip keeps the shape and keeps the section one screen tall |
| The chart is `min(62svh, 460px)` | `vh` on a phone measures the viewport with the toolbar hidden, so the desktop `90vh` is taller than anything the reader can see. `svh` is the small one, and a `vh` line before it covers browsers without `svh` |
| One control per row, search box full width | All three fields wrap to their own row at any phone width anyway |
| Chart buttons stretch instead of right-aligning | Right-aligned, three buttons wrap into a ragged stack |
| Canvas gutters drop from 78px to 62px | A fixed 78px is a quarter of a 278px plot. The y labels and their swatches shrink with it |

The gestures are replaced rather than reinterpreted, and the hint line under the chart says
whichever set applies:

| Desktop | Touch |
| --- | --- |
| `ctrl`/`⌘`+wheel zoom | pinch |
| drag pan | swipe sideways |
| hover names a point | tap names a point, for 2.6s |
| double-click reset | double-tap |
| shift+drag box zoom | — |

| Load-bearing detail | Why |
| --- | --- |
| One finger still scrolls the page | `touch-action:pan-y` hands the vertical swipe to the page, so the chart cannot trap a reader mid-page. It is the same rule the wheel modifier follows, and it leaves the chart the horizontal component |
| A tap, not a hover | Hover needs a mouse, so without it a phone cannot read a single word off the scatter at all. The hit radius is 18px for a finger against 10px for a cursor |
| `pointerleave` ignores touch | A touch pointer leaves the canvas the instant it lifts, which wiped the tap's own tooltip before it could be read |
| `pointercancel` releases like `pointerup` | The browser takes a gesture back whenever it decides the swipe was a page scroll. A pointer that never lifts leaves the chart panning under the next touch |
| Full screen hides itself | iPhone Safari has no element fullscreen. `document.fullscreenEnabled` is what says so |

Verified in headless Chromium at 320, 360, 390, 430, 600, 768 and 820px with synthetic
touch events: no horizontal page scroll at any of them, and the desktop rendering at 1440
is pixel-identical to before.

## Accessibility

Targets WCAG AAA where it is reachable without changing the design. Every colour was solved
numerically rather than eyeballed — `pipeline/solve.py` derives the tokens, `pipeline/wcag.py`
checks them. Re-run `wcag.py` after any palette edit; it exits 1 on any failing pair.

`wcag.py` reads the tokens straight out of `page_template.html` rather than keeping a copy,
so it cannot go on reporting failures the palette has already fixed.

| Criterion | Level | Where it landed |
| --- | --- | --- |
| 1.4.6 Contrast (enhanced) | AAA | Every text token >= 7:1 on all three grounds, both themes |
| 1.4.11 Non-text contrast | AA | All 7 ramp steps >= 3:1 against their track |
| 1.4.12 Text spacing | AAA | Line height 1.5-1.65 on every text block |
| 1.4.8 Visual presentation | AAA | Measure capped at 74ch, no justified text |
| 2.5.5 Target size | AAA | All buttons and the search field >= 44px tall |
| 1.4.4 / 1.4.10 Resize, reflow | AA | No horizontal scroll at 320px; figures restack and the columns become a swipe strip |
| 2.4.7 Focus visible | AA | 3px accent outline, 2px offset |

Nothing on the page is below 13px, and body text is 16px. 3.1.2 Language of Parts is met by
tagging the Portuguese content (`lang="pt"` on the columns, the lookup word and the tooltip).

Word rows are 15px, which lets a long word overflow a 140px column. Two traps sit behind the
fix. A list setting `overflow-y:auto` has CSS compute `overflow-x` to `auto` as well, so an
overflow produces a horizontal scrollbar per column. And `hyphens:auto` is not a fix, because
headless Chromium ships no `pt` hyphenation dictionary and a real browser's availability is
not something to rely on. The row is `flex-wrap` instead, so the **rank** drops to a second
line rather than the word breaking mid-letter. Only 25 of 35,827 words (0.1%) are long enough
to need a break at all.

**Not met.** The scatter cannot satisfy 1.4.11 per point — 22,824 overlapping marks at any
useful alpha is inherently low contrast. Mitigated by a .30 alpha floor,
the minimum radius, and the hover tooltip, which is the accessible route to any single point.
The chart is an overview; the columns and the word lookup carry the same data in text.

## Page width

`--page: 1600px` is the one width. Every block is a `.wrap` at that cap, the scatter
included, so the text column and the chart share a left edge. Side gutters are
`clamp(20px, 2vw, 40px)`.

Browse holds **eight** columns (D1-D7 plus No level), and this width is what keeps them on
one row. Anything narrower wraps the eighth to a row of its own at every laptop width.

| Viewport | Content width | Browse columns per row | Column width |
| --- | --- | --- | --- |
| 1280 | 1214 | 8 | 143px |
| 1440 | 1367 | 8 | 162px |
| 1512 | 1437 | 8 | 171px |
| 1728 | 1600 | 8 | 191px |
| 1920 | 1600 | 8 | 191px |

The column track minimum is 140px, which is what lets the eight survive at 1280 once the
gutters grow. Below 700px the eight stop being a row at all — see **On a phone**. Prose is unaffected by the width: `.note`, `.method p` and the masthead cap
themselves at 70-74ch, so the container only ever moves the bars, the columns and the
scatter.

`pipeline/render_page.py` inlines `pt_levels.json` into `pipeline/page_template.html` and
writes `defining-pt.html`. Edit the template, never the built page.

## Deploying

The page is published on its own, not as a route in the app. It is a report about a method,
and the app is a tool; coupling them costs four things and buys nothing a link does not.

| Cost of putting it in `apps/web` | Detail |
| --- | --- |
| The CSP | `next.config.mjs` sends `style-src 'self'` and `font-src 'self'` on `/:path*`, `public/` included, so this page's Google Fonts are blocked and blocked quietly. Naming the host instead fails `next-config.test.ts`'s "names no host anywhere", which is `HEAD-2` to `HEAD-4` |
| The design system | The app is Fondue tokens and Diatype. This page's palette is solved by `pipeline/solve.py` and gated by `pipeline/wcag.py` |
| The data | 360KB of inlined Portuguese-only JSON, against an app that serves per-language artifacts through routes |
| The spec | Every surface in that repo carries a rule ID and a test naming it. This page carries none, and writing rules for a spike's prose is the wrong work |

What belongs in the app is the *feature* this argues for — a `defining` value beside
`freq` and `cefr`, fed by a column in `wordbands.pt.json`. That shares `bands.ts`, the band
browser and the URL state. This page shares none of it and never has to move.

`render_page.py` writes the deploy into `site/`: `index.html`, its headers, and the
allowlist that keeps everything else out of the upload. Any static host serves it; there is
no build step and no repo behind it, so a publish is the two commands.

    python3 pipeline/render_page.py
    vercel deploy site --prod --scope sanoodles-dev

`site/` is gitignored, so a fresh clone has neither the page nor the Vercel link. The first
publish on a new machine takes one command more:

    vercel link --cwd site --scope sanoodles-dev --project defining-vocabulary --yes

That writes a `VERCEL_OIDC_TOKEN` into `site/.env.local`, which is no use to a static page —
delete it. `.vercelignore` keeps it out of the upload either way, which is the reason it is
an allowlist rather than a list of exclusions.

| Choice | Why |
| --- | --- |
| `site/` rather than the directory root | The root holds 6MB of intermediate JSON and a 339MB extract's leftovers. A deploy directory of exactly one page cannot leak them by accident |
| `.vercelignore` is an allowlist, not a list of exclusions | `vercel link` writes a `VERCEL_OIDC_TOKEN` into `.env.local` in the directory it links, and a static deploy serves whatever it uploads. `*` then `!index.html` means a file that appears later is out by default rather than in |
| The page keeps its Google Fonts | It is same-origin nowhere near the app's CSP, so `site/vercel.json` names `fonts.googleapis.com` for styles and `fonts.gstatic.com` for faces, and nothing else |
| `connect-src 'none'` | The page fetches nothing — the data is inlined so it opens over `file://`. Saying so is what makes a later accidental fetch loud |
| The same five headers as the app | `HEAD-1`'s set, minus the parts that only make sense with an API behind them |

Verified under those exact headers before deploying, and again against the live URL at
390px and 1440px: no CSP violation, no JS error, all three webfonts loaded, the scatter
drawing, no horizontal scroll. `/.env.local`, `/vercel.json`, `/.vercelignore`,
`/.vercel/project.json` and `/.gitignore` all answer 404 — the page is the only thing
served.
