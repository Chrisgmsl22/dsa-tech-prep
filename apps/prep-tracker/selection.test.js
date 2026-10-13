"use strict";
const test = require("node:test");
const assert = require("node:assert");
const S = require("./selection.js");

// Bump CATEGORY_COUNT when you add a category to CAT_META in app.js. The point
// of the check is that every category sits in exactly one tier — a category
// missing from TIERS silently falls back to tier 3 and skews the daily window.
const CATEGORY_COUNT = 14;

test("tier tables cover every category exactly once", () => {
  const all = [...S.TIERS[1], ...S.TIERS[2], ...S.TIERS[3]];
  assert.strictEqual(all.length, CATEGORY_COUNT);
  assert.strictEqual(new Set(all).size, CATEGORY_COUNT);
});

/* Policy test, not a correctness test. WINDOW_SIZE dropped from 5 to 3 on
 * 2026-08-24, which changes the daily mix from 2/2/1 to 2/1/0 -- tier 3 (heaps,
 * backtracking, dp, greedy, sorting) now only surfaces via the urgency bypass
 * or the backfill pass. That is consistent with tier 3 being "differentiators
 * you can be thin on", but it should fail loudly if the window moves again. */
test("a 3-wide window splits 2 tier-1, 1 tier-2, 0 tier-3", () => {
  assert.strictEqual(S.WINDOW_SIZE, 3);
  assert.deepStrictEqual(S.largestRemainder(S.TIER_SHARE, 3), { 1: 2, 2: 1, 3: 0 });
});

