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
 *   box 4  fast & confident           -> review in 21 days   (mastered)
 *   box 0  never attempted (new)      -> not scheduled
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
  { cat: "arrays_and_strings", n: 5,  title: "Best Time to Buy and Sell Stock", s: false },
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

// Leitner intervals (days) keyed by box.
const INTERVAL = { 1: 1, 2: 3, 3: 7, 4: 21 };
// Sub-labels are anchored to the time-box protocol in CLAUDE.md so that
// self-grading is a measurement rather than a mood.
const GRADES = [
  { box: 1, cls: "g1", label: "Failed",  sub: "hit the cap / read the solution · +1d" },
  { box: 2, cls: "g2", label: "Slow",    sub: "needed a hint, or >40 min · +3d" },
  { box: 3, cls: "g3", label: "Clean",   sub: "solved unaided, under ~30 min · +7d" },
  { box: 4, cls: "g4", label: "Fast",    sub: "under ~15 min, no stumbles · +21d" },
];
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
function sprintFilePath(s) {
  return `sprint/${SPRINT_GROUP_BY_N[s.g].dir}/${s.slug.replace(/-/g, "_")}.py`;
}

/* ---------- persistence ----------
 * Two modes:
 *  - SERVER MODE: opened via server.py. Progress is read from and written back to
 *    prep-tracker/progress.json in this repo — the repo is the source of truth,
 *    so `git pull` on any machine resumes your progress. localStorage mirrors it as a cache.
 *  - OFFLINE MODE: opened via file:// (no server). Falls back to localStorage only.
 */
const API = "api/progress";
let SERVER_MODE = false;
let saveTimer = null;

function loadLocal() {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY)) || {};
  } catch (_) {
    return {};
  }
}

async function loadProgress() {
  try {
    const r = await fetch(API, { cache: "no-store" });
    if (r.ok) {
      SERVER_MODE = true;
      const data = await r.json();
      return data && typeof data === "object" ? data : {};
    }
  } catch (_) {
    /* no server — fall through to offline mode */
  }
  SERVER_MODE = false;
  return loadLocal();
}

function postState() {
  saveTimer = null;
  return fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(STATE),
  })
    .then((r) => {
      if (!r.ok) throw new Error("HTTP " + r.status);
      setFootNote(true);
    })
    // Previously `.catch(() => {})` — a dead server meant every grade looked
    // saved and silently wasn't. You'd only find out at `git status`, or never.
    .catch(() => setFootNote(false));
}

/* `immediate` skips the debounce. Only textarea typing needs debouncing;
 * grading and reset are single discrete events, and debouncing them means a
 * reload within 400ms loses the write — after which the next server-mode load
 * overwrites localStorage with the stale file and the grade is gone for good. */
function saveState(opts) {
  // Always mirror locally so an offline reload still has the latest.
  try { localStorage.setItem(STORE_KEY, JSON.stringify(STATE)); } catch (_) {}
  if (!SERVER_MODE) return;
  clearTimeout(saveTimer);
  if (opts && opts.immediate) {
    postState();
    return;
  }
  saveTimer = setTimeout(postState, 400);
}

/* A pending debounced write would be lost on reload/close. Flush it with
 * sendBeacon, which survives teardown where fetch does not. */
window.addEventListener("beforeunload", () => {
  if (!SERVER_MODE || !saveTimer) return;
  clearTimeout(saveTimer);
  saveTimer = null;
  navigator.sendBeacon(
    API,
    new Blob([JSON.stringify(STATE)], { type: "application/json" })
  );
});

/* Seed any solved problem that has no progress yet: put it in box 2 with a
 * staggered due date so the initial review load is ~NEW_PER_DAY_SEED per day.
 * Idempotent — only touches problems missing an entry, so it also picks up
 * newly-added solved problems on later loads. */
