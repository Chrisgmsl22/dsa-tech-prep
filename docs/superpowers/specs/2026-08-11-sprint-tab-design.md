# Sprint Tab — Interview Prep Plan

**Date:** 2026-08-11

## Problem

A technical-assessment invite arrived with a fixed practice plan: 39 problems split into 9 topic
days. The existing Prep Tracker is a *long-horizon spaced-repetition* tool over the AlgoMap 100.
The two do not mix:

- Only 10 of the 39 sprint problems exist in the `PROBLEMS` catalog.
- Two sprint groups (greedy/intervals, sorting & divide-and-conquer) are categories the tracker
  does not model.
- The student will not solve all 39. Most are a study reference.

## Decision

Add a fifth tab, **Sprint**, to the existing app. It is a checklist with memory, not a second
scheduler. After the test, the keepers merge into `PROBLEMS` and join the Leitner rotation.

**No calendar.** The plan ships with day numbers, and those are kept as *labels for chunks of the
list* — they order the groups and let the student say "I'm on Day 3". Nothing computes a date, a
countdown, or an overdue state. A hard-coded calendar would be stale within a week, and the list
is meant to survive into the next interview.

### Non-goals

- No scheduling. No Leitner box, no due date, no effect on **Due today**.
- No dates, no countdown, no "today" marker, no falling-behind state.
- No change to `selection.js` and no change to the daily window logic.
- No new server behavior. The existing `api/progress` endpoint carries the new state.

## Data — `prep-tracker/sprint.js`

Loaded as a classic script before `app.js`, the same as `selection.js`. Three exports:

- `SPRINT_META` — `{ format, order }`: the test's shape and its suggested problem order. No dates.
- `SPRINT_GROUPS` — 9 rows of `{ g, dir, label }`. `g` orders the groups and renders as the day
  number; `dir` is the folder under `sprint/`.
- `SPRINT` — 39 records:

```js
{ g: 5, slug: "rotate-image", title: "Rotate Image",
  url: "https://leetcode.com/problems/rotate-image/",
  pri: "essential",                 // essential | stretch | optional
  maps: "arrays_and_strings#11" }   // optional: the catalog twin
```

`maps` is what makes the post-test merge mechanical. Ten sprint problems have a twin. Each `url`
is derived from the slug at load time, so the LeetCode prefix appears once rather than 39 times.

## State

Flat keys in the existing progress object, namespaced by prefix:

```json
"sprint#rotate-image": { "status": "done", "trigger": "square ring by ring, offset by layer" }
```

The prefix scheme is deliberate: the existing `input` handler already writes `STATE[pid].trigger`
for whatever `data-id` the row carries, so the note field needs **zero** new code. `seedIfNeeded()`
iterates `PROBLEMS` only, so sprint keys can never be given a box or a due date by accident.

`status` is one of `done` / `stuck` / `skipped`, or absent. Clicking the active status clears it.

**Reset** preserves every `sprint#` key. Wiping the Leitner state must not wipe a sprint that is
mid-flight; the confirm text says so.

## UI

A `Sprint` tab between `All` and `How it works`. When it is active:

- The category filter chips hide — they describe AlgoMap categories, not sprint groups.
- The stat strip swaps to: marked stuck, essential done, sprint done, trigger notes.
- All 39 problems render under 9 day headers, each with a done/total count. A finished group turns
  green with a ✓. Every group is always visible — a problem from Day 1 is still fair game later.
- Within a group, rows sort by set, then essential → stretch → optional. The set key matters only
  for Day 9, where sorting by priority alone would interleave Set A and Set B.
- A row shows a priority tag, the title, and its status; the meta reads "already solved" when its
  catalog twin is done.
- Clicking a row opens a panel with: the 3 status buttons, the trigger-sentence textarea, the
  LeetCode link, the suggested repo path, and the twin's state if it has one.

## Solution files

`sprint/<topic>/<problem>.py`, with the usual `NOTES:` block. Topic folders match the `patterns/`
naming so the merge is a move, not a rename. The panel prints the exact path.

## Merge, after the test

Documented in `prep-tracker/README.md` §7. For each keeper: move the file into
`patterns/<category>/`, flip or add the `PROBLEMS` entry, copy the trigger note onto the new key,
delete the `sprint#` key, and — for the two categories the catalog lacks — add `greedy_intervals`
and `sorting` to `CAT_META`, `CAT_ORDER`, and `TIERS[3]`.

## Triage encoded in `pri`

39 problems does not fit inside a 60-minute-per-problem cap, and several listed problems sit above
the test's stated scope (1D/2D arrays, hash maps, stacks, matrix traversal, lists, graphs). The
`pri` field encodes the cut:

- **essential** (20) — arrays, two pointers, matrix, hash maps, the core sliding window pair,
  binary search, and sorting.
- **stretch** (7) — do these when a day runs short.
- **optional** (12) — the Hards and most of the greedy day. Reference only; skipping them is the
  plan working as intended, not a failure.

## Verification

Exercised in a real browser against a throwaway fixture on a separate port, never the committed
`progress.json`: all 39 rows render under 9 headers; status write, note write, and reload restore
all persist to disk; a second click on the active status clears it and the note survives; no
sprint key ever receives a box; **Reset all** keeps the sprint and reseeds the catalog; the other
four tabs render unchanged (3 / 43 / 100 / help) and the filter chips return with them.