test("a thin tier-1 supply backfills rather than shrinking the window", () => {
  const pool = [
    { key: "a", cat: "two_pointers", box: 3, daysUntil: 0 },   // tier 1, only one
    { key: "b", cat: "trees", box: 3, daysUntil: -1 },
    { key: "c", cat: "trees", box: 3, daysUntil: -2 },
    { key: "d", cat: "dp", box: 3, daysUntil: -3 },
  ];
  const picked = S.selectWindow(pool, 3);
  assert.strictEqual(picked.length, 3, "the freed tier-1 slot must be reused");
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

// ---- boxes 5 and 6 ----

const FAILED = 1, SLOW = 2, CLEAN = 3, FAST = 4;

test("INTERVAL covers boxes 1 to 6", () => {
  assert.deepStrictEqual(S.INTERVAL, { 1: 1, 2: 3, 3: 7, 4: 21, 5: 45, 6: 120 });
});

test("nextBox: Fast climbs one box from 4, jumps to 4 from below, holds at 6", () => {
  const expected = { 0: 4, 1: 4, 2: 4, 3: 4, 4: 5, 5: 6, 6: 6 };
  for (let cur = 0; cur <= 6; cur++) {
    assert.strictEqual(S.nextBox(cur, FAST, "full"), expected[cur], `box ${cur}`);
  }
});

test("nextBox: Failed, Slow and Clean set box 1, 2, 3 from every box", () => {
  for (let cur = 0; cur <= 6; cur++) {
    assert.strictEqual(S.nextBox(cur, FAILED, "full"), 1, `Failed from ${cur}`);
    assert.strictEqual(S.nextBox(cur, SLOW, "full"), 2, `Slow from ${cur}`);
    assert.strictEqual(S.nextBox(cur, CLEAN, "quick"), 3, `Clean from ${cur}`);
  }
});

test("nextBox: a missing current box counts as box 0", () => {
  assert.strictEqual(S.nextBox(undefined, FAST, "new"), 4);
});

test("nextBox: a quick rep cannot promote to box 6", () => {
  assert.strictEqual(S.nextBox(5, FAST, "quick"), 5);
  assert.strictEqual(S.nextBox(4, FAST, "quick"), 5);
  assert.strictEqual(S.nextBox(6, FAST, "quick"), 6, "box 6 stays 6");
  assert.strictEqual(S.nextBox(6, FAILED, "quick"), 1);
});

// ---- weekly line ----

test("weeklyCounts: started this week is new, other grades this week are reps", () => {
  const entries = [
    { started: "2026-10-12", last: "2026-10-13" },  // new, re-graded: counts once, as new
    { started: "2026-10-18", last: "2026-10-18" },  // Sunday: still this week
    { started: "2026-10-05", last: "2026-10-14" },  // started last week: a rep
    { last: "2026-10-12" },                         // legacy entry, no started: a rep
    { last: "2026-10-11" },                         // last Sunday: outside
    { started: "2026-10-19", last: "2026-10-19" },  // next Monday: outside
    { status: "done", trigger: "" },                // sprint entry: ignored
    null,
  ];
  assert.deepStrictEqual(
    S.weeklyCounts(entries, "2026-10-12", "2026-10-18"),
    { newCount: 2, reps: 2 }
  );
});

// ---- new-problem order ----

/* Builds a catalog from { cat: [startedCount, totalCount] } in the given
 * order. Keys are `${cat}#${n}` and the started ones come first. */
function catalogOf(spec) {
  const out = [];
  for (const [cat, [done, total]] of Object.entries(spec)) {
    for (let n = 1; n <= total; n++) out.push({ key: `${cat}#${n}`, cat, started: n <= done });
  }
  return out;
}

test("pickNewProblem: a category with nothing started comes first, in catalog order", () => {
  const catalog = catalogOf({
    arrays_and_strings: [2, 5], graphs: [1, 5], greedy: [0, 4], sorting: [0, 1], dp: [1, 5],
  });
  assert.strictEqual(S.pickNewProblem(catalog).key, "greedy#1");
});

test("pickNewProblem: an even started total picks the roadmap category", () => {
  const catalog = catalogOf({
    arrays_and_strings: [1, 5], hashmaps_and_sets: [1, 4], graphs: [1, 5], dp: [1, 5],
  });
  assert.strictEqual(S.ROADMAP_CATEGORY, "graphs");
  assert.strictEqual(S.pickNewProblem(catalog).key, "graphs#2");
});

test("pickNewProblem: an odd started total picks the thinnest tier-1 category", () => {
  const catalog = catalogOf({
    arrays_and_strings: [2, 5], hashmaps_and_sets: [1, 4], graphs: [1, 5], dp: [1, 5],
  });
  // 5 started → odd. arrays 2/5 = 0.4, hashmaps 1/4 = 0.25 → hashmaps.
  assert.strictEqual(S.pickNewProblem(catalog).key, "hashmaps_and_sets#2");
});

test("pickNewProblem: alternates as the started total changes", () => {
  const catalog = catalogOf({
    arrays_and_strings: [1, 5], hashmaps_and_sets: [1, 4], graphs: [1, 5], dp: [1, 5],
  });
  const first = S.pickNewProblem(catalog);
  assert.strictEqual(first.cat, "graphs");
  first.started = true;
  assert.strictEqual(S.pickNewProblem(catalog).cat, "arrays_and_strings",
    "odd now: arrays at 0.2 is thinner than hashmaps at 0.25");
});

test("pickNewProblem: an exhausted pick falls back by tier, then coverage", () => {
  const catalog = catalogOf({
    stacks: [2, 2], trees: [1, 4], linked_lists: [1, 2], heaps: [1, 6], graphs: [3, 3], dp: [1, 5],
  });
  // 9 started → odd → tier-1 pick is stacks, which is full. Tier 2 next:
  // trees 0.25 beats linked_lists 0.5.
  assert.strictEqual(S.pickNewProblem(catalog).key, "trees#2");
  // Even → graphs, also full. Same fallback.
  catalog.find((p) => p.key === "heaps#2").started = true;
  assert.strictEqual(S.pickNewProblem(catalog).key, "trees#2");
});

test("pickNewProblem: dp comes last, even when it is the thinnest", () => {
  const catalog = catalogOf({ stacks: [1, 2], graphs: [2, 2], dp: [1, 14] });
  assert.strictEqual(S.pickNewProblem(catalog).key, "stacks#2");
  catalog.find((p) => p.key === "stacks#2").started = true;
  assert.strictEqual(S.pickNewProblem(catalog).key, "dp#2");
});

test("pickNewProblem: an untouched dp does not jump the queue", () => {
  const catalog = catalogOf({ graphs: [1, 3], dp: [0, 3] });
  assert.strictEqual(S.pickNewProblem(catalog).cat, "graphs");
});

test("pickNewProblem: returns null when everything is started", () => {
  assert.strictEqual(S.pickNewProblem(catalogOf({ stacks: [2, 2], dp: [1, 1] })), null);
});

// ---- grade kind and started (plan rev 3: "new" means box 0) ----

const DAY = "2026-10-12";
const dueFor = (box) => `+${box}`;
const TRIAGE = { box: 2, due: "2026-09-01", last: null, attempts: 0, trigger: "" };
const LEGACY = { box: 4, due: "2026-10-01", last: "2026-09-10", attempts: 2, trigger: "" };
const UNSTARTED = { box: 0, due: null, last: null, attempts: 0, trigger: "" };

test("gradeKind: only box 0 is new; triage and legacy entries are reps", () => {
  assert.strictEqual(S.gradeKind(UNSTARTED), "new");
  assert.strictEqual(S.gradeKind({}), "new");
  assert.strictEqual(S.gradeKind(TRIAGE), "full");
  assert.strictEqual(S.gradeKind(LEGACY), "full");
});

test("applyGrade: a grade from box 0 is new and dates started", () => {
  const got = S.applyGrade(UNSTARTED, CLEAN, DAY, dueFor);
  assert.deepStrictEqual(
    [got.box, got.kind, got.started, got.attempts, got.last, got.due],
    [3, "new", DAY, 1, DAY, "+3"]
  );
});

test("applyGrade: a triage grade gets no started and is not new this week", () => {
  for (const grade of [FAILED, SLOW, CLEAN, FAST]) {
    const got = S.applyGrade(TRIAGE, grade, DAY, dueFor);
    assert.strictEqual(got.kind, "full");
    assert.ok(!("started" in got), `grade ${grade}`);
    assert.deepStrictEqual(S.weeklyCounts([got], "2026-10-12", "2026-10-18"), { newCount: 0, reps: 1 });
  }
});

test("applyGrade: a legacy grade gets no started, and Fast climbs from its box", () => {
  const got = S.applyGrade(LEGACY, FAST, DAY, dueFor);
  assert.deepStrictEqual([got.box, got.kind, got.attempts, got.due], [5, "full", 3, "+5"]);
  assert.ok(!("started" in got));
});

test("applyGrade: keeps an existing started and every other field", () => {
  const got = S.applyGrade({ ...LEGACY, started: "2026-01-05", note: "x" }, SLOW, DAY, dueFor);
  assert.strictEqual(got.started, "2026-01-05");
  assert.strictEqual(got.note, "x");
});

test("weeklyCounts: a grade.py quick rep (no started) counts as a rep", () => {
  const quick = { ...TRIAGE, box: 3, last: DAY, attempts: 1, kind: "quick" };
  assert.deepStrictEqual(S.weeklyCounts([quick], "2026-10-12", "2026-10-18"), { newCount: 0, reps: 1 });
});
