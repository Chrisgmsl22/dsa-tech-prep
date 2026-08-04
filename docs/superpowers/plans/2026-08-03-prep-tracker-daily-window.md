# Prep Tracker Daily Window Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cap the Prep Tracker's Due list at a 5-wide rolling window filled from three interview-frequency tiers, so a 55-problem backlog presents as a manageable daily worklist without rewriting any due dates.

**Architecture:** All selection logic moves into a new pure module `prep-tracker/selection.js` — no DOM, no dates, no global state, operating only on plain `{key, cat, box, daysUntil}` candidate objects. `app.js` keeps all DOM and persistence concerns and calls into it. This boundary exists so the quota math is unit-testable under `node --test`; `app.js` itself cannot be imported by Node because it touches `document` at module scope (`app.js:309`).

**Tech Stack:** Vanilla ES2020 browser JS (classic `<script>` tags, no bundler, no framework). Tests use Node's built-in `node:test` and `node:assert` — no `package.json`, no dependencies, no install step. Node v24.16.0 confirmed present.

## Global Constraints

- **Zero new persisted state.** No new keys in `progress.json`. The graded-today counter derives from the existing `last` field, already written at `app.js:568`.
- **The window never writes.** It is a display filter. `git diff prep-tracker/progress.json` must be clean after browsing without grading.
- **No changes to `INTERVAL` (`app.js:177`), box semantics, or the scheduling math in `gradeProblem()` (`app.js:562`).**
- **No new files may be added to `prep-tracker/` beyond `selection.js` and `selection.test.js`.** No `package.json` — adding one would switch `.js` to ESM under some tooling and break the CommonJS `require` in the test.
- **`selection.js` must load in both browser and Node.** Browser: classic script, top-level `const` bindings are visible to `app.js` loaded afterward. Node: `module.exports` behind a `typeof module !== "undefined"` guard.
- **No identifier declared in `selection.js` may also be declared in `app.js`** — two classic scripts sharing the global lexical scope will throw `SyntaxError: Identifier 'X' has already been declared`.
- **Window size default is 5**, as the module constant `WINDOW_SIZE`.
- **Tier shares are `{1: 0.50, 2: 0.35, 3: 0.15}`**, allocated by largest-remainder with ties broken by ascending tier number.
- **Urgency rule:** a candidate is urgent if `box === 1` **or** `daysUntil <= -30`.

**Reference spec:** `docs/superpowers/specs/2026-08-03-prep-tracker-daily-window-design.md`

## File Structure

| File | Responsibility |
|---|---|
| `prep-tracker/selection.js` | **Create.** Pure selection logic: tier tables, `tierOf`, `largestRemainder`, `isUrgent`, `comparePriority`, `selectWindow`. No DOM, no `Date`, no globals. |
| `prep-tracker/selection.test.js` | **Create.** `node:test` unit tests for the above. |
| `prep-tracker/index.html:53` | **Modify.** Add `<script src="selection.js"></script>` before `app.js`. |
| `prep-tracker/app.js` | **Modify.** Derive `CORE` from `TIERS[1]`; build candidates and call `selectWindow` in `renderList()`; add the window note and `SHOW_ALL` toggle; retune four grade `sub` strings. |
| `prep-tracker/styles.css` | **Modify.** One `.window-note` rule. |
| `CLAUDE.md` | **Modify.** Document the time-box protocol. |

---

### Task 1: Pure module scaffold and quota allocation

**Files:**
- Create: `prep-tracker/selection.js`
- Create: `prep-tracker/selection.test.js`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `TIERS: {1: string[], 2: string[], 3: string[]}`
  - `TIER_SHARE: {1: 0.50, 2: 0.35, 3: 0.15}`
  - `WINDOW_SIZE: 5`
  - `largestRemainder(shares: {[tier: string]: number}, total: number) -> {[tier: string]: number}` — returns one integer per key of `shares`, summing exactly to `total`.

- [ ] **Step 1: Write the failing test**

Create `prep-tracker/selection.test.js`:

