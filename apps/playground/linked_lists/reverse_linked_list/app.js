"use strict";

/* ------------------------------------------------------------------ *
 * Source — the student's iterative reversal, mirrored exactly.
 * Line numbers below (1-based) are what each frame highlights.
 * ------------------------------------------------------------------ */
const SOURCE = `class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        curr = head
        temp = None

        while curr:
            next = curr.next
            curr.next = temp

            temp = curr
            curr = next

        return temp`;

const LINE = { call: 2, curr: 3, temp: 4, loop: 6, saveNext: 7, flip: 8, moveTemp: 10, moveCurr: 11, ret: 13 };

const DEFAULT_LIST = [1, 2, 3, 4, 5];
const MAX_NODES = 8;
const NONE = -1; // pointer value for Python None (undefined = name not assigned yet)

/* ------------------------------------------------------------------ *
 * Frame generation — run the real algorithm over an array-backed list
 * (nodes are indices, nextOf[i] is node i's .next) and snapshot after
 * every executed line. The UI is a pure function of frames[i].
 * ------------------------------------------------------------------ */
function generateFrames(vals) {
  const n = vals.length;
  const nextOf = vals.map((_, i) => (i + 1 < n ? i + 1 : NONE));
  const flipped = new Array(n).fill(false);
  const frames = [];
  let curr, temp, next; // undefined until the code assigns them

  const name = (v) => (v === NONE ? "<code>None</code>" : `<b>${vals[v]}</b>`);
  const listStr = (start) => {
    const out = [];
    let v = start, guard = 0;
    while (v !== NONE && guard++ <= n) { out.push(vals[v]); v = nextOf[v]; }
    return out.concat("None").join(" → ");
  };
  const P = (p) => `<span class="c-${p}">${p}</span>`;

  const snap = (line, message, extra = {}) =>
    frames.push({
      line, message,
      curr, temp, next,
      nextOf: [...nextOf],
      flipped: [...flipped],
      arrow: extra.arrow || null,      // { node, kind: "read" | "flip" }
      cond: extra.cond,                // true / false for the while check
      changed: extra.changed || [],    // pointer names assigned on this line
      ret: !!extra.ret,
    });

  snap(LINE.call, n
    ? `<code>reverseList(head)</code> is called on ${listStr(0)}. Press <b>Play</b> or <b>Step</b>.`
    : `<code>reverseList(head)</code> is called on an <b>empty list</b> (head is <code>None</code>). Press <b>Play</b> or <b>Step</b>.`);

  curr = n ? 0 : NONE;
  snap(LINE.curr, n
    ? `${P("curr")} = head: ${P("curr")} starts at node ${name(0)}, the front of the list.`
    : `${P("curr")} = head: head is <code>None</code>, so ${P("curr")} is <code>None</code> too.`,
    { changed: ["curr"] });

  temp = NONE;
  snap(LINE.temp,
    `${P("temp")} = None: ${P("temp")} will hold the reversed list. Nothing is reversed yet, so it starts as <code>None</code>.`,
    { changed: ["temp"] });

  while (curr !== NONE) {
    snap(LINE.loop, `<code>while curr</code>: ${P("curr")} is ${name(curr)}, not <code>None</code> — enter the loop.`, { cond: true });

    next = nextOf[curr];
    snap(LINE.saveNext, next === NONE
      ? `Save ${P("next")} = <code>None</code>. ${name(curr)} is the last node, but we still save it so ${P("curr")} can move on afterwards.`
      : `Save ${P("next")} = ${name(next)} so we don't lose the rest of the list when we flip ${name(curr)}.next.`,
      { arrow: { node: curr, kind: "read" }, changed: ["next"] });

    const oldNext = nextOf[curr];
    nextOf[curr] = temp;
    flipped[curr] = true;
    let flipMsg;
    if (temp === NONE && oldNext === NONE) {
      flipMsg = `Flip: ${name(curr)}.next now points to ${P("temp")}, which is <code>None</code>. It already pointed to <code>None</code>, so a single node is its own reverse.`;
    } else if (temp === NONE) {
      flipMsg = `Flip: ${name(curr)}.next now points to <code>None</code> — it becomes the tail of the reversed list. The old link to ${name(oldNext)} is cut; only ${P("next")} still reaches it.`;
    } else if (oldNext === NONE) {
      flipMsg = `Flip: ${name(curr)}.next now points to ${name(temp)}. Its old link to <code>None</code> is gone — every arrow now points back.`;
    } else {
      flipMsg = `Flip: ${name(curr)}.next now points to ${name(temp)}. The old link ${name(curr)} → ${name(oldNext)} is cut; ${P("next")} still holds ${name(oldNext)}.`;
    }
    snap(LINE.flip, flipMsg, { arrow: { node: curr, kind: "flip" } });

    temp = curr;
    snap(LINE.moveTemp,
      `${P("temp")} = curr: move ${P("temp")} up to ${name(temp)}. The reversed list now reads ${listStr(temp)}.`,
      { changed: ["temp"] });

    curr = next;
    snap(LINE.moveCurr, curr === NONE
      ? `${P("curr")} = next: move ${P("curr")} to <code>None</code>. No unprocessed nodes are left.`
      : `${P("curr")} = next: move ${P("curr")} to ${name(curr)}, the next unprocessed node.`,
      { changed: ["curr"] });
  }

  snap(LINE.loop, `<code>while curr</code>: ${P("curr")} is <code>None</code> — the condition is false, so the loop ends.`, { cond: false });

  snap(LINE.ret, n
    ? `<code>return temp</code>: the new head is ${name(temp)}. Reversed list: ${listStr(temp)}.`
    : `<code>return temp</code>: ${P("temp")} is <code>None</code>. An empty list reversed is still empty.`,
    { ret: true });

  return frames;
}

