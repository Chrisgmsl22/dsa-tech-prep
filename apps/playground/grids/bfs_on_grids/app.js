"use strict";

/* ------------------------------------------------------------------ *
 * Input — mirrors bfs_on_grids.py
 *   grid = [[1,2,3],[4,5,6],[7,8,9]]
 *   start = (0, 0)
 *   directions = up, down, left, right  (same order as the .py)
 * ------------------------------------------------------------------ */
const GRID = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];
const ROWS = GRID.length;
const COLS = GRID[0].length;
const DIRECTIONS = [
  { d: [-1, 0], name: "up" },
  { d: [1, 0], name: "down" },
  { d: [0, -1], name: "left" },
  { d: [0, 1], name: "right" },
];

const SOURCE = `class Solution:
    def performBfs(self, grid: list[list[int]]) -> list[int]:
        rows, cols = len(grid), len(grid[0])
        queue = []   # store coordinates, not the value
        result = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited = set()

        # seed the queue
        queue.append((0, 0))
        result.append(grid[0][0])
        visited.add((0, 0))

        while queue:
            i, j = queue.pop(0)

            for dI, dJ in directions:
                nI = dI + i
                nJ = dJ + j

                isWithinBounds = nI in range(rows) and nJ in range(cols)
                if isWithinBounds:
                    neighbor = (nI, nJ)
                    if neighbor not in visited:
                        result.append(grid[nI][nJ])
                        queue.append(neighbor)
                        visited.add(neighbor)

        return result`;

/* ------------------------------------------------------------------ *
 * Frame generation — instrument the BFS, one snapshot per step.
 * Key detail mirrored from the source: a cell is marked visited at
 * ENQUEUE time, so it never enters the queue twice.
 * ------------------------------------------------------------------ */
const key = (i, j) => `${i},${j}`;
const coord = (i, j) => `(${i},${j})`;

function generateFrames() {
  const frames = [];
  const visited = new Set();
  const queue = []; // array of [i, j]
  const output = []; // array of values

  // probe = the neighbor cell currently being examined (transient highlight)
  const snap = (message, active, probe, dirName, oob) =>
    frames.push({
      message,
      active: active || null,            // [i,j] cell being processed
      probe: probe || null,              // [i,j] neighbor being looked at
      dirName: dirName || null,          // which direction we are probing
      oob: !!oob,                        // probe is out of bounds?
      queue: queue.map((c) => [...c]),
      visited: [...visited],
      output: [...output],
    });

  snap("Press <b>Play</b> to run BFS from cell <b>(0,0)</b>.", null, null, null, false);

  // seed
  queue.push([0, 0]);
  output.push(GRID[0][0]);
  visited.add(key(0, 0));
  snap(
    `Seed: enqueue start <b>(0,0)</b>, mark it visited, and record its value <b>${GRID[0][0]}</b>.`,
    null, null, null, false
  );

  while (queue.length) {
    const [i, j] = queue.shift(); // queue.pop(0)
    snap(
      `Dequeue <b>${coord(i, j)}</b> from the front → now probe its 4 neighbors.`,
      [i, j], null, null, false
    );

    for (const { d, name } of DIRECTIONS) {
      const nI = d[0] + i;
      const nJ = d[1] + j;
      const within = nI >= 0 && nI < ROWS && nJ >= 0 && nJ < COLS;

      if (!within) {
        snap(
          `${name} → ${coord(nI, nJ)} is <b>out of bounds</b> → skip.`,
          [i, j], [nI, nJ], name, true
        );
        continue;
      }

      if (visited.has(key(nI, nJ))) {
        snap(
          `${name} → ${coord(nI, nJ)} already <b>visited</b> → skip.`,
          [i, j], [nI, nJ], name, false
        );
      } else {
        output.push(GRID[nI][nJ]);
        queue.push([nI, nJ]);
        visited.add(key(nI, nJ));
        snap(
          `${name} → ${coord(nI, nJ)} is new → enqueue, mark visited, record value <b>${GRID[nI][nJ]}</b>.`,
          [i, j], [nI, nJ], name, false
        );
      }
    }
  }

  snap(
    "Queue empty — BFS <b>complete</b>. Visit order: " + output.join(" → ") + ".",
    null, null, null, false
  );
  return frames;
}

const FRAMES = generateFrames();

/* ------------------------------------------------------------------ *
 * Build the static SVG grid
 * ------------------------------------------------------------------ */
const SVG_NS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("grid");
const cellEls = {}; // key(i,j) -> <g>

