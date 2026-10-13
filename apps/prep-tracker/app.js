"use strict";

/* ============================================================================
 * DSA Spaced-Repetition Tracker
 * ---------------------------------------------------------------------------
 * Model: every problem lives in a Leitner "box". Grading a problem sets its
 * box and schedules the next review. You only practice what is DUE.
 *
 *   box 1  failed / needed solution   -> review in  1 day
 *   box 2  solved slow / with hints   -> review in  3 days
 *   box 3  solved clean               -> review in  7 days
 *   box 4  fast & confident           -> review in 21 days
 *   box 5  Fast again from box 4      -> review in 45 days
 *   box 6  Fast again from box 5      -> review in 120 days
 *   box 0  never attempted (new)      -> not scheduled
 *
 * The rules (grades, boxes, new-problem order) live in PRACTICE.md at the
 * repo root; INTERVAL and nextBox() are in selection.js.
 *
 * `s: true`  => a solution file already exists in this repo (seeded into
 *               review rotation, staggered so only a few come due per day).
 * `f`        => repo path of that file, shown in the UI.
 * ========================================================================== */

/* Tier 1 doubles as the "core" set used for stat counts, chip highlighting,
 * and group ordering. TIERS comes from selection.js, loaded before this file. */
const CORE = new Set(TIERS[1]);

const CAT_META = {
  arrays_and_strings: { label: "Arrays & Strings", glyph: "[ ]" },
  hashmaps_and_sets:  { label: "Hashmaps & Sets",  glyph: "#" },
  two_pointers:       { label: "Two Pointers",     glyph: "⇄" },
  sliding_window:     { label: "Sliding Window",   glyph: "▭" },
  stacks:             { label: "Stacks",           glyph: "≡" },
  linked_lists:       { label: "Linked Lists",     glyph: "→" },
  binary_search:      { label: "Binary Search",    glyph: "÷" },
  trees:              { label: "Trees",            glyph: "⑂" },
  heaps:              { label: "Heaps",            glyph: "▲" },
  backtracking:       { label: "Backtracking",     glyph: "⌥" },
  graphs:             { label: "Graphs",           glyph: "◈" },
  dp:                 { label: "Dynamic Programming", glyph: "Σ" },
  greedy:             { label: "Greedy & Intervals", glyph: "◤" },
  sorting:            { label: "Sorting",          glyph: "⇅" },
};

// Category display order (core first, then roadmap order).
const CAT_ORDER = [
  "arrays_and_strings", "hashmaps_and_sets", "two_pointers", "sliding_window",
  "stacks", "linked_lists", "binary_search", "trees", "heaps",
  "backtracking", "graphs", "dp", "greedy", "sorting",
];