function seedIfNeeded() {
  const solved = PROBLEMS.filter((p) => p.s).sort((a, b) => {
    const ca = CORE.has(a.cat) ? 0 : 1;
    const cb = CORE.has(b.cat) ? 0 : 1;
    if (ca !== cb) return ca - cb;
    if (catRank(a.cat) !== catRank(b.cat)) return catRank(a.cat) - catRank(b.cat);
    return a.n - b.n;
  });
  const today = todayISO();
  let seeded = false;
  solved.forEach((p, i) => {
    // Guard on box, NOT on presence. Typing a trigger note creates a box-0
    // entry (see the "input" handler), so a presence check would permanently
    // exclude any problem you'd jotted a note on before solving it — it would
    // never get a due date and never enter the rotation.
    const existing = STATE[id(p)];
    if (existing && existing.box > 0) return;
    STATE[id(p)] = {
      box: 2,
      due: addDays(today, Math.floor(i / NEW_PER_DAY_SEED)),
      last: null,
      attempts: 0,
      trigger: (existing && existing.trigger) || "", // keep any note already written
    };
    seeded = true;
  });
  if (seeded) saveState({ immediate: true });
}

/* ---------- app state ---------- */
let STATE = {};
let VIEW = "due";
let CAT_FILTER = "all";
let OPEN_ID = null;
let SHOW_ALL = false; // session-only Due-view override; not persisted
let FOCUS_TRIGGER = false; // one-shot: focus the note field after the next render

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

function renderStats() {
  const dueCount = PROBLEMS.filter(isDue).length;
  const solvedCount = PROBLEMS.filter((p) => p.s).length;
  const coreTotal = PROBLEMS.filter((p) => CORE.has(p.cat)).length;
  const coreSolved = PROBLEMS.filter((p) => CORE.has(p.cat) && p.s).length;
  const mastered = PROBLEMS.filter((p) => prog(p).box === 4).length;
  const sprintDone = SPRINT.filter((s) => sprog(s).status === "done").length;

  dueBadge.textContent = dueCount;
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

  statsEl.innerHTML = [
    stat("due", dueCount, "due today"),
    stat("solved", `${solvedCount}/${PROBLEMS.length}`, "solved locally"),
    stat("core", `${coreSolved}/${coreTotal}`, "core solved"),
    stat("", mastered, "mastered (box 4)"),
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
  else if (VIEW === "new") items = items.filter((p) => !p.s && prog(p).box === 0);
  // "all" => everything
  if (CAT_FILTER !== "all") items = items.filter((p) => p.cat === CAT_FILTER);
  return items;
}

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

    const done = PROBLEMS
      .filter((p) => (CAT_FILTER === "all" || p.cat === CAT_FILTER) && isDoneToday(p))
      .sort((a, b) => catRank(a.cat) - catRank(b.cat) || a.n - b.n);

    const body = picked.length
      ? picked.map((x) => rowHTML(x.problem)).join("")
      : `<p class="empty">${emptyMessage()}</p>`;

    listEl.innerHTML =
      windowNoteHTML(picked.length, candidates.length) + body + doneSectionHTML(done);
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
      ? "Nothing due today. 🎉 Pull a fresh problem from the New tab, or come back tomorrow."
      : "Nothing due in this category today.";
  if (VIEW === "new") return "No new problems left in this filter — you've started them all.";
  return "No problems match this filter.";
}

function rowHTML(p) {
  const st = prog(p);
  const pid = id(p);
  const open = pid === OPEN_ID ? " is-open" : "";
  const solved = p.s ? " is-solved" : "";
  const doneToday = isDoneToday(p);
  const doneCls = doneToday ? " is-done" : "";

  let meta = "";
  if (doneToday) {
    const g = GRADES.find((x) => x.box === st.box);
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
        `${meta}` +
      `</div>` +
      `<div class="row__panel">${panelHTML(p, st)}</div>` +
    `</div>`
  );
}

