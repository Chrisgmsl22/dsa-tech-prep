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
  - Floor (5 min): 1 `/quick-rep`. On a rough day this is a win. The streak survives.
  - Standard (45 min): reps, or 1 new problem, plus the evening block.
  - Full (about 85 min): the whole budget. Do not plan above it.

## Rep types

| Type | Time | Used for | How |
|---|---|---|---|
| Quick rep | 5 min | Box 4 and up, and the triage set | `/quick-rep` session. Plan in plain words, no code |
| Full rep | 25 min cap | Box 1 to 3, and every other rep of a box 4+ problem | Blind code in `reps/YYYY-MM-DD_slug.py`, then LeetCode |
| New problem | 60 min cap | Unstarted problems | Time-box protocol in `CLAUDE.md` |

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

**Quick rep → tracker grade.** The student clicks the grade in the tracker. The skill only says
which one.

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
| 5 | Fast on box 4 | Planned, not built yet | 45 days |
| 6 | Fast on box 5 (coded) | Planned, not built yet | 120 days |

Until the tracker supports boxes 5 and 6, Fast means box 4.

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

## Planned tracker changes (not built)

- Boxes 5 and 6, with Fast as a climb.
- A weekly line ("new this week: 1/2, reps: 4") in place of the total due count.
- Hide the category of a problem until it is graded.
