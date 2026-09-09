# EXAMPLE — Null Object

- **Family:** Behavioral
- **Prerequisite items:** none
- **Status:** done — **this is the worked example. Read it, do not edit it.**

> **Why this pattern is the example.** Null Object is not 1 of the 16 queue items, and it will
> never be added. So a filled-in copy shows you the **shape of a finished item** without a
> spoiler for any night you have ahead.
>
> **What it does reveal:** an abstract base class with 1 abstract method, and 2 classes that
> implement it. Item 01 Strategy uses that same skeleton. What Strategy adds — several real
> algorithms, and the question of who picks one — is still yours to find.
>
> Length check: 43 lines of code, 25 lines of test, 15 minutes of work.

## The problem it solves

A caller holds a collaborator that is sometimes absent. Do you write `if printer is not None:`
at all 6 call sites, or can the absent case be an object like any other?

## Why it sits outside the queue

It is 1 idea, it needs no prerequisite, and it is the cheapest possible demonstration of "code
to an interface". Perfect as a sample, too small to earn a night.

---

## 1. In my own words

A null object implements the interface in full and does nothing. The caller keeps 1 code path,
because the absent case is now a normal object rather than a missing one.

## 2. The parts

- `Printer` — the interface. It states the only thing a till may ask of a printer.
- `ThermalPrinter` — the real behavior. It appends to a log, so a test can read the result.
- `NoPrinter` — the null object. Same interface, empty body, returns `None`.
- `Till` — the caller. It holds a `Printer` and never asks which kind it holds.

## 3. One good case

A coffee shop runs 2 counters. The second counter has no receipt printer. `NoPrinter` keeps the
till code identical at both counters, and a new counter needs no branch.

## 4. One wrong case

When silence hides a real fault. If a card terminal is absent, a `NoTerminal` that quietly
approves every payment is a bug in the shape of a pattern. Use a null object for behavior that
is **optional**, never for behavior that is **required**. A missing required collaborator must
raise.

## 5. The alternative I reject

**A default argument of `None`, plus a check in `Till`.** It works, and for 1 call site it is
less code. I reject it at 3 or more call sites, because each site then repeats the same check and
1 forgotten check is an `AttributeError` in production.

I also reject `unittest.mock.Mock()` here. A mock is a test tool. This absent printer is a real
production case.

## 6. Where I saw it

`logging.NullHandler` in the Python standard library. A library attaches it so that an
application which configures no logging still gets no error and no output.

## 7. SOLID link

**L, the Liskov substitution principle.** `NoPrinter` is usable everywhere a `Printer` is
expected, and `Till` needs no knowledge of the difference. It also serves **D**, because `Till`
depends on the `Printer` abstraction and receives it through its constructor — dependency
injection, item 00.
