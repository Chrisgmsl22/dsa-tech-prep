# Reviews — Active-Recall Attempt History

Append-only log of **blind re-solves** for spaced-repetition practice. Every review rep gets its
own dated file, so nothing is overwritten and you can see your progression on a problem over time.

## Structure

```
reviews/<category>/<problem_slug>/
    YYYY-MM-DD_<grade>.py
```

- `<category>` — same slug as in `patterns/` (e.g. `arrays_and_strings`, `two_pointers`).
- `<problem_slug>` — snake_case problem name (e.g. `merge_strings_alternately`).
- `YYYY-MM-DD` — the date of the attempt (sorts chronologically).
- `<grade>` — how it went: `failed` | `slow` | `clean` | `fast` (matches the app's grades).

Example:

```
reviews/arrays_and_strings/merge_strings_alternately/
    2026-07-16_slow.py
    2026-07-23_clean.py
    2026-08-14_fast.py
```

## The rule

- **Canonical solution** lives in `patterns/<category>/<problem>.py` — that's the reference the
  Prep Tracker points at, and where your detailed `NOTES:` block lives.
- **Each review rep** is a *new* file here, written **cold** (don't open the canonical file or a
  past attempt until after you've solved it). The blind retrieval is the whole point.
- **New problems** are NOT reviews — their first solve goes in `patterns/`, not here.

## Why dated files instead of editing one

- `ls reviews/<cat>/<problem>/` → your rep history at a glance, grades trending toward `fast`.
- `diff` two dated attempts → exactly what your memory changed between reps.
- Nothing is lost; the timeline is the feedback.

## Loop

1. App shows a problem **due**. Don't peek at old code.
2. Solve cold into a new `reviews/.../YYYY-MM-DD_<grade>.py`.
3. Submit on LeetCode to catch every edge case.
4. Grade in the app (writes `prep-tracker/progress.json`).
5. If you found a cleaner approach, update the canonical `patterns/` file too.
