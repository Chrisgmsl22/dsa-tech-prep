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
