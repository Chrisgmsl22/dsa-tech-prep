# Playground Guide — Building Interactive Code Visualizations

This file tells Claude **exactly how to build a visual example** when the student says something like:

> "Show me a visual example of how `<X>` works"
> "Visualize this code" / "Animate how this runs"

The goal: a small, polished, **interactive web app** that lets the student *play* the algorithm — step through it, watch state change, and build intuition.

---

## 1. The playground is ONE mini-site (single dev server)

The whole `playground/` directory is a single small web app served by **one** static
server. `playground/index.html` is the **home page**: it lists every visualization, grouped
by category, as searchable cards. You browse from the home into each visualization and back.

```
playground/
  index.html                  # HOME — catalog of all visualizations
  home.css  home.js           # home page styling + logic
  playgrounds.json            # MANIFEST — the registry every viz must appear in
  PLAYGROUND_GUIDE.md         # this file
  <category>/                 # graphs, trees, backtracking, sliding_window, heaps, ...
    <descriptive_name>/        # snake_case, one folder per visualization
      index.html
      styles.css
      app.js
```

- `<category>` = the pattern / data structure / algorithm family. **Create it if it doesn't exist.**
- `<descriptive_name>` = a specific, snake_case name for the request.
  - If visualizing a specific file, mirror its name (e.g. `traverse_graph_using_dfs`).
  - If it's a general concept, name it for the concept (e.g. `dfs_vs_bfs`, `quicksort_partition`).

Example: visualizing `patterns/graphs/traverse_graph_using_dfs.py` →
`playground/graphs/traverse_graph_using_dfs/`.

### Two things every new visualization MUST do

1. **Register in `playgrounds.json`** — append one entry so the home page shows it:

   ```json
   {
     "category": "graphs",
     "slug": "traverse_graph_using_dfs",
     "title": "Depth-First Traversal",
     "blurb": "One-line description shown on the card.",
     "tags": ["recursion", "adjacency list"],
     "source": "patterns/graphs/traverse_graph_using_dfs.py"
   }
   ```
   The home links to `<category>/<slug>/index.html`. If the category is new, add a label/glyph
   for it to `CATEGORY_META` in `home.js` (optional — it falls back gracefully).

2. **Add a back-link** in the visualization's header pointing home: `../../index.html`
   (two levels up, since the app lives at `playground/<category>/<slug>/`).

---

## 2. What to visualize

**If the student gives you specific code** (a file or snippet): mirror that code's logic *exactly*.
Re-implement it faithfully in JS so the animation reflects the real execution order
(same neighbor order, same base cases, same recursion). Do **not** "improve" their algorithm —
the point is to see *their* code run. Keep a copy of the original source visible in the UI.

**If the student gives no code**: write a clean, idiomatic reference implementation of the
concept and visualize that.

---

## 3. Tech stack (keep it zero-build)

- **Plain HTML + CSS + JS only.** No frameworks, no bundlers, no `npm install`.
  Rationale: the rendering is browser-native regardless of language; a build step or a
  Python/WASM runtime adds friction without improving these small apps. (If provable
  fidelity to the Python is ever needed, add an optional script that runs the real code and
  exports `frames.json` for the JS to play — Python as source of truth, browser for rendering.)
- **Run ONE static server at the playground root**, then navigate from the home page:

  ```
  cd playground && python3 -m http.server 8000     # then open http://localhost:8000/
  ```

  The home page uses `fetch()` to read `playgrounds.json`, so it must be served over HTTP —
  a `file://` path will not work.
- Use **SVG** for graph/tree/grid structures (easy to animate, crisp at any size).
  Use the DOM for arrays/stacks/cards. Canvas only if there are hundreds of elements.
- Fonts via Google Fonts `<link>` with a system fallback, so it still works offline-ish.
- No external JS libraries unless there's a strong reason. Vanilla keeps it portable.

---

