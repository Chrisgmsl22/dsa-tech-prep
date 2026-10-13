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
 *   box       - Leitner box, 1..6
 *   daysUntil - days until due; NEGATIVE means overdue by that many days
 * ========================================================================== */

// Leitner intervals (days) keyed by box. grade.py keeps a copy; change both.
const INTERVAL = { 1: 1, 2: 3, 3: 7, 4: 21, 5: 45, 6: 120 };

/* `grade` is the button: 1 Failed, 2 Slow, 3 Clean, 4 Fast. Only Fast climbs
 * past box 4, one box at a time. A quick rep is a plan in words, not code, so
 * it may keep box 6 but never earn it. grade.py's next_box() is the twin. */
function nextBox(current, grade, kind) {
  const cur = current || 0;
  let box = grade;
  if (grade === 4) box = cur < 4 ? 4 : Math.min(cur + 1, 6);
  if (kind === "quick" && box === 6 && cur !== 6) box = 5;
  return box;
}

/* Box 0, not attempts 0: the triage set sits at box 2 with 0 attempts, and
 * those problems are solved already. Counting them as new would fill the
 * weekly quota with reps. grade.py writes the third kind, "quick". */
function gradeKind(entry) {
  return (entry.box || 0) === 0 ? "new" : "full";
}

/* An app grade. `dueFor(box)` returns the due date, so this file stays free
 * of Date. Only a grade from box 0 dates `started`; grade.py never does. */
function applyGrade(base, grade, today, dueFor) {
  const kind = gradeKind(base);
  const box = nextBox(base.box, grade, kind);
  const graded = {
    ...base, box, due: dueFor(box), last: today, attempts: (base.attempts || 0) + 1, kind,
  };
  if (kind === "new" && !base.started) graded.started = today;
  return graded;
}

/* Week tallies for the stat strip. Dates are ISO strings, so a plain string
 * compare is a date compare. A problem started this week counts once, as new,
 * even if it was also re-graded; everything else graded this week is a rep. */
function weeklyCounts(entries, weekStart, weekEnd) {
  const inWeek = (iso) => !!iso && iso >= weekStart && iso <= weekEnd;
  let newCount = 0, reps = 0;
  for (const e of entries) {
    if (!e || typeof e !== "object") continue;
    if (inWeek(e.started)) newCount++;
    else if (inWeek(e.last)) reps++;
  }
  return { newCount, reps };
}

// Interview-frequency tiers. Tier 1 is what phone screens actually ask;
// tier 2 is very common (tree traversal and binary search are not optional);
// tier 3 are differentiators you can be thin on and still pass most loops.
const TIERS = {
  1: ["arrays_and_strings", "hashmaps_and_sets", "two_pointers", "sliding_window", "stacks"],
  2: ["trees", "binary_search", "linked_lists", "graphs"],
  3: ["heaps", "backtracking", "dp", "greedy", "sorting"],
};

const TIER_SHARE = { 1: 0.5, 2: 0.35, 3: 0.15 };
/* Three, not five. A rep costs ~10-15 min and a new problem up to 60, so a
 * 5-rep day leaves no room to grow the list. Three fits in ~35 minutes, which
 * means it gets finished -- and a queue you can empty is what gives you
 * permission to open something new. Chosen 2026-08-24 with the daily plan
 * "3 reps + 1 new problem when there is capacity". */
const WINDOW_SIZE = 3;

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

/* The roadmap topic new problems alternate with. PRACTICE.md says "grids,
 * then graphs"; grids problems live in the graphs category here. */
const ROADMAP_CATEGORY = "graphs";
const LAST_CATEGORY = "dp";

/* PRACTICE.md "Order of new problems". `catalog` is [{ key, cat, started }] in
 * catalog order. Parity of the started total alternates the two tracks with
 * no stored state: even → roadmap, odd → thinnest tier-1 category. */
function pickNewProblem(catalog) {
  const unstarted = catalog.filter((p) => !p.started);
  if (!unstarted.length) return null;

  const total = {}, started = {}, order = [];
  let startedTotal = 0;
  for (const p of catalog) {
    if (!(p.cat in total)) { total[p.cat] = 0; started[p.cat] = 0; order.push(p.cat); }
    total[p.cat]++;
    if (p.started) { started[p.cat]++; startedTotal++; }
  }
  // Ratio, not raw count: stacks at 4/5 is nearly done, hashmaps at 4/12 is not.
  const coverage = (c) => started[c] / total[c];
  const firstIn = (c) => unstarted.find((p) => p.cat === c) || null;
  const byTierThenCoverage = (a, b) =>
    tierOf(a) - tierOf(b) || coverage(a) - coverage(b) || order.indexOf(a) - order.indexOf(b);

  const untouched = unstarted.find((p) => p.cat !== LAST_CATEGORY && started[p.cat] === 0);
  if (untouched) return untouched;

  const thinnestTier1 = order
    .filter((c) => tierOf(c) === 1)
    .sort(byTierThenCoverage)[0];
  const chosen = startedTotal % 2 === 0 ? ROADMAP_CATEGORY : thinnestTier1;
  const pick = chosen && chosen !== LAST_CATEGORY ? firstIn(chosen) : null;
  if (pick) return pick;

  const fallback = order
    .filter((c) => c !== LAST_CATEGORY && firstIn(c))
    .sort(byTierThenCoverage)[0];
  return fallback ? firstIn(fallback) : firstIn(LAST_CATEGORY);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    TIERS, TIER_SHARE, WINDOW_SIZE, INTERVAL, ROADMAP_CATEGORY, LAST_CATEGORY,
    largestRemainder, tierOf, isUrgent, comparePriority, selectWindow,
    nextBox, gradeKind, applyGrade, weeklyCounts, pickNewProblem,
  };
}
