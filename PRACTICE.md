# DSA practice framework

Set 2026-10-12. This file is the single source of truth for how DSA practice runs: the week, the
rep types, the boxes, and the order of new problems. `CLAUDE.md` points here. The tracker
(`apps/prep-tracker/`) and the `/quick-rep` skill follow it.

## Why it looks like this

- The goal has 2 parts: keep solved patterns alive, and get through all 129 problems.
- Real capacity is about 45 minutes a day, 5 days a week, with on-call weeks and home events.
- The old setup asked for about 12 reps a day (27 problems at box 2 on a 3-day interval, and a
  21-day cap on box 4). Real rate was about 1 a day. The pile was a math result, not a lapse.
- New problems have the higher return now. A new problem in a known pattern is also a rep of that
  pattern. A new problem in an unknown pattern closes a gap that no rep can close.
- Reps protect what new problems built. Their return drops as a problem climbs the boxes, so the
  cheap rep type goes to the high boxes.

## The week

- **New problems: target 2 a week, stretch 3.** A weekly quota, so a missed day moves nothing.
- **Daily rule:** if there are 45 minutes and fewer than 2 new problems this week → do a new
  problem. Otherwise → reps.
- **Day levels:**
  - Floor (10 min): 1 `/quick-rep`. On a rough day this is a win. The streak survives.
  - Standard (45 min): reps, or 1 new problem, plus the evening block.
  - Full (about 85 min): the whole budget. Do not plan above it.

## Rep types

| Type | Time | Used for | How |
|---|---|---|---|
| Quick rep | 10 min, hard stop | Box 4 and up, and the triage set | `/quick-rep` session. Plan in plain words, no code |
| Full rep | 35 min, hard stop | Box 1 to 3, and every other rep of a box 4+ problem | Blind code in `reps/YYYY-MM-DD_slug.py`, then LeetCode |
| New problem | 60 min, hard stop | Unstarted problems | Time-box protocol in `CLAUDE.md` |

## How to grade

Check from the top. The first row that matches is the grade. Use the clock, not the feeling.

**Full rep**

| Grade | Check |
|---|---|
| Failed | No accepted solution at 35 min, or you looked at the solution or the old file |
| Slow | Accepted, but you needed a hint, or it took 26 to 35 min, or 3 or more wrong submits |
| Clean | Accepted with no hint, 16 to 25 min, at most 2 wrong submits |
| Fast | Accepted with no hint, 15 min or less, at most 1 wrong submit |

**New problem**

| Grade | Check |
|---|---|
| Failed | You read the solution, or you hit 60 min |
| Slow | Accepted, but you needed the pattern-name hint, or it took more than 40 min |
| Clean | Accepted with no hint, 21 to 40 min |
| Fast | Accepted with no hint, 20 min or less |

- **A hint** is anything outside your head: the mentor, the `trigger` note, an old file, a video,
  an AI autocomplete. A pattern name counts.
- **A wrong submit** is a LeetCode submit that fails. A failed "Run" on the sample does not count.
- **Grade up honestly.** If the clock says 12 minutes and the code passed, click Fast, not Clean.
  Problems must climb to box 4 and higher, or the queue fills again.
- **You never pick box 5 or 6.** Fast on a box 4 problem moves it to box 5. Fast on box 5 moves it to
  box 6. Any other grade sets the box in the table above, so a miss drops the problem down.

**Quick rep rules**

- The answer has 3 parts: the pattern and why it fits, the key step, the time and space complexity.
- The key step must be **codeable**: a stranger could write the main loop from it. "Use a set" is
  the pattern again, not a step.
- The interviewer asks up to 2 follow-ups aimed at the trap in the code (`k > n`, empty input,
  an off-by-one bound, a value used as a sentinel).
- The answer key is the accepted solution file in `patterns/`, not the `trigger` note. A correct
  approach that differs from the file still passes.
- **Alternate.** A problem never gets 2 quick reps in a row. A coded rep sits between them.
- Box 6 needs a clean coded rep. A quick rep can never promote a problem to box 6.
- A same-day correction of a quick rep in the tracker stays a quick rep, so it also stops at box 5.

**Quick rep → tracker grade.** The `/quick-rep` skill records the grade with
`apps/prep-tracker/grade.py <key> pass|fail`. The tracker tab picks it up when you return to it,
and step 01 of the Today page ticks.

| Set | PASS | FAIL |
|---|---|---|
| Box 4 and up | Fast | Failed |
| Triage (box 2, 0 attempts) | Clean | Failed |

**The triage set** is the 23 problems seeded at box 2 with 0 attempts and no `last` date. They
were never graded in the tracker. `/quick-rep` picks from them first, 1 a day, until none are
left. This turns 23 unknowns into real boxes.

## Boxes

| Box | Grade | Meaning | Next review |
|---|---|---|---|
| 0 | none | Never tried, not in rotation | never |
| 1 | Failed | Needed the solution | 1 day |
| 2 | Slow | Solved slow or with hints | 3 days |
| 3 | Clean | Solved with no help | 7 days |
| 4 | Fast | Fast and confident | 21 days |
| 5 | Fast on box 4 | Known well | 45 days |
| 6 | Fast on box 5 (coded) | Known for a long time | 120 days |

## Order of new problems

1. The first problem in each pattern with 0 solved: 1 greedy, 1 sorting.
2. Then alternate: the roadmap topic (grids, then graphs) and a tier 1 gap (hashmaps and sets,
   then arrays and strings).
3. DP comes last.
4. Trees and graphs stay tier 2. Linked lists can stay thin.

## Files

- `patterns/<category>/<problem>.py`: the accepted solution. The answer key for quick reps.
- `reps/YYYY-MM-DD_slug.py`: one file per full rep. See `reps/README.md`.
- `quick-reps/YYYY-MM-DD_slug.md`: one file per quick rep, written by `/quick-rep`.
- `.claude/skills/quick-rep/SKILL.md`: the interviewer script.

## The tracker

Built 2026-10-13 to match this file: boxes 1 to 6, the Today page (01 quick rep, 02 reps, 03 new
problem), the weekly line in place of the due count, hidden categories in rep rows, and `grade.py`.
How to run it and how each view works: `apps/prep-tracker/README.md`.
