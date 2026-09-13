# Defining vocabulary — Portuguese prototype

Feasibility spike for a third band view in eigenlex, alongside `freq` and `cefr`.
Nothing here is wired into the app.

## Open this first

**Published at <https://eigenlex-defining-vocabulary.vercel.app>** — Vercel project
`eigenlex/eigenlex-defining-vocabulary`, deployed from `site/`. See **Deploying** below.

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
D7 = core 0 = never used in any definition.

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

`igual` and `porco` are each used in exactly **67** definitions and finish three levels
apart, which is the shortest proof that this is not a popularity count. Raw usage counts
near 50 spread across five different levels.

| Round starts | Words still using `igual` | Words still using `porco` |
| --- | --- | --- |
| 1 | 67 | 67 |
| 2 | 55 | 32 |
| 3 | 40 | 12 -> falls to 2, out |
| 4 | 28 | — |
| 5 | 17 | — |
| 6 | 7 -> falls to 5, out | — |
| **Level** | **D2** | **D5** |

`porco` is used only by words more specific than itself (`presunto`, `javali`,
`toucinho`, `leitão`, `pocilga`), and 55 of its 67 users are gone before round 3. `igual`
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

Run `pipeline/variants.py` and `pipeline/variantD.py` to reproduce the table.

## Results

| File | Holds |
| --- | --- |
| `pt_levels.json` | `words` (frequency order), `cores` (one char, `-` = no level), `pos` (`c` content / `f` function / `m` metalanguage / `?` no entry) |
| `pt_core.json` | word -> out-degree core number, 22,824 entries |
| `pt_peel.json` | the naive 1-core peel: strata, kernel, no-level list |
| `pt_graph.json` | the definitional graph, 22,824 nodes / 308,680 edges |
| `pt_core_content4.json` `pt_core_content3.json` `pt_core_D.json` | the rejected variants, kept for comparison |

## Numbers

| | |
| --- | --- |
| Levels | 7, shares 0.2 / 1.8 / 5.2 / 9.0 / 18.2 / 26.8 / 38.7% |
| Coverage | 22,824 of 35,827 = 64%, plus 1,191 recoverable inflection-only entries |
| Mean out-degree | 13.5 |
| Correlation with log frequency rank | -0.59 |

The naive 1-core peel does **not** work on Wiktionary: 61% kernel, empty middle.
Wiktionary has no controlled defining vocabulary, so the graph is too dense to peel.
The k-core generalisation is the fix and is what produced the levels above.

## Pipeline

Run in order from this directory. Needs the source extract first:

    curl -o pt.jsonl \
      'https://kaikki.org/ptwiktionary/Portugu%C3%AAs/kaikki.org-dictionary-Portugu%C3%AAs.jsonl'   # 339MB

| Script | Does |
| --- | --- |
| `pipeline/build_graph.py` | Parse glosses, resolve tokens through `forms.pt.json`, write `pt_graph.json` |
| `pipeline/kcore.py` | Out-degree core decomposition -> `pt_core.json` |
| `pipeline/analyse.py` | Correlation with frequency, frequency-controlled samples |
| `pipeline/gap.py` | Split the no-level words by cause |
| `pipeline/peel_pt.py` | The naive 1-core peel, kept to show why it fails |
| `pipeline/peel2.py` | The toy dictionary demo of peeling and its traps |

Paths inside the scripts point at `apps/web/data/` in the repo.

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
`freq` and `cefr`, fed by a column in `word-bands.pt.json`. That shares `bands.ts`, the band
browser and the URL state. This page shares none of it and never has to move.

`render_page.py` writes the deploy into `site/`: `index.html`, its headers, and the
allowlist that keeps everything else out of the upload. Any static host serves it; there is
no build step and no repo behind it, so a publish is the two commands.

    python3 pipeline/render_page.py
    vercel deploy site --prod --scope eigenlex

`site/` is gitignored, so a fresh clone has neither the page nor the Vercel link. The first
publish on a new machine takes one command more:

    vercel link --cwd site --scope eigenlex --project eigenlex-defining-vocabulary --yes

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