/* ------------------------------------------------------------------ *
 * SVG geometry — slot 0 = left None (where temp starts),
 * slots 1..n = nodes, slot n+1 = right None (end of the original list).
 * ------------------------------------------------------------------ */
const SVG_NS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("list");
const VIEW_W = 1000;
const CY = 112;
const BOX_W = 60, BOX_H = 48;
const NONE_W = 58, NONE_H = 38;
const LANES = { curr: 186, temp: 220, next: 254, ret: 290 };

let VALS = DEFAULT_LIST.slice();
let FRAMES = [];
let geo = null;          // { n, slotX(s) }
let els = null;          // element handles for the current SVG

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}

function makeMarker(defs, id, cls) {
  const m = el("marker", {
    id, viewBox: "0 0 10 10", refX: 9, refY: 5,
    markerWidth: 11, markerHeight: 11, markerUnits: "userSpaceOnUse", orient: "auto-start-reverse",
  }, defs);
  el("path", { d: "M0,0 L10,5 L0,10 z", class: cls }, m);
}

function buildSvg(vals) {
  svg.innerHTML = "";
  const n = vals.length;
  const slots = n + 2;
  const spacing = Math.min(118, 930 / (slots - 1));
  const x0 = VIEW_W / 2 - (spacing * (slots - 1)) / 2;
  const slotX = (s) => x0 + s * spacing;
  geo = { n, slotX };

  const defs = el("defs", {}, svg);
  for (const k of ["fwd", "rev", "read", "cut", "flip"]) makeMarker(defs, "mk-" + k, "mk-" + k);

  const halfW = (slot) => (slot === 0 || slot === n + 1 ? NONE_W / 2 : BOX_W / 2);
  const halfH = (slot) => (slot === 0 || slot === n + 1 ? NONE_H / 2 : BOX_H / 2);

  // Arrows first (under the boxes). Node i lives in slot i+1.
  const fwd = [], rev = [], cutX = [];
  for (let i = 0; i < n; i++) {
    const s = i + 1;
    const xs = slotX(s), xt = slotX(s + 1);
    const x1 = xs + BOX_W / 2 + 3, x2 = xt - halfW(s + 1) - 3;
    fwd.push(el("path", { d: `M ${x1} ${CY} L ${x2} ${CY}`, class: "arrow fwd", "marker-end": "url(#mk-fwd)" }, svg));
    cutX.push(el("text", { x: (x1 + x2) / 2, y: CY - 14, class: "cut-x", opacity: 0 }, svg));
    cutX[i].textContent = "✕";

    // Reversed arrow: an arc over the top, back to slot s-1.
    const xb = slotX(s - 1);
    const sx = xs - 12, sy = CY - BOX_H / 2 - 2;
    const ex = xb + 12, ey = CY - halfH(s - 1) - 3;
    const cx = (sx + ex) / 2, cyc = CY - 92;
    rev.push(el("path", {
      d: `M ${sx} ${sy} Q ${cx} ${cyc} ${ex} ${ey}`,
      class: "arrow rev hidden", pathLength: 1, "marker-end": "url(#mk-rev)",
    }, svg));
  }

  // None terminals.
  const noneEls = [];
  for (const slot of [0, n + 1]) {
    const g = el("g", { class: "none" }, svg);
    const x = slotX(slot);
    el("rect", { x: x - NONE_W / 2, y: CY - NONE_H / 2, width: NONE_W, height: NONE_H, rx: 8 }, g);
    const t = el("text", { x, y: CY }, g);
    t.textContent = "None";
    noneEls.push(g);
  }

  // Nodes.
  const nodeEls = vals.map((v, i) => {
    const x = slotX(i + 1);
    const g = el("g", { class: "node" }, svg);
    el("rect", { x: x - BOX_W / 2, y: CY - BOX_H / 2, width: BOX_W, height: BOX_H, rx: 9 }, g);
    const t = el("text", { x, y: CY }, g);
    t.textContent = v;
    return g;
  });

  // Pointer tags (one lane each, so they never overlap).
  const makeTag = (cls, label, w) => {
    const g = el("g", { class: `ptr ptr--${cls} off` }, svg);
    el("path", { d: "M -6 -12 L 0 -19 L 6 -12 z" }, g);
    el("rect", { x: -w / 2, y: -12, width: w, height: 24, rx: 6 }, g);
    const t = el("text", { x: 0, y: 0 }, g);
    t.textContent = label;
    g.style.transform = `translate(${slotX(1)}px, ${LANES[cls]}px)`;
    return g;
  };
  const tags = {
    curr: makeTag("curr", "curr", 56),
    temp: makeTag("temp", "temp", 56),
    next: makeTag("next", "next", 56),
    ret: makeTag("ret", "new head", 84),
  };
  tags.temp.style.transform = `translate(${slotX(0)}px, ${LANES.temp}px)`;

  els = { fwd, rev, cutX, nodeEls, noneEls, tags };
}