// AlgoMap roadmap. s = has a solution file in this repo; f = its path.
const PROBLEMS = [
  // ---- Arrays & Strings ----
  { cat: "arrays_and_strings", n: 1,  title: "Find Closest Number to Zero", s: true,  f: "patterns/arrays_and_strings/find_closest_number_to_zero.py" },
  { cat: "arrays_and_strings", n: 2,  title: "Merge Strings Alternately",    s: true,  f: "patterns/arrays_and_strings/merge_strings_alternately.py" },
  { cat: "arrays_and_strings", n: 3,  title: "Roman to Integer",             s: true,  f: "patterns/arrays_and_strings/roman_to_integer.py" },
  { cat: "arrays_and_strings", n: 4,  title: "Is Subsequence",               s: true,  f: "patterns/arrays_and_strings/is_subsequence.py" },
  { cat: "arrays_and_strings", n: 5,  title: "Best Time to Buy and Sell Stock", s: true,  f: "patterns/arrays_and_strings/best_time_to_sell_stock.py" },
  { cat: "arrays_and_strings", n: 6,  title: "Longest Common Prefix",        s: true,  f: "patterns/two_pointers/longest_prefix.py" },
  { cat: "arrays_and_strings", n: 7,  title: "Summary Ranges",               s: false },
  { cat: "arrays_and_strings", n: 8,  title: "Product of Array Except Self", s: true,  f: "patterns/prefix_sum/product_of_array_except_self.py" },
  { cat: "arrays_and_strings", n: 9,  title: "Merge Intervals",              s: false },
  { cat: "arrays_and_strings", n: 10, title: "Spiral Matrix",                s: true,  f: "patterns/grids/spiral_traverse.py" },
  { cat: "arrays_and_strings", n: 11, title: "Rotate Image",                 s: false },
  { cat: "arrays_and_strings", n: 12, title: "Running Sum of 1d Array",      s: true,  f: "patterns/prefix_sum/running_sum.py" },
  { cat: "arrays_and_strings", n: 13, title: "Rotate Array",                 s: true,  f: "patterns/arrays_and_strings/rotate_array.py" },
  { cat: "arrays_and_strings", n: 14, title: "Reverse String II",            s: false },
  { cat: "arrays_and_strings", n: 15, title: "Spiral Matrix III",            s: false },
  { cat: "arrays_and_strings", n: 16, title: "Text Justification",           s: false },
  { cat: "arrays_and_strings", n: 17, title: "Longest Common Prefix of K Strings After Removal", s: false },

  // ---- Hashmaps & Sets ----
  { cat: "hashmaps_and_sets", n: 1,  title: "Jewels and Stones",             s: true,  f: "patterns/hashmaps_and_sets/jewels_and_stones.py" },
  { cat: "hashmaps_and_sets", n: 2,  title: "Contains Duplicate",            s: true,  f: "patterns/hashmaps_and_sets/contains_duplicate.py" },
  { cat: "hashmaps_and_sets", n: 3,  title: "Ransom Note",                   s: true,  f: "patterns/hashmaps_and_sets/ransom_note.py" },
  { cat: "hashmaps_and_sets", n: 4,  title: "Valid Anagram",                 s: true,  f: "patterns/hashmaps_and_sets/valid_anagram.py" },
  { cat: "hashmaps_and_sets", n: 5,  title: "Maximum Number of Balloons",    s: false },
  { cat: "hashmaps_and_sets", n: 6,  title: "Two Sum",                       s: false },
  { cat: "hashmaps_and_sets", n: 7,  title: "Valid Sudoku",                  s: false },
  { cat: "hashmaps_and_sets", n: 8,  title: "Group Anagrams",                s: false },
  { cat: "hashmaps_and_sets", n: 9,  title: "Majority Element",              s: false },
  { cat: "hashmaps_and_sets", n: 10, title: "Longest Consecutive Sequence",  s: false },
  { cat: "hashmaps_and_sets", n: 11, title: "Happy Number",                  s: false },
  { cat: "hashmaps_and_sets", n: 12, title: "Count Anagrams",                s: false },

  // ---- 2 Pointers ----
  { cat: "two_pointers", n: 1, title: "Squares of a Sorted Array",           s: true,  f: "patterns/two_pointers/squares_of_sorted_arr.py" },
  { cat: "two_pointers", n: 2, title: "Reverse String",                      s: true,  f: "patterns/two_pointers/reverse_string.py" },
  { cat: "two_pointers", n: 3, title: "Two Sum II - Input Array Is Sorted",  s: true,  f: "patterns/two_pointers/two_sum_ii.py" },
  { cat: "two_pointers", n: 4, title: "Valid Palindrome",                    s: true,  f: "patterns/two_pointers/valid_palindrome.py" },
  { cat: "two_pointers", n: 5, title: "3Sum",                                s: false },
  { cat: "two_pointers", n: 6, title: "Container With Most Water",           s: false },
  { cat: "two_pointers", n: 7, title: "Trapping Rain Water",                 s: false },
  { cat: "two_pointers", n: 8, title: "Merge Sorted Array",              s: true,  f: "patterns/two_pointers/merge_sorted_array.py" },
  { cat: "two_pointers", n: 9, title: "Remove Duplicates from Sorted Array II", s: false },
  { cat: "two_pointers", n: 10, title: "Move Zeroes",                    s: false },
  { cat: "two_pointers", n: 11, title: "4Sum",                           s: false },

  // ---- Sliding Window ----
  { cat: "sliding_window", n: 1, title: "Maximum Average Subarray I",        s: true,  f: "patterns/sliding_window/max_average_subarr.py" },
  { cat: "sliding_window", n: 2, title: "Max Consecutive Ones III",          s: true,  f: "patterns/sliding_window/max_consecutive_ones_iii.py" },
  { cat: "sliding_window", n: 3, title: "Longest Substring Without Repeating Characters", s: true, f: "patterns/sliding_window/longest_substring_without_repeated_characters.py" },
  { cat: "sliding_window", n: 4, title: "Longest Repeating Character Replacement", s: true, f: "patterns/sliding_window/longest_repeating_character_replacement.py" },
  { cat: "sliding_window", n: 5, title: "Minimum Size Subarray Sum",         s: true,  f: "patterns/sliding_window/2025/smallest_subarray_with_num_s.py" },
  { cat: "sliding_window", n: 6, title: "Permutation in String",             s: false },
  { cat: "sliding_window", n: 7, title: "Minimum Window Substring",       s: false },
  { cat: "sliding_window", n: 8, title: "Substring with Concatenation of All Words", s: false },

  // ---- Stacks ----
  { cat: "stacks", n: 1, title: "Baseball Game",                             s: true,  f: "patterns/stacks/baseball_game.py" },
  { cat: "stacks", n: 2, title: "Valid Parentheses",                         s: true,  f: "patterns/stacks/valid_parentheses.py" },
  { cat: "stacks", n: 3, title: "Evaluate Reverse Polish Notation",          s: true,  f: "patterns/stacks/evaluate_rpn.py" },
  { cat: "stacks", n: 4, title: "Daily Temperatures",                        s: true,  f: "patterns/stacks/daily_temperatures.py" },
  { cat: "stacks", n: 5, title: "Min Stack",                                 s: false },

  // ---- Linked Lists ----
  { cat: "linked_lists", n: 1, title: "Remove Duplicates from Sorted List",  s: true,  f: "patterns/linked_lists/remove_duplicates.py" },
  { cat: "linked_lists", n: 2, title: "Reverse Linked List",                 s: true,  f: "patterns/linked_lists/reverse_linked_list.py" },
  { cat: "linked_lists", n: 3, title: "Merge Two Sorted Lists",              s: true,  f: "patterns/linked_lists/merge2_sorted_lists.py" },
  { cat: "linked_lists", n: 4, title: "Linked List Cycle",                   s: true,  f: "patterns/linked_lists/has_cycle.py" },
  { cat: "linked_lists", n: 5, title: "Middle of the Linked List",           s: false },
  { cat: "linked_lists", n: 6, title: "Remove Nth Node from End of List",    s: false },
  { cat: "linked_lists", n: 7, title: "Copy List with Random Pointer",       s: false },

  // ---- Binary Search ----
  { cat: "binary_search", n: 1, title: "Binary Search",                      s: true,  f: "patterns/binary_search/classic_binary_search.py" },
  { cat: "binary_search", n: 2, title: "Search Insert Position",             s: true,  f: "patterns/binary_search/search_insert_position.py" },
  { cat: "binary_search", n: 3, title: "First Bad Version",                  s: true,  f: "patterns/binary_search/first_bad_version.py" },
  { cat: "binary_search", n: 4, title: "Valid Perfect Square",               s: false },
  { cat: "binary_search", n: 5, title: "Search a 2D Matrix",                 s: false },
  { cat: "binary_search", n: 6, title: "Find Minimum in Rotated Sorted Array", s: false },
  { cat: "binary_search", n: 7, title: "Search in Rotated Sorted Array",     s: false },
  { cat: "binary_search", n: 8, title: "Koko Eating Bananas",                s: true,  f: "patterns/binary_search/binary_search_on_answer.py" },
  { cat: "binary_search", n: 9, title: "Search in Rotated Sorted Array II", s: false },
  { cat: "binary_search", n: 10, title: "Online Majority Element in Subarray", s: false },

  // ---- Trees ----
  { cat: "trees", n: 1,  title: "Invert Binary Tree",                        s: true,  f: "patterns/trees/DFS/invert_binary_tree.py" },
  { cat: "trees", n: 2,  title: "Maximum Depth of Binary Tree",              s: true,  f: "patterns/trees/BFS/maximum_depth_bt.py" },
  { cat: "trees", n: 3,  title: "Balanced Binary Tree",                      s: true,  f: "patterns/trees/DFS/is_balanced_tree.py" },
  { cat: "trees", n: 4,  title: "Diameter of Binary Tree",                   s: true,  f: "patterns/trees/DFS/diameter_of_binary_tree.py" },
  { cat: "trees", n: 5,  title: "Same Binary Tree",                          s: false },
  { cat: "trees", n: 6,  title: "Symmetric Tree",                            s: true,  f: "patterns/trees/DFS/symetric_tree.py" },
  { cat: "trees", n: 7,  title: "Path Sum",                                  s: true,  f: "patterns/trees/DFS/path_sum.py" },
  { cat: "trees", n: 8,  title: "Subtree of Another Tree",                   s: false },
  { cat: "trees", n: 9,  title: "Binary Tree Level Order Traversal (BFS)",   s: true,  f: "patterns/trees/BFS/binary_tree_level_order_traversal.py" },
  { cat: "trees", n: 10, title: "Kth Smallest Element in a BST",             s: false },
  { cat: "trees", n: 11, title: "Minimum Absolute Difference in BST",        s: false },
  { cat: "trees", n: 12, title: "Validate Binary Search Tree",              s: false },
  { cat: "trees", n: 13, title: "Lowest Common Ancestor of a BST",           s: false },
  { cat: "trees", n: 14, title: "Implement Trie (Prefix Tree)",              s: false },

  // ---- Heaps ----
  { cat: "heaps", n: 1, title: "Last Stone Weight",                          s: true,  f: "patterns/heaps/last_stone_weight.py" },
  { cat: "heaps", n: 2, title: "Kth Largest Element in an Array",            s: true,  f: "patterns/heaps/kth_largest_element.py" },
  { cat: "heaps", n: 3, title: "Top K Frequent Elements",                    s: true,  f: "patterns/heaps/top_k_frequent_elements.py" },
  { cat: "heaps", n: 4, title: "K Closest Points to Origin",                 s: true,  f: "patterns/heaps/k_closest_points_to_origin.py" },
  { cat: "heaps", n: 5, title: "Merge K Sorted Linked Lists",                s: false },
  { cat: "heaps", n: 6, title: "Find Median from Data Stream",             s: false },

  // ---- Recursive Backtracking ----
  { cat: "backtracking", n: 1, title: "Subsets",                             s: true,  f: "patterns/backtracking/subsets.py" },
  { cat: "backtracking", n: 2, title: "Permutations",                        s: true,  f: "patterns/backtracking/permutations.py" },
  { cat: "backtracking", n: 3, title: "Combinations",                        s: true,  f: "patterns/backtracking/combinations.py" },
  { cat: "backtracking", n: 4, title: "Combination Sum",                     s: true,  f: "patterns/backtracking/combination_sum.py" },
  { cat: "backtracking", n: 5, title: "Letter Combinations of a Phone Number", s: true, f: "patterns/backtracking/phone_letters_combination.py" },
  { cat: "backtracking", n: 6, title: "Generate Parentheses",                s: false },
  { cat: "backtracking", n: 7, title: "Word Search",                         s: false },
  { cat: "backtracking", n: 8, title: "Word Search II",                    s: false },
  { cat: "backtracking", n: 9, title: "Sudoku Solver",                     s: false },

  // ---- Graphs ----
  { cat: "graphs", n: 1,  title: "Find if Path Exists in Graph",             s: true,  f: "patterns/graphs/find_if_path_exists.py" },
  { cat: "graphs", n: 2,  title: "Number of Islands",                        s: true,  f: "patterns/grids/number_of_islands.py" },
  { cat: "graphs", n: 3,  title: "Max Area of Island",                       s: true,  f: "patterns/grids/max_area_of_islands.py" },
  { cat: "graphs", n: 4,  title: "Course Schedule (Detecting Cycles)",       s: true,  f: "patterns/graphs/course_schedule.py" },
  { cat: "graphs", n: 5,  title: "Course Schedule II (Topological Sort)",    s: false },
  { cat: "graphs", n: 6,  title: "Pacific Atlantic Water Flow",              s: false },
  { cat: "graphs", n: 7,  title: "Clone Graph",                              s: false },
  { cat: "graphs", n: 8,  title: "Rotting Oranges",                          s: false },
  { cat: "graphs", n: 9,  title: "Min Cost to Connect All Points (Prim's)",  s: false },
  { cat: "graphs", n: 10, title: "Network Delay Time (Dijkstra's)",          s: false },
  { cat: "graphs", n: 11, title: "Number of Enclaves",                    s: false },

  // ---- Dynamic Programming ----
  { cat: "dp", n: 1,  title: "Fibonacci Number",                             s: true,  f: "patterns/DP/fibonacci_number.py" },
  { cat: "dp", n: 2,  title: "Climbing Stairs",                              s: true,  f: "patterns/DP/climbing_stairs.py" },
  { cat: "dp", n: 3,  title: "Min Cost Climbing Stairs",                     s: true,  f: "patterns/DP/min_cost_climbing_stairs.py" },
  { cat: "dp", n: 4,  title: "House Robber",                                 s: true,  f: "patterns/DP/house_robber.py" },
  { cat: "dp", n: 5,  title: "Unique Paths",                                 s: false },
  { cat: "dp", n: 6,  title: "Maximum Subarray (Kadane's)",                  s: false },
  { cat: "dp", n: 7,  title: "Jump Game",                                    s: false },
  { cat: "dp", n: 8,  title: "Coin Change",                                  s: true,  f: "patterns/DP/coin_change.py" },
  { cat: "dp", n: 9,  title: "Longest Increasing Subsequence",               s: false },
  { cat: "dp", n: 10, title: "Longest Common Subsequence",                   s: false },
  { cat: "dp", n: 11, title: "Best Time to Buy and Sell Stock IV",         s: false },
  { cat: "dp", n: 12, title: "Minimum Changes to Make K Semi-palindromes", s: false },
  { cat: "dp", n: 13, title: "Maximum Number of Non-overlapping Palindrome Substrings", s: false },
  { cat: "dp", n: 14, title: "Dungeon Game",                               s: false },

  // ---- Greedy & Intervals ----
  { cat: "greedy", n: 1, title: "Insert Interval",                         s: false },
  { cat: "greedy", n: 2, title: "Non-overlapping Intervals",               s: false },
  { cat: "greedy", n: 3, title: "Jump Game II",                            s: false },
  { cat: "greedy", n: 4, title: "Gas Station",                             s: false },

  // ---- Sorting ----
  { cat: "sorting", n: 1, title: "Sort an Array",                          s: false },
];

