# Prep Tracker — Daily Window, Tiered Fill, and Clock-Anchored Grades

**Date:** 2026-08-03
**Status:** Design approved, pending implementation
**Touches:** `prep-tracker/app.js` only

---

## Problem

After ~3 weeks away from practice, the Due Today list shows **55 problems**. Opening the
app presents a wall of overdue work, which is demotivating and gives no sense of what to
actually do today.

The cause is **not** a scheduling bug. Two distinct concerns were conflated:

| Concern | Where it lives | State |
|---|---|---|
| *When* a problem becomes due | `INTERVAL` (`app.js:177`) + `gradeProblem()` (`app.js:562`) | Working correctly — already grade-driven |
| *How many* problems are shown today | nowhere | **Missing** |

`isDue()` (`app.js:303`) returns `daysUntil(due) <= 0` — every problem whose date has
passed, with no upper bound. The seeder (`app.js:269`) staggered 57 solved problems at
`NEW_PER_DAY_SEED = 3` per day into the future; skipping ~3 weeks slid all of those dates
into the past. Each day away adds ~3 more permanently, and nothing drains the queue.

A secondary problem: with 55 due and no cap, the sort order is decorative. Once a cap
exists, **the sort order becomes the entire product** — whatever ranks below the cap
effectively does not exist that day.

## Goals

1. Cap the visible Due list so the app always presents a manageable amount of work.
2. Never lose or rewrite real due dates — the Leitner data stays honest.
3. Always have more work available; the user sets the daily pace, not the app.
4. Bias the window toward interview-critical patterns without starving the rest.
5. Make grading objective rather than a vibe.

## Non-Goals

- No changes to `INTERVAL`, box semantics, or `gradeProblem()` scheduling math.
- No rewriting, decaying, or re-staggering of existing due dates.
- No new fields in `progress.json`. **The feature adds zero persisted state.**
- No timer, stopwatch, or time-tracking UI. The time-box protocol (below) is a practice
  discipline documented in `CLAUDE.md`, enforced by honest grading — not by the app.

---

## Design

### 1. Capped rolling window

`renderList()` (`app.js:367`) gains a `.slice()` step after sorting, when `VIEW === "due"`.

- **`WINDOW_SIZE = 5`**, defined as a module constant next to `NEW_PER_DAY_SEED`.
- The window **auto-refills**. Grading a problem sets its `due` to a future date, so it
  drops out of `isDue()` and the next candidate slides up on the next `render()`. This
  requires no extra code — it falls out of the existing re-render in `gradeProblem()`
  (`app.js:574`).
- Rationale for auto-refill over a fixed daily budget: some days finish 2, some days
  finish 8. Work should always be available. There is deliberately **no "done for today"
  state**.

**Header affordance.** Above the list, when the window is truncating:

```
Showing 5 of 55 due  ·  3 graded today        [Show all]
```

- `5 of 55` — window size vs. true due count.
- `3 graded today` — derived, not stored: `Object.values(STATE).filter(s => s.last === todayISO()).length`.
  `last` is already written on every grade (`app.js:568`).
- `[Show all]` — toggles a module-level `SHOW_ALL` boolean that bypasses the slice for the
  current session. Not persisted; resets on reload.

### 2. Three-tier fill

Replaces the current binary `CORE` set (`app.js:20`), which has only 4 categories and
misses `stacks`.

```js
const TIERS = {
  1: ["arrays_and_strings", "hashmaps_and_sets", "two_pointers", "sliding_window", "stacks"],
  2: ["trees", "binary_search", "linked_lists", "graphs"],
  3: ["heaps", "backtracking", "dp"],
};
const TIER_SHARE = { 1: 0.50, 2: 0.35, 3: 0.15 };
```

**Rationale for the tier boundaries.** Tier 1 is what phone screens and most onsites
actually ask. Tier 2 — trees, binary search, linked lists, graphs — are *not* nice-to-haves;
tree traversal and binary search are among the most-asked problems anywhere. Tier 3 are the
genuine differentiators: a candidate can be thin here and still pass most loops. The point
of the split is to keep breadth cheap (~1 problem/day) rather than all-or-nothing.

**Quota allocation** uses the largest-remainder method over `TIER_SHARE`, so quotas always
sum exactly to the available slot count.

At `WINDOW_SIZE = 5`: raw `[2.50, 1.75, 0.75]` → floors `[2, 1, 0]` (3 assigned) → 2 slots
remain → highest remainders are tier 2 (`.75`) and tier 3 (`.75`) → final **`[2, 2, 1]`**.

Ties in the remainder are broken by ascending tier number.

> **Known behavior at small window sizes:** at `WINDOW_SIZE = 3` the allocation is
> `[2, 1, 0]` and tier 3 gets no reserved slot (it can still appear via backfill). This is
> accepted — the default is 5.

### 3. Starvation guard

A pure quota cannot express urgency: a tier-3 problem failed 40 days ago is genuinely more
important than a tier-1 problem solved cleanly last week. So a subset of problems bypasses
tiering entirely.

**A problem is `urgent` if `box === 1` OR `daysUntil(due) <= -30`.**

Urgent problems are placed in the window first, in priority order, before any quota is
computed. If urgent problems alone meet or exceed `WINDOW_SIZE`, the window is entirely
urgent and no quota is computed that day — this is correct behavior, not a bug.

### 4. Selection algorithm

