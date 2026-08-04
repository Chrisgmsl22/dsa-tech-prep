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
