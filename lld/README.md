# lld — low level design practice

Design a small system with OOP: classes, responsibilities, a deliberately chosen pattern.
This is an interview round in its own right, and it is also the **organic projects** track —
small apps written **by hand**, in **Python**, to keep the fundamentals sharp as more code gets
generated.

**Python on purpose.** It is the language of the DSA track, so the syntax costs nothing and the
attention goes to the design. `abc.ABC`, `@abstractmethod`, `@property`, `__iter__` and
`dataclasses` are the Python parts this track teaches you.

---

## 1. Two lanes, and they never block each other

| Lane | Slot | Unit of work | Depends on |
| --- | --- | --- | --- |
| **A — pattern drills** | any weekday evening, 40 min | 1 pattern: `README.md` + `demo.py` + `test_demo.py` | nothing |
| **B — LLD problems** | Sunday, 90 min | 1 problem: `README.md` first, then code | the pattern bank, never on this week |

**The rule that removes every dependency between days:** a Sunday build uses **any pattern
already in the bank**, never this week's pattern. The bank only grows. So a missed Tuesday
delays lane A by 1 item and does not touch Sunday.

**Both lanes are queues, not calendars.** You take the next item off the top. There is no
"behind". If you skip 4 days, the top of the queue is the same item it was.

Roughly every 4 weeks, lane B takes a **full problem** that combines 3 or more patterns instead
of 2.

---

## 2. The README is the deliverable

Every folder starts with a `README.md`, written **before** the code. The stub asks the
questions; you answer them **from memory**, after 10 minutes of reading at most.

In an LLD round you are graded on the reasoning, not the syntax. Code is also the part you
cannot re-read usefully in a month. The README is.

**An article you read is not practice.** A session that ends with no written file did not happen.

---

## 3. Lane A — the pattern queue

Ordered so that each item makes the next one cheaper. The GoF families are marked, because a
reviewer names them.

| # | Pattern | Family | Needs | Round | Work |
| --- | --- | --- | --- | --- | --- |
| — | **EXAMPLE — Null Object** *(worked, read first)* | Behavioral | — | — | ✅ |
| 00 | SOLID + Dependency Injection | *vocabulary* | — | ✅ | ✅✅ |
| 01 | Strategy | Behavioral | — | ✅✅ | ✅ |
| 02 | Factory Method | Creational | 01 | ✅✅ | ✅ |
| 03 | Template Method | Behavioral | 01 | — | ✅ |
| 04 | Observer | Behavioral | — | ✅✅ | ✅✅ |
| 05 | State | Behavioral | 01 | ✅✅ | — |
| 06 | Command | Behavioral | 01 | ✅ | ✅ |
| 07 | Chain of Responsibility | Behavioral | 06 | ✅ | ✅✅ |
| 08 | Adapter | Structural | — | ✅ | ✅✅ |
| 09 | Repository (+ DI in practice) | *not GoF* | 08, 00 | — | ✅✅ |
| 10 | Decorator | Structural | 08 | ✅ | ✅✅ |
| 11 | Facade | Structural | 08 | — | ✅✅ |
| 12 | Composite | Structural | 10 | ✅ | ✅ |
| 13 | Iterator | Behavioral | 12 | — | ✅ |
| 14 | Singleton | Creational | 09 | ✅ | ✅ |
| 15 | Builder | Creational | 02 | ✅ | ✅ |

**Round** = how often an LLD interview wants it. **Work** = how often you must recognize it to
read and review real code. The 2 columns do not overlap, which is why both exist.

**Family counts:** 3 Creational, 4 Structural, 7 Behavioral, plus 1 non-GoF and the vocabulary
item. That is the GoF spread, weighted toward Behavioral because that is where LLD rounds live.

### The 3 chains inside that order

1. **01 → 02 → 03 → 05 → 06 → 07.** One interface with swappable bodies, then who picks it,
   then the inheritance version, then a body that swaps itself, then a body stored as an object,
   then a list of those objects.