// Which slot a pointer value is drawn at. temp = None means "nothing reversed"
// (left terminal); curr / next = None means "past the end" (right terminal).
function slotOf(ptr, v) {
  if (v === NONE) return ptr === "temp" ? 0 : geo.n + 1;
  return v + 1;
}

/* ------------------------------------------------------------------ *
 * Render — pure function of FRAMES[i]
 * ------------------------------------------------------------------ */
const statusMsg = document.getElementById("status-msg");
const progressText = document.getElementById("progress-text");
const progressFill = document.getElementById("progress-fill");
const varsEl = document.getElementById("vars");
const chainsEl = document.getElementById("chains");
const sourceEl = document.getElementById("source");

const label = (v) => (v === NONE ? "None" : String(VALS[v]));

function walk(start, nextOf) {
  const out = [];
  let v = start, guard = 0;
  while (v !== NONE && guard++ <= VALS.length) { out.push(v); v = nextOf[v]; }
  return out;
}

function setMarker(path, state) {
  if (state === "hidden") path.removeAttribute("marker-end");
  else path.setAttribute("marker-end", `url(#mk-${state})`);
}

function render(i) {
  const f = FRAMES[i];
  const n = VALS.length;

  // nodes
  els.nodeEls.forEach((g, k) => {
    let cls = "node";
    if (f.flipped[k]) cls += " reversed";
    if (f.curr === k && !f.ret) cls += " is-curr";
    if (f.ret && f.temp === k) cls += " is-head";
    g.setAttribute("class", cls);
  });
  els.noneEls[0].setAttribute("class", "none" + (f.ret && f.temp === NONE ? " is-head" : ""));

  // arrows
  for (let k = 0; k < n; k++) {
    const isFlipNow = f.arrow && f.arrow.kind === "flip" && f.arrow.node === k;
    const isReadNow = f.arrow && f.arrow.kind === "read" && f.arrow.node === k;
    let fc = "fwd", rc = "rev";
    if (f.flipped[k]) {
      fc = isFlipNow ? "cut" : "hidden";
      rc = isFlipNow ? "flip" : "rev";
    } else {
      fc = isReadNow ? "read" : "fwd";
      rc = "hidden";
    }
    els.fwd[k].setAttribute("class", "arrow " + fc);
    setMarker(els.fwd[k], fc);
    els.rev[k].setAttribute("class", "arrow " + rc);
    setMarker(els.rev[k], rc);
    els.cutX[k].setAttribute("opacity", isFlipNow ? 1 : 0);
  }

  // pointer tags
  for (const p of ["curr", "temp", "next"]) {
    const g = els.tags[p];
    const v = f[p];
    let cls = `ptr ptr--${p}`;
    if (v === undefined) cls += " off";
    else g.style.transform = `translate(${geo.slotX(slotOf(p, v))}px, ${LANES[p]}px)`;
    if (f.changed.includes(p)) cls += " moved";
    g.setAttribute("class", cls);
  }
  const rt = els.tags.ret;
  if (f.ret) {
    rt.style.transform = `translate(${geo.slotX(slotOf("temp", f.temp))}px, ${LANES.ret}px)`;
    rt.setAttribute("class", "ptr ptr--ret");
  } else {
    rt.setAttribute("class", "ptr ptr--ret off");
  }

  // source line highlight
  sourceEl.querySelectorAll(".ln").forEach((ln) => {
    const on = Number(ln.dataset.line) === f.line;
    ln.classList.toggle("active", on);
    ln.classList.toggle("false", on && f.cond === false);
  });

  // variables
  const varRow = (p, note) => {
    const v = f[p];
    let val;
    if (v === undefined) val = `<span class="var__val unset">not assigned yet</span>`;
    else if (v === NONE) val = `<span class="var__val">None</span>`;
    else val = `<span class="var__val">Node(${VALS[v]})</span><span class="var__note">.next → ${label(f.nextOf[v])}</span>`;
    const changed = f.changed.includes(p) ? " changed" : "";
    return `<div class="var var--${p}${changed}" title="${note}">` +
      `<span class="var__name">${p}</span><span class="var__eq">=</span>${val}</div>`;
  };
  varsEl.innerHTML =
    varRow("curr", "the node being processed") +
    varRow("temp", "head of the reversed part") +
    varRow("next", "saved rest of the original list");

  // two lists (plus what next is holding on to)
  const chain = (p, title) => {
    const v = f[p];
    let row;
    if (v === undefined) row = `<span class="empty">${p} not assigned yet</span>`;
    else {
      const items = walk(v, f.nextOf).map((k) => `<span class="chip">${VALS[k]}</span>`);
      items.push(`<span class="chip chip--none">None</span>`);
      row = items.join(`<span class="arrow-t">→</span>`);
    }
    return `<div class="chain chain--${p}"><div class="chain__label"><b class="c-${p}">${p}</b> → ${title}</div>` +
      `<div class="chain__row">${row}</div></div>`;
  };
  chainsEl.innerHTML =
    chain("temp", "reversed so far") +
    chain("curr", "remaining (unprocessed)") +
    (f.next !== undefined ? chain("next", "what next is holding on to") : "");

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

// YouTube-style discrete playback rates; the slider picks an index into this.
const SPEEDS = [0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4];
const BASE_MS = 900; // one frame lasts 900ms at 1× (pointer moves need a beat)

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
  const t = e.target;
  if (t && t.tagName === "INPUT" && t.type === "text") return; // typing in the input box
  if (e.code === "Space") { e.preventDefault(); playBtn.click(); }
  else if (e.code === "ArrowRight") { e.preventDefault(); document.getElementById("step").click(); }
  else if (e.key === "r" || e.key === "R") { document.getElementById("reset").click(); }
});