// Sub-labels are the "How to grade" checks in PRACTICE.md, so that
// self-grading is a measurement rather than a mood. A first attempt has a
// 60-minute cap and a full rep 35, so the two sets of checks differ.
const GRADES = [
  { box: 1, cls: "g1", label: "Failed",
    full: "no pass at 35 min, or saw the solution", new: "read the solution, or hit 60 min" },
  { box: 2, cls: "g2", label: "Slow",
    full: "hint, 26–35 min, or 3+ wrong submits",   new: "pattern hint, or >40 min" },
  { box: 3, cls: "g3", label: "Clean",
    full: "no hint, 16–25 min",                     new: "no hint, 21–40 min" },
  { box: 4, cls: "g4", label: "Fast",
    full: "no hint, ≤15 min",                       new: "no hint, ≤20 min" },
];
// Boxes 5 and 6 are only reachable through Fast, so they wear its label.
function gradeOf(box) { return GRADES.find((g) => g.box === Math.min(box, 4)); }
const NEW_PER_WEEK = 2;   // PRACTICE.md "The week": target 2, stretch 3
const NEW_STRETCH = 3;
const NEW_PER_DAY_SEED = 3; // stagger solved problems so ~3 come due per day

const STORE_KEY = "srt.v1";

/* ---------- date helpers (local time, date-only ISO) ---------- */
function todayISO() {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return toISO(d);
}
function toISO(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}
function addDays(iso, n) {
  const d = new Date(iso + "T00:00:00");
  d.setDate(d.getDate() + n);
  return toISO(d);
}
function daysUntil(iso) {
  const a = new Date(todayISO() + "T00:00:00");
  const b = new Date(iso + "T00:00:00");
  return Math.round((b - a) / 86400000);
}
// Monday to Sunday, local time.
function weekBounds(iso) {
  const monday = mondayOf(iso, new Date(iso + "T00:00:00").getDay());
  return { start: monday, end: addDays(monday, 6) };
}
function id(p) { return p.cat + "#" + p.n; }
function catRank(cat) {
  const i = CAT_ORDER.indexOf(cat);
  return i === -1 ? 99 : i;
}

/* ---------- sprint helpers (see sprint.js) ----------
 * Sprint rows live in the SAME flat STATE object as catalog problems, keyed
 * "sprint#<slug>". Two consequences, both deliberate:
 *   - the existing `input` handler writes STATE[pid].trigger for whatever
 *     data-id a row carries, so the note field needs no new code;
 *   - seedIfNeeded() iterates PROBLEMS only, so a sprint key can never be
 *     handed a Leitner box or a due date and can never reach "Due today".
 */
const SPRINT_PREFIX = "sprint#";
const SPRINT_STATUS = [
  { key: "done",    cls: "s-done",    label: "Done",    sub: "solved it — write the trigger" },
  { key: "stuck",   cls: "s-stuck",   label: "Stuck",   sub: "read the solution / hit the cap" },
  { key: "skipped", cls: "s-skipped", label: "Skipped", sub: "reference only — moving on" },
];
const PRI_RANK = { essential: 0, stretch: 1, optional: 2 };

const PROBLEM_BY_ID = {};
for (const p of PROBLEMS) PROBLEM_BY_ID[id(p)] = p;
const SPRINT_GROUP_BY_N = {};
for (const grp of SPRINT_GROUPS) SPRINT_GROUP_BY_N[grp.g] = grp;

function sid(s) { return SPRINT_PREFIX + s.slug; }
function sprog(s) { return STATE[sid(s)] || { status: null, trigger: "" }; }
function isSprintKey(k) { return k.indexOf(SPRINT_PREFIX) === 0; }
/* A sprint problem is a FIRST SOLVE that happened to come from an interview
 * list, so its solution belongs in patterns/ like any other -- patterns/ is
 * indexed by pattern, not by where the problem came from. There used to be a
 * sprint/ staging directory here; it was never used once in 39 problems, and
 * deleting it (2026-08-25) removed the "move the file" step from the merge.
 *
 * If the problem has a catalog twin, borrow its category. Otherwise fall back
 * to the sprint group's folder name, which is close enough to pick by hand. */
function sprintFilePath(s) {
  const twin = s.maps ? PROBLEM_BY_ID[s.maps] : null;
  const dir = twin ? twin.cat : SPRINT_GROUP_BY_N[s.g].dir;
  return `patterns/${dir}/${s.slug.replace(/-/g, "_")}.py`;
}

/* ---------- persistence ----------
 * Two modes:
 *  - SERVER MODE: opened via server.py. Progress is read from and written back to
 *    apps/prep-tracker/progress.json in this repo — the repo is the source of truth,
 *    so `git pull` on any machine resumes your progress. localStorage mirrors it as a cache.
 *  - OFFLINE MODE: opened via file:// (no server). Falls back to localStorage only.
 */
const API = "api/progress";
let SERVER_MODE = false;
let saveTimer = null;

/* HALT states. Both mean "the stored data is in doubt", and while either is set
 * the app renders an explanation and REFUSES TO WRITE. That refusal is the
 * point: every verified way this app destroyed history ended with a well-meaning
 * save over a file it had just misread. */
let HALT = null;        // {title, detail} -- load failure, or this tab is stale
let LOCAL_AHEAD = null; // {keys, mirror} -- this browser holds work the file lacks
let REVISION = null;    // ETag of the progress file this tab loaded
let postsInFlight = 0;
let localEdits = 0;     // bumped on every save, so a refresh can tell it raced one
let savedEdits = 0;     // the localEdits value the server last accepted

/* A save the server has not accepted yet: pending, in flight, or FAILED. The
 * failed case is the one that matters. A refresh that ignored it would replace
 * STATE and drop the grade; leaving it lets the next save 409 and halt. */
function hasUnsaved() { return savedEdits < localEdits; }

function isHalted() { return HALT !== null || LOCAL_AHEAD !== null; }

/* The mirror is stored as {savedAt, state}. The old format was the bare state
 * object, so a first load after this change still recognises it. */
function loadLocal() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE_KEY));
    if (!raw || typeof raw !== "object") return { savedAt: null, state: {} };
    if (raw.state && typeof raw.state === "object") {
      return { savedAt: raw.savedAt || null, state: raw.state };
    }
    return { savedAt: null, state: raw }; // legacy flat shape
  } catch (_) {
    return { savedAt: null, state: {} };
  }
}

/* Keys where this browser holds a GRADE the server file lacks. The safety net
 * for a lost write — a dead server, a dropped unload flush, a file restored from
 * git behind the app's back. Without it the mirror was written on every save and
 * never read, so the first save after a restart destroyed the only copy.
 *
 * Three guards, each closing a false positive that would cry wolf. A recovery
 * prompt that fires when nothing was lost is worse than none: it trains you to
 * dismiss the one that matters.
 *
 *  1. A mirror with no `savedAt` predates this format, so its age is unknown and
 *     it cannot be shown to be newer than anything. It was never read before
 *     this change either, so skipping it loses nothing.
 *  2. `sprint#` keys are a separate namespace with no Leitner state and their own
 *     lifecycle — the post-test merge DELETES them on purpose. Their absence
 *     from the file is the intended end state, not a lost write.
 *  3. A key the server lacks only counts if the mirror actually graded it
 *     (`last` is set). An entry created by typing a note has no grade to lose.
 */
function mirrorAhead(mirrorBox, server) {
  if (!mirrorBox.savedAt) return []; // guard 1: unknown age
  const mirror = mirrorBox.state;
  return Object.keys(mirror).filter((k) => {
    if (isSprintKey(k)) return false; // guard 2: deleted on purpose by a merge
    const m = mirror[k], s = server[k];
    if (!m || typeof m !== "object") return false;
    if (!s) return !!m.last; // guard 3: only a real grade counts as lost
    return (m.last || "") > (s.last || "");
  });
}