```
selectWindow(dueItems, N):
  if CAT_FILTER !== "all":
      return sortByPriority(dueItems).slice(0, N)      # tiering is meaningless when filtered

  urgent, rest = partition(dueItems, isUrgent)
  window = sortByPriority(urgent).slice(0, N)

  slotsLeft = N - window.length
  if slotsLeft == 0: return window

  quotas = largestRemainder(TIER_SHARE, slotsLeft)
  for tier in [1, 2, 3]:
      pool = sortByPriority(rest.filter(p => tierOf(p) === tier))
      window += pool.slice(0, quotas[tier])

  # backfill: a tier with fewer due problems than its quota gives its slots away
  if window.length < N:
      remaining = sortByPriority(rest.filter(p => p not in window))
      window += remaining.slice(0, N - window.length)

  return sortByPriority(window)      # final display order
```

**`sortByPriority(a, b)`** — the existing comparator at `app.js:382`, with the binary
`CORE` tiebreak replaced by tier rank:

1. Ascending `box` (weakest first)
2. Ascending tier number
3. Ascending `daysUntil(due)` (most overdue first)

The final re-sort ensures the displayed window reads in a sensible order regardless of the
order slots were filled in.

### 5. Clock-anchored grade labels

Four `sub` string edits at `app.js:179-182`. Box values and intervals are unchanged.

| Box | Label | Current `sub` | New `sub` |
|---|---|---|---|
| 1 | Failed | needed the solution · +1d | hit the cap / read the solution · +1d |
| 2 | Slow | solved with hints · +3d | needed a hint, or >40 min · +3d |
| 3 | Clean | solved, some hesitation · +7d | solved unaided, under ~30 min · +7d |
| 4 | Fast | instant & confident · +21d | under ~15 min, no stumbles · +21d |

This makes self-grading objective. It is the mechanism that makes the time-box protocol
below self-enforcing without any timer in the app.

---

## Time-Box Protocol (practice discipline, documented in `CLAUDE.md`)

Not code. Recorded here because the grade labels in §5 exist to serve it.

**Motivating case:** `spaced-repetition-practice/spiral_matrix_july22.py` took ~4 days
(~3-4 hours) to reach ~90%. The approach was correct from day one — four boundary pointers.
All of that time went to implementation mechanics, and produced a construct
(`while u == up:` wrapping a body that increments `up`, i.e. an `if` that runs once,
repeated four times) that would not survive a hint at minute 20.

The failure was not the 4 hours. It was **4 hours without ever seeing a correct solution** —
the spacing benefit of re-deriving daily, with none of the correction benefit.

**Two kinds of stuck, only one worth paying for:**

| Stuck on | Value of grinding | Action |
|---|---|---|
| The **approach** — pattern unknown | ≈ zero; an unknown pattern cannot be derived from first principles | Take the pattern name only, fast |
| The **implementation** — approach right, code wrong | High; debugging your own bounds is the transferable skill | Grind, but bounded |

**New problem — 60 minute hard cap:**

- **0–20 min** — blind, no hints. Brainstorm in a `NOTES:` comment block first.
- **@20 min, no approach** → take the *pattern name only* (not code, not pseudocode).
  Reset the clock.
- **20–50 min** — implement. Bugs here are the productive struggle.
- **@50–60 min, still broken** → read the solution, understand it, **close it**,
  re-implement from memory. Grade **Failed** → box 1 → returns tomorrow.
- **Never a second day on a first attempt.**

**Review rep — 15 minutes:**

- Can't get it in 15 min? The memory is genuinely gone. Grade **Failed**, skim the existing
  file in `patterns/`, move on. Reviews are never ground out — that is what the 1-day
  box-1 interval is for.

**Principle:** tomorrow's second attempt is worth more than today's third hour. Retrieval
after forgetting builds durable memory; re-reading your own stuck code builds almost nothing.

**Interaction with `WINDOW_SIZE = 5`:** at ~1 hr/day, a new problem consumes the entire
session; reviews at 15 min mean 3-4 fit. The window is sized for review days. Doing exactly
one thing on a new-problem day is the expected outcome, not a shortfall.

---

## Testing

No test harness exists in `prep-tracker/`. Verification is manual against the real
`progress.json` (55 due, 12 categories):

1. **Cap** — Due tab shows exactly 5 rows; header reads `Showing 5 of 55 due`.
2. **Tier mix** — with no urgent problems, the 5 rows are 2 tier-1, 2 tier-2, 1 tier-3.
3. **Refill** — grading the top row leaves 5 rows; the graded problem is gone; the counter
   increments to `1 graded today`.
4. **Urgency bypass** — grade something Failed, reload: it appears in the window regardless
   of its tier.
5. **Backfill** — apply a category filter with fewer than 5 due; confirm no crash, no
   duplicate rows, and that quotas are not exceeded by the backfill.
6. **Show all** — `[Show all]` reveals all 55; reload restores the cap.
7. **Data integrity** — `git diff prep-tracker/progress.json` after browsing (without
   grading) shows **no changes**. This is the key invariant: the window is a display
   filter and must never write.

## Risks

- **The window hides real work.** Mitigated by showing the true count (`5 of 55`) and the
  `[Show all]` escape hatch. The backlog is never silently misrepresented as empty.
- **Quota constants are guesses.** `TIER_SHARE` and the 30-day urgency threshold are
  judgment calls, not measured. They are single-line module constants, trivially tunable
  after a few weeks of real use.
- **Tier assignment is static.** As focus shifts (per `CLAUDE.md`, graphs are next), the
  tiers may need revisiting. Accepted — it is a one-line edit to `TIERS`, and the tiers
  encode general interview frequency rather than the current study topic.

## Open Questions

None. All decisions resolved during design.
