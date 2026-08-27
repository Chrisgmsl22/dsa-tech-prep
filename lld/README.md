# lld — low level design practice

Design a small system with OOP: classes, responsibilities, a deliberately chosen pattern. This is
an interview round in its own right, and it is also the "organic projects" track — small apps
written **by hand**, to keep the fundamentals sharp as more code gets generated.

## Two sizes, matching the weekly plan

```
lld/
  patterns/          one pattern, one small demo        -- weekly, Sunday
    01_factory/
    02_observer/
  problems/          a full design, several patterns    -- roughly monthly
    01_parking_lot/
    02_elevator/
```

The weekday blocks feed the Sunday session: **Tue** study the pattern, **Thu** sketch the classes,
**Sun** build it.

## The README is the deliverable

Every folder starts with a `README.md`, written **before** the code:

1. **Requirements** — what it must do, in your own words. Interviews start here, and the
   clarifying questions you ask are part of the grade.
2. **Out of scope** — what you deliberately are not building. Saying this out loud is half of
   what separates a senior answer from a junior one.
3. **The classes** — names and responsibilities. One line each.
4. **The pattern, and why** — including which alternative you rejected.
5. **What you would change** if the requirements doubled.

Then the code, as evidence that the design survives contact with a keyboard.

In an LLD round you are graded on the reasoning, not the syntax. Code alone is also the part you
cannot re-read usefully in a month; the README is.

## Problems worth doing

Parking lot · elevator · vending machine · rate limiter · ATM · library · chess board ·
food delivery · notification service.

Small enough to finish in a session, and they are literally the interview questions.
