# Prep Tracker — architecture & safety review

**Date:** 2026-08-21 · **Baseline:** commit `19f81ed` · **Scope:** `apps/prep-tracker/` (1851 lines)

Four independent reviewers, each blind to the others: structure, data safety, testability, rendering.
Findings below are **deduplicated** and **re-ranked** across all four. Every claim marked *verified*
was reproduced by execution or measurement. Two reviewer claims were rejected — see the last section.

---

## Status

**Tier 0 and finding 8 are DONE** (2026-08-21). Verified by `apps/prep-tracker/server_test.py` (22/22) and
a browser pass on an isolated origin:

- an empty / conflict-markered / scalar `progress.json` now returns 409, and the app halts instead of
  seeding over it — the corrupt file was confirmed still corrupt after a full page load
- writes are revision-checked (`ETag` / `If-Match`); a stale snapshot gets 409
- cross-origin and non-JSON writes are refused (403 / 415), oversized bodies 413
- a reachable-but-broken server no longer reports "offline"; a 404 still does, so
  `python3 -m http.server` and `file://` keep working
- the localStorage mirror is read on load, with Merge / Discard — verified restoring a lost grade
- `escapeHTML` no longer throws on a non-string, `fsync` before rename, file mode 0644,
  `ThreadingHTTPServer` so a half-open request cannot stall a save
- the seed stagger now spreads only what it seeds: a newly solved `dp` problem comes due **today**
  instead of 19 days out

Everything below Tier 1 finding 8 is still open.

---

## Verdict

**It is not spaghetti, and it does not need a framework.** Of 1048 lines in `app.js`, 158 are the
static catalog, 55 are two prose blocks, and ~150 are comments recording real past bugs. The actual
logic is ~500 lines across five render paths, coherently named. Measured: a full 129-row re-render
takes 2.64 ms, so the innerHTML rebuild is the correct simple choice and no incremental DOM is
warranted.

**But the review did not find a tidiness problem — it found seven ways to lose your practice
history**, two of them reachable without any mistake on your part. That reframes the answer to
"how should this be organised": reorganising is the *third* priority, and its real justification is
that the code which can corrupt `progress.json` currently cannot be tested at all.

The reason it cannot be tested is one line: `app.js` touches `document` at load, so `node` cannot
require it. Every path that can destroy data sits behind that line. Two reviewers converged on the
same fix independently, which is the strongest signal in the review.

---

## Tier 0 — can destroy your practice history

Fix these first. All are small and none require restructuring.

| # | Finding | Where | Status |
|---|---|---|---|
| 1 | **A zero-byte `progress.json` makes a page load overwrite it.** `f.read() or b"{}"` reports an empty file as "no progress yet"; the app seeds all 60 solved problems and immediately POSTs over the file. Footer stays green. | `server.py:46`, `app.js:297,360` | verified — measured 63 keys / 15 notes / 28 attempts → 60 / 0 / 0 from one navigation |
| 2 | **Any web page open in your browser can wipe the file.** `do_POST` checks neither `Origin` nor `Content-Type`. A `text/plain` POST is CORS-simple, so no preflight protects it. | `server.py:58` | verified — `Origin: https://evil.example.com` + `text/plain` returned 204 and wrote |
| 3 | **Every POST is a blind whole-file replace.** No revision, no `If-Match`, no merge. An old tab that POSTs its stale snapshot silently reverts everything done since. | `server.py:58`, `app.js:312` | verified — one 20-byte POST took the file from 61 keys to 1 |
| 4 | **An unparseable file is reported as "no server".** `await r.json()` throws inside the same `try` that means "fetch failed", so a conflict-markered file silently demotes to offline mode and tells you to run `server.py` — which is already running. | `app.js:297` | verified |
| 5 | **localStorage is written on every save and never read in server mode.** After a server death and restart, the mirror holds the only copy of your recent grades, and the first save overwrites it. No merge path exists. | `app.js:334` vs `297` | verified by trace |
| 6 | **`escapeHTML` throws on a non-string, blanking the whole app.** One `"trigger": 3` in `progress.json` makes every render throw before the `innerHTML` assignment. The list stays permanently empty and no error surfaces. | `app.js:839` | verified — `3`, `true`, `{}` all raise `TypeError` |
| 7 | **No `fsync` before `os.replace`.** The atomic rename can be durable while the data is not, producing exactly the zero-byte file that finding 1 then destroys. | `server.py:82` | suspected (not induced) |

