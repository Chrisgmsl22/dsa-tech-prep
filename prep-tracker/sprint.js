"use strict";
/* ============================================================================
 * Prep Tracker — 9-day interview sprint (data only, no DOM, no dates computed)
 * ---------------------------------------------------------------------------
 * Loaded as a classic <script> before app.js, the same way selection.js is.
 *
 * This is a CHECKLIST WITH MEMORY, not a second scheduler. Nothing here gets a
 * Leitner box or a due date, and nothing here can reach the "Due today" list.
 * After the test, the keepers get merged into PROBLEMS in app.js — see the
 * "Merging the sprint back in" section of README.md.
 *
 * `pri` encodes the triage. The plan is 39 problems in 9 days, which does not
 * fit inside a 60-minute-per-problem cap, and several of them sit well above
 * the test's stated scope (1D/2D arrays, hash maps, stacks, matrix traversal,
 * lists, graphs). Skipping an `optional` is the plan working, not a failure.
 *
 *   essential  do it — core pattern, squarely in scope
 *   stretch    do it if the day runs short
 *   optional   reference only (the Hards, and most of the greedy day)
 *
 * `maps` points at a PROBLEMS entry ("cat#n") when the catalog already has the
 * same problem. It drives the ✓ marker and makes the post-test merge mechanical.
 * ========================================================================== */

/* Deliberately undated. "Day 1" is a label for a chunk of the list, not a
 * calendar entry: the list outlives any one interview, and a hard-coded date
 * would be stale a week after it was written. Fall behind a day and nothing
 * turns red — the day number just tells you where you are. */
const SPRINT_META = {
  format: "70 minutes · 4 problems · no pausing",
  order: "order: 1 → 2 → 4 → 3 (longest last)",
};

// group -> folder name under sprint/ and the display label. `g` orders the
// groups and is shown as the day number.
const SPRINT_GROUPS = [
  { g: 1, dir: "arrays",          label: "Arrays (1D) Foundations" },
  { g: 2, dir: "strings",         label: "Strings & String Manipulation" },
  { g: 3, dir: "two_pointers",    label: "Two Pointers" },
  { g: 4, dir: "sliding_window",  label: "Sliding Window" },
  { g: 5, dir: "matrix",          label: "Matrix & Multidimensional Arrays" },
  { g: 6, dir: "hashmaps",        label: "HashMaps & Sets" },
  { g: 7, dir: "greedy",          label: "Greedy Strategies" },
  { g: 8, dir: "divide_conquer",  label: "Divide & Conquer + Recursion" },
  { g: 9, dir: "simulation",      label: "Full Timed Simulation" },
];

const LC = "https://leetcode.com/problems/";

