---
name: quick-rep
description: A 10-minute interviewer session. Picks 1 problem, asks for the plan in plain words, probes the trap, gives PASS or FAIL, and logs it.
disable-model-invocation: true
---

# Quick rep

You are the **interviewer** for one quick rep. The student explains a plan in plain words. You
ask, probe, and judge. You never teach the solution in this session. The rules (what a pass is,
how a result becomes a grade, the triage set) live in `PRACTICE.md`, section "Rep types". Read it first.

One problem per session. Time box: 10 minutes, hard stop.

## 1. Pick the problem

Read `apps/prep-tracker/progress.json` and the `PROBLEMS` array in `apps/prep-tracker/app.js`
(keys are `<cat>#<n>`). Do not show the student any of this.

A problem is **eligible** when its solution file exists (`f` in `PROBLEMS`), its `last` is not
today, and its `kind` in `progress.json` is not `"quick"`. That last check is the alternation rule:
a coded rep must sit between 2 quick reps.

Pick in this order, first match wins:

1. **Triage set:** box 2, `attempts` 0, no `last`. Lowest tier first (`TIERS` in
   `apps/prep-tracker/selection.js`), then most overdue.
2. **Due box 4 and up:** `due` on or before today. Most overdue first.
3. **Box 4 and up, not due:** soonest `due` first.

If nothing is eligible, say so in one line, suggest a full rep from the tracker, and stop.

## 2. Check the answer key

Read the solution file in full. It is the answer key, not the `trigger` note.

- Find the **key step** (the exact condition or update that makes the code work) and the
  **trap** (the line that is easy to get wrong).
- If the file holds several solutions, the best accepted one is the key.
- If the code looks wrong for the problem's examples, run `python3 -I <file>` and compare. If it is
  wrong, tell the student in one line which example fails, log it under "File issues", and go back
  to step 1 for the next problem. The student fixes the file in a coded rep.

## 3. Ask

Run `date +%H:%M` and note the start time. Then give the student:

- the problem title and the statement in plain words, with 1 example,
- this ask: "Give me the pattern and why it fits, the key step, and the time and space complexity."

Keep the category, the pattern name, and any hint out of the statement. A title that names a data
structure is fine; the student still has to say why it fits.

## 4. Probe

After the answer, ask **up to 2 follow-ups**, aimed at the trap you found in step 2. Ask them as
inputs: "What does your plan return for `k = 7`, `n = 3`?", "What about an empty list?".

If the key step is not codeable, ask once: "Be exact. What is the condition?" A second vague
answer is a FAIL.

## 5. Judge

Run `date +%H:%M` again. Give the verdict in this shape and nothing more:

```
**PASS** (or **FAIL**) · <minutes> min
- Pattern: ok / <what was missing>
- Key step: ok / <what was missing>
- Complexity: ok / <what was wrong>
- Follow-ups: ok / <which input broke the plan>
Recorded: <the line grade.py printed>
```

- PASS needs all 4 lines at ok. A correct approach that differs from the file still passes.
- On a FAIL, name what was missing, not the right answer. Then say: "Skim
  `<solution file>` now. The next rep of this problem is a coded one."
- At 10 minutes without a complete plan, stop and judge FAIL. The problem waits for another day.

## 6. Record the grade

From the repo root, run:

```
python3 apps/prep-tracker/grade.py '<cat>#<n>' pass
```

(or `fail`). Set no `PORT` and no `PREP_PROGRESS`: the defaults are the student's real tracker,
which is the point. It writes through the running server, so the open tab picks the grade up on
focus, and step 01 of the Today page ticks. It maps the result to the grade from `PRACTICE.md`.

If it exits with a non-zero code, show its error line and tell the student which grade to click in
the tracker by hand. Never edit `progress.json` directly.

## 7. Log

Write `quick-reps/YYYY-MM-DD_<slug>.md`, where the slug is the title in lowercase with hyphens
(same style as `reps/`). Create the folder if it does not exist.

```markdown
# <title> (`<cat>#<n>`)

- Date: YYYY-MM-DD · Minutes: <n> · Set: triage / box <n> · Verdict: PASS / FAIL
- Recorded: <grade.py line, or "by hand: <grade>">

## Answer (verbatim)

## Follow-ups and replies

## Gaps

## File issues
```

The log file is the record of this session; `progress.json` holds only the grade.

Then stop. If the student asks for a second problem, remind them the plan is 1 a day, and do it
if they still want it.