**Fixes.** 1: return `409` for present-but-empty or unparseable, and make the client refuse to seed
when the server said `{}` but the mirror is non-empty. 2: reject non-`application/json`, and reject a
foreign `Origin`. 3: `ETag` from `st_mtime_ns` on GET, `If-Match` on POST, `409` on mismatch, red
banner plus Export. 4: split the two `try` blocks. 5: store the mirror as `{savedAt, state}` and offer
Merge / Discard on divergence. 6: `String(s ?? "")`. 7: `f.flush()` + `os.fsync()`.

---

## Tier 1 — wrong behaviour you would read as "the app ignored me"

| # | Finding | Where | Status |
|---|---|---|---|
| 8 | **A newly solved problem is scheduled up to 19 days out.** The seed stagger index runs over *all* solved problems, not the ones being seeded, so `due = today + floor(i/3)` depends on the problem's position in the whole list. Follow the documented workflow and a new `dp` problem will not be reviewed for three weeks. | `app.js:370` | verified — measured `arrays_and_strings` +2d, `stacks` +8d, `trees` +13d, `dp` +19d |
| 9 | **Grading from the New tab makes the row and its note prompt vanish.** The New filter is `box === 0`; grading breaks it, the row leaves the view, and `FOCUS_TRIGGER` finds no target. Same regression class as the bug that once left 56 of 57 problems with no note. | `app.js:502,990` | verified in browser |
| 10 | **Correcting a mis-grade inflates the attempt count.** The panel's own "Graded it wrong? Change it" control adds another attempt, corrupting the difficulty signal. | `app.js:984` | verified — 3 → 4 on a same-day regrade |
| 11 | **645 focusable controls live inside collapsed panels.** `max-height: 0` hides them visually but leaves them in the tab order. Tab from the filter chips and focus disappears into invisible grade buttons; Enter grades a problem you cannot see. | `styles.css:167`, `app.js:658` | verified — 646 tab stops measured |
| 12 | **A click in an open panel that misses a control collapses the row**, so the solution file path cannot be selected or copied. | `app.js:947` | verified |
| 13 | **The note indicators go stale.** The `input` handler patches the row's pill but not the "N without a note" header or the Sprint note stat. | `app.js:968` vs `601,458` | verified |
| 14 | **The single-threaded server drops saves while any request is stalled.** `Content-Length` is trusted with no cap or timeout, so a half-open connection blocks all service — including an unload beacon, which has nowhere to report failure. | `server.py:62,103` | verified — a concurrent GET was never served |

**Fixes.** 8: build the to-seed list first, then stagger within it. 9: keep graded rows visible in
New, or render the done section there. 10: `attempts: cur.last === today ? cur.attempts : cur.attempts + 1`.
11: `inert` on closed panels (or `visibility: hidden`). 12: `if (e.target.closest(".row__panel")) return;`
before the toggle. 13: one `refreshNoteIndicators()` called from both the input handler and `render()`.
14: `ThreadingHTTPServer`, a handler `timeout`, and a `Content-Length` cap.

---

## Tier 2 — the organisation question you actually asked

Both the structure and testability reviewers arrived at the same answer independently: extract the
pure logic behind the **same CommonJS export guard `selection.js` already uses**, so `node --test`
can reach it. Not for tidiness — because Tier 0 and Tier 1 are full of bugs that a test would have
caught, and the one well-tested file has never had a reported bug.

**Proposed layout** (script order matters; all classic scripts, `file://` unaffected):

