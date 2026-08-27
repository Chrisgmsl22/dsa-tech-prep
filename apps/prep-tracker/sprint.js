"use strict";
/* ============================================================================
 * Prep Tracker — interview sprint (data only)
 * ---------------------------------------------------------------------------
 * EMPTY BY DESIGN. The 2026-08 assessment's 39 problems were merged into the
 * PROBLEMS catalog in app.js on 2026-08-21, so they now ride the normal
 * spaced-repetition rotation. See "Merging the sprint back in" in README.md.
 *
 * This file is the shell for the NEXT interview. When a screen arrives with its
 * own problem list, fill in the three constants below and the Sprint tab wakes
 * up. Nothing else needs to change.
 *
 * The tab is a CHECKLIST WITH MEMORY, not a second scheduler. Nothing here ever
 * gets a Leitner box or a due date, and nothing here reaches "Due today".
 *
 * ---------------------------------------------------------------------------
 * HOW TO LOAD THE NEXT SPRINT
 *
 * 1. SPRINT_META — the test's shape. Free text, shown in the header strip.
 *
 * 2. SPRINT_GROUPS — one row per chunk of the list:
 *      { g: 1, dir: "arrays", label: "Arrays (1D) Foundations" }
 *    `g` orders the groups and renders as the day number. `dir` is the folder
 *    under sprint/ where that group's solutions go. Day numbers are LABELS,
 *    not deadlines — nothing computes a date.
 *
 * 3. SPRINT — one row per problem:
 *      { g: 5, slug: "rotate-image", title: "Rotate Image",
 *        pri: "essential",                 // essential | stretch | optional
 *        maps: "arrays_and_strings#11" }   // optional: existing catalog twin
 *
 *    `slug` must be the LeetCode slug; the URL is derived from it below.
 *    `pri` is the triage — be honest, a list that does not fit is normal:
 *        essential  do it — core pattern, squarely in scope
 *        stretch    do it if the day runs short
 *        optional   reference only
 *    `maps` points at a PROBLEMS entry ("cat#n") when the catalog already has
 *    the same problem. It drives the ✓ marker and makes the merge mechanical.
 * ========================================================================== */

const SPRINT_META = {
  format: "",   // e.g. "70 minutes · 4 problems · no pausing"
  order: "",    // e.g. "order: 1 → 2 → 4 → 3 (longest last)"
};

const SPRINT_GROUPS = [];

const LC = "https://leetcode.com/problems/";

const SPRINT = [];

// Derive each URL from its slug so the prefix is written once, not per row.
for (const s of SPRINT) s.url = LC + s.slug + "/";

if (typeof module !== "undefined" && module.exports) {
  module.exports = { SPRINT, SPRINT_META, SPRINT_GROUPS };
}
