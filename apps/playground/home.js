"use strict";

// Display metadata per category. Unknown categories fall back to a default.
const CATEGORY_META = {
  arrays_and_strings: { label: "Arrays & Strings", glyph: "[ ]" },
  hashmaps_and_sets: { label: "Hashmaps & Sets", glyph: "#" },
  two_pointers: { label: "Two Pointers", glyph: "⇄" },
  stacks: { label: "Stacks", glyph: "≡" },
  linked_lists: { label: "Linked Lists", glyph: "→" },
  binary_search: { label: "Binary Search", glyph: "÷" },
  sliding_window: { label: "Sliding Window", glyph: "▭" },
  trees: { label: "Trees", glyph: "⑂" },
  heaps: { label: "Heaps", glyph: "▲" },
  backtracking: { label: "Backtracking", glyph: "⌥" },
  grids: { label: "Grids", glyph: "▦" },
  graphs: { label: "Graphs", glyph: "◈" },
  dp: { label: "Dynamic Programming", glyph: "Σ" },
  recursion: { label: "Recursion", glyph: "↺" },
};

const catalog = document.getElementById("catalog");
const search = document.getElementById("search");
const countEl = document.getElementById("count");

let DATA = [];

fetch("playgrounds.json")
  .then((r) => {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  })
  .then((d) => {
    DATA = Array.isArray(d.playgrounds) ? d.playgrounds : [];
    render("");
  })
  .catch(() => {
    catalog.innerHTML =
      '<p class="error">Could not load <code>playgrounds.json</code>. ' +
      "Make sure you opened this through a local server (not a file:// path).</p>";
  });

function meta(cat) {
  return CATEGORY_META[cat] || { label: cat.replace(/_/g, " "), glyph: "▢" };
}

function matches(p, q) {
  if (!q) return true;
  const hay = [p.title, p.category, p.blurb, (p.tags || []).join(" ")]
    .join(" ")
    .toLowerCase();
  return hay.includes(q);
}

function render(query) {
  const q = query.trim().toLowerCase();
  const items = DATA.filter((p) => matches(p, q));

  countEl.textContent =
    items.length + " visualization" + (items.length === 1 ? "" : "s");

  if (items.length === 0) {
    catalog.innerHTML = '<p class="empty">No matches. Try a different search.</p>';
    return;
  }

  // Group by category, preserving first-seen order.
  const order = [];
  const groups = {};
  for (const p of items) {
    if (!groups[p.category]) {
      groups[p.category] = [];
      order.push(p.category);
    }
    groups[p.category].push(p);
  }

  catalog.innerHTML = "";
  for (const cat of order) {
    const m = meta(cat);
    const section = document.createElement("section");
    section.className = "cat";

    const head = document.createElement("div");
    head.className = "cat__head";
    head.innerHTML =
      '<span class="cat__glyph">' + m.glyph + "</span>" +
      "<h2>" + m.label + "</h2>" +
      '<span class="cat__count">' + groups[cat].length + "</span>";
    section.appendChild(head);

    const row = document.createElement("div");
    row.className = "cards";
    for (const p of groups[cat]) {
      const a = document.createElement("a");
      a.className = "card";
      a.href = p.category + "/" + p.slug + "/index.html";
      a.innerHTML =
        '<div class="card__top"><span class="card__cat">' + m.label +
        '</span><span class="card__arrow">→</span></div>' +
        '<h3 class="card__title">' + p.title + "</h3>" +
        '<p class="card__blurb">' + (p.blurb || "") + "</p>" +
        '<div class="card__tags">' +
        (p.tags || []).map((t) => "<span>" + t + "</span>").join("") +
        "</div>";
      row.appendChild(a);
    }
    section.appendChild(row);
    catalog.appendChild(section);
  }
}

search.addEventListener("input", (e) => render(e.target.value));
