# Prep Tracker

A self-contained spaced-repetition tracker built on the [AlgoMap](https://algomap.io/roadmap)
roadmap, now **129 problems** (the original 100 plus 29 folded in from the 2026-08 interview
sprint). It runs on two evidence-backed learning techniques:

- **Active recall** — you solve each problem *blind*, from scratch. The struggle to retrieve
  is what builds the memory. Re-reading solutions feels productive but barely sticks.
- **Spaced repetition** — you revisit each problem at *growing* intervals, timed to hit right
  before you'd forget it. Each successful recall pushes the memory deeper (Ebbinghaus curve).

The goal is a **mix**: keep your already-solved problems sharp (retention) while dripping in
new ones (growth), at a sustainable ~30–60 min/day.

**The rules live in [`PRACTICE.md`](../../PRACTICE.md)**: rep types, how to grade, the boxes, and
the order of new problems. This file covers how the app implements them.

---

## 1. How to start it

**Recommended — run the server** (so the repo is your source of truth):

```bash
python3 apps/prep-tracker/server.py        # then open http://localhost:8000/
# custom port:  PORT=8137 python3 apps/prep-tracker/server.py
```

The server serves the app **and** saves your progress to `apps/prep-tracker/progress.json` in this
repo. Commit that file and your progress follows you to any machine via `git pull`. No build
step, no `npm install`, no dependencies — just Python 3.

**Offline fallback** — you can also open the file directly:

```bash
open apps/prep-tracker/index.html          # macOS
```

Opened this way (no server), progress saves only to the browser's `localStorage` and is **not**
written to the repo. The footer tells you which mode you're in (✓ repo file vs ⚠ offline).

**Running against test data** — point `PREP_PROGRESS` at a throwaway file to poke at the app
without touching your real history:

```bash
echo '{}' > /tmp/fixture.json
PREP_PROGRESS=/tmp/fixture.json PORT=8137 python3 apps/prep-tracker/server.py
```

Use a different port as well as a different file. `localStorage` is scoped per origin, so
`localhost:8137` gets its own mirror too and the sandbox is fully isolated from `localhost:8000`.
An empty `{}` fixture will seed itself from the catalog on first load, exactly like a fresh start.

### Running the tests

```bash
cd apps/prep-tracker && node --test               # selection logic: window, boxes, new-problem order
.venv/bin/python -m pytest apps/prep-tracker      # grade.py, plus the server safety script
python3 apps/prep-tracker/server_test.py          # persistence safety on its own (22 cases)
```

No install step for the app — Node's built-in test runner and the Python stdlib; pytest comes from
the repo's `.venv`. The Python tests point throwaway servers at temp files on OS-assigned ports, so
they never touch your real progress or a tracker running on :8000.

---

## 2. The daily loop (how to use it)

The **Due today** tab opens on the **Today card**, three steps in order:

1. **Quick rep.** Run `/quick-rep` in Claude Code (10 min). The step ticks itself once a
   quick-rep grade lands today (see `grade.py` below). On a rough day this alone is a win.
2. **Reps.** The 3-problem window. Weak buckets (red/amber) sort to the top. Solve each one
   **blind**, then click it and grade. The row shows **no category** until you grade it, and
   the file path hides too: spotting the pattern is part of the rep. The window shrinks as you
   grade and does not refill: at 0 the step reads **Reps done for today**, and **Show all**
   has more if you want them. New problems and quick reps do not use up the 3.
3. **New problem.** The next one in the PRACTICE.md order, with a weekly counter
   (`this week: N/2`). At 2 it stays visible as a **stretch**; at 3 the step says
   **week done** and shows no problem. The quota is weekly, so a missed day moves nothing.

**Grading.** Click a problem and press one of the four buttons. Each sub-label is the
PRACTICE.md "How to grade" check: the new-problem checks for a problem at box 0 (never
attempted), the full-rep checks for everything else, triage included. Each ends with the
real next interval for that problem (Fast on a box 4 problem says `+45d`).

**Graded it wrong?** The panel stays open after a grade so you can change it. A re-grade on the
same day starts from the entry as it was before the day's first grade, so clicking Fast twice
climbs once. That earlier entry is stored in the entry as `prev`, so this also holds after a
reload and after a `grade.py` write.

| Box | Reached by | Next review |
| --- | --- | --- |
| 1 | 🔴 **Failed** | +1 day |
| 2 | 🟡 **Slow** | +3 days |
| 3 | 🟢 **Clean** | +7 days |
| 4 | 🔵 **Fast** from box 0 to 3 | +21 days |
| 5 | **Fast** from box 4 | +45 days |
| 6 | **Fast** from box 5 | +120 days |

Fast climbs one box at a time; any other grade sets that grade's box, so a miss drops the
problem down. A quick rep can hold box 6 but never earn it: it lands on box 5 instead.

**Write the trigger sentence** after each grade, in the panel that stays open — e.g. *"sorted
array + find a pair → two pointers from both ends."* It saves automatically.

**Done today** keeps every problem graded today on screen, with its category.

### Recording a quick rep: `grade.py`

```bash
python3 apps/prep-tracker/grade.py two_pointers#3 pass          # or: fail
python3 apps/prep-tracker/grade.py stacks#1 pass --date 2026-10-12
```

- `fail` → Failed (box 1). `pass` on a triage problem (box 2, never graded) → Clean (box 3).
  `pass` on box 4 and up → Fast as a quick rep (box 5 at most). Any other `pass` → Clean.
- It writes `kind: "quick"`, adds 1 to `attempts`, sets `last` and `due`, keeps the trigger, and
  never writes `started`: a quick rep is always a rep, never a new problem. Like the app, it
  stores `prev` on the day's first grade and starts a same-day grade from it. It prints one
  line: `key: box 4 → 5, next due …`.
- **Write path.** When the server answers on `localhost:${PORT:-8000}`, the grade goes through
  it with the same `If-Match` check the app uses (one retry after a `409`). Only when nothing
  listens does it write `$PREP_PROGRESS` (default `progress.json`) directly, with the same
  temp-file-and-rename as the server. An open tab picks the change up when you return to it.
- An unknown key exits with code 2. A file or server it cannot read exits with code 1 and
  writes nothing.

Every grade, from the app or `grade.py`, records `kind` (`new`, `full`, or `quick`). Only an app
grade from box 0 records `started`, so the 23 triage problems (box 2, never graded) and older
entries count as reps, not new problems. Older entries without these fields keep working.

---

## 3. The tabs

- **Due today** — the Today card. The badge counts the reps still to do in today's window
  (0 to 3), the same rows the window shows, not the backlog. **Show all** lists the whole backlog.
- **New** — the ~68 problems you haven't started yet, grouped by category (core first).
  Grading one for the first time pulls it into the rotation.
- **All** — all 129 problems with every problem's current box and next-review date.
- **Sprint** — a one-off problem list for a specific interview (see section 7). Empty between
  interviews, and separate from everything above.
- **How it works** — an in-app summary of everything here.

Use the **category chips** under the tabs to filter any view down to one category (handy for a
focused "just drill Two Pointers today" session).

---

## 4. The stat strip

Across the top:

- **This week** — `New this week: N/2 · Reps this week: M`, Monday to Sunday. N counts
  problems whose `started` date is this week; M counts the other problems graded this week. It
  replaces the old due count on purpose: the week is the unit, not the pile.
- **Solved locally** — how many of the 129 have a solution file in `patterns/` (60 as of the
  2026-08 sprint merge).
- **Core solved** — your coverage of the 4 core categories (the interview bread-and-butter).
- **Box 4 and up** — problems you've graded **Fast** at least once and not missed since.

---

## 5. Where your progress lives

- **With the server (recommended):** progress is written to `apps/prep-tracker/progress.json`, a
  committed file. This is the **source of truth** — commit it and `git pull` on any machine to
  resume. localStorage is kept as a local cache/mirror.
- **Offline (`file://`):** progress lives only in the browser's `localStorage` (key `srt.v1`),
  per-browser and per-machine, and is **not** written to the repo.
- **Export progress** downloads a JSON backup (handy regardless of mode).
- **Reset all** wipes every box, due date, and trigger note (with a confirm), then re-seeds the
  solved problems and their staggered due dates. It deliberately **keeps** the Sprint checklist.

### How writes are protected

A 2026-08-21 review found several ways a page load could silently destroy history. The rules below
are the fix. The governing principle: **when the stored data is in doubt, the app stops writing.**

- **An empty or unparseable `progress.json` is an error, not "no progress yet."** The server answers
  `409` and the app shows a red panel naming the file and the `git checkout` that restores it. It used
  to report an empty file as `{}`, which made the app seed from scratch and immediately save over it —
  measured at 63 entries with 15 notes becoming 60 with none, in one page load.
- **Every write is revision-checked.** `GET /api/progress` returns an `ETag`; the app echoes it as
  `If-Match` on save. If the file changed underneath (another tab, another machine, a `git pull`), the
  server answers `409` and the app halts rather than reverting the newer work.
- **Writes only come from this origin, as JSON.** A `text/plain` POST is a CORS-simple request, so
  without this check any page open in the browser could erase the file with one `fetch()`.
- **A reachable server that answers badly is not "offline."** Those were conflated, so a file with
  merge-conflict markers told you to run `server.py` while it was already running — and a whole day of
  grades went into a mirror that server mode never read back.
- **The localStorage mirror is now read on load.** If this browser holds entries the file lacks, or
  graded something more recently, the app halts and offers **Merge** (keep the newer of each) or
  **Discard**. Previously the mirror was written on every save and never read, so the first save
  after a server restart destroyed the only remaining copy.
- **A refused localStorage write is surfaced**, not swallowed. Offline, that mirror is the only store.
- **A tab reloads on focus.** When the tab becomes visible again and the file's revision moved
  (`grade.py`, a `git pull`), the app takes the new file, but only if it has no save of its own
  pending or in flight. If it has one, the next save gets the usual `409` and the halt panel.

**After pulling these changes, restart the server and reload the page.** The client and server now
speak a protocol the older versions do not: an old page against the new server gets `428` on every
save, and a new page against the old server never sees an `ETag`.

A 404 on `/api/progress` still means offline mode, so serving the directory with
`python3 -m http.server` keeps working, exactly like `file://`.

---

## 6. Keeping it in sync with the repo

The solved/unsolved state and repo file paths live in the `PROBLEMS` array near the top of
`app.js`. When you solve a new problem and add its file under `patterns/`:

```js
// change this:
{ cat: "hashmaps_and_sets", n: 6, title: "Two Sum", s: false },
// to this:
{ cat: "hashmaps_and_sets", n: 6, title: "Two Sum", s: true, f: "patterns/hashmaps_and_sets/two_sum.py" },
```

On the next load, the app seeds that newly-solved problem into the review rotation automatically
(the seeding step is idempotent — it only touches problems it hasn't seen before).

---

## 7. The Sprint tab

A second track for **one specific interview**: the one-off problem list that arrives with a take-home
plan, a screen's prep sheet, or a recruiter's topic list. It sits beside the rotation and does not
interact with it.

It is a **checklist with memory, not a second scheduler**:

- No Leitner box, no due date, **no calendar**. Day names are labels for chunks of the list, not
  deadlines — nothing turns red and falling a day behind costs nothing.
- Nothing in the Sprint tab can ever appear in **Due today**.
- Mark each problem **Done**, **Stuck**, or **Skipped**. Clicking the active status clears it.
- The trigger-sentence field works exactly as it does in the review flow, and it survives the
  merge below.
- **Reset all** deliberately *keeps* the sprint. Wiping Leitner state is recoverable; wiping a
  mid-flight sprint days before a real test is not.

### It is currently empty

`sprint.js` holds three empty constants and a header that documents them. The tab renders a
"No sprint loaded" panel until you fill them in.

### Loading the next sprint

Edit `apps/prep-tracker/sprint.js` and reload. Nothing else changes.

1. `SPRINT_META` — `{ format, order }`. Free text for the header strip, e.g.
   `"70 minutes · 4 problems · no pausing"`.
2. `SPRINT_GROUPS` — one row per chunk: `{ g: 1, dir: "arrays", label: "Arrays (1D) Foundations" }`.
   `g` orders the groups and renders as the day number. `dir` names the group's topic and is
   used to guess a `patterns/` folder when a problem has no catalog twin.
3. `SPRINT` — one row per problem:

```js
{ g: 5, slug: "rotate-image", title: "Rotate Image",
  pri: "essential",                 // essential | stretch | optional
  maps: "arrays_and_strings#11" }   // optional: existing catalog twin
```

`slug` must be the LeetCode slug — the URL is derived from it. `maps` points at a `PROBLEMS`
entry when the catalog already has the same problem; it drives the ✓ marker and makes the merge
mechanical.

**Be honest with `pri`.** A list that does not fit is the normal case, and the tag is what you cut:
`essential` = do it, `stretch` = if the day runs short, `optional` = reference only. Skipping an
optional is the plan working.

Solutions go in `patterns/<category>/<problem>.py` — the same place as any other first solve.
There is no staging directory: `patterns/` is indexed by *pattern*, not by which interview sent
you there. Each row's panel prints the suggested path.

### Merging a finished sprint back in

Once the test is done, fold the keepers into the catalog so they join the review rotation. For each:

1. **Run the solution first** — only mark a problem solved if it actually passes. The file is
   already in `patterns/`, so there is nothing to move.
2. If it has a `maps` twin, flip that `PROBLEMS` entry to `s: true` and set its `f` path.
   Otherwise add a new `PROBLEMS` entry with the next free `n` for its category.
3. Carry the note across: `progress.json`'s `"sprint#<slug>".trigger` → the new `"cat#n".trigger`.
   Map the status to a box — `stuck` → box 1 (returns tomorrow), `done` → box 2 unless you know it
   was clean.
4. Delete the `sprint#` keys you merged, so no note lives in two places.
5. For a category the catalog lacks, add it to `CAT_META` and `CAT_ORDER` in `app.js`, and to
   `TIERS` in `selection.js`. Then bump `CATEGORY_COUNT` in `selection.test.js` — the test guards
   against a category silently falling back to tier 3.
6. Empty the three `sprint.js` constants so the tab is ready for the next one.

The seeding step then pulls each newly-solved problem into the rotation on the next load.

### Worked example — the 2026-08 merge

The first sprint held 39 problems across 9 days. On 2026-08-21 all 39 were merged:

- **10 already existed** in the catalog as `maps` twins, so they needed no new entry.
- **29 were new**, taking the roadmap from 100 to **129 problems**.
- Two new categories were added, `greedy` (Greedy & Intervals) and `sorting`, both in tier 3.
  `CATEGORY_COUNT` went from 12 to 14.
- **3 solutions** moved into `patterns/` after passing 15 test cases; **4 statuses and notes**
  became Leitner entries; the 4 `sprint#` keys were deleted.
