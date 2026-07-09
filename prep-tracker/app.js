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

const CORE = new Set([
  "arrays_and_strings",
  "hashmaps_and_sets",
  "two_pointers",
  "sliding_window",
]);

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
};

// Category display order (core first, then roadmap order).
const CAT_ORDER = [
  "arrays_and_strings", "hashmaps_and_sets", "two_pointers", "sliding_window",
  "stacks", "linked_lists", "binary_search", "trees", "heaps",
  "backtracking", "graphs", "dp",
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

  // ---- 2 Pointers ----
  { cat: "two_pointers", n: 1, title: "Squares of a Sorted Array",           s: true,  f: "patterns/two_pointers/squares_of_sorted_arr.py" },
  { cat: "two_pointers", n: 2, title: "Reverse String",                      s: true,  f: "patterns/two_pointers/reverse_string.py" },
  { cat: "two_pointers", n: 3, title: "Two Sum II - Input Array Is Sorted",  s: true,  f: "patterns/two_pointers/two_sum_ii.py" },
  { cat: "two_pointers", n: 4, title: "Valid Palindrome",                    s: true,  f: "patterns/two_pointers/valid_palindrome.py" },
  { cat: "two_pointers", n: 5, title: "3Sum",                                s: false },
  { cat: "two_pointers", n: 6, title: "Container With Most Water",           s: false },
  { cat: "two_pointers", n: 7, title: "Trapping Rain Water",                 s: false },

  // ---- Sliding Window ----
  { cat: "sliding_window", n: 1, title: "Maximum Average Subarray I",        s: true,  f: "patterns/sliding_window/max_average_subarr.py" },
  { cat: "sliding_window", n: 2, title: "Max Consecutive Ones III",          s: true,  f: "patterns/sliding_window/max_consecutive_ones_iii.py" },
  { cat: "sliding_window", n: 3, title: "Longest Substring Without Repeating Characters", s: true, f: "patterns/sliding_window/longest_substring_without_repeated_characters.py" },
  { cat: "sliding_window", n: 4, title: "Longest Repeating Character Replacement", s: true, f: "patterns/sliding_window/longest_repeating_character_replacement.py" },
  { cat: "sliding_window", n: 5, title: "Minimum Size Subarray Sum",         s: true,  f: "patterns/sliding_window/2025/smallest_subarray_with_num_s.py" },
  { cat: "sliding_window", n: 6, title: "Permutation in String",             s: false },

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

  // ---- Recursive Backtracking ----
  { cat: "backtracking", n: 1, title: "Subsets",                             s: true,  f: "patterns/backtracking/subsets.py" },
  { cat: "backtracking", n: 2, title: "Permutations",                        s: true,  f: "patterns/backtracking/permutations.py" },
  { cat: "backtracking", n: 3, title: "Combinations",                        s: true,  f: "patterns/backtracking/combinations.py" },
  { cat: "backtracking", n: 4, title: "Combination Sum",                     s: true,  f: "patterns/backtracking/combination_sum.py" },
  { cat: "backtracking", n: 5, title: "Letter Combinations of a Phone Number", s: true, f: "patterns/backtracking/phone_letters_combination.py" },
  { cat: "backtracking", n: 6, title: "Generate Parentheses",                s: false },
  { cat: "backtracking", n: 7, title: "Word Search",                         s: false },

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
];

// Leitner intervals (days) keyed by box.
const INTERVAL = { 1: 1, 2: 3, 3: 7, 4: 21 };
const GRADES = [
  { box: 1, cls: "g1", label: "Failed",  sub: "needed the solution · +1d" },
  { box: 2, cls: "g2", label: "Slow",    sub: "solved with hints · +3d" },
  { box: 3, cls: "g3", label: "Clean",   sub: "solved, some hesitation · +7d" },
  { box: 4, cls: "g4", label: "Fast",    sub: "instant & confident · +21d" },
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

function saveState() {
  // Always mirror locally so an offline reload still has the latest.
  try { localStorage.setItem(STORE_KEY, JSON.stringify(STATE)); } catch (_) {}
  if (!SERVER_MODE) return;
  // Debounce writes to the repo file (textarea typing fires often).
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(STATE),
    }).catch(() => {});
  }, 400);
}

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
    if (STATE[id(p)]) return;
    STATE[id(p)] = {
      box: 2,
      due: addDays(today, Math.floor(i / NEW_PER_DAY_SEED)),
      last: null,
      attempts: 0,
      trigger: "",
    };
    seeded = true;
  });
  if (seeded) saveState();
}