/* ------------------------------------------------------------------ *
 * Input — comma-separated values, 0..8 nodes
 * ------------------------------------------------------------------ */
const inputEl = document.getElementById("list-input");
const errEl = document.getElementById("input-err");

function parseList(text) {
  const s = text.trim();
  if (s === "" || s === "[]") return { vals: [] };
  const tokens = s.replace(/^\[|\]$/g, "").split(",").map((t) => t.trim());
  if (tokens.some((t) => t === "")) return { error: "Empty value between commas. Example: 1, 2, 3" };
  if (tokens.some((t) => !/^-?\d{1,3}$/.test(t))) return { error: "Use whole numbers with up to 3 digits, e.g. 4, -2, 17." };
  if (tokens.length > MAX_NODES) return { error: `At most ${MAX_NODES} nodes, so the list fits on screen. You entered ${tokens.length}.` };
  return { vals: tokens.map(Number) };
}

function build(vals) {
  setPlaying(false);
  VALS = vals;
  FRAMES = generateFrames(vals);
  buildSvg(vals);
  current = 0;
  render(0);
}

document.getElementById("input-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const res = parseList(inputEl.value);
  if (res.error) {
    errEl.textContent = res.error;
    inputEl.classList.add("bad");
    return;
  }
  errEl.textContent = "";
  inputEl.classList.remove("bad");
  build(res.vals);
  inputEl.blur();
});