```js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const S = require("./selection.js");

test("tier tables cover all 12 categories exactly once", () => {
  const all = [...S.TIERS[1], ...S.TIERS[2], ...S.TIERS[3]];
  assert.strictEqual(all.length, 12);
  assert.strictEqual(new Set(all).size, 12);
});

test("tier shares sum to 1", () => {
  const sum = S.TIER_SHARE[1] + S.TIER_SHARE[2] + S.TIER_SHARE[3];
  assert.ok(Math.abs(sum - 1) < 1e-9);
});

test("largestRemainder allocates 5 slots as 2/2/1", () => {
  assert.deepStrictEqual(S.largestRemainder(S.TIER_SHARE, 5), { 1: 2, 2: 2, 3: 1 });
});

test("largestRemainder allocates 3 slots as 2/1/0", () => {
  assert.deepStrictEqual(S.largestRemainder(S.TIER_SHARE, 3), { 1: 2, 2: 1, 3: 0 });
});

test("largestRemainder handles zero slots", () => {
  assert.deepStrictEqual(S.largestRemainder(S.TIER_SHARE, 0), { 1: 0, 2: 0, 3: 0 });
});

test("largestRemainder quotas always sum to the total", () => {
  for (let n = 0; n <= 40; n++) {
    const q = S.largestRemainder(S.TIER_SHARE, n);
    assert.strictEqual(q[1] + q[2] + q[3], n, `failed at n=${n}`);
  }
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test prep-tracker/selection.test.js`
Expected: FAIL — `Cannot find module './selection.js'`

- [ ] **Step 3: Write minimal implementation**

Create `prep-tracker/selection.js`:

```js
"use strict";
/* ============================================================================
 * Prep Tracker — daily window selection (pure logic, no DOM, no dates)
 * ---------------------------------------------------------------------------
 * Loaded as a classic <script> before app.js in the browser, and require()d
 * by selection.test.js under `node --test`. Keep this file free of DOM access,
 * Date construction, and mutable module state so it stays trivially testable.
 *
 * A "candidate" is a plain object: { key, cat, box, daysUntil }
 *   key       - stable id string, opaque here
 *   cat       - category slug, must be a key of some TIERS entry
 *   box       - Leitner box, 1..4
 *   daysUntil - days until due; NEGATIVE means overdue by that many days
 * ========================================================================== */

// Interview-frequency tiers. Tier 1 is what phone screens actually ask;
// tier 2 is very common (tree traversal and binary search are not optional);
// tier 3 are differentiators you can be thin on and still pass most loops.
const TIERS = {
  1: ["arrays_and_strings", "hashmaps_and_sets", "two_pointers", "sliding_window", "stacks"],
  2: ["trees", "binary_search", "linked_lists", "graphs"],
  3: ["heaps", "backtracking", "dp"],
};

const TIER_SHARE = { 1: 0.5, 2: 0.35, 3: 0.15 };
const WINDOW_SIZE = 5;

/* Distribute `total` whole slots across `shares` by the largest-remainder
 * method, so the quotas always sum to exactly `total`. Ties in the remainder
 * are broken by ascending tier number. */
function largestRemainder(shares, total) {
  const tiers = Object.keys(shares).map(Number).sort((a, b) => a - b);
  const quotas = {};
  let assigned = 0;

  const remainders = tiers.map((t) => {
    const raw = shares[t] * total;
    quotas[t] = Math.floor(raw);
    assigned += quotas[t];
    return { tier: t, rem: raw - Math.floor(raw) };
  });

  remainders.sort((a, b) => b.rem - a.rem || a.tier - b.tier);
  for (let i = 0; i < total - assigned; i++) quotas[remainders[i].tier] += 1;
  return quotas;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { TIERS, TIER_SHARE, WINDOW_SIZE, largestRemainder };
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test prep-tracker/selection.test.js`
Expected: PASS — 6 tests passing.

- [ ] **Step 5: Commit**

