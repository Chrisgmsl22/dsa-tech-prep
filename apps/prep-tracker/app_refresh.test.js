"use strict";
/* Reload-on-focus against the real app.js persistence code. app.js is a
 * browser script, so it runs here in a vm with a stub DOM and a stub fetch
 * that plays the server. No network, no real progress file. */
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const tick = () => new Promise((r) => setTimeout(r, 0));
async function settle() { for (let i = 0; i < 20; i++) await tick(); }

function element() {
  return {
    innerHTML: "", textContent: "", style: {}, className: "",
    classList: { toggle() {} },
    addEventListener() {}, querySelector: () => null, querySelectorAll: () => [],
  };
}

/* A fake server.py: ETag revisions, If-Match on POST, and a switch to make it
 * unreachable. `outsideWrite` is grade.py writing the file behind the tab. */
function fakeServer(data) {
  const server = { data, etag: "r1", down: false, rev: 1 };
  server.outsideWrite = (key, entry) => {
    server.data = { ...server.data, [key]: entry };
    server.etag = "r" + ++server.rev;
  };
  server.fetch = async (url, opts) => {
    if (server.down) throw new TypeError("Failed to fetch");
    const headers = (etag) => ({ get: (h) => (h === "ETag" ? etag : null) });
    if (opts && opts.method === "POST") {
      if (opts.headers["If-Match"] !== server.etag) {
        return { ok: false, status: 409, headers: headers(server.etag), json: async () => ({}) };
      }
      server.data = JSON.parse(opts.body);
      server.etag = "r" + ++server.rev;
      return { ok: true, status: 204, headers: headers(server.etag) };
    }
    const snapshot = JSON.parse(JSON.stringify(server.data));
    return { ok: true, status: 200, headers: headers(server.etag), json: async () => snapshot };
  };
  return server;
}

async function loadApp(server) {
  const els = {};
  const store = {};
  const ctx = vm.createContext({
    console, setTimeout, clearTimeout, URL, Blob,
    fetch: (...a) => server.fetch(...a),
    window: { addEventListener() {} },
    document: {
      visibilityState: "visible",
      getElementById: (id) => (els[id] ||= element()),
      querySelector: () => null, querySelectorAll: () => [], addEventListener() {},
      createElement: element, body: { appendChild() {} },
    },
    localStorage: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
    },
  });
  for (const f of ["selection.js", "sprint.js", "app.js"]) {
    vm.runInContext(fs.readFileSync(path.join(__dirname, f), "utf8"), ctx, { filename: f });
  }
  await settle();
  return { run: (code) => vm.runInContext(code, ctx), store };
}

const seed = () => ({
  "stacks#1": { box: 3, due: "2026-01-01", last: "2026-01-01", attempts: 2, trigger: "" },
});
const quickEntry = { box: 5, due: "2027-01-01", last: "2026-10-12", attempts: 3, trigger: "", kind: "quick" };

test("a refresh replaces STATE and the mirror when the tab has nothing unsaved", async () => {
  const server = fakeServer(seed());
  const app = await loadApp(server);
  assert.strictEqual(app.run("SERVER_MODE && !isHalted()"), true);

  server.outsideWrite("stacks#2", quickEntry);
  await app.run("refreshIfChanged()");

  assert.strictEqual(app.run('STATE["stacks#2"].kind'), "quick");
  assert.strictEqual(app.run("REVISION"), server.etag);
  assert.strictEqual(app.run("isHalted()"), false);
  const mirror = JSON.parse(app.store["srt.v1"]);
  assert.strictEqual(mirror.state["stacks#2"].kind, "quick", "the mirror follows the refresh");
});

test("a failed save blocks the refresh, so the grade survives and the next save halts", async () => {
  const server = fakeServer(seed());
  const app = await loadApp(server);
  const revBefore = app.run("REVISION");

  server.down = true;
  app.run('gradeProblem("stacks#1", 4)');            // the POST fails: server down
  await settle();
  const graded = app.run('JSON.stringify(STATE["stacks#1"])');
  assert.strictEqual(app.run("hasUnsaved()"), true);

  server.down = false;
  server.outsideWrite("stacks#2", quickEntry);       // grade.py moved the ETag meanwhile
  await app.run("refreshIfChanged()");

  assert.strictEqual(app.run('JSON.stringify(STATE["stacks#1"])'), graded, "the grade is kept");
  assert.strictEqual(app.run("REVISION"), revBefore, "the refresh did not adopt the file");
  assert.strictEqual(app.run("isHalted()"), false, "the refresh itself never halts");

  app.run("saveState({ immediate: true })");         // any next save
  await settle();
  assert.strictEqual(app.run("HALT && HALT.title"), "This tab is out of date");
  assert.strictEqual(server.data["stacks#1"].box, 3, "the file was not overwritten");
});

test("a successful save clears the unsaved state", async () => {
  const server = fakeServer(seed());
  const app = await loadApp(server);
  app.run('gradeProblem("stacks#1", 3)');
  await settle();
  assert.strictEqual(app.run("hasUnsaved()"), false);
  assert.strictEqual(server.data["stacks#1"].attempts, 3);
});

/* Plan rev 6. The rows shown in the window are everything before step 3,
 * which holds the new-problem row. */
const windowRows = (app) =>
  (app.run('listEl.innerHTML.split("today__step--new")[0]').match(/class="row /g) || []).length;

test("the window shrinks as reps are graded, and the badge equals the rows shown", async () => {
  const server = fakeServer(seed());
  const app = await loadApp(server);
  app.run("render()");
  for (let left = 3; left >= 0; left--) {
    assert.strictEqual(windowRows(app), left, `rows with ${left} left`);
    assert.strictEqual(String(app.run("dueBadge.textContent")), String(left), `badge with ${left} left`);
    if (left) app.run("gradeProblem(todayWindow()[0].key, 3)");
  }
  assert.match(app.run("listEl.innerHTML"), /Reps done for today/);
  assert.match(app.run("listEl.innerHTML"), /id="windowToggle">Show all/);
  assert.doesNotMatch(app.run("listEl.innerHTML"), /Nothing due today/);
});

test("a Fast re-grade after a grade.py quick rep gives box 5, before and after a reload", async () => {
  const server = fakeServer(seed());
  const app = await loadApp(server);
  const today = app.run("todayISO()");
  const prev = { box: 4, due: "2026-01-01", last: "2025-12-01", attempts: 2 };
  server.outsideWrite("stacks#2", { box: 5, due: "2099-01-01", last: today, attempts: 3, trigger: "", kind: "quick", prev });
  await app.run("refreshIfChanged()");

  app.run('gradeProblem("stacks#2", 4)');
  await settle();
  const first = server.data["stacks#2"];
  assert.deepStrictEqual([first.box, first.attempts, first.prev], [5, 3, prev]);

  const reloaded = await loadApp(server);
  assert.match(reloaded.run('panelHTML(PROBLEMS.find((p) => id(p) === "stacks#2"), STATE["stacks#2"], false)'), /Fast<small>[^<]*\+45d/);
  reloaded.run('gradeProblem("stacks#2", 4)');
  await settle();
  assert.deepStrictEqual(server.data["stacks#2"], first, "a reload changes nothing");
});