document.getElementById("presets").addEventListener("click", (e) => {
  const b = e.target.closest(".preset");
  if (!b) return;
  inputEl.value = b.dataset.list.split(",").filter(Boolean).join(", ");
  document.getElementById("input-form").requestSubmit();
});

/* ------------------------------------------------------------------ *
 * Minimal, dependency-free Python syntax highlighter (same as the
 * reference app), applied per line so each line can be highlighted.
 * ------------------------------------------------------------------ */
function highlightPython(code) {
  const KW = new Set(["class", "def", "for", "if", "elif", "else", "in", "not",
    "and", "or", "return", "while", "import", "from", "as", "with", "lambda",
    "is", "pass", "break", "continue", "try", "except", "finally", "raise", "yield"]);
  const CONST = new Set(["None", "True", "False"]);
  const SELF = new Set(["self", "cls"]);
  const BUILTIN = new Set(["print", "len", "range", "set", "dict", "list", "append", "add", "int", "str"]);

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

function buildSource() {
  sourceEl.innerHTML = SOURCE.split("\n").map((line, idx) =>
    `<span class="ln" data-line="${idx + 1}"><span class="ln__no">${idx + 1}</span>` +
    `<span class="ln__code">${highlightPython(line) || " "}</span></span>`
  ).join("");
}

/* ------------------------------------------------------------------ *
 * Boot
 * ------------------------------------------------------------------ */
buildSource();
updateSpeedLabel();
build(DEFAULT_LIST.slice());
