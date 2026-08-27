# reps — attempt history

Every **blind re-solve** of a problem you have already solved. Append-only: a new file per
attempt, never an edit to an old one. The dated trail *is* the point — `diff` two attempts and you
see exactly what your memory changed.

## The filename is the whole convention

```
YYYY-MM-DD_problem-slug.py
```

```
reps/2026-08-25_rotate-arr.py
reps/2026-08-25_reverse-string-ii.py
reps/2026-08-11_squared-sorted-array.py
```

Flat, and deliberately so. An earlier version of this file described a
`reviews/<category>/<problem>/DATE_grade.py` tree. **It was never created once**, because at 6pm
finishing a rep it costs four decisions — category, slug, two directories — and a flat file costs
one. Friction beats good intentions. The same thing happened to `sprint/`, which held zero files
across 39 problems before being deleted.

So: date first, so it sorts chronologically and the day's reps sit together.

```bash
ls reps                      # everything, oldest first
ls reps | grep rotate        # one problem's whole history
ls reps | grep 2026-08-25    # what you did today
```

**No grade in the filename.** The tracker already stores it, and a filename that disagreed with
`progress.json` would be worse than one that stays quiet.

## The loop

1. The app shows a problem **due**. Do not open the old file.
2. Solve it cold into a new `reps/YYYY-MM-DD_problem-slug.py`.
3. Submit on LeetCode to catch the edge cases.
4. Grade honestly in the app. That writes `apps/prep-tracker/progress.json`.
5. Write the trigger sentence while it is fresh — 46 of 61 problems still have none.
6. Found something cleaner? Update the canonical file in `patterns/` too.

## What does NOT go here

- **A first solve** of a new problem → `patterns/<category>/<problem>.py`. That is the canonical
  reference the tracker points at, and where the detailed `NOTES:` block lives.
- **Design practice** → `lld/`.
