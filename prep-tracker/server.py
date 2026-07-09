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
from http.server import HTTPServer, SimpleHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "progress.json")


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
        # Pretty-print + stable key order so git diffs stay readable.
        with open(PROGRESS, "w") as f:
            json.dump(parsed, f, indent=2, sort_keys=True)
            f.write("\n")
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