function panelHTML(p, st) {
  const gradedToday = isDoneToday(p);
  const grades = GRADES.map(
    (g) =>
      `<button class="grade ${g.cls}${gradedToday && g.box === st.box ? " is-chosen" : ""}" ` +
      `data-grade="${g.box}">${g.label}<small>${g.sub}</small></button>`
  ).join("");

  const src = p.f
    ? `<p class="history">📄 <code>${p.f}</code></p>`
    : `<p class="history">No local file yet — this is a fresh problem.</p>`;

  const hist =
    st.attempts > 0
      ? `<p class="history">Attempts: ${st.attempts}${st.last ? ` · last reviewed ${st.last}` : ""}</p>`
      : "";

  const triggerBlock = (label) => triggerBlockHTML(label, st.trigger);

  // After grading, the note prompt comes FIRST and the panel stays open — the
  // old flow put it below the grade buttons, which dismissed the panel, so it
  // was unreachable in normal use (56 of 57 problems ended up with no note).
  if (gradedToday) {
    const g = GRADES.find((x) => x.box === st.box);
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
    triggerBlock("Trigger sentence — what tips you off to the pattern?") +
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
  return s.replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

const SPRINT_EMPTY_HTML = `
<div class="help">
  <h2>No sprint loaded</h2>
  <p>This tab holds a <strong>one-off problem list</strong> that comes with a specific interview — a take-home plan, a screen's prep sheet, a recruiter's topic list. It is a checklist with memory: mark each problem <strong>Done</strong>, <strong>Stuck</strong>, or <strong>Skipped</strong>, and write the trigger sentence. Nothing here gets a box or a due date, so it never touches <strong>Due today</strong>.</p>
  <h3>To load the next one</h3>
  <ul>
    <li>Open <code>prep-tracker/sprint.js</code> — the header documents all three constants.</li>
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

  <h3>The daily loop</h3>
  <ul>
    <li>Open the <strong>Due today</strong> tab. These are the problems the schedule wants you to revisit.</li>
    <li>Pick one, open your editor, and solve it <em>from scratch</em> — no peeking. Time-box ~25 min.</li>
    <li>Come back, click the problem, and <strong>grade honestly</strong>. The grade sets when you see it next.</li>
    <li>Write the <strong>trigger sentence</strong> — the cue that unlocks the pattern. That's the part that transfers.</li>
    <li>When the due list is short, pull one from <strong>New</strong> (core categories are marked <span style="color:#6c9cff">★</span>).</li>
  </ul>

  <h3>The Leitner boxes</h3>
  <table>
    <tr><th>Grade</th><th>Box</th><th>Next review</th></tr>
    <tr><td><span class="dot" style="background:#f4726a"></span>Failed</td><td>1</td><td>tomorrow</td></tr>
    <tr><td><span class="dot" style="background:#f4b942"></span>Slow / hints</td><td>2</td><td>3 days</td></tr>
    <tr><td><span class="dot" style="background:#4fe0c0"></span>Clean</td><td>3</td><td>1 week</td></tr>
    <tr><td><span class="dot" style="background:#6c9cff"></span>Fast</td><td>4</td><td>3 weeks (mastered)</td></tr>
  </table>

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
  <p>After the test, the keepers get folded into the 100-problem catalog and join this rotation. See <em>Merging the sprint back in</em> in the README.</p>

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

function gradeProblem(pid, box) {
  const today = todayISO();
  const cur = STATE[pid] || { box: 0, due: null, last: null, attempts: 0, trigger: "" };
  STATE[pid] = {
    box,
    due: addDays(today, INTERVAL[box]),
    last: today,
    attempts: cur.attempts + 1,
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

document.getElementById("exportBtn").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(STATE, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "dsa-prep-progress.json";
  a.click();
  URL.revokeObjectURL(url);
});

/* Footer status. `ok: false` means a POST to the repo file failed, which is
 * worth shouting about — it's the difference between "saved" and "only in this
 * browser". */
function setFootNote(ok) {
  const note = document.querySelector(".foot__note");
  if (!note) return;
  if (!SERVER_MODE) {
    note.className = "foot__note is-warn";
    note.textContent =
      "⚠ Offline mode (localStorage only). Run server.py to make the repo the source of truth.";
  } else if (ok) {
    note.className = "foot__note";
    note.textContent =
      "✓ Saving to prep-tracker/progress.json — commit it to sync across machines.";
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
