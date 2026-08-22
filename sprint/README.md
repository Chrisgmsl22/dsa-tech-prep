# Interview Sprint

Solutions for a **one-off problem list tied to a specific interview** — a take-home plan, a
screen's prep sheet, a recruiter's topic list. The checklist itself, the per-problem status, and
the trigger notes live in the **Sprint** tab of the Prep Tracker
(`python3 prep-tracker/server.py`). This directory holds only the code.

Empty right now. The last sprint was merged into the main catalog; see the record at the bottom.

## How a sprint runs

1. Load the problem list into `prep-tracker/sprint.js` — its header documents the three constants,
   and `prep-tracker/README.md` §7 has the walkthrough.
2. Tag every problem `essential`, `stretch`, or `optional`. **A list that does not fit is the
   normal case**, and the tag is what you cut.
3. Solve into `sprint/<topic>/<problem>.py`, with the usual `NOTES:` block. Each row's panel in
   the app prints the exact path, so there is nothing to decide mid-session.
4. Mark each problem **Done**, **Stuck**, or **Skipped**, and write the trigger sentence while it
   is fresh.
5. After the test, merge the keepers into the catalog — `prep-tracker/README.md` §7 — and empty
   `sprint.js` for next time.

**Day numbers in the app are labels, not deadlines.** Nothing tracks a calendar, nothing turns
red, and falling a day behind costs nothing.

## The rules that still apply

The time-box protocol in `CLAUDE.md` does not relax because a real test is close. If anything it
matters more:

- 60-minute hard cap on a first attempt. Past 50 minutes and still broken → read the solution,
  close it, retype it from memory, grade **Failed**.
- Never a second day on a first attempt.
- At ~20 minutes with no approach, take the **pattern name only**. An unknown pattern cannot be
  derived from first principles, so grinding on it returns nothing.

## Test-day tactics worth reusing

Generic enough to survive to the next interview:

1. Run the platform's sample test first, so the editor holds no surprises.
2. Do the short problems first and leave the longest for last. Read all of them before starting.
3. Use your strongest language. Most platforms let you switch between problems.
4. Write clean, structured code — the approach is usually graded, not only the output.
5. Run and submit as often as allowed. Print freely to debug.
6. If you stall, skip and come back. Do not burn the clock on one problem.
7. State the time and space complexity in a comment above each solution. Cheap marks.

**Before you submit anything**, the four checks that cost real time in the 2026-08 sprint:

1. Test with a parameter that **separates a constant's roles** — `k = 2` hid a bug that `k = 3`
   exposed immediately.
2. Run one edge case by hand: empty, size 1, `k > n`, all-equal, negatives.
3. Never use a data value as a sentinel. `if nums[i] == 0` breaks when `0` is real data — use the
   given lengths and indices.
4. Apply a named fix and **re-run before writing anything new**.

One more, earned the hard way: when an index or count can exceed the data, ask whether the
structure **wraps** (`% n`, as in a rotation) or **clamps** (`min`, as in fixed-size chunks). The
two look identical and behave in opposite ways.

## Record — 2026-08 sprint (merged)

- A 70-minute, 4-problem assessment. Practice plan: 39 problems across 9 days.
- 4 attempted: Running Sum (done), Merge Sorted Array, Rotate Array, Reverse String II (stuck).
  The remaining 35 stayed reference reading — the triage working as intended.
- The last session before the test was a pattern crash course, not new problems. The drill sheet
  is `spaced-repetition-practice/crash_course.py` and is worth re-running before any interview.
- Merged 2026-08-21: 10 problems already existed in the catalog, 29 were new, taking the roadmap
  from 100 to 129. Added the `greedy` and `sorting` categories. 3 solutions moved into `patterns/`.