2. **08 → 10 → 12 → 13.** Wrap to translate, wrap and keep the interface, then a tree of the
   same interface, then how to walk that tree.
3. **02 → 15** and **09 → 14.** The creational family closes each of its 2 questions.

### Deliberately skipped

Abstract Factory (a Factory of Factories — read item 02 and you can derive it) · Prototype
(`copy.deepcopy` in Python) · Bridge (rare, and it reads as 2 Strategies) · Flyweight (a memory
trick, not a design lesson) · Proxy (item 10 with a gate; add it if a round asks) · Mediator ·
Memento (add it when you build undo) · Visitor (worth it only with item 12 in place) ·
Interpreter (a compiler topic).

Add any of them as item 16 or later, when a real problem asks for it — never before.

---

## 4. Lane B — the problem queue

Ordered easy to hard. The **Needs** column is a hint, not a gate: take the top problem whose
patterns you already drilled, and pass over one that is not ready.

| # | Problem | Patterns it pulls | Needs |
| --- | --- | --- | --- |
| 01 | Vending machine | Strategy, State | 01, 05 |
| 02 | Parking lot | Factory, Strategy | 01, 02 |
| 03 | Logger | Chain of Responsibility, Decorator, Singleton | 07, 10, 14 |
| 04 | ATM | State, Chain of Responsibility | 05, 07 |
| 05 | Notification service | Observer, Adapter, Strategy | 04, 08 |
| 06 | File system | Composite, Iterator | 12, 13 |
| 07 | LRU cache | Strategy, Repository | 09 |
| 08 | Rate limiter | Strategy, Repository | 01, 09 |
| 09 | Library lending | Repository, Observer | 04, 09 |
| 10 | Elevator | State, Command, Observer | 04, 05, 06 |
| 11 | Tic-tac-toe, then a chess board | Strategy, State, Composite | 05, 12 |
| 12 | Food delivery *(the monthly big one)* | 4 or more | most |

Deck of cards and snake-and-ladder are good 45-minute warm-ups if a Sunday is short.

---

## 5. Folder layout

```
lld/
  README.md                      this file — both queues
  run_tests.sh                   runs every test
  _templates/                    copy these to start an item
  patterns/
    EXAMPLE_null_object/  README.md  null_object.py  test_null_object.py   <- solved
    00_solid_and_di/    README.md
    01_strategy/        README.md  strategy.py  test_strategy.py
    05_state/           README.md  state.py     test_state.py
    ...
  problems/
    01_vending_machine/ README.md  <then the code>
```

File names carry the slug, not the word `demo`. Two files named `demo.py` in 2 folders collide
under pytest, and the error message is not obvious. This layout avoids it.

---

## 6. One shared domain for all 16 patterns

**This is the trick that makes the patterns comparable.** If every item uses a different toy
problem, you learn 16 toys. If every item uses the **same** domain, only the pattern changes, so
the difference between Strategy and State becomes visible instead of theoretical.

**The domain: a coffee shop order system.** The nouns need no explanation, and it is the domain
the standard literature already uses — Head First Design Patterns builds its Decorator chapter on
a coffee shop. So the video you watch at minute 3 uses the same nouns as the file you write at
minute 25.

| # | Pattern | The slice of the coffee shop to use |
| --- | --- | --- |
| 00 | SOLID + DI | critique 1 file you already wrote against the 5 letters |
| 01 | Strategy | the price rule: full price, happy hour, or staff discount |
| 02 | Factory Method | build a drink from a name: `"latte"` → a `Latte` |
| 03 | Template Method | the prep skeleton: grind, brew, add, serve — 1 step varies per drink |
| 04 | Observer | an order becomes ready. The screen, the printer and the barista all react |
| 05 | State | the order status: `Placed` → `InProgress` → `Ready` → `Collected` |
| 06 | Command | "add a latte" as an object, so a wrong tap is undone |
| 07 | Chain of Responsibility | the order checks, in order: size valid → stock → payment |
| 08 | Adapter | 1 payment interface, 2 back ends: cash and a card terminal |
| 09 | Repository + DI | all order reads and writes behind 1 interface |
| 10 | Decorator | milk, syrup, an extra shot. **The textbook case for this pattern** |
| 11 | Facade | 1 call, `shop.order("latte", ["oat"])`, over 5 collaborators |
| 12 | Composite | menu → section → item, all answering `price()` |
| 13 | Iterator | walk the open-order queue with `__iter__`, then a generator |
| 14 | Singleton | the price list. Then write the test it makes hard |
| 15 | Builder | a custom drink has 9 optional fields. Assemble one readably |