async function loadProgress() {
  let r;
  try {
    r = await fetch(API, { cache: "no-store" });
  } catch (_) {
    // Genuinely no server: the file:// path. localStorage is the only store.
    SERVER_MODE = false;
    return loadLocal().state;
  }

  // A REACHABLE server that answers badly is NOT "offline". Conflating the two
  // told the user to run server.py while it was already running, and sent a
  // whole day of grades into a mirror that server mode never reads back.
  SERVER_MODE = true;
  REVISION = r.headers.get("ETag");

  // A 404 means this server does not implement persistence at all -- someone is
  // serving the directory with `python3 -m http.server`, which is the same
  // situation as file://. That is offline mode, not a broken file.
  if (r.status === 404) {
    SERVER_MODE = false;
    REVISION = null;
    return loadLocal().state;
  }

  if (!r.ok) {
    let detail = `The server answered ${r.status}.`;
    try {
      const body = await r.json();
      if (body && body.detail) detail = body.detail;
    } catch (_) { /* keep the status-only message */ }
    HALT = { title: "Could not read progress.json", detail };
    return {};
  }

  let data;
  try {
    data = await r.json();
  } catch (e) {
    HALT = { title: "progress.json is not valid JSON", detail: String(e) };
    return {};
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    HALT = { title: "progress.json is not an object", detail: "Refusing to seed over it." };
    return {};
  }

  const mirrorBox = loadLocal();
  const ahead = mirrorAhead(mirrorBox, data);
  if (ahead.length) LOCAL_AHEAD = { keys: ahead, mirror: mirrorBox.state };
  return data;
}

function postState() {
  saveTimer = null;
  postsInFlight++;
  const sending = localEdits;
  return fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json", "If-Match": REVISION || "*" },
    body: JSON.stringify(STATE),
  })
    .then((r) => {
      // 409: the file moved under us — another tab, another machine, a git pull.
      // Writing again would revert that newer work, so stop writing entirely.
      if (r.status === 409) {
        HALT = {
          title: "This tab is out of date",
          detail:
            "progress.json changed since this tab loaded it, probably from another tab " +
            "or a git pull. Saving now would revert that newer work. Export a backup, " +
            "then reload.",
        };
        render();
        return;
      }
      if (!r.ok) throw new Error("HTTP " + r.status);
      REVISION = r.headers.get("ETag") || REVISION;
      savedEdits = Math.max(savedEdits, sending);
      setFootNote(true);
    })
    // Previously `.catch(() => {})` — a dead server meant every grade looked
    // saved and silently wasn't. You'd only find out at `git status`, or never.
    .catch(() => setFootNote(false))
    .finally(() => { postsInFlight--; });
}

function writeMirror() {
  try {
    localStorage.setItem(
      STORE_KEY,
      JSON.stringify({ savedAt: new Date().toISOString(), state: STATE })
    );
    return true;
  } catch (_) {
    return false;
  }
}

/* `immediate` skips the debounce. Only textarea typing needs debouncing;
 * grading and reset are single discrete events, and debouncing them means a
 * reload within 400ms loses the write — after which the next server-mode load
 * overwrites localStorage with the stale file and the grade is gone for good. */
function saveState(opts) {
  if (isHalted()) return; // never write while the stored data is in doubt
  localEdits++;
  // Always mirror locally so an offline reload still has the latest.
  // Offline, localStorage IS the store, so a refused write is total loss.
  if (!writeMirror() && !SERVER_MODE) setFootNote(false, "storage");
  if (!SERVER_MODE) return;
  clearTimeout(saveTimer);
  if (opts && opts.immediate) {
    postState();
    return;
  }
  saveTimer = setTimeout(postState, 400);
}

/* A pending debounced write would be lost on reload/close. `keepalive` lets the
 * request outlive the page. sendBeacon cannot be used any more: the revision
 * check needs an If-Match header and beacons cannot set headers. If this flush
 * is dropped anyway, mirrorAhead() catches it on the next load. */
window.addEventListener("beforeunload", () => {
  if (!SERVER_MODE || !saveTimer || isHalted()) return;
  clearTimeout(saveTimer);
  saveTimer = null;
  try {
    fetch(API, {
      method: "POST",
      keepalive: true,
      headers: { "Content-Type": "application/json", "If-Match": REVISION || "*" },
      body: JSON.stringify(STATE),
    });
  } catch (_) { /* nothing left to try at teardown */ }
});

/* grade.py writes the file while this tab sits in the background, so pick its
 * grade up on return. Only when this tab has nothing of its own to send:
 * otherwise the next save's 409 is the correct outcome, and it halts. */
async function refreshIfChanged() {
  const busy = () => isHalted() || saveTimer !== null || postsInFlight > 0 || hasUnsaved();
  if (!SERVER_MODE || busy()) return;
  const editsBefore = localEdits;
  let r, data;
  try {
    r = await fetch(API, { cache: "no-store" });
    if (!r.ok) return; // a broken file surfaces on the next save, not here
    data = await r.json();
  } catch (_) {
    return;
  }
  const etag = r.headers.get("ETag");
  if (!etag || etag === REVISION) return;
  if (!data || typeof data !== "object" || Array.isArray(data)) return;
  if (busy() || localEdits !== editsBefore) return; // a grade landed mid-fetch
  STATE = data;
  REVISION = etag;
  writeMirror(); // else the next load compares the file with a stale mirror
  render();
}
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") refreshIfChanged();
});
window.addEventListener("focus", refreshIfChanged);

/* Seed any solved problem that has no progress yet: put it in box 2 with a
 * staggered due date so the initial review load is ~NEW_PER_DAY_SEED per day.
 * Idempotent — only touches problems missing an entry, so it also picks up
 * newly-added solved problems on later loads. */
function seedIfNeeded() {
  if (isHalted()) return; // a suspect load must never trigger a full reseed
  const solved = PROBLEMS.filter((p) => p.s).sort((a, b) => {
    const ca = CORE.has(a.cat) ? 0 : 1;
    const cb = CORE.has(b.cat) ? 0 : 1;
    if (ca !== cb) return ca - cb;
    if (catRank(a.cat) !== catRank(b.cat)) return catRank(a.cat) - catRank(b.cat);
    return a.n - b.n;
  });
  const today = todayISO();

  // Guard on box, NOT on presence. Typing a trigger note creates a box-0
  // entry (see the "input" handler), so a presence check would permanently
  // exclude any problem you'd jotted a note on before solving it — it would
  // never get a due date and never enter the rotation.
  const toSeed = solved.filter((p) => {
    const e = STATE[id(p)];
    return !(e && e.box > 0);
  });

  // Stagger across the problems BEING SEEDED, not across every solved problem.
  // Indexing into `solved` meant one new addition inherited its position in the
  // whole list: a newly-solved `dp` problem came due 19 days out instead of
  // today, so the app looked like it had ignored the solution. On a first run
  // toSeed is everything, so the original spread is unchanged.
  toSeed.forEach((p, i) => {
    const existing = STATE[id(p)];
    STATE[id(p)] = {
      box: 2,
      due: addDays(today, Math.floor(i / NEW_PER_DAY_SEED)),
      last: null,
      attempts: 0,
      trigger: (existing && existing.trigger) || "", // keep any note already written
    };
  });
  if (toSeed.length) saveState({ immediate: true });
}

/* ---------- app state ---------- */
let STATE = {};
let VIEW = "due";
let CAT_FILTER = "all";
let OPEN_ID = null;
let SHOW_ALL = false; // session-only Due-view override; not persisted
let FOCUS_TRIGGER = false; // one-shot: focus the note field after the next render
/* Each entry as it was before today's first grade. A re-grade ("graded it
 * wrong?") must start from there: Fast now climbs from the current box, so
 * re-clicking Fast would otherwise climb twice. Session-only on purpose. */
const BEFORE_TODAY = {};

/* ---------- derived helpers ---------- */
function prog(p) {
  return STATE[id(p)] || { box: 0, due: null, last: null, attempts: 0, trigger: "" };
}
function isDue(p) {
  const st = prog(p);
  return st.box >= 1 && st.due && daysUntil(st.due) <= 0;
}
/* Graded today. These leave the due list the moment they're graded (their due
 * date jumps forward), so without a section of their own they'd just vanish —
 * taking the trigger prompt with them. */
function isDoneToday(p) {
  const st = prog(p);
  return st.box >= 1 && st.last === todayISO();
}

/* ---------- rendering ---------- */
const listEl = document.getElementById("list");
const statsEl = document.getElementById("stats");
const filterEl = document.getElementById("filter");
const dueBadge = document.getElementById("dueBadge");
const sprintBadge = document.getElementById("sprintBadge");