const CELL = 104;
const GAP = 12;
const PAD = 16;

function buildGridSvg() {
  for (let i = 0; i < ROWS; i++) {
    for (let j = 0; j < COLS; j++) {
      const x = PAD + j * (CELL + GAP);
      const y = PAD + i * (CELL + GAP);

      const g = document.createElementNS(SVG_NS, "g");
      g.setAttribute("class", "cell idle");

      const rect = document.createElementNS(SVG_NS, "rect");
      rect.setAttribute("x", x); rect.setAttribute("y", y);
      rect.setAttribute("width", CELL); rect.setAttribute("height", CELL);
      rect.setAttribute("rx", 12);

      const val = document.createElementNS(SVG_NS, "text");
      val.setAttribute("class", "cell__val");
      val.setAttribute("x", x + CELL / 2); val.setAttribute("y", y + CELL / 2 + 4);
      val.textContent = GRID[i][j];

      const lbl = document.createElementNS(SVG_NS, "text");
      lbl.setAttribute("class", "cell__coord");
      lbl.setAttribute("x", x + 9); lbl.setAttribute("y", y + 18);
      lbl.textContent = coord(i, j);

      g.appendChild(rect); g.appendChild(val); g.appendChild(lbl);
      svg.appendChild(g);
      cellEls[key(i, j)] = g;
    }
  }
}

/* ------------------------------------------------------------------ *
 * Directions panel
 * ------------------------------------------------------------------ */
const dirsEl = document.getElementById("dirs");
function buildDirsPanel() {
  for (const { d, name } of DIRECTIONS) {
    const row = document.createElement("div");
    row.className = "dir__row";
    row.dataset.name = name;
    row.innerHTML =
      `<span class="dir__name">${name}</span>` +
      `<span class="dir__vec">(${d[0]}, ${d[1]})</span>`;
    dirsEl.appendChild(row);
  }
}

/* ------------------------------------------------------------------ *
 * Render — pure function of FRAMES[i]
 * ------------------------------------------------------------------ */
const queueEl = document.getElementById("queue");
const visitedEl = document.getElementById("visited");
const outputEl = document.getElementById("output");
const statusMsg = document.getElementById("status-msg");
const progressText = document.getElementById("progress-text");
const progressFill = document.getElementById("progress-fill");

function render(idx) {
  const f = FRAMES[idx];
  const inQueue = new Set(f.queue.map(([i, j]) => key(i, j)));
  const visitedSet = new Set(f.visited);
  const activeKey = f.active ? key(f.active[0], f.active[1]) : null;
  const probeKey = f.probe && !f.oob ? key(f.probe[0], f.probe[1]) : null;

  // cells: active = dequeued now; probe = neighbor under inspection;
  // queued (amber) = waiting; visited = discovered; idle = undiscovered.
  for (let i = 0; i < ROWS; i++) {
    for (let j = 0; j < COLS; j++) {
      const k = key(i, j);
      let cls = "cell idle";
      if (activeKey === k) cls = "cell active";
      else if (inQueue.has(k)) cls = "cell queued";
      else if (visitedSet.has(k)) cls = "cell visited";
      if (probeKey === k && activeKey !== k) cls += " probe";
      cellEls[k].setAttribute("class", cls);
    }
  }

  // queue (front rendered at top)
  queueEl.innerHTML = "";
  if (f.queue.length === 0) {
    queueEl.innerHTML = `<li class="empty-li"><span class="empty">empty</span></li>`;
  } else {
    f.queue.forEach(([i, j], n) => {
      const li = document.createElement("li");
      if (n === 0) li.className = "top";
      const tag = n === 0 ? "front" : (n === f.queue.length - 1 ? "back" : "");
      li.innerHTML = `<span>${coord(i, j)}</span><span class="frame">${tag}</span>`;
      queueEl.appendChild(li);
    });
  }

  // visited
  visitedEl.innerHTML = f.visited.length === 0
    ? `<span class="empty">{ }</span>`
    : f.visited.map((c) => `<span class="chip chip--coord">${"(" + c + ")"}</span>`).join("");

  // output (values, in visit order)
  outputEl.innerHTML = f.output.length === 0
    ? `<span class="empty">no output yet</span>`
    : f.output.map((v, k2) => (k2 ? `<span class="arrow">›</span>` : "") + `<span class="chip">${v}</span>`).join("");

  // directions highlight
  dirsEl.querySelectorAll(".dir__row").forEach((row) => {
    row.classList.toggle("active", row.dataset.name === f.dirName);
  });

  // status + progress
  statusMsg.innerHTML = f.message;
  progressText.textContent = `${idx} / ${FRAMES.length - 1}`;
  progressFill.style.width = `${(idx / (FRAMES.length - 1)) * 100}%`;
}