**Guard rail:** you are not building a coffee shop app. Each file stays at 40 lines or fewer and
touches 1 slice. **No folder imports another folder.** Item 01 and item 05 never meet. The domain
supplies the **names**, nothing else.

At item 09 this domain also feeds the FastAPI step for free: 3 routes — place an order, read an
order, list open orders — over the repository you already built.

---

## 7. How to start a pattern — the 40-minute protocol

You asked whether to read or watch first. **Yes, read first — and this is not cheating.** It is
the same rule as your DSA time box: an unfamiliar pattern cannot be derived from first
principles, so you take the name and the shape, then you earn it back by a blind rewrite.

| Minutes | Do this |
| --- | --- |
| 0–10 | Read or watch. **1 source only.** Refactoring.Guru, or 1 video. Then **close it.** |
| 10–20 | Write README sections 1 and 2 **from memory**, source closed. |
| 20–35 | Write the test **first**, then the demo, until the test passes. |
| 35–40 | Write README sections 4, 5 and 6. Set **Status: done**. |

**Test first, on purpose.** A test forces you to name the caller's view of the pattern before you
write the machinery. If you cannot write the test, you have not understood the pattern — and that
is a cheaper discovery at minute 20 than at minute 35.

**The 2 sections that matter most** are 4 (one wrong case) and 5 (the alternative I reject).
Anybody can restate a definition. Only understanding produces those 2.

**If minute 20 arrives and section 2 is blank:** reopen the source for 5 minutes, then close it
again. That is the pattern-name hint from the DSA protocol, applied here.

**Never a second night on 1 pattern.** Set Status to `done` at a weak level, and let the next
problem in lane B expose the gap. Retrieval later beats a re-read now.

---

## 8. `demo` file rules

- 40 lines or fewer. It is not an app.
- **No `print`.** The test is how you check it.
- Real names from section 6. `LeitnerScheduler`, never `ConcreteStrategyA`.
- 1 test for each part you named in README section 2. If a part needs no test, you probably do
  not need the part.

## 9. How to run a test

```bash
python3 -m venv .venv                                   # once
.venv/bin/python -m pip install -r requirements-dev.txt # once
./lld/run_tests.sh                                      # every LLD test
.venv/bin/pytest lld/patterns/01_strategy -q             # 1 item
```

pytest puts the item folder on `sys.path`, so `from strategy import LeitnerScheduler` resolves.

---

## 10. When FastAPI enters — item 09, not before

A web framework adds HTTP, async, serialization and a server loop. That is 4 new subjects in
competition with the 1 subject you study, and a framework **hides** a pattern behind its own
machinery. So the first 8 items stay plain Python.

**At item 09 that reverses.** FastAPI's `Depends` *is* dependency injection, and a route handler
is the clearest place to see why a Repository behind an interface pays. So:

| Milestone | What happens |
| --- | --- |
| After item 09 | Add `fastapi` and `uvicorn` to `requirements-dev.txt`. |
| Lane B problem 08 or 09 | Build it as a small FastAPI app: 3 routes, 1 repository, no database. |
| Test it | `fastapi.testclient.TestClient`, still pytest, still 1 command. |

Until then, FastAPI is a distraction with a good reputation.

## 11. Progress

Set **Status** in each item's README to `not started`, `in progress` or `done`. That line is the
queue pointer. Nothing else tracks it.