```bash
git add prep-tracker/selection.js prep-tracker/selection.test.js
git commit -m "feat(tracker): add pure selection module with tier quota allocation"
```

---

### Task 2: Tier lookup, urgency, and priority ordering

**Files:**
- Modify: `prep-tracker/selection.js`
- Modify: `prep-tracker/selection.test.js`

**Interfaces:**
- Consumes: `TIERS` from Task 1.
- Produces:
  - `tierOf(cat: string) -> 1|2|3` — unknown categories fall back to `3`.
  - `isUrgent(candidate) -> boolean` — `box === 1 || daysUntil <= -30`.
  - `comparePriority(a, b) -> number` — an `Array.prototype.sort` comparator: ascending box, then ascending tier, then ascending `daysUntil` (most overdue first).

- [ ] **Step 1: Write the failing test**

Append to `prep-tracker/selection.test.js`:

```js
const c = (cat, box, daysUntil, key = `${cat}#${box}#${daysUntil}`) =>
  ({ key, cat, box, daysUntil });

test("tierOf maps categories to their tier", () => {
  assert.strictEqual(S.tierOf("stacks"), 1);
  assert.strictEqual(S.tierOf("sliding_window"), 1);
  assert.strictEqual(S.tierOf("trees"), 2);
  assert.strictEqual(S.tierOf("graphs"), 2);
  assert.strictEqual(S.tierOf("dp"), 3);
});

test("tierOf falls back to tier 3 for unknown categories", () => {
  assert.strictEqual(S.tierOf("grids"), 3);
});

test("isUrgent flags failed problems regardless of due date", () => {
  assert.strictEqual(S.isUrgent(c("dp", 1, 0)), true);
  assert.strictEqual(S.isUrgent(c("dp", 2, 0)), false);
});

test("isUrgent flags anything more than 30 days overdue", () => {
  assert.strictEqual(S.isUrgent(c("dp", 4, -31)), true);
  assert.strictEqual(S.isUrgent(c("dp", 4, -30)), true);
  assert.strictEqual(S.isUrgent(c("dp", 4, -29)), false);
});

test("comparePriority orders weakest box first", () => {
  const sorted = [c("dp", 3, -1), c("dp", 1, -1), c("dp", 2, -1)].sort(S.comparePriority);
  assert.deepStrictEqual(sorted.map((x) => x.box), [1, 2, 3]);
});

