"use strict";

/* ------------------------------------------------------------------ *
 * Input — mirrors bfs_template_for_graphs.py
 *   edgeList = [[0,1],[0,2],[1,3],[2,4],[3,5],[4,5]]
 *   start = edgeList[0][0] = 0
 * ------------------------------------------------------------------ */
const EDGE_LIST = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]];

// Faithful port of Graph._buildGraph (bidirectional, insertion order).
function buildGraph(edgeList) {
  const graph = {};
  for (const [v1, v2] of edgeList) {
    if (!(v1 in graph)) graph[v1] = [];
    if (!(v2 in graph)) graph[v2] = [];
    graph[v1].push(v2);
    graph[v2].push(v1);
  }
  return graph;
}

const GRAPH = buildGraph(EDGE_LIST);
const START = EDGE_LIST[0][0];

// Fixed diamond layout (same as the DFS view, for easy comparison).
const POS = {
  0: { x: 300, y: 64 },
  1: { x: 158, y: 196 }, 2: { x: 442, y: 196 },
  3: { x: 158, y: 338 }, 4: { x: 442, y: 338 },
  5: { x: 300, y: 408 },
};
const EDGES = EDGE_LIST;

const SOURCE = `from collections import deque

class Graph:
    def _buildGraph(self, edgeList):
        graph = {}
        for v1, v2 in edgeList:
            if v1 not in graph:
                graph[v1] = []
            if v2 not in graph:
                graph[v2] = []
            graph[v1].append(v2)
            graph[v2].append(v1)
        return graph

    def bfs(self, edgeList):
        graph = self._buildGraph(edgeList)
        queue = deque([])
        visited = set()

        queue.append(edgeList[0][0])     # seed the queue
        visited.add(edgeList[0][0])      # mark visited on ENQUEUE

        while queue:
            currNode = queue.popleft()
            print(currNode)              # process

            for neighbor in graph[currNode]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)`;

/* ------------------------------------------------------------------ *
 * Frame generation — instrument the BFS, one snapshot per step.
 * Key detail mirrored from the source: a node is marked visited at
 * ENQUEUE time, so it never enters the queue twice.
 * ------------------------------------------------------------------ */
function generateFrames(graph, start) {
  const frames = [];
  const visited = new Set();
  const queue = [];
  const output = [];

  const snap = (message, activeNode, activeEdge) =>
    frames.push({
      message,
      activeNode: activeNode == null ? null : activeNode,
      activeEdge: activeEdge || null,
      queue: [...queue],
      visited: [...visited],
      output: [...output],
    });

  snap("Press <b>Play</b> to start BFS from node 0.", null, null);

  queue.push(start);
  visited.add(start);
  snap(`Enqueue start node <b>${start}</b> and mark it visited.`, null, null);

  while (queue.length) {
    const node = queue.shift(); // popleft
    output.push(node);
    snap(`Dequeue <b>${node}</b> from the front → process it (<code>print(${node})</code>).`, node, null);

    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
        snap(`Neighbor <b>${neighbor}</b> is unvisited → enqueue &amp; mark visited.`, node, [node, neighbor]);
      } else {
        snap(`Neighbor <b>${neighbor}</b> already visited → skip.`, node, [node, neighbor]);
      }
    }
  }

  snap("Queue empty — BFS <b>complete</b>. Visit order: " + output.join(" → ") + ".", null, null);
  return frames;
}

const FRAMES = generateFrames(GRAPH, START);

/* ------------------------------------------------------------------ *
 * Build the static SVG graph
 * ------------------------------------------------------------------ */
const SVG_NS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("graph");
const edgeEls = {};
const nodeEls = {};

function edgeKey(a, b) { return a < b ? `${a}-${b}` : `${b}-${a}`; }

