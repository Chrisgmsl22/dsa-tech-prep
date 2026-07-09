# Prep Tracker

A self-contained spaced-repetition tracker for the [AlgoMap](https://algomap.io/roadmap)
100-problem roadmap. It runs on two evidence-backed learning techniques:

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
- **New** — the ~43 roadmap problems you haven't solved yet, grouped by category (core first).
  Grading one for the first time pulls it into the rotation.
- **All** — the entire 100-problem roadmap with every problem's current box and next-review date.
- **How it works** — an in-app summary of everything here.

Use the **category chips** under the tabs to filter any view down to one category (handy for a
focused "just drill Two Pointers today" session).

---

## 4. The stat strip

Across the top:

- **Due today** — how many problems are scheduled for now.
- **Solved locally** — how many of the 100 have a solution file in `patterns/` (seeded at ~57).
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
