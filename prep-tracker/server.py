#!/usr/bin/env python3
"""Prep Tracker server.

Serves the tracker app AND persists your progress to `progress.json` in this repo,
so the repo is the source of truth for what you've practiced. Commit progress.json
and `git pull` on any machine to resume exactly where you left off.

Run:
    python3 prep-tracker/server.py          # http://localhost:8000/
    PORT=8137 python3 prep-tracker/server.py # custom port

Endpoints:
    GET  /                -> the app (index.html)
    GET  /api/progress    -> current progress.json (or {} if none yet)
    POST /api/progress    -> overwrite progress.json with the request body
"""

import json
import os
import tempfile
from http.server import HTTPServer, SimpleHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))

# PREP_PROGRESS points the server at a different progress file, so you can run
# the app against fixture data without touching your real history:
#
#     PREP_PROGRESS=/tmp/fixture.json PORT=8137 python3 prep-tracker/server.py
#
# Use a different PORT too — localStorage is per-origin, so :8137 also gets its
# own mirror and the sandbox is fully isolated.
PROGRESS = os.environ.get("PREP_PROGRESS") or os.path.join(HERE, "progress.json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files out of the prep-tracker directory.
        super().__init__(*args, directory=HERE, **kwargs)

    def _route(self):
        return self.path.split("?", 1)[0]

    def do_GET(self):
        if self._route() == "/api/progress":
            data = b"{}"
            if os.path.exists(PROGRESS):
                with open(PROGRESS, "rb") as f:
                    data = f.read() or b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def do_POST(self):
        if self._route() != "/api/progress":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            parsed = json.loads(body or b"{}")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        # Reject non-objects. `json.loads(b"5")` succeeds, and writing a scalar
        # here would make the next load fall back to {} and reseed from
        # scratch -- silently destroying all history.
        if not isinstance(parsed, dict):
            self.send_error(400, "Progress must be a JSON object")
            return
        # Write to a temp file in the same directory, then atomically rename.
        # Opening PROGRESS with "w" truncates it first, so an interrupt mid-dump
        # would leave the source of truth truncated. os.replace is atomic on
        # POSIX, so the file is either the old version or the new one.
        # Pretty-print + stable key order so git diffs stay readable.
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(PROGRESS) or ".", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(parsed, f, indent=2, sort_keys=True)
                f.write("\n")
            os.replace(tmp, PROGRESS)
        except Exception:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
        self.send_response(204)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # keep the console quiet


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Prep Tracker  ->  http://localhost:{port}/")
    print(f"Progress file ->  {PROGRESS}")
    print("Ctrl-C to stop.")
    try:
        HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
