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

---

## 1. How to start it

**Recommended — run the server** (so the repo is your source of truth):

```bash
python3 prep-tracker/server.py        # then open http://localhost:8000/
# custom port:  PORT=8137 python3 prep-tracker/server.py
```

The server serves the app **and** saves your progress to `prep-tracker/progress.json` in this
repo. Commit that file and your progress follows you to any machine via `git pull`. No build
step, no `npm install`, no dependencies — just Python 3.

**Offline fallback** — you can also open the file directly:

```bash
open prep-tracker/index.html          # macOS
```

Opened this way (no server), progress saves only to the browser's `localStorage` and is **not**
written to the repo. The footer tells you which mode you're in (✓ repo file vs ⚠ offline).

**Running against test data** — point `PREP_PROGRESS` at a throwaway file to poke at the app
without touching your real history:

```bash
echo '{}' > /tmp/fixture.json
PREP_PROGRESS=/tmp/fixture.json PORT=8137 python3 prep-tracker/server.py
```

Use a different port as well as a different file. `localStorage` is scoped per origin, so
`localhost:8137` gets its own mirror too and the sandbox is fully isolated from `localhost:8000`.
An empty `{}` fixture will seed itself from the catalog on first load, exactly like a fresh start.

### Running the tests

```bash
node --test prep-tracker/selection.test.js
```

No install step — this uses Node's built-in test runner.

---

## 2. The daily loop (how to use it)

1. **Open the app.** It lands on the **Due today** tab — the problems the schedule wants you
   to revisit right now. On day one that's ~3 of your already-solved problems.
2. **Pick the top one.** Weak buckets (red/amber) always sort to the top, so you face your
   shakiest problems first.
3. **Solve it blind.** Open your editor, set a ~25-min timer, and write the solution *from
   scratch* — no peeking at your old file. If you stall for 10 min, jot down which *pattern*
   you think it is, then peek.
4. **Grade yourself honestly** by clicking the problem to expand it, then one of:

   | Button | Meaning | Next review |
   | ------ | ------- | ----------- |
   | 🔴 **Failed** | needed the solution | tomorrow (+1d) |
   | 🟡 **Slow** | solved, but with hints / slowly | +3 days |
   | 🟢 **Clean** | solved with some hesitation | +1 week |
   | 🔵 **Fast** | instant & confident | +3 weeks (mastered) |

   The grade sets the problem's **box** and schedules when it comes back. Grading collapses the
   row and removes it from today's list — it feels like clearing a worklist.
5. **Write the trigger sentence.** In the expanded panel, fill in *"what tips you off to the
   pattern?"* — e.g. *"sorted array + find a pair → two pointers from both ends."* This single
   sentence is the thing that transfers to problems you've never seen. It saves automatically.
6. **Want more?** When Due today is empty, switch to the **New** tab and pull a fresh problem.
   Core categories (Arrays & Strings, Hashmaps & Sets, Two Pointers, Sliding Window) are
   starred ★ — prioritize those.

---

## 3. The tabs

- **Due today** — your worklist for the session. A badge shows how many are due.
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

- **Due today** — how many problems are scheduled for now.
- **Solved locally** — how many of the 129 have a solution file in `patterns/` (60 as of the
  2026-08 sprint merge).
- **Core solved** — your coverage of the 4 core categories (the interview bread-and-butter).
- **Mastered (box 4)** — problems you've graded **Fast**; they're on the longest interval.

---

## 5. Where your progress lives

- **With the server (recommended):** progress is written to `prep-tracker/progress.json`, a
  committed file. This is the **source of truth** — commit it and `git pull` on any machine to
  resume. localStorage is kept as a local cache/mirror.
- **Offline (`file://`):** progress lives only in the browser's `localStorage` (key `srt.v1`),
  per-browser and per-machine, and is **not** written to the repo.
- **Export progress** downloads a JSON backup (handy regardless of mode).
- **Reset all** wipes every box, due date, and trigger note (with a confirm), then re-seeds the
  solved problems and their staggered due dates.

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

Edit `prep-tracker/sprint.js` and reload. Nothing else changes.

1. `SPRINT_META` — `{ format, order }`. Free text for the header strip, e.g.
   `"70 minutes · 4 problems · no pausing"`.
2. `SPRINT_GROUPS` — one row per chunk: `{ g: 1, dir: "arrays", label: "Arrays (1D) Foundations" }`.
   `g` orders the groups and renders as the day number. `dir` is the folder under `sprint/`.
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

Solutions go in `sprint/<topic>/<problem>.py`. Each row's panel prints the exact path.

### Merging a finished sprint back in

Once the test is done, fold the keepers into the catalog so they join the review rotation. For each:

1. Move the file from `sprint/<topic>/` into `patterns/<category>/`. **Run it first** — only mark
   a problem solved if it actually passes.
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