test("comparePriority breaks box ties by tier, then by most overdue", () => {
  const sorted = [
    c("dp", 2, -5, "tier3"),
    c("trees", 2, -5, "tier2"),
    c("stacks", 2, -1, "tier1-recent"),
    c("stacks", 2, -9, "tier1-stale"),
  ].sort(S.comparePriority);
  assert.deepStrictEqual(sorted.map((x) => x.key), [
    "tier1-stale", "tier1-recent", "tier2", "tier3",
  ]);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test prep-tracker/selection.test.js`
Expected: FAIL — `S.tierOf is not a function`

- [ ] **Step 3: Write minimal implementation**

In `prep-tracker/selection.js`, insert after the `largestRemainder` function and before the `module.exports` guard:

```js
// Flattened reverse index, built once: category slug -> tier number.
const TIER_OF_CAT = {};
for (const tier of Object.keys(TIERS)) {
  for (const cat of TIERS[tier]) TIER_OF_CAT[cat] = Number(tier);
}

/* Unknown categories fall back to tier 3 so a newly-added category can never
 * crowd out the interview-critical tiers before someone classifies it. */
function tierOf(cat) {
  return TIER_OF_CAT[cat] || 3;
}

/* Urgent problems bypass tier quotas entirely. A quota cannot express urgency:
 * a tier-3 problem failed 40 days ago matters more than a tier-1 problem
 * solved cleanly last week. Without this, quotas would bury rot forever. */
function isUrgent(candidate) {
  return candidate.box === 1 || candidate.daysUntil <= -30;
}

/* Sort comparator: weakest box, then most interview-critical tier, then most
 * overdue. `daysUntil` is negative when overdue, so ascending puts the
 * longest-overdue problem first. */
function comparePriority(a, b) {
  if (a.box !== b.box) return a.box - b.box;
  const ta = tierOf(a.cat), tb = tierOf(b.cat);
  if (ta !== tb) return ta - tb;
  return a.daysUntil - b.daysUntil;
}
```

Then replace the export line so it reads:

```js
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    TIERS, TIER_SHARE, WINDOW_SIZE,
    largestRemainder, tierOf, isUrgent, comparePriority,
  };
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test prep-tracker/selection.test.js`
Expected: PASS — 12 tests passing.

- [ ] **Step 5: Commit**

```bash
git add prep-tracker/selection.js prep-tracker/selection.test.js
git commit -m "feat(tracker): add tier lookup, urgency guard, and priority comparator"
```

---

### Task 3: The window selection algorithm

**Files:**
- Modify: `prep-tracker/selection.js`
- Modify: `prep-tracker/selection.test.js`

**Interfaces:**
- Consumes: `TIER_SHARE`, `largestRemainder`, `tierOf`, `isUrgent`, `comparePriority` from Tasks 1-2.
- Produces: `selectWindow(candidates: Candidate[], windowSize: number) -> Candidate[]` — returns at most `windowSize` of the input objects (by identity, never copies), in `comparePriority` display order.

- [ ] **Step 1: Write the failing test**

Append to `prep-tracker/selection.test.js`:

```js
// 5 per tier, all box 2, all mildly overdue — no urgency, plenty of supply.
function evenPool() {
  const out = [];
  for (const [cat, n] of [["stacks", 5], ["trees", 5], ["dp", 5]]) {
    for (let i = 0; i < n; i++) out.push(c(cat, 2, -1 - i, `${cat}-${i}`));
  }
  return out;
}

test("selectWindow returns exactly windowSize when supply is plentiful", () => {
  assert.strictEqual(S.selectWindow(evenPool(), 5).length, 5);
});

test("selectWindow fills a 5-wide window as 2 tier-1, 2 tier-2, 1 tier-3", () => {
  const counts = { 1: 0, 2: 0, 3: 0 };
  for (const x of S.selectWindow(evenPool(), 5)) counts[S.tierOf(x.cat)]++;
  assert.deepStrictEqual(counts, { 1: 2, 2: 2, 3: 1 });
});

test("selectWindow returns results in priority display order", () => {
  const out = S.selectWindow(evenPool(), 5);
  const resorted = out.slice().sort(S.comparePriority);
  assert.deepStrictEqual(out.map((x) => x.key), resorted.map((x) => x.key));
});

test("selectWindow lets urgent problems bypass tier quotas", () => {
  const pool = evenPool();
  pool.push(c("dp", 1, 0, "failed-dp"));
  pool.push(c("dp", 4, -40, "ancient-dp"));
  const keys = S.selectWindow(pool, 5).map((x) => x.key);
  assert.ok(keys.includes("failed-dp"), "box-1 problem must appear");
  assert.ok(keys.includes("ancient-dp"), "40d-overdue problem must appear");
});

test("selectWindow fills entirely with urgent problems when there are enough", () => {
  const pool = evenPool();
  for (let i = 0; i < 6; i++) pool.push(c("dp", 1, 0, `failed-${i}`));
  const out = S.selectWindow(pool, 5);
  assert.strictEqual(out.length, 5);
  assert.ok(out.every((x) => S.isUrgent(x)));
});

test("selectWindow backfills when a tier has fewer problems than its quota", () => {
  // Tier 2 and tier 3 are empty; tier 1 must cover all 5 slots.
  const pool = [];
  for (let i = 0; i < 8; i++) pool.push(c("stacks", 2, -1 - i, `s-${i}`));
  const out = S.selectWindow(pool, 5);
  assert.strictEqual(out.length, 5);
  assert.strictEqual(new Set(out.map((x) => x.key)).size, 5, "no duplicates");
});

test("selectWindow returns everything when supply is under the window size", () => {
  const pool = [c("stacks", 2, -1, "a"), c("trees", 2, -2, "b")];
  assert.strictEqual(S.selectWindow(pool, 5).length, 2);
});

test("selectWindow handles an empty pool", () => {
  assert.deepStrictEqual(S.selectWindow([], 5), []);
});

test("selectWindow never mutates its input array", () => {
  const pool = evenPool();
  const before = pool.map((x) => x.key);
  S.selectWindow(pool, 5);
  assert.deepStrictEqual(pool.map((x) => x.key), before);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test prep-tracker/selection.test.js`
Expected: FAIL — `S.selectWindow is not a function`

- [ ] **Step 3: Write minimal implementation**

In `prep-tracker/selection.js`, insert after `comparePriority` and before the `module.exports` guard:

```js
/* Pick the problems to show today.
 *
 *   1. Urgent problems (failed, or badly rotted) fill the window first,
 *      ignoring tiers entirely. If they fill it, we are done.
 *   2. Remaining slots are split across tiers by TIER_SHARE.
 *   3. A tier with fewer due problems than its quota gives its slots away —
 *      the backfill pass hands them to whoever is next by priority.
 *
 * Returns the input objects by identity, never copies, so callers can map
 * straight back to their own records. Does not mutate `candidates`. */
function selectWindow(candidates, windowSize) {
  const byPriority = (arr) => arr.slice().sort(comparePriority);

  const urgent = candidates.filter(isUrgent);
  const rest = candidates.filter((x) => !isUrgent(x));

  const picked = byPriority(urgent).slice(0, windowSize);
  const slotsLeft = windowSize - picked.length;
  if (slotsLeft <= 0) return byPriority(picked);

  const quotas = largestRemainder(TIER_SHARE, slotsLeft);
  const taken = new Set();
  for (const tier of [1, 2, 3]) {
    const pool = byPriority(rest.filter((x) => tierOf(x.cat) === tier));
    for (const candidate of pool.slice(0, quotas[tier])) {
      picked.push(candidate);
      taken.add(candidate);
    }
  }

  if (picked.length < windowSize) {
    const leftovers = byPriority(rest.filter((x) => !taken.has(x)));
    picked.push(...leftovers.slice(0, windowSize - picked.length));
  }

  return byPriority(picked);
}
```

Then replace the export line so it reads:

```js
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    TIERS, TIER_SHARE, WINDOW_SIZE,
    largestRemainder, tierOf, isUrgent, comparePriority, selectWindow,
  };
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test prep-tracker/selection.test.js`
Expected: PASS — 21 tests passing.

- [ ] **Step 5: Commit**

```bash
git add prep-tracker/selection.js prep-tracker/selection.test.js
git commit -m "feat(tracker): add tiered window selection with urgency bypass and backfill"
```

---

### Task 4: Wire the window into the Due view

**Files:**
- Modify: `prep-tracker/index.html:53`
- Modify: `prep-tracker/app.js:20-25` (the `CORE` declaration)
- Modify: `prep-tracker/app.js:380-391` (the `VIEW === "due"` branch of `renderList`)

**Interfaces:**
- Consumes: `TIERS`, `WINDOW_SIZE`, `selectWindow`, `comparePriority` — available as globals because `selection.js` is a classic script loaded first.
- Produces: `SHOW_ALL` (module-level `let`, default `false`), read by Task 5.

**Note on `CORE`:** it is referenced at `app.js:271, 272, 326, 327, 351, 385, 397, 405`. Redefining it as `new Set(TIERS[1])` keeps all eight call sites working unchanged and correctly adds `stacks` to the core set. The "core solved" stat will change from `20/34` to `24/39` — this is intended.

- [ ] **Step 1: Load the pure module before app.js**

In `prep-tracker/index.html`, replace line 53:

```html
  <script src="app.js"></script>
```

with:

```html
  <script src="selection.js"></script>
  <script src="app.js"></script>
```

- [ ] **Step 2: Derive CORE from the tier table**

In `prep-tracker/app.js`, replace lines 20-25:

```js
const CORE = new Set([
  "arrays_and_strings",
  "hashmaps_and_sets",
  "two_pointers",
  "sliding_window",
]);
```

with:

```js
/* Tier 1 doubles as the "core" set used for stat counts, chip highlighting,
 * and group ordering. TIERS comes from selection.js, loaded before this file. */
const CORE = new Set(TIERS[1]);
```

- [ ] **Step 3: Add the SHOW_ALL flag**

In `prep-tracker/app.js`, in the `/* ---------- app state ---------- */` block (currently lines 293-297), add one line after `let OPEN_ID = null;`:

```js
let SHOW_ALL = false; // session-only Due-view override; not persisted
```

- [ ] **Step 4: Replace the Due branch of renderList**

In `prep-tracker/app.js`, replace lines 380-391:

```js
  if (VIEW === "due") {
    // Flat list, weakest box first, then core, then most overdue.
    items.sort((a, b) => {
      const pa = prog(a), pb = prog(b);
      if (pa.box !== pb.box) return pa.box - pb.box;
      const ca = CORE.has(a.cat) ? 0 : 1, cb = CORE.has(b.cat) ? 0 : 1;
      if (ca !== cb) return ca - cb;
      return daysUntil(pa.due) - daysUntil(pb.due);
    });
    listEl.innerHTML = items.map(rowHTML).join("");
    return;
  }
```

with:

```js
  if (VIEW === "due") {
    // Project each problem into the plain shape selection.js expects, keeping
    // a back-reference so we can render the original record afterwards.
    const candidates = items.map((p) => {
      const st = prog(p);
      return { key: id(p), cat: p.cat, box: st.box, daysUntil: daysUntil(st.due), problem: p };
    });

    let picked;
    if (SHOW_ALL) {
      picked = candidates.slice().sort(comparePriority);
    } else if (CAT_FILTER === "all") {
      picked = selectWindow(candidates, WINDOW_SIZE);
    } else {
      // Tier quotas are meaningless inside a single category — just cap.
      picked = candidates.slice().sort(comparePriority).slice(0, WINDOW_SIZE);
    }

    listEl.innerHTML =
      windowNoteHTML(picked.length, candidates.length) +
      picked.map((x) => rowHTML(x.problem)).join("");
    return;
  }
```

- [ ] **Step 5: Add a temporary stub so the page loads**

`windowNoteHTML` is written in Task 5. Add this stub immediately above `function renderList()` in `prep-tracker/app.js` so Task 4 is independently verifiable:

```js
function windowNoteHTML(shown, total) {
  return ""; // replaced in Task 5
}
```

- [ ] **Step 6: Verify in the browser**

Run: `python3 prep-tracker/server.py` and open `http://localhost:8000`.

Expected:
- Due tab shows exactly **5** rows (the badge still reads the true count, 55).
- Of those 5: two from Arrays/Hashmaps/Two Pointers/Sliding Window/Stacks, two from Trees/Binary Search/Linked Lists/Graphs, one from Heaps/Backtracking/DP.
- The "core solved" stat reads `24/39`.
- The browser console is clean — in particular no `Identifier 'X' has already been declared`.

- [ ] **Step 7: Verify the window never writes**

Run: `git diff --stat prep-tracker/progress.json`
Expected: empty output. Browsing the Due tab, switching tabs, and clicking category chips must not modify progress.

- [ ] **Step 8: Commit**

```bash
git add prep-tracker/index.html prep-tracker/app.js
git commit -m "feat(tracker): cap the Due view at a tiered 5-wide window"
```

---

### Task 5: Window note and Show-all toggle

**Files:**
- Modify: `prep-tracker/app.js` (replace the `windowNoteHTML` stub from Task 4)
- Modify: `prep-tracker/app.js:535-550` (the `listEl` click handler)
- Modify: `prep-tracker/styles.css` (append one rule)

**Interfaces:**
- Consumes: `SHOW_ALL` from Task 4; `STATE` and `todayISO()` from `app.js`.
- Produces: no new exports. The graded-today count is derived, never stored.

- [ ] **Step 1: Replace the stub with the real header**

In `prep-tracker/app.js`, replace the Task 4 stub:

```js
function windowNoteHTML(shown, total) {
  return ""; // replaced in Task 5
}
```

with:

```js
/* Header strip above the Due list. Shows how much of the real backlog is
 * hidden, plus today's grading count — derived from the `last` field that
 * gradeProblem() already writes, so this adds no persisted state. */
function windowNoteHTML(shown, total) {
  const gradedToday = Object.values(STATE).filter((s) => s.last === todayISO()).length;
  const hidden = total - shown;
  let toggle = "";
  if (SHOW_ALL) {
    toggle = `<button class="ghost" id="windowToggle">Show window</button>`;
  } else if (hidden > 0) {
    toggle = `<button class="ghost" id="windowToggle">Show all ${total}</button>`;
  }
  return (
    `<div class="window-note">` +
    `<span>Showing <strong>${shown}</strong> of ${total} due · ` +
    `<strong>${gradedToday}</strong> graded today</span>${toggle}</div>`
  );
}
```

- [ ] **Step 2: Handle the toggle click**

In `prep-tracker/app.js`, in the `listEl` click handler at line 535, insert a branch as the first statement inside the callback — before the `.grade` lookup:

```js
listEl.addEventListener("click", (e) => {
  // window size toggle?
  if (e.target.id === "windowToggle") {
    SHOW_ALL = !SHOW_ALL;
    render();
    return;
  }
  // grade button?
  const g = e.target.closest(".grade");
```

- [ ] **Step 3: Style the header strip**

Append to `prep-tracker/styles.css`:

```css
.window-note {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}
.window-note strong { color: var(--text); }
```

- [ ] **Step 4: Verify in the browser**

Run: `python3 prep-tracker/server.py` and open `http://localhost:8000`.

Expected:
- Header reads `Showing 5 of 55 due · 0 graded today` with a `Show all 55` button.
- Clicking `Show all 55` reveals all 55 rows; the button becomes `Show window`; clicking it returns to 5.
- Reloading the page restores the 5-row window (`SHOW_ALL` is session-only).
- Grading the top row: it disappears, a new row slides in to keep 5 visible, the total drops to 54, and the counter reads `1 graded today`.
- With a category chip active, the header still appears and the list is capped at 5.

- [ ] **Step 5: Verify the counter survives a reload**

Grade one problem, then reload the page.
Expected: the counter still reads `1 graded today` — it is derived from the persisted `last` field, not from in-memory session state.

- [ ] **Step 6: Commit**

```bash
git add prep-tracker/app.js prep-tracker/styles.css
git commit -m "feat(tracker): add window note with graded-today count and show-all toggle"
```

---

### Task 6: Clock-anchored grade labels and the time-box protocol

**Files:**
- Modify: `prep-tracker/app.js:179-182` (the `GRADES` array)
- Modify: `CLAUDE.md` (append to the "Prep Tracker & Practice Workflow" section)

**Interfaces:**
- Consumes: nothing.
- Produces: nothing. Box numbers, `cls` values, and `INTERVAL` are all unchanged — only the `sub` display strings differ.

- [ ] **Step 1: Retune the grade sub-labels**

In `prep-tracker/app.js`, replace lines 178-183:

```js
const GRADES = [
  { box: 1, cls: "g1", label: "Failed",  sub: "needed the solution · +1d" },
  { box: 2, cls: "g2", label: "Slow",    sub: "solved with hints · +3d" },
  { box: 3, cls: "g3", label: "Clean",   sub: "solved, some hesitation · +7d" },
  { box: 4, cls: "g4", label: "Fast",    sub: "instant & confident · +21d" },
];
```

with:

```js
// Sub-labels are anchored to the time-box protocol in CLAUDE.md so that
// self-grading is a measurement rather than a mood.
const GRADES = [
  { box: 1, cls: "g1", label: "Failed",  sub: "hit the cap / read the solution · +1d" },
  { box: 2, cls: "g2", label: "Slow",    sub: "needed a hint, or >40 min · +3d" },
  { box: 3, cls: "g3", label: "Clean",   sub: "solved unaided, under ~30 min · +7d" },
  { box: 4, cls: "g4", label: "Fast",    sub: "under ~15 min, no stumbles · +21d" },
];
```

- [ ] **Step 2: Document the time-box protocol**

In `CLAUDE.md`, append the following at the end of the "Prep Tracker & Practice Workflow" section, immediately before the `### My Role Here Is Mentor — Reinforced` heading:

```markdown
**Time-box protocol (the grade buttons are anchored to these numbers):**

Two kinds of stuck, and only one is worth paying for. Being stuck on the
*approach* (pattern unknown) has near-zero return from grinding — an unknown
pattern cannot be derived from first principles. Being stuck on the
*implementation* (approach right, code wrong) is the productive struggle.

*New problem — 60 minute hard cap:*

-   **0–20 min** — blind, no hints. Brainstorm in a `NOTES:` comment block first.
-   **@20 min, no approach** → take the *pattern name only* — not code, not
    pseudocode. Then reset the clock.
-   **20–50 min** — implement. Bugs here are the good struggle; stay with them.
-   **@50–60 min, still broken** → read the solution, understand it, **close it**,
    re-implement from memory. Grade **Failed** → box 1 → it returns tomorrow.
-   **Never a second day on a first attempt.**

*Review rep — 15 minutes:* can't get it in 15? The memory is genuinely gone.
Grade **Failed**, skim the existing file in `patterns/`, move on. Reviews are
never ground out — that is what the 1-day box-1 interval is for.

**The principle:** tomorrow's second attempt is worth more than today's third
hour. Retrieval after forgetting builds durable memory; re-reading your own
stuck code builds almost nothing.

**As mentor, hold this line.** When the student is past ~20 minutes with no
approach, give the pattern name — that is the correct hint at that moment, not
a failure of the Progressive Hint System. When they are past ~50 minutes on a
first attempt, tell them to read the solution and grade Failed rather than
letting a problem consume multiple days.
```

- [ ] **Step 3: Verify the labels render**

Run: `python3 prep-tracker/server.py` and open `http://localhost:8000`.
Click any row to expand it.
Expected: the four grade buttons read `Failed / hit the cap / read the solution · +1d`, `Slow / needed a hint, or >40 min · +3d`, `Clean / solved unaided, under ~30 min · +7d`, `Fast / under ~15 min, no stumbles · +21d`. Button colors and layout are unchanged.

- [ ] **Step 4: Run the full test suite**

Run: `node --test prep-tracker/selection.test.js`
Expected: PASS — 21 tests passing, 0 failing.

- [ ] **Step 5: Commit**

```bash
git add prep-tracker/app.js CLAUDE.md
git commit -m "feat(tracker): anchor grade labels to the time-box protocol"
```

---

## Final Verification

Run through the spec's test list end to end with the real `progress.json`:

- [ ] **Cap** — Due tab shows exactly 5 rows; header reads `Showing 5 of 55 due`.
- [ ] **Tier mix** — with no urgent problems present, the 5 rows are 2 tier-1, 2 tier-2, 1 tier-3.
- [ ] **Refill** — grading the top row leaves 5 rows, the graded problem is gone, and the counter increments.
- [ ] **Urgency bypass** — grade something Failed, reload: it appears in the window regardless of tier.
- [ ] **Backfill** — apply a category filter with fewer than 5 due: no crash, no duplicate rows.
- [ ] **Show all** — the toggle reveals all 55; reload restores the cap.
- [ ] **Data integrity** — `git diff prep-tracker/progress.json` is clean after browsing without grading.
- [ ] **Tests** — `node --test prep-tracker/selection.test.js` passes.
- [ ] **Console** — no errors or warnings in the browser console.