/* ------------------------------------------------------------------ *
 * Player
 * ------------------------------------------------------------------ */
let current = 0;
let playing = false;
let timer = null;

const playBtn = document.getElementById("play");
const playGlyph = document.getElementById("play-glyph");
const playLabel = document.getElementById("play-label");
const speedEl = document.getElementById("speed");
const speedVal = document.getElementById("speed-val");

const SPEEDS = [0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4];
const BASE_MS = 700;

function currentSpeed() { return SPEEDS[Number(speedEl.value)]; }
function intervalMs() { return BASE_MS / currentSpeed(); }
function updateSpeedLabel() { speedVal.textContent = currentSpeed() + "×"; }

speedEl.addEventListener("input", () => {
  updateSpeedLabel();
  if (playing) { clearTimeout(timer); timer = setTimeout(tick, intervalMs()); }
});

function setPlaying(on) {
  playing = on;
  playGlyph.innerHTML = on ? "&#10073;&#10073;" : "&#9654;";
  playLabel.textContent = on ? "Pause" : "Play";
  playBtn.classList.toggle("btn--primary", !on);
  clearTimeout(timer);
  if (on) tick();
}

function tick() {
  if (!playing) return;
  if (current >= FRAMES.length - 1) { setPlaying(false); return; }
  current += 1;
  render(current);
  timer = setTimeout(tick, intervalMs());
}

playBtn.addEventListener("click", () => {
  if (!playing && current >= FRAMES.length - 1) { current = 0; render(current); }
  setPlaying(!playing);
});
document.getElementById("step").addEventListener("click", () => {
  setPlaying(false);
  if (current < FRAMES.length - 1) { current += 1; render(current); }
});
document.getElementById("reset").addEventListener("click", () => {
  setPlaying(false); current = 0; render(current);
});

document.addEventListener("keydown", (e) => {
  if (e.code === "Space") { e.preventDefault(); playBtn.click(); }
  else if (e.code === "ArrowRight") { e.preventDefault(); document.getElementById("step").click(); }
  else if (e.key === "r" || e.key === "R") { document.getElementById("reset").click(); }
});

/* ------------------------------------------------------------------ *
 * Minimal Python syntax highlighter (dependency-free)
 * ------------------------------------------------------------------ */
function highlightPython(code) {
  const KW = new Set(["class", "def", "for", "if", "elif", "else", "in", "not",
    "and", "or", "return", "while", "import", "from", "as", "with", "lambda",
    "is", "pass", "break", "continue", "try", "except", "finally", "raise", "yield"]);
  const CONST = new Set(["None", "True", "False"]);
  const SELF = new Set(["self", "cls"]);
  const BUILTIN = new Set(["print", "len", "range", "set", "dict", "list", "append", "add", "pop"]);

  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const re = /(#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+\.?\d*\b)|([A-Za-z_]\w*)|(\s+)|([\s\S])/g;

  let out = "";
  let m;
  let nameAfter = null;
  while ((m = re.exec(code)) !== null) {
    if (m[1]) out += `<span class="t-com">${esc(m[1])}</span>`;
    else if (m[2]) out += `<span class="t-str">${esc(m[2])}</span>`;
    else if (m[3]) out += `<span class="t-num">${esc(m[3])}</span>`;
    else if (m[4]) {
      const w = m[4];
      if (nameAfter) { out += `<span class="t-${nameAfter}">${esc(w)}</span>`; nameAfter = null; }
      else if (KW.has(w)) { out += `<span class="t-kw">${esc(w)}</span>`; if (w === "def") nameAfter = "fn"; else if (w === "class") nameAfter = "cls"; }
      else if (CONST.has(w)) out += `<span class="t-const">${esc(w)}</span>`;
      else if (SELF.has(w)) out += `<span class="t-self">${esc(w)}</span>`;
      else if (BUILTIN.has(w)) out += `<span class="t-builtin">${esc(w)}</span>`;
      else out += esc(w);
    }
    else if (m[5]) out += m[5];
    else out += esc(m[6]);
  }
  return out;
}

/* ------------------------------------------------------------------ *
 * Boot
 * ------------------------------------------------------------------ */
buildGridSvg();
buildDirsPanel();
document.getElementById("source").innerHTML = highlightPython(SOURCE);
updateSpeedLabel();
render(0);