```html
<script src="selection.js"></script>   <!-- unchanged -->
<script src="core.js"></script>        <!-- NEW: dates, grading, seeding, filters -->
<script src="catalog.js"></script>     <!-- NEW: CAT_META, CAT_ORDER, PROBLEMS, id() -->
<script src="sprint.js"></script>      <!-- unchanged -->
<script src="app.js"></script>         <!-- ~620 lines: state, persistence, render, events -->
```

Two hard rules keep the order safe:

- `core.js` depends on nothing — the taxonomy is passed in as arguments, never read as a global.
- **Delete every moved `const` from `app.js`.** Two classic scripts declaring the same `const` in the
  shared global scope throw `SyntaxError` and the page renders blank. A leftover `function` is worse:
  it silently shadows the tested one, so every test passes against dead code.

**The shape that makes it testable** — each of these currently interleaves a decision with
`saveState()`, `OPEN_ID`, and `render()`. Split the decision out, keep the effect in `app.js`:

```
applyGrade(state, pid, box, today)      -> newState
applySprintStatus(state, pid, status)   -> newState
resetKeepingSprint(state)               -> newState
seedPlan(problems, state, today, opts)  -> {state, seeded}
buildDueCandidates(problems, state, today) -> candidate[]   (must preserve object identity)
```

**Smaller cleanups worth taking with it:**

- **Delete the `s` flag.** Verified redundant with `f` across all 129 entries — two hand-maintained
  fields carrying one fact. Use `Boolean(p.f)` at the seven read sites.
- **`CAT_ORDER` is byte-identical to `Object.keys(CAT_META)`.** Derive it; delete the second list.
- **One record factory** instead of the default `{box:0,due:null,...}` literal repeated five times,
  branching on `isSprintKey` so a sprint row never gets a catalog shape.
- **Fix the category test.** `CATEGORY_COUNT = 14` compares `TIERS` against a hand-typed number and
  never reads `CAT_META`, so adding a category and forgetting `TIERS` still passes — the exact failure
  its comment claims to guard. Once `catalog.js` exists, assert real set equality instead.
- **`GRADES` sub-labels hardcode `+1d/+3d/+7d/+21d`**, duplicating `INTERVAL`. Interpolate or assert.
- **`postState()` calls `setFootNote()`**, so persistence reaches into footer DOM. An assignable
  `onSaveStatus` callback is the one change that makes a `store.js` possible later.

**Highest-value tests to write** (all `node:test`, no dependencies):

1. `resetKeepingSprint` keeps every `sprint#` key and drops the rest — the exact past bug.
2. A debounced save followed by an immediate save POSTs exactly one body, and it is the latest — the exact past bug.
3. `seedPlan` seeds a box-0 entry that has a note, and never touches `box >= 1` — the exact past bug.
4. `seedPlan` staggers only what it seeds — finding 8.
5. `applyGrade` rejects a box outside 1–4 instead of writing `"NaN-NaN-NaN"`.
6. `addDays` / `daysUntil` across both DST boundaries with `process.env.TZ` set.
7. Catalog integrity against the committed files: unique `cat#n`, every `f` exists on disk, every
   category in exactly one tier, no orphaned progress keys.

Persistence cannot be pure — wrap it instead: `createStore({fetchFn, storage, setTimer, ...})` so a
test can inject a fake fetch and a fake clock. That is the only way to cover the debounce race.

---

## Tier 3 — worth doing cheaply, or skipping

- `.back` at `styles.css:47` is **dead** — verified, zero references. Delete.
- `--idle` as text is **1.89:1 contrast**, effectively invisible ("optional" tag, sprint tip). Add a `--muted-2`.
- Both display fonts have **no fallback chain**, so `file://` with no network renders headings in Times.
- Six palette hex values are **hardcoded inline** in the two help templates, so a token change misses them.
- `--active`/`--box3`, `--stack`/`--box2`, `--danger`/`--box1` are **duplicate names for identical values**.
- `focus()` after `scrollIntoView({behavior:"smooth"})` cancels the animation — `preventScroll: true`.
- The category filter is **live on the How-it-works tab** and does nothing.
- The `640px` panel cap **clips with no scrollbar** if you drag the note field taller (`resize: vertical`).
- Export uses a detached anchor with a synchronous `revokeObjectURL` — works in Chromium, historically
  fragile elsewhere, and it sits next to **Reset all**.