const SPRINT = [
  // ---- Arrays (1D) Foundations ----
  { g:1, slug: "merge-sorted-array",   title: "Merge Sorted Array",   pri: "essential" },
  { g:1, slug: "running-sum-of-1d-array", title: "Running Sum of 1d Array", pri: "essential" },
  { g:1, slug: "rotate-array",         title: "Rotate Array",         pri: "essential" },
  { g:1, slug: "reverse-string-ii",    title: "Reverse String II",    pri: "essential" },

  // ---- Strings & String Manipulation ----
  // Three Hards that the test's own topic list does not mention. Read them,
  // don't grind them. Find Median is the one worth real time (heap + two-heap
  // invariant shows up far more often than semi-palindromes).
  { g:2, slug: "find-median-from-data-stream", title: "Find Median from Data Stream", pri: "stretch" },
  { g:2, slug: "count-anagrams",       title: "Count Anagrams",       pri: "optional" },
  { g:2, slug: "minimum-changes-to-make-k-semi-palindromes", title: "Minimum Changes to Make K Semi-palindromes", pri: "optional" },
  { g:2, slug: "longest-common-prefix-of-k-strings-after-removal", title: "Longest Common Prefix of K Strings After Removal", pri: "optional" },

  // ---- Two Pointers ----
  { g:3, slug: "two-sum-ii-input-array-is-sorted", title: "Two Sum II - Input Array Is Sorted", pri: "essential", maps: "two_pointers#3" },
  { g:3, slug: "remove-duplicates-from-sorted-array-ii", title: "Remove Duplicates from Sorted Array II", pri: "essential" },
  { g:3, slug: "move-zeroes",          title: "Move Zeroes",          pri: "essential" },
  { g:3, slug: "trapping-rain-water",  title: "Trapping Rain Water",  pri: "stretch", maps: "two_pointers#7" },

  // ---- Sliding Window ----
  { g:4, slug: "maximum-subarray",     title: "Maximum Subarray",     pri: "essential", maps: "dp#6" },
  { g:4, slug: "minimum-window-substring", title: "Minimum Window Substring", pri: "essential" },
  { g:4, slug: "substring-with-concatenation-of-all-words", title: "Substring with Concatenation of All Words", pri: "stretch" },
  { g:4, slug: "best-time-to-buy-and-sell-stock-iv", title: "Best Time to Buy and Sell Stock IV", pri: "optional" },

  // ---- Matrix & Multidimensional Arrays ----
  { g:5, slug: "rotate-image",         title: "Rotate Image",         pri: "essential", maps: "arrays_and_strings#11" },
  { g:5, slug: "number-of-islands",    title: "Number of Islands",    pri: "essential", maps: "graphs#2" },
  { g:5, slug: "number-of-enclaves",   title: "Number of Enclaves",   pri: "essential" },
  { g:5, slug: "spiral-matrix-iii",    title: "Spiral Matrix III",    pri: "stretch" },

  // ---- HashMaps & Sets ----
  { g:6, slug: "group-anagrams",       title: "Group Anagrams",       pri: "essential", maps: "hashmaps_and_sets#8" },
  { g:6, slug: "happy-number",         title: "Happy Number",         pri: "essential" },
  { g:6, slug: "longest-consecutive-sequence", title: "Longest Consecutive Sequence", pri: "essential", maps: "hashmaps_and_sets#10" },
  { g:6, slug: "4sum",                 title: "4Sum",                 pri: "stretch" },

  // ---- Greedy Strategies ----
  // Deliberately thin. Interval merging earns its slot; the rest are reference.
  { g:7, slug: "insert-interval",      title: "Insert Interval",      pri: "essential" },
  { g:7, slug: "non-overlapping-intervals", title: "Non-overlapping Intervals", pri: "stretch" },
  { g:7, slug: "jump-game-ii",         title: "Jump Game II",         pri: "optional" },
  { g:7, slug: "gas-station",          title: "Gas Station",          pri: "optional" },

  // ---- Divide & Conquer + Recursion ----
  { g:8, slug: "binary-search",        title: "Binary Search",        pri: "essential", maps: "binary_search#1" },
  { g:8, slug: "sort-an-array",        title: "Sort an Array",        pri: "essential" },
  { g:8, slug: "search-in-rotated-sorted-array-ii", title: "Search in Rotated Sorted Array II", pri: "stretch" },
  { g:8, slug: "online-majority-element-in-subarray", title: "Online Majority Element in Subarray", pri: "optional" },

  // ---- Full Timed Simulation ----
  // Pick ONE set and run it under a 70-minute clock, in the test's suggested
  // order: problems 1-2 first, then 4, then 3 last. Grade the run, not the
  // problems. Set B is the backup if Set A goes badly and you want a re-run.
  { g:9, set: "A", slug: "product-of-array-except-self", title: "Product of Array Except Self", pri: "essential", maps: "arrays_and_strings#8" },
  { g:9, set: "A", slug: "maximum-number-of-non-overlapping-palindrome-substrings", title: "Maximum Number of Non-overlapping Palindrome Substrings", pri: "optional" },
  { g:9, set: "A", slug: "word-search-ii",  title: "Word Search II",  pri: "optional" },
  { g:9, set: "A", slug: "text-justification", title: "Text Justification", pri: "optional" },
  { g:9, set: "B", slug: "3sum",            title: "3Sum",            pri: "essential", maps: "two_pointers#5" },
  { g:9, set: "B", slug: "sudoku-solver",   title: "Sudoku Solver",   pri: "optional" },
  { g:9, set: "B", slug: "dungeon-game",    title: "Dungeon Game",    pri: "optional" },
];

// Every entry's LeetCode URL is its slug — derive it once rather than repeating
// the prefix 39 times and risking a typo in one of them.
for (const s of SPRINT) s.url = LC + s.slug + "/";

if (typeof module !== "undefined" && module.exports) {
  module.exports = { SPRINT, SPRINT_META, SPRINT_GROUPS };
}
