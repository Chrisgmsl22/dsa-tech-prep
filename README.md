# dsa-tech-prep

Interview preparation: algorithms, low level design, and the tooling that keeps it honest.

## Layout

```
patterns/       canonical solutions, one file per problem, organised by pattern
reps/           attempt history — a dated file per blind re-solve, append-only
lld/            low level design practice (also the "build it by hand" track)
fundamentals/   how things work: python idioms, data structures, tree theory
docs/           design specs, reviews, and dated records
apps/           the tools
  prep-tracker/   spaced-repetition tracker over the 129-problem catalog
  playground/     visual explainers for algorithms
CLAUDE.md       the mentor brief and the study plan  (AGENTS.md symlinks to it)
```

**Where does a file go?** By *what it is*, never by where the problem came from:

| | |
| --- | --- |
| First time solving a problem | `patterns/<category>/<problem>.py` |
| Re-solving one you have done before | `reps/YYYY-MM-DD_problem-slug.py` |
| Designing a small system with classes | `lld/patterns/` or `lld/problems/` |
| Notes on how a structure or idiom works | `fundamentals/` |

An interview-specific problem list does **not** get its own directory. `patterns/` is indexed by
pattern; which interview sent you there is metadata, and the tracker already stores it. A `sprint/`
folder was tried and deleted — it held zero files across 39 problems.

## Daily use

```bash
python3 apps/prep-tracker/server.py     # then open http://localhost:8000/
```

3 reps a day, plus one new problem when there is time. The plan, the time-boxes, and the rest days
are in `CLAUDE.md`.

## Tests

```bash
node --test apps/prep-tracker/selection.test.js   # daily-window selection logic
python3 apps/prep-tracker/server_test.py          # persistence safety, 22 cases
```