function render() {
  // A halted app must not draw lists as though the data were trustworthy.
  if (isHalted()) {
    renderHalt();
    return;
  }
  renderStats();
  renderFilter();
  renderList();
  document.querySelectorAll(".tab").forEach((t) =>
    t.classList.toggle("is-active", t.dataset.view === VIEW)
  );

  // The graded row moves down into "Done today", so follow it and land the
  // cursor in the note field — otherwise you'd have to hunt for where it went.
  if (FOCUS_TRIGGER) {
    FOCUS_TRIGGER = false;
    const ta = listEl.querySelector(".row.is-open textarea[data-trigger]");
    if (ta) {
      ta.closest(".row").scrollIntoView({ behavior: "smooth", block: "center" });
      ta.focus();
      ta.setSelectionRange(ta.value.length, ta.value.length);
    }
  }
}

/* The halt panel replaces the whole list. There is deliberately no "continue
 * anyway" button: every path that destroyed history did so by carrying on. */
function renderHalt() {
  filterEl.style.display = "none";
  statsEl.innerHTML = "";
  dueBadge.textContent = "0";
  sprintBadge.textContent = "0";

  if (LOCAL_AHEAD) {
    const n = LOCAL_AHEAD.keys.length;
    listEl.innerHTML =
      `<div class="help halt">` +
        `<h2>&#9888; This browser holds ${n} change${n === 1 ? "" : "s"} the repo file does not</h2>` +
        `<p>Saving now would discard ${n === 1 ? "it" : "them"}, so writes are paused until you choose. ` +
        `This usually means the server died, or the file was restored from git while a tab was open.</p>` +
        `<p class="history">${LOCAL_AHEAD.keys.map(escapeHTML).join(", ")}</p>` +
        `<div class="foot__actions">` +
          `<button class="ghost" id="haltExport">Export a backup first</button>` +
          `<button class="ghost" id="haltMerge">Merge — keep the newer of each</button>` +
          `<button class="ghost danger" id="haltDiscard">Discard this browser&#39;s copy</button>` +
        `</div>` +
      `</div>`;
    return;
  }

  listEl.innerHTML =
    `<div class="help halt">` +
      `<h2>&#9888; ${escapeHTML(HALT.title)}</h2>` +
      `<p>${escapeHTML(HALT.detail)}</p>` +
      `<p>Nothing will be written until this is resolved. That is deliberate — ` +
      `saving over a file the app has misread is how history gets lost.</p>` +
      `<div class="foot__actions">` +
        `<button class="ghost" id="haltExport">Export what this tab has</button>` +
        `<button class="ghost" id="haltReload">Reload</button>` +
      `</div>` +
    `</div>`;
}

/* "merge" keeps the mirror's entry for each diverged key; "discard" keeps the
 * server's. Either way the save that follows rewrites the mirror from STATE, so
 * the two are back in agreement. */
function resolveLocalAhead(mode) {
  const ahead = LOCAL_AHEAD;
  LOCAL_AHEAD = null;
  if (mode === "merge") {
    for (const k of ahead.keys) STATE[k] = ahead.mirror[k];
  }
  saveState({ immediate: true });
  render();
}

/* Shared by the footer button and the halt panel. Appending the anchor and
 * revoking on the next tick matters: a detached anchor and a synchronous revoke
 * both fail outside Chromium, and this is the app's only backup path — it sits
 * directly beside Reset all. */