## 4. The interaction model (the important part)

Every visualization follows the same **"precompute frames, then play them"** pattern:

1. **Instrument the algorithm** to push a *snapshot* onto a `frames[]` array at each meaningful
   step (enter function, mutate state, make a choice, return, etc.). A snapshot captures the
   *entire* visible state at that instant (current node, call stack, visited set, output, a
   human-readable `message`, and which element is "active").
2. **A player** walks `frames[]`. The UI is a pure function of `frames[currentStep]`.
   This makes Step / Play / Reset trivial and bug-free — you never mutate UI state directly.

Required controls (mirror these names/behaviors):

| Control | Behavior |
| ------- | -------- |
| **Play / Pause** | Auto-advance one frame every *interval* (from the Speed slider). Toggles to Pause. |
| **Step** | Advance exactly one frame. Pauses auto-play. |
| **Reset** | Jump back to frame 0. |
| **Speed** | Slider controlling the auto-advance interval (e.g. ~120ms fast → ~1200ms slow). |

Always render a **status line** describing the current frame in plain English
("`recurse(3)` called — push to call stack", "neighbor 0 already visited, skip").
This narration is what turns a pretty animation into a *learning* tool.

---

## 5. State panels

Show the data structures that matter for the algorithm, updating live each frame. Pick what's
relevant:

- **Graphs/Trees (DFS/BFS):** the structure (SVG), **call stack** (DFS) or **queue** (BFS),
  **visited set**, **output / visit order**, and the **input** (adjacency list / edges).
- **Backtracking:** the decision tree or current path, the `temp`/partial array, the results
  collected so far, and the choice being made.
- **Sliding window / two pointers:** the array with highlighted pointers/window, and the
  running aggregate (sum, max, counts).
- **Heaps:** the array-as-tree, plus the backing array.

Color the structure by state (e.g. idle / active / on-stack / visited). Define these as CSS
variables so every app feels consistent (see §6).

---

## 6. Visual identity (so all playground apps feel like a family)

Default to a **dark "HUD console"** aesthetic unless the student asks otherwise:

- **Background:** near-black ink with a faint dot-grid and a soft radial vignette.
- **Accent (active/current):** phosphor mint/cyan `#4fe0c0`.
- **On-stack / in-progress:** amber `#f4b942`.
- **Visited / done:** muted indigo `#6c7a9c`.
- **Idle:** low-contrast slate.
- **Fonts:** `Chakra Petch` for headings/labels (technical HUD feel) + `JetBrains Mono` for
  code/data values.
- **Motion:** smooth transitions on state changes; a "signal pulse" along the edge being
  traversed; stack items slide in/out. High-impact but not exhausting — this is a study tool
  used repeatedly, so favor clarity over spectacle.

Suggested CSS variables to copy into each app's `styles.css`:

```css
:root {
  --ink: #0a0e12;        --panel: #11161d;     --line: #1e2730;
  --idle: #3a4654;       --active: #4fe0c0;     --stack: #f4b942;
  --visited: #6c7a9c;    --text: #d7e0ea;       --muted: #7f8c9b;
}
```

It's fine for each app to be self-contained (copy the tokens in). Don't build a shared
framework — portability beats DRY here.

---

## 7. Quality bar & checklist

Before calling it done:

- [ ] Opens with no console errors; works from `file://`.
- [ ] The animation order matches the real code's execution exactly.
- [ ] Play, Step, Reset, and Speed all work; Reset returns to a clean initial state.
- [ ] Status line narrates every frame in plain English.
- [ ] The original source code is viewable in the UI.
- [ ] **Verify it in a browser** (screenshot via the available browser tooling) before reporting done.
- [ ] Responsive enough to be usable on a laptop screen.

---

## 8. Reference implementation

`playground/graphs/traverse_graph_using_dfs/` is the canonical example of all of the above.
When in doubt, match its structure (frame generation, player, panels, theme).
