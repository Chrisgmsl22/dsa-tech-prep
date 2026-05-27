# DSA Playground

Interactive, step-through visualizations of the patterns I'm learning. The whole folder is
one tiny web app — a home page that lists every visualization, and one sub-app per pattern.

## Run it

```bash
cd playground
python3 -m http.server 8000
```

Then open **http://localhost:8000/** — the home page lists every visualization. Click a card to
play it; use the **← Playground** link to come back.

> Any static server works (`npx serve`, VS Code "Live Server", etc.). It must be served over
> **HTTP** — opening `index.html` as a `file://` path won't work, because the home page
> `fetch()`es `playgrounds.json`.

## Using a visualization

- **Play / Pause**, **Step**, **Reset**, and a **Speed** slider.
- Keyboard: <kbd>Space</kbd> play/pause · <kbd>→</kbd> step · <kbd>R</kbd> reset.
- The status line narrates each step; expand **Source** to see the code being visualized.

## Add a new visualization

Easiest: ask Claude — *"show me a visual example of how `<X>` works."* It follows
[`PLAYGROUND_GUIDE.md`](./PLAYGROUND_GUIDE.md): creates `playground/<category>/<name>/`, builds
the app, and registers it in `playgrounds.json` so it shows up on the home page automatically.

Manually, you'd:
1. Add `playground/<category>/<name>/` with `index.html`, `styles.css`, `app.js`.
2. Add an entry to `playgrounds.json`.
3. (Refresh the home page — no rebuild needed.)

## Files

| Path | What it is |
| ---- | ---------- |
| `index.html`, `home.css`, `home.js` | The home page / catalog |
| `playgrounds.json` | Registry of every visualization (drives the home page) |
| `PLAYGROUND_GUIDE.md` | Spec for *how* to build a visualization (for Claude) |
| `<category>/<name>/` | One self-contained visualization |