/* ---------- app state ---------- */
let STATE = {};
let VIEW = "due";
let CAT_FILTER = "all";
let OPEN_ID = null;

/* ---------- derived helpers ---------- */
function prog(p) {
  return STATE[id(p)] || { box: 0, due: null, last: null, attempts: 0, trigger: "" };
}
function isDue(p) {
  const st = prog(p);
  return st.box >= 1 && st.due && daysUntil(st.due) <= 0;
}

/* ---------- rendering ---------- */
const listEl = document.getElementById("list");
const statsEl = document.getElementById("stats");
const filterEl = document.getElementById("filter");
const dueBadge = document.getElementById("dueBadge");

function render() {
  renderStats();
  renderFilter();
  renderList();
  document.querySelectorAll(".tab").forEach((t) =>
    t.classList.toggle("is-active", t.dataset.view === VIEW)
  );
}

function renderStats() {
  const dueCount = PROBLEMS.filter(isDue).length;
  const solvedCount = PROBLEMS.filter((p) => p.s).length;
  const coreTotal = PROBLEMS.filter((p) => CORE.has(p.cat)).length;
  const coreSolved = PROBLEMS.filter((p) => CORE.has(p.cat) && p.s).length;
  const mastered = PROBLEMS.filter((p) => prog(p).box === 4).length;

  dueBadge.textContent = dueCount;
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

function renderList() {
  if (VIEW === "help") {
    listEl.innerHTML = HELP_HTML;
    return;
  }

  const items = visibleProblems();

  if (items.length === 0) {
    listEl.innerHTML = `<p class="empty">${emptyMessage()}</p>`;
    return;
  }

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

  let meta = "";
  if (st.box === 0) {
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
    `<div class="row box-${st.box}${open}${solved}" data-id="${pid}">` +
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
  const grades = GRADES.map(
    (g) =>
      `<button class="grade ${g.cls}" data-grade="${g.box}">` +
      `${g.label}<small>${g.sub}</small></button>`
  ).join("");

  const src = p.f
    ? `<p class="history">📄 <code>${p.f}</code></p>`
    : `<p class="history">No local file yet — this is a fresh problem.</p>`;

  const hist =
    st.attempts > 0
      ? `<p class="history">Attempts: ${st.attempts}${st.last ? ` · last reviewed ${st.last}` : ""}</p>`
      : "";

  return (
    `<p class="panel__label">Grade your attempt (solve it blind first)</p>` +
    `<div class="grades">${grades}</div>` +
    `<div class="trigger">` +
      `<p class="panel__label">Trigger sentence — what tips you off to the pattern?</p>` +
      `<textarea data-trigger placeholder="e.g. 'sorted array + find a pair → two pointers from both ends'">${escapeHTML(st.trigger || "")}</textarea>` +
      `<p class="trigger__hint">This one sentence is what transfers to new problems. Saved automatically.</p>` +
    `</div>` +
    src +
    hist
  );
}

function escapeHTML(s) {
  return s.replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

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

  <p style="color:#7f8c9b">No hard interview date, ~30–60 min/day → this pacing is built for steady, sustainable progress while you start applying.</p>
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
  // grade button?
  const g = e.target.closest(".grade");
  if (g) {
    const row = g.closest(".row");
    gradeProblem(row.dataset.id, Number(g.dataset.grade));
    e.stopPropagation();
    return;
  }
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
  saveState();
  OPEN_ID = null; // collapse after grading so the list feels like a worklist
  render();
}

document.getElementById("resetBtn").addEventListener("click", () => {
  if (!confirm("Reset ALL progress? This clears every box, due date, and trigger note.")) return;
  STATE = {};
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

/* ---------- go ---------- */
async function init() {
  STATE = await loadProgress();
  seedIfNeeded();
  render();
  const note = document.querySelector(".foot__note");
  if (note) {
    note.textContent = SERVER_MODE
      ? "✓ Saving to prep-tracker/progress.json — commit it to sync across machines."
      : "⚠ Offline mode (localStorage only). Run server.py to make the repo the source of truth.";
  }
}
init();