- **Skip the tab-list ARIA.** The tabs are real buttons and already keyboard-operable; `role="tab"`
  would then oblige roving `tabindex` and arrow keys. One worthwhile addition: `aria-live="polite"`
  on `.foot__note`, so the "save FAILED" message is not announced in silence.

---

## Leave alone — load-bearing code that looks redundant

- **The full innerHTML rebuild.** 2.64 ms for 129 rows. One path from state to pixels is worth more.
- **The `input` handler that refuses to re-render.** Correct — a render destroys the caret and the
  native undo stack mid-sentence. The defect is that it patches one of three dependants, not the rule.
- **`Math.round` in `daysUntil`.** Not sloppy rounding — it is the DST fix. `floor` would fire every
  box-4 review a day early, twice a year, forever.
- **`new Date(iso + "T00:00:00")`.** The explicit time forces *local* parsing. Without it, a bare
  `YYYY-MM-DD` parses as UTC and every date shifts by a day west of Greenwich.
- **`seedIfNeeded` guarding on `box > 0`, not key presence.** A presence check permanently excluded
  any problem with a note written before it was solved. Keep the guard through the refactor.
- **The `immediate` flag and the `beforeunload` beacon.** Both still necessary; `fetch` does not
  survive teardown.
- **Reset preserving sprint keys.** A deliberate, documented asymmetry.
- **The click-handler branch order.** `[data-close]` before the row toggle, `[data-status]` before
  `.grade`. Every early return is load-bearing; no click reaches two branches. Add a header comment
  saying the order is significant, and leave it.
- **`isinstance(parsed, dict)` in `do_POST`.** Blocks a scalar write that the next load would read as
  `{}` and reseed over. Directly guards Tier 0 finding 1.
- **`mkstemp` + `os.replace`.** Add `fsync`; do not simplify back to `open(..., "w")`.
- **No path traversal.** `/../CLAUDE.md` and the URL-encoded variant both 404. Verified.
- **No XSS.** The only field the UI writes is the trigger note, and it is escaped on every path.
- **`sprint.js` empty with a how-to header.** A documented seam, not dead code.

---

## Two reviewer claims rejected

1. **"box ≥ 1 implies `s: true`."** Two reviewers independently proposed this invariant and both
   flagged `arrays_and_strings#14` (Reverse String II) as drifted data. **The invariant is wrong.** A
   problem you attempted and failed with no working solution legitimately has box 1 and no file —
   that is what *stuck* means. Their proposed test would fail on correct data.
   The real defect is one line of copy: the panel says *"No local file yet — this is a fresh problem"*
   about a problem in active rotation with a note you wrote. It conflates "no file" with "never
   attempted". Worth a comment in the code, since the wrong model is evidently intuitive.
2. **"'Solved locally' should read 61/129."** No. There is no file for that problem, so counting it
   as solved would be a false number. 60/129 is correct, and all 60 files were verified on disk.

---

## Recommended sequence

1. **Tier 0, as one commit.** Surgical, no restructuring, ~40 lines across `server.py` and `app.js`.
   This is the only tier with a deadline, because the exposure is live.
2. **Finding 8 (the seed stagger) next**, on its own. It is four lines and it is actively wrong today.
3. **Tier 2 extraction plus the seven tests.** Do the extraction *because* of the tests, not instead
   of them. If the tests get skipped, skip the extraction too — it buys nothing on its own.
4. **Tier 1 UX**, cheapest first: 12 and 10 are one line each, 11 is one attribute, 13 is one function.
5. **Tier 3** whenever. `.back` and the contrast fix are a two-minute commit.
