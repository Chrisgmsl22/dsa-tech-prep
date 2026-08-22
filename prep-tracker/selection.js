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
  3: ["heaps", "backtracking", "dp", "greedy", "sorting"],
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

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    TIERS, TIER_SHARE, WINDOW_SIZE,
    largestRemainder, tierOf, isUrgent, comparePriority, selectWindow,
  };
}