function exportProgress() {
  const blob = new Blob([JSON.stringify(STATE, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "dsa-prep-progress.json";
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 0);
}

// The badge: today's reps, not the backlog total, which measured the pile.
function repsLeftToday() {
  const windowLen = selectWindow(dueCandidates(PROBLEMS.filter(isDue)), WINDOW_SIZE).length;
  const gradedToday = PROBLEMS.filter(isDoneToday).map(prog);
  return repsLeft(windowLen, gradedToday, todayISO(), WINDOW_SIZE);
}

function thisWeek() {
  const { start, end } = weekBounds(todayISO());
  return weeklyCounts(Object.values(STATE), start, end);
}

function renderStats() {
  const solvedCount = PROBLEMS.filter((p) => p.s).length;
  const coreTotal = PROBLEMS.filter((p) => CORE.has(p.cat)).length;
  const coreSolved = PROBLEMS.filter((p) => CORE.has(p.cat) && p.s).length;
  const mastered = PROBLEMS.filter((p) => prog(p).box >= 4).length;
  const sprintDone = SPRINT.filter((s) => sprog(s).status === "done").length;

  dueBadge.textContent = repsLeftToday();
  sprintBadge.textContent = sprintDone;

  // The sprint answers a different question from the rotation: not "how deep is
  // my memory" but "how much of the list have I covered, and where am I stuck".
  if (VIEW === "sprint" && SPRINT.length) {
    const essential = SPRINT.filter((s) => s.pri === "essential");
    const essentialDone = essential.filter((s) => sprog(s).status === "done").length;
    const stuck = SPRINT.filter((s) => sprog(s).status === "stuck").length;
    const noted = SPRINT.filter((s) => (sprog(s).trigger || "").trim()).length;
    statsEl.innerHTML = [
      stat("due", stuck, "marked stuck"),
      stat("core", `${essentialDone}/${essential.length}`, "essential done"),
      stat("solved", `${sprintDone}/${SPRINT.length}`, "sprint done"),
      stat("", noted, "trigger notes"),
    ].join("");
    return;
  }

  const week = thisWeek();
  statsEl.innerHTML = [
    stat("due stat--week",
      `New this week: ${week.newCount}/${NEW_PER_WEEK} · Reps this week: ${week.reps}`,
      "Monday to Sunday"),
    stat("solved", `${solvedCount}/${PROBLEMS.length}`, "solved locally"),
    stat("core", `${coreSolved}/${coreTotal}`, "core solved"),
    stat("", mastered, "box 4 and up"),
  ].join("");
}
function stat(mod, num, label) {
  return (
    `<div class="stat ${mod ? "stat--" + mod : ""}">` +
    `<div class="stat__num">${num}</div>` +
    `<div class="stat__label">${label}</div></div>`
  );
}

function renderFilter() {
  // AlgoMap category chips mean nothing inside the sprint, which groups by day.
  filterEl.style.display = VIEW === "sprint" ? "none" : "";
  if (VIEW === "sprint") return;

  const cats = ["all", ...CAT_ORDER];
  filterEl.innerHTML = cats
    .map((c) => {
      const label = c === "all" ? "All" : CAT_META[c].label;
      const core = c !== "all" && CORE.has(c) ? " is-core" : "";
      const active = c === CAT_FILTER ? " is-active" : "";
      return `<button class="chip${core}${active}" data-cat="${c}">${label}</button>`;
    })
    .join("");
}

function visibleProblems() {
  let items = PROBLEMS.slice();
  if (VIEW === "due") items = items.filter(isDue);
  // Keep a problem visible in New after you grade it. The filter used to be
  // box === 0 alone, so grading made the row disappear on the spot -- and the
  // trigger-note prompt went with it, because FOCUS_TRIGGER had no open row to
  // land in. That is the daily path now ("3 reps + 1 new"), so it has to hold.
  else if (VIEW === "new") items = items.filter((p) => !p.s && (prog(p).box === 0 || isDoneToday(p)));
  // "all" => everything
  if (CAT_FILTER !== "all") items = items.filter((p) => p.cat === CAT_FILTER);
  return items;
}

/* Header strip above the Due list, plus today's grading count — derived from
 * the `last` field that gradeProblem() already writes. The backlog total shows
 * only after "Show all": by default the day is the unit, not the pile. */
function windowNoteHTML(shown, total) {
  const gradedToday = Object.values(STATE).filter((s) => s && s.last === todayISO()).length;
  let toggle = "";
  if (SHOW_ALL) {
    toggle = `<button class="ghost" id="windowToggle">Show window</button>`;
  } else if (total > shown) {
    toggle = `<button class="ghost" id="windowToggle">Show all</button>`;
  }
  let scope = `<strong>${repsLeftToday()}</strong> of ${WINDOW_SIZE} reps left today`;
  if (SHOW_ALL) scope = `Showing all <strong>${total}</strong> due`;
  else if (CAT_FILTER !== "all") scope = `Showing <strong>${shown}</strong> in this category`;
  return (
    `<div class="window-note">` +
    `<span>${scope} · <strong>${gradedToday}</strong> graded today</span>${toggle}</div>`
  );
}

// The plain shape selection.js expects, with a back-reference to the problem.
function dueCandidates(problems) {
  return problems.map((p) => {
    const st = prog(p);
    return { key: id(p), cat: p.cat, box: st.box, daysUntil: daysUntil(st.due), problem: p };
  });
}

function renderList() {
  if (VIEW === "help") {
    listEl.innerHTML = HELP_HTML;
    return;
  }
  if (VIEW === "sprint") {
    renderSprintList();
    return;
  }

  const items = visibleProblems();

  if (VIEW === "due") {
    const candidates = dueCandidates(items);

    let picked;
    if (SHOW_ALL) {
      picked = candidates.slice().sort(comparePriority);
    } else if (CAT_FILTER === "all") {
      picked = selectWindow(candidates, WINDOW_SIZE);
    } else {
      // Tier quotas are meaningless inside a single category — just cap.
      picked = candidates.slice().sort(comparePriority).slice(0, WINDOW_SIZE);
    }

    const done = PROBLEMS
      .filter((p) => (CAT_FILTER === "all" || p.cat === CAT_FILTER) && isDoneToday(p))
      .sort((a, b) => catRank(a.cat) - catRank(b.cat) || a.n - b.n);

    const body = picked.length
      ? picked.map((x) => rowHTML(x.problem, { hideCat: true })).join("")
      : `<p class="empty">${emptyMessage()}</p>`;
    const reps = windowNoteHTML(picked.length, candidates.length) + body;

    // A filtered view is a focused drill, not the daily plan.
    listEl.innerHTML =
      (CAT_FILTER === "all" ? todayCardHTML(reps) : reps) + doneSectionHTML(done);
    return;
  }

  if (items.length === 0) {
    listEl.innerHTML = `<p class="empty">${emptyMessage()}</p>`;
    return;
  }

  // "new" / "all": group by category.
  const groups = {};
  for (const p of items) (groups[p.cat] ||= []).push(p);
  const cats = Object.keys(groups).sort((a, b) => {
    const ca = CORE.has(a) ? 0 : 1, cb = CORE.has(b) ? 0 : 1;
    if (ca !== cb) return ca - cb;
    return catRank(a) - catRank(b);
  });

  listEl.innerHTML = cats
    .map((c) => {
      const rows = groups[c].sort((a, b) => a.n - b.n).map(rowHTML).join("");
      const coreTag = CORE.has(c) ? '<span class="core-tag">core</span>' : "";
      return (
        `<div class="group__head"><h2>${CAT_META[c].glyph} ${CAT_META[c].label}</h2>` +
        `${coreTag}<span class="group__count">${groups[c].length}</span></div>` +
        rows
      );
    })
    .join("");
}

/* The order rule lives in selection.js. Catalog order is PROBLEMS order, so
 * "the first unstarted problem" means the same thing in both files. */
function suggestNewProblem() {
  const catalog = PROBLEMS.map((p) => ({
    key: id(p), cat: p.cat, started: p.s || prog(p).box >= 1, problem: p,
  }));
  const pick = pickNewProblem(catalog);
  return pick ? pick.problem : null;
}

/* The day in PRACTICE.md order: the floor first (one quick rep keeps the
 * streak), then the reps, then growth. Growth lives here, not only in the New
 * tab, because a step you have to remember is a step that stops happening. */
function todayCardHTML(repsHTML) {
  const today = todayISO();
  const quickDone = Object.values(STATE).some((s) => s && s.kind === "quick" && s.last === today);
  return (
    `<section class="today">` +
      `<div class="today__step${quickDone ? " is-done" : ""}">` +
        `<span class="today__num">${quickDone ? "✓" : "1"}</span>` +
        `<span>Start with a quick rep: run <code>/quick-rep</code> in Claude Code (10 min)</span>` +
      `</div>` +
      `<div class="today__step"><span class="today__num">2</span><span>Reps</span></div>` +
      repsHTML +
      newStepHTML() +
    `</section>`
  );
}

/* Step 3. The quota is weekly, so a missed day moves nothing. A third problem
 * is a stretch, not the target, and past it the week is done: more new
 * problems would starve the reps that keep the first ones. */
function newStepHTML() {
  const n = thisWeek().newCount;
  let status = `this week: ${n}/${NEW_PER_WEEK}`;
  if (n >= NEW_STRETCH) status += " · week done";
  else if (n >= NEW_PER_WEEK) status += " · stretch";

  const head =
    `<div class="today__step today__step--new">` +
      `<span class="today__num">3</span><span>New problem</span>` +
      `<span class="group__count">${status}</span>` +
    `</div>`;
  if (n >= NEW_STRETCH) return head;

  const p = suggestNewProblem();
  if (!p) return head + `<p class="grow__hint">Every problem is started 🎉</p>`;
  return (
    head +
    rowHTML(p, { hideCat: true }) +
    `<p class="grow__hint">60-minute cap. If it does not land, grade it <strong>Failed</strong>: ` +
    `it joins the rotation tomorrow, and that is a finished session.</p>`
  );
}

/* Problems graded today, kept on screen so the trigger sentence stays reachable
 * after grading instead of disappearing with the row. */
function doneSectionHTML(done) {
  if (!done.length) return "";
  const withNotes = done.filter((p) => (prog(p).trigger || "").trim()).length;
  const missing = done.length - withNotes;
  const count = missing
    ? `${done.length} · <span class="done__missing">${missing} without a note</span>`
    : `${done.length} · all noted`;
  return (
    `<div class="group__head done__head">` +
      `<h2>✓ Done today</h2><span class="group__count">${count}</span>` +
    `</div>` +
    done.map(rowHTML).join("")
  );
}

function emptyMessage() {
  if (VIEW === "due")
    return CAT_FILTER === "all"
      ? "Nothing due today. 🎉 Step 3 below has a new problem, or come back tomorrow."
      : "Nothing due in this category today.";
  if (VIEW === "new") return "No new problems left in this filter — you've started them all.";
  return "No problems match this filter.";
}

/* `hideCat`: the Due window hides the category until the problem is graded
 * today, because spotting the pattern is part of the rep. The file path in
 * the panel names the category too, so it hides with it. */
function rowHTML(p, opts) {
  const st = prog(p);
  const pid = id(p);
  const open = pid === OPEN_ID ? " is-open" : "";
  const solved = p.s ? " is-solved" : "";
  const doneToday = isDoneToday(p);
  const doneCls = doneToday ? " is-done" : "";
  const hideCat = !!(opts && opts.hideCat) && !doneToday;
  const cat = doneToday
    ? `<span class="row__cat">${CAT_META[p.cat].glyph} ${CAT_META[p.cat].label}</span>`
    : "";

  let meta = "";
  if (doneToday) {
    const g = gradeOf(st.box);
    const noteCls = (st.trigger || "").trim() ? "" : " needs-note";
    meta =
      `<span class="row__meta is-graded${noteCls}">` +
      `${g ? g.label : "graded"} · next in ${daysUntil(st.due)}d` +
      `${noteCls ? " · no note yet" : ""}</span>`;
  } else if (st.box === 0) {
    meta = '<span class="row__meta">new</span>';
  } else {
    const d = daysUntil(st.due);
    let cls = "row__meta", txt;
    if (d < 0) { cls += " is-overdue"; txt = `${-d}d overdue`; }
    else if (d === 0) { cls += " is-due"; txt = "due today"; }
    else { txt = `in ${d}d`; }
    meta = `<span class="${cls}">box ${st.box} · ${txt}</span>`;
  }

  return (
    `<div class="row box-${st.box}${open}${solved}${doneCls}" data-id="${pid}">` +
      `<div class="row__top">` +
        `<span class="row__box"></span>` +
        `<span class="row__num">${p.n}</span>` +
        `<span class="row__title">${p.title}</span>` +
        `${cat}${meta}` +
      `</div>` +
      `<div class="row__panel">${panelHTML(p, st, hideCat)}</div>` +
    `</div>`
  );
}

/* Sub-labels and intervals describe what THIS click would do. A re-grade
 * starts from the entry as it was before today's first grade, exactly as
 * gradeProblem() does, so the Fast interval shown is the one you get. */
function panelHTML(p, st, hideCat) {
  const gradedToday = isDoneToday(p);
  const { base } = regradeBase(st, BEFORE_TODAY[id(p)], todayISO());
  const kind = gradeKind(base);
  const grades = GRADES.map((g) => {
    const days = INTERVAL[nextBox(base.box, g.box, kind)];
    const chosen = gradedToday && g.box === Math.min(st.box, 4) ? " is-chosen" : "";
    return (
      `<button class="grade ${g.cls}${chosen}" data-grade="${g.box}">` +
      `${g.label}<small>${g[kind]} · +${days}d</small></button>`
    );
  }).join("");

  let src = `<p class="history">No local file yet — this is a fresh problem.</p>`;
  if (p.f && hideCat) src = `<p class="history">📄 file path shows after you grade it</p>`;
  else if (p.f) src = `<p class="history">📄 <code>${p.f}</code></p>`;

  const hist =
    st.attempts > 0
      ? `<p class="history">Attempts: ${st.attempts}${st.last ? ` · last reviewed ${st.last}` : ""}</p>`
      : "";

  const triggerBlock = (label) => triggerBlockHTML(label, st.trigger);

  // After grading, the note prompt comes FIRST and the panel stays open — the
  // old flow put it below the grade buttons, which dismissed the panel, so it
  // was unreachable in normal use (56 of 57 problems ended up with no note).
  if (gradedToday) {
    const g = gradeOf(st.box);
    return (
      `<p class="panel__confirm">✓ Graded <strong>${g ? g.label : "?"}</strong>` +
      ` · next review in ${daysUntil(st.due)} days</p>` +
      triggerBlock("Before you close this — what tipped you off to the pattern?") +
      `<button class="close-panel" data-close>done, close it</button>` +
      `<p class="panel__label panel__regrade">Graded it wrong? Change it</p>` +
      `<div class="grades">${grades}</div>` +
      src +
      hist
    );
  }

  return (
    `<p class="panel__label">Grade your attempt (solve it blind first)</p>` +
    `<div class="grades">${grades}</div>` +
    (hideCat
      ? ((st.trigger || "").trim() ? `<p class="history">📝 your note shows after you grade</p>` : "")
      : triggerBlock("Trigger sentence — what tips you off to the pattern?")) +
    src +
    hist
  );
}

/* Shared by the catalog panel and the sprint panel. The note field is the one
 * piece of the review flow the sprint keeps, because the trigger sentence is
 * what survives past the test. */
function triggerBlockHTML(label, value) {
  return (
    `<div class="trigger">` +
      `<p class="panel__label">${label}</p>` +
      `<textarea data-trigger placeholder="e.g. 'sorted array + find a pair → two pointers from both ends'">${escapeHTML(value || "")}</textarea>` +
      `<p class="trigger__hint">This one sentence is what transfers to new problems. Saved automatically.</p>` +
    `</div>`
  );
}

/* ---------- sprint view ----------
 * A flat checklist, every day always visible: a problem from Tuesday is still
 * fair game on Friday, so nothing is collapsed or filtered away.
 */
function sprintNoteHTML() {
  const done = SPRINT.filter((s) => sprog(s).status === "done").length;
  return (
    `<div class="window-note sprint-note">` +
      `<span><strong>${done}</strong> of ${SPRINT.length} covered · ` +
      `${SPRINT_META.format}</span>` +
      `<span class="sprint-note__tip">${SPRINT_META.order}</span>` +
    `</div>`
  );
}

function renderSprintList() {
  // Empty between interviews. The tab stays so the next problem list has a
  // home; sprint.js documents the three constants to fill in.
  if (SPRINT.length === 0) {
    listEl.innerHTML = SPRINT_EMPTY_HTML;
    return;
  }

  const sections = SPRINT_GROUPS.map((grp) => {
    // Set first, then essential-first, so the list reads top-down as "do these,
    // then these". The simulation group is a timed run of ONE set — sorting by
    // priority alone would interleave A and B and scramble that grouping.
    const items = SPRINT.filter((s) => s.g === grp.g).sort(
      (a, b) =>
        (a.set || "").localeCompare(b.set || "") || PRI_RANK[a.pri] - PRI_RANK[b.pri]
    );
    const done = items.filter((s) => sprog(s).status === "done").length;
    const complete = done === items.length ? " is-complete" : "";

    return (
      `<div class="group__head day__head${complete}">` +
        `<h2>Day ${grp.g} · ${grp.label}</h2>` +
        `<span class="group__count">${done}/${items.length}</span>` +
      `</div>` +
      items.map((s, i) => sprintRowHTML(s, i + 1)).join("")
    );
  }).join("");

  listEl.innerHTML = sprintNoteHTML() + sections;
}

function sprintRowHTML(s, n) {
  const st = sprog(s);
  const key = sid(s);
  const open = key === OPEN_ID ? " is-open" : "";
  const twin = s.maps ? PROBLEM_BY_ID[s.maps] : null;
  const status = st.status || "none";
  const hasNote = (st.trigger || "").trim() !== "";

  let meta = "";
  if (status === "done") {
    meta = `<span class="row__meta is-graded${hasNote ? "" : " needs-note"}">` +
           `done${hasNote ? "" : " · no note yet"}</span>`;
  } else if (status === "stuck") {
    meta = '<span class="row__meta is-overdue">stuck</span>';
  } else if (status === "skipped") {
    meta = '<span class="row__meta">skipped</span>';
  } else if (twin && twin.s) {
    meta = '<span class="row__meta is-due">already solved</span>';
  }

  const setTag = s.set ? `<span class="set-tag">set ${s.set}</span> ` : "";

  return (
    `<div class="row row--sprint st-${status}${open}" data-id="${key}">` +
      `<div class="row__top">` +
        `<span class="row__box"></span>` +
        `<span class="row__num">${n}</span>` +
        `<span class="prio prio--${s.pri}">${s.pri}</span>` +
        `<span class="row__title">${setTag}${s.title}</span>` +
        `${meta}` +
      `</div>` +
      `<div class="row__panel">${sprintPanelHTML(s, st)}</div>` +
    `</div>`
  );
}

function sprintPanelHTML(s, st) {
  const buttons = SPRINT_STATUS.map(
    (g) =>
      `<button class="grade ${g.cls}${st.status === g.key ? " is-chosen" : ""}" ` +
      `data-status="${g.key}">${g.label}<small>${g.sub}</small></button>`
  ).join("");

  const twin = s.maps ? PROBLEM_BY_ID[s.maps] : null;
  let twinLine = "";
  if (twin && twin.s) {
    twinLine = `<p class="history">✓ already in the tracker · <code>${twin.f}</code></p>`;
  } else if (twin) {
    twinLine = `<p class="history">in the AlgoMap catalog under ${CAT_META[twin.cat].label}, not solved yet</p>`;
  }

  return (
    `<p class="panel__label">Mark it — no box, no due date, nothing enters your review queue</p>` +
    `<div class="grades">${buttons}</div>` +
    triggerBlockHTML("Trigger sentence — what tips you off to the pattern?", st.trigger) +
    `<p class="history">🔗 <a href="${s.url}" target="_blank" rel="noopener">open on LeetCode</a></p>` +
    `<p class="history">📄 put your solution in <code>${sprintFilePath(s)}</code></p>` +
    twinLine
  );
}

/* Clicking the active status clears it, so a mis-click is one click to undo. */
function setSprintStatus(pid, status) {
  const cur = STATE[pid] || { status: null, trigger: "" };
  cur.status = cur.status === status ? null : status;
  STATE[pid] = cur;
  saveState({ immediate: true }); // discrete event — never debounce it
  OPEN_ID = pid;
  FOCUS_TRIGGER = true;
  render();
}

function escapeHTML(s) {
  // String() because this reads straight out of progress.json: one hand-edited
  // `"trigger": 3` used to throw here and leave the whole list permanently blank.
  return String(s ?? "").replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

const SPRINT_EMPTY_HTML = `
<div class="help">
  <h2>No sprint loaded</h2>
  <p>This tab holds a <strong>one-off problem list</strong> that comes with a specific interview — a take-home plan, a screen's prep sheet, a recruiter's topic list. It is a checklist with memory: mark each problem <strong>Done</strong>, <strong>Stuck</strong>, or <strong>Skipped</strong>, and write the trigger sentence. Nothing here gets a box or a due date, so it never touches <strong>Due today</strong>.</p>
  <h3>To load the next one</h3>
  <ul>
    <li>Open <code>apps/prep-tracker/sprint.js</code> — the header documents all three constants.</li>
    <li>Fill in <code>SPRINT_META</code> (the test's shape), <code>SPRINT_GROUPS</code> (the day chunks), and <code>SPRINT</code> (the problems).</li>
    <li>Tag each problem <span style="color:#4fe0c0">essential</span>, <span style="color:#6c9cff">stretch</span>, or <span style="color:#3a4654">optional</span>. A list that does not fit is normal — the tag is what you cut.</li>
    <li>Reload. The tab wakes up.</li>
  </ul>
  <h3>The last one</h3>
  <p>The 2026-08 assessment ran 39 problems across 9 days. All 39 were merged into the main catalog on 2026-08-21, so they are in the normal rotation now — look for them in <strong>All</strong>, including the new <strong>Greedy &amp; Intervals</strong> and <strong>Sorting</strong> categories.</p>
</div>`;

const HELP_HTML = `
<div class="help">
  <h2>How this tracker works</h2>
  <p>Two evidence-backed techniques run this: <strong>active recall</strong> (solve blind — struggling is the learning) and <strong>spaced repetition</strong> (revisit each problem at growing intervals, right before you'd forget it).</p>

  <p>The rules (rep types, how to grade, boxes, the order of new problems) live in <code>PRACTICE.md</code> at the repo root. This page is the short version.</p>

  <h3>The Today card</h3>
  <ul>
    <li><strong>1. Quick rep.</strong> Run <code>/quick-rep</code> in Claude Code (10 min). It ticks itself when a quick-rep grade lands today. On a rough day this alone is a win.</li>
    <li><strong>2. Reps.</strong> Up to 3 problems from the schedule. Solve each <em>blind</em>, then click it and <strong>grade honestly</strong>. The category stays hidden until you grade: spotting the pattern is part of the rep.</li>
    <li><strong>3. New problem.</strong> The next one in the PRACTICE.md order. Target 2 a week, a 3rd is a stretch, then the week is done.</li>
    <li>Write the <strong>trigger sentence</strong> after each grade — the cue that unlocks the pattern. That's the part that transfers.</li>
  </ul>
  <p>The stat strip shows the week (Monday to Sunday), not the backlog: new problems started and reps graded. <strong>Show all</strong> in the Due tab still lists the whole backlog.</p>

  <h3>The Leitner boxes</h3>
  <table>
    <tr><th>Grade</th><th>Box</th><th>Next review</th></tr>
    <tr><td><span class="dot" style="background:#f4726a"></span>Failed</td><td>1</td><td>tomorrow</td></tr>
    <tr><td><span class="dot" style="background:#f4b942"></span>Slow / hints</td><td>2</td><td>3 days</td></tr>
    <tr><td><span class="dot" style="background:#4fe0c0"></span>Clean</td><td>3</td><td>1 week</td></tr>
    <tr><td><span class="dot" style="background:#6c9cff"></span>Fast</td><td>4</td><td>3 weeks</td></tr>
    <tr><td><span class="dot" style="background:#b48cff"></span>Fast again from box 4</td><td>5</td><td>45 days</td></tr>
    <tr><td><span class="dot" style="background:#e8d48a"></span>Fast again from box 5</td><td>6</td><td>120 days</td></tr>
  </table>
  <p>You never pick box 5 or 6: Fast climbs one box at a time from box 4, and any other grade sets that grade's box. A quick rep can hold box 6 but never earn it.</p>

  <h3>Quick-rep grades from the terminal</h3>
  <p><code>python3 apps/prep-tracker/grade.py &lt;key&gt; pass|fail [--date YYYY-MM-DD]</code> records a quick-rep result, for example <code>grade.py two_pointers#3 pass</code>. It writes through the running server when there is one, else straight to the file. This tab picks the change up when you come back to it.</p>

  <h3>The mix</h3>
  <p>Your solved problems (📄 = a file already exists in this repo) were seeded into rotation and staggered so only ~3 come due per day — that's your <strong>retention</strong> work. Drip in a new problem whenever you have appetite — that's your <strong>growth</strong>. Weak buckets (red/amber) always sort to the top so you face them first.</p>

  <h3>The Sprint tab</h3>
  <p>A separate track for a specific interview: the 39-problem plan that came with the assessment invite, grouped into 9 days. It is a <strong>checklist with memory</strong>, not a second scheduler — no boxes, no due dates, no calendar, and nothing there ever appears in <strong>Due today</strong>. The day numbers are labels for chunks of the list, so falling a day behind costs you nothing.</p>
  <ul>
    <li>Mark each one <strong>Done</strong>, <strong>Stuck</strong>, or <strong>Skipped</strong>. Click the active one again to clear it.</li>
    <li>The trigger sentence works exactly as it does here, and it survives the merge.</li>
    <li><span style="color:#4fe0c0">essential</span> = do it · <span style="color:#6c9cff">stretch</span> = if the day runs short · <span style="color:#3a4654">optional</span> = reference only. Skipping an optional is the plan working, not a failure.</li>
    <li><strong>Reset all</strong> does not touch the sprint.</li>
  </ul>
  <p>After the test, the keepers get folded into the main catalog and join this rotation. See <em>Merging the sprint back in</em> in the README.</p>

  <p style="color:#7f8c9b">Retention here stays at ~30–60 min/day. The sprint is the thing with a clock on it.</p>
</div>`;

/* ---------- events ---------- */
document.getElementById("tabs").addEventListener("click", (e) => {
  const t = e.target.closest(".tab");
  if (!t) return;
  VIEW = t.dataset.view;
  OPEN_ID = null;
  render();
});

filterEl.addEventListener("click", (e) => {
  const c = e.target.closest(".chip");
  if (!c) return;
  CAT_FILTER = c.dataset.cat;
  render();
});

listEl.addEventListener("click", (e) => {
  // Halt-panel actions first: while halted, nothing else in the list is real.
  if (e.target.id === "haltExport") { exportProgress(); return; }
  if (e.target.id === "haltReload") { location.reload(); return; }
  if (e.target.id === "haltMerge") { resolveLocalAhead("merge"); return; }
  if (e.target.id === "haltDiscard") { resolveLocalAhead("discard"); return; }
  // window size toggle?
  if (e.target.id === "windowToggle") {
    SHOW_ALL = !SHOW_ALL;
    render();
    return;
  }
  // "done, close it"? Must run before the row toggle below, or the row would
  // just reopen on the same click.
  if (e.target.closest("[data-close]")) {
    OPEN_ID = null;
    render();
    return;
  }
  // sprint status button? Checked before .grade — sprint buttons reuse the
  // .grade class for styling but carry data-status instead of data-grade.
  const sb = e.target.closest("[data-status]");
  if (sb) {
    setSprintStatus(sb.closest(".row").dataset.id, sb.dataset.status);
    e.stopPropagation();
    return;
  }
  // grade button?
  const g = e.target.closest(".grade");
  if (g) {
    const row = g.closest(".row");
    gradeProblem(row.dataset.id, Number(g.dataset.grade));
    e.stopPropagation();
    return;
  }
  // A link inside a panel (the LeetCode button) must not collapse the row out
  // from under the click.
  if (e.target.closest("a")) return;
  // toggle open?
  const row = e.target.closest(".row");
  if (!row) return;
  if (e.target.closest(".trigger")) return; // don't toggle when interacting with textarea
  OPEN_ID = OPEN_ID === row.dataset.id ? null : row.dataset.id;
  render();
});

listEl.addEventListener("input", (e) => {
  const ta = e.target.closest("[data-trigger]");
  if (!ta) return;
  const row = ta.closest(".row");
  const pid = row.dataset.id;
  STATE[pid] = STATE[pid] || { box: 0, due: null, last: null, attempts: 0, trigger: "" };
  STATE[pid].trigger = ta.value;
  saveState();

  // Keep the row's "no note yet" warning honest as you type. A full render()
  // here would destroy the textarea and drop the cursor mid-sentence, so patch
  // the one element instead. Both row kinds end their meta the same way.
  const meta = row.querySelector(".row__meta.is-graded");
  if (meta) {
    const hasNote = ta.value.trim() !== "";
    meta.classList.toggle("needs-note", !hasNote);
    meta.textContent = meta.textContent.replace(/ · no note yet$/, "");
    if (!hasNote) meta.textContent += " · no note yet";
  }
});

function gradeProblem(pid, grade) {
  const today = todayISO();
  const cur = STATE[pid] || { box: 0, due: null, last: null, attempts: 0, trigger: "" };
  const { base, snapshot } = regradeBase(cur, BEFORE_TODAY[pid], today);
  BEFORE_TODAY[pid] = snapshot;
  STATE[pid] = {
    ...applyGrade(base, grade, today, (box) => addDays(today, INTERVAL[box])),
    trigger: cur.trigger || "",
  };
  saveState({ immediate: true }); // a grade is one discrete event — never debounce it
  // Stay open. The row relocates to "Done today" and keeps the note prompt on
  // screen; FOCUS_TRIGGER makes render() put the cursor in it.
  OPEN_ID = pid;
  FOCUS_TRIGGER = true;
  render();
}

document.getElementById("resetBtn").addEventListener("click", () => {
  if (!confirm("Reset ALL progress? This clears every box, due date, and trigger note.\n\nYour Sprint checklist is KEPT — it has a deadline and no way to rebuild itself.")) return;
  // Preserve the sprint. Wiping Leitner state is a recoverable annoyance;
  // wiping a mid-flight sprint days before a real test is not.
  const kept = {};
  for (const k of Object.keys(STATE)) if (isSprintKey(k)) kept[k] = STATE[k];
  STATE = kept;
  // Debounced on purpose: seedIfNeeded() below saves immediately, and its
  // clearTimeout cancels this empty write so only the seeded state is posted.
  saveState();
  seedIfNeeded();
  OPEN_ID = null;
  render();
});

document.getElementById("exportBtn").addEventListener("click", exportProgress);

/* Footer status. `ok: false` means a POST to the repo file failed, which is
 * worth shouting about — it's the difference between "saved" and "only in this
 * browser". */
function setFootNote(ok, kind) {
  const note = document.querySelector(".foot__note");
  if (!note) return;
  if (kind === "storage") {
    note.className = "foot__note is-error";
    note.textContent =
      "⚠ This browser refused to save (storage full or blocked) — export now; nothing is being kept.";
    return;
  }
  if (!SERVER_MODE) {
    note.className = "foot__note is-warn";
    note.textContent =
      "⚠ Offline mode (localStorage only). Run server.py to make the repo the source of truth.";
  } else if (ok) {
    note.className = "foot__note";
    note.textContent =
      "✓ Saving to apps/prep-tracker/progress.json — commit it to sync across machines.";
  } else {
    note.className = "foot__note is-error";
    note.textContent =
      "⚠ Save to progress.json FAILED — changes are in this browser only. Is server.py still running?";
  }
}

/* ---------- go ---------- */
async function init() {
  STATE = await loadProgress();
  seedIfNeeded();
  render();
  setFootNote(true);
}
init();
