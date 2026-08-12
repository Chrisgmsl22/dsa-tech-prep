# Interview Sprint

Solutions for the practice plan that came with a technical-assessment invite. The checklist, the
status of each problem, and the trigger notes live in the **Sprint** tab of the Prep Tracker
(`python3 prep-tracker/server.py`). This directory holds only the code.

## The test format

| | |
| --- | --- |
| **Format** | 70 minutes · 4 problems · **no pausing** once started |
| **Window** | Take it within 10 days of the invite |
| **Setup** | Webcam + mic on the whole session, screen shared, latest Chrome or Firefox |
| **Result** | Pass/fail only, no score detail. A retake is allowed after 6 months. |
| **Topics** | 1D/2D arrays, hash maps, stacks, matrix traversal (spiral, row/col order), lists, graphs |

## On the day

1. Run the platform's sample test first (5–10 exercises) so the editor holds no surprises.
2. Order: **problems 1 and 2 first → skip to 4 → leave 3 for last.** Problem 3 is the longest.
3. Use Python. You may switch languages between problems.
4. Write clean, structured code. They grade the approach, not only the output.
5. Run and submit as often as you want. There is no penalty.
6. Print freely to debug.
7. If you stall, skip and come back. Do not burn the clock on one problem.
8. You may look up **syntax only**, in a new tab — not a new window. No full solutions.

## The 9 groups

The plan splits 39 problems into 9 named days. **They are labels, not deadlines.** Nothing in the
app tracks a calendar, nothing turns red, and falling a day behind costs you nothing.

| Day | Topic | Folder |
| --- | --- | --- |
| 1 | Arrays (1D) Foundations | `sprint/arrays/` |
| 2 | Strings & String Manipulation | `sprint/strings/` |
| 3 | Two Pointers | `sprint/two_pointers/` |
| 4 | Sliding Window | `sprint/sliding_window/` |
| 5 | Matrix & Multidimensional Arrays | `sprint/matrix/` |
| 6 | HashMaps & Sets | `sprint/hashmaps/` |
| 7 | Greedy Strategies | `sprint/greedy/` |
| 8 | Divide & Conquer + Recursion | `sprint/divide_conquer/` |
| 9 | Full Timed Simulation | `sprint/simulation/` |

Day 9 is a **mock run**, not a study day: pick Set A or Set B, set a 70-minute clock, use the
order above, and grade the *run* rather than the problems.

## File convention

```
sprint/matrix/rotate_image.py
```

Same as `patterns/`: the solution plus a `NOTES:` block. Each row's panel in the Sprint tab prints
the exact path to use, so there is nothing to decide mid-session.

## Triage — read this before you feel behind

39 problems is more than the time available at a 60-minute-per-problem cap. **The list does not
fit, by design.** The tag on every row says what to cut:

- **essential** (20) — do these. Arrays, two pointers, matrix, hash maps, the core sliding-window
  pair, binary search, sorting.
- **stretch** (7) — do these when a day runs short.
- **optional** (12) — the LeetCode Hards and most of the greedy day. Several sit above the test's
  own stated topic list. Read them as reference and move on.

Skipping an optional is the plan working. Grinding a Hard on Day 2 while Day 5 matrix traversal
goes untouched is the actual failure mode.

The 60-minute cap and the "never a second day on a first attempt" rule from `CLAUDE.md` still
apply. A deadline is a reason to hold the time-box harder, not to abandon it.

## After the test

The problems worth keeping get folded into the tracker's 100-problem catalog and join the
spaced-repetition rotation. Steps are in `prep-tracker/README.md` §7.