function buildGraphSvg() {
  for (const [a, b] of EDGES) {
    const line = document.createElementNS(SVG_NS, "line");
    line.setAttribute("x1", POS[a].x); line.setAttribute("y1", POS[a].y);
    line.setAttribute("x2", POS[b].x); line.setAttribute("y2", POS[b].y);
    line.setAttribute("class", "edge");
    svg.appendChild(line);
    edgeEls[edgeKey(a, b)] = line;
  }
  for (const id of Object.keys(POS)) {
    const g = document.createElementNS(SVG_NS, "g");
    g.setAttribute("class", "node idle");
    const c = document.createElementNS(SVG_NS, "circle");
    c.setAttribute("cx", POS[id].x); c.setAttribute("cy", POS[id].y); c.setAttribute("r", 26);
    const t = document.createElementNS(SVG_NS, "text");
    t.setAttribute("x", POS[id].x); t.setAttribute("y", POS[id].y); t.textContent = id;
    g.appendChild(c); g.appendChild(t); svg.appendChild(g);
    nodeEls[id] = g;
  }
}

/* ------------------------------------------------------------------ *
 * Adjacency-list panel
 * ------------------------------------------------------------------ */
const adjEl = document.getElementById("adj");
function buildAdjPanel() {
  for (const id of Object.keys(GRAPH)) {
    const row = document.createElement("div");
    row.className = "adj__row";
    row.dataset.node = id;
    row.innerHTML =
      `<span class="adj__key">${id}</span><span class="adj__sep">:</span>` +
      `<span class="adj__vals">[${GRAPH[id].join(", ")}]</span>`;
    adjEl.appendChild(row);
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

function render(i) {
  const f = FRAMES[i];
  const inQueue = new Set(f.queue);
  const visitedSet = new Set(f.visited);

  // nodes: active = processing now; queued (amber) = waiting in queue;
  // visited = discovered & already dequeued; idle = undiscovered.
  for (const id of Object.keys(nodeEls)) {
    const n = Number(id);
    let cls = "node idle";
    if (f.activeNode === n) cls = "node active";
    else if (inQueue.has(n)) cls = "node stack";
    else if (visitedSet.has(n)) cls = "node visited";
    nodeEls[id].setAttribute("class", cls);
  }

  // edges
  for (const [a, b] of EDGES) {
    const el = edgeEls[edgeKey(a, b)];
    const isActive = f.activeEdge && edgeKey(f.activeEdge[0], f.activeEdge[1]) === edgeKey(a, b);
    if (isActive) el.setAttribute("class", "edge active");
    else if (visitedSet.has(a) && visitedSet.has(b)) el.setAttribute("class", "edge done");
    else el.setAttribute("class", "edge");
  }

  // queue (front rendered at top)
  queueEl.innerHTML = "";
  if (f.queue.length === 0) {
    queueEl.innerHTML = `<li class="empty-li"><span class="empty">empty</span></li>`;
  } else {
    f.queue.forEach((node, idx) => {
      const li = document.createElement("li");
      if (idx === 0) li.className = "top";
      const tag = idx === 0 ? "front" : (idx === f.queue.length - 1 ? "back" : "");
      li.innerHTML = `<span>node ${node}</span><span class="frame">${tag}</span>`;
      queueEl.appendChild(li);
    });
  }

  // visited
  visitedEl.innerHTML = f.visited.length === 0
    ? `<span class="empty">{ }</span>`
    : f.visited.map((v) => `<span class="chip">${v}</span>`).join("");

  // output
  outputEl.innerHTML = f.output.length === 0
    ? `<span class="empty">no output yet</span>`
    : f.output.map((v, k) => (k ? `<span class="arrow">›</span>` : "") + `<span class="chip">${v}</span>`).join("");

  // adjacency highlight
  adjEl.querySelectorAll(".adj__row").forEach((row) => {
    row.classList.toggle("active", Number(row.dataset.node) === f.activeNode);
  });

  // status + progress
  statusMsg.innerHTML = f.message;
  progressText.textContent = `${i} / ${FRAMES.length - 1}`;
  progressFill.style.width = `${(i / (FRAMES.length - 1)) * 100}%`;
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
  const BUILTIN = new Set(["print", "len", "range", "set", "dict", "list", "append", "add", "popleft", "deque", "int", "str"]);

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
buildGraphSvg();
buildAdjPanel();
document.getElementById("source").innerHTML = highlightPython(SOURCE);
updateSpeedLabel();
render(0);
