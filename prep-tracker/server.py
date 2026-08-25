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
    GET  /api/progress    -> current progress, plus an ETag revision
    POST /api/progress    -> replace progress.json, guarded by If-Match

SAFETY MODEL -- this file guards a year of practice history that cannot be
reconstructed. Four rules, each closing a path that was verified to destroy it:

 1. An EMPTY or UNPARSEABLE progress file is an ERROR (409), never an empty
    object. Reporting it as "{}" made the app seed from scratch and immediately
    save over the file: 63 entries with 15 notes became 60 with none, in one
    page load, with no warning.
 2. Every write is REVISION-CHECKED. The client echoes the ETag it loaded as
    If-Match; a mismatch is 409. Without it, a stale tab posting its old
    snapshot silently reverted every grade made since that tab loaded.
 3. A write is only accepted from OUR OWN ORIGIN and only as application/json.
    A text/plain POST is a CORS-simple request, so no preflight protects it --
    any page in the browser could erase the file with one fetch().
 4. The temp file is FSYNCED before the atomic rename. Without it a crash can
    leave the rename durable and the data not, producing exactly the zero-byte
    file that rule 1 exists to refuse.
"""

import json
import os
import tempfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

# PREP_PROGRESS points the server at a different progress file, so you can run
# the app against fixture data without touching your real history:
#
#     PREP_PROGRESS=/tmp/fixture.json PORT=8137 python3 prep-tracker/server.py
#
# Use a different PORT too -- localStorage is per-origin, so :8137 also gets its
# own mirror and the sandbox is fully isolated.
PROGRESS = os.environ.get("PREP_PROGRESS") or os.path.join(HERE, "progress.json")

MAX_BODY = 8 * 1024 * 1024  # a 129-problem file is ~15 KB; 8 MB is absurdly generous
FILE_MODE = 0o644           # mkstemp makes 0600 and os.replace carries the mode over


def revision():
    """Opaque ETag for the current file. "0" means the file does not exist yet."""
    try:
        return str(os.stat(PROGRESS).st_mtime_ns)
    except FileNotFoundError:
        return "0"


class Handler(SimpleHTTPRequestHandler):
    timeout = 10  # a half-open connection must not stall every other request

    def __init__(self, *args, **kwargs):
        # Serve static files out of the prep-tracker directory.
        super().__init__(*args, directory=HERE, **kwargs)

    def _route(self):
        return self.path.split("?", 1)[0]

    def _json(self, code, payload, etag=None):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        if etag is not None:
            self.send_header("ETag", etag)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _same_origin(self):
        """True unless an Origin header names somewhere that is not us.

        Browsers always send Origin on a cross-origin POST, so rejecting a
        foreign one closes the CSRF path. A missing Origin means curl or a
        script on this machine, which is allowed.
        """
        origin = self.headers.get("Origin")
        if not origin:
            return True
        port = self.server.server_address[1]
        return origin in (f"http://localhost:{port}", f"http://127.0.0.1:{port}")

    def do_GET(self):
        if self._route() != "/api/progress":
            return super().do_GET()

        if not os.path.exists(PROGRESS):
            # Genuinely nothing yet -- a first run. Seeding from scratch is correct.
            self._json(200, {}, etag="0")
            return

        with open(PROGRESS, "rb") as f:
            raw = f.read()

        if not raw.strip():
            self._json(409, {
                "error": "empty_file",
                "detail": f"{PROGRESS} exists but is empty. Refusing to report it as "
                          "'no progress', because the app would seed from scratch and "
                          "save over it. Restore it with: git checkout -- "
                          "prep-tracker/progress.json",
            })
            return

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            self._json(409, {
                "error": "unparseable",
                "detail": f"{PROGRESS} is not valid JSON ({e}). If you just merged, it may "
                          "still contain conflict markers. Fix the file, or restore it with: "
                          "git checkout -- prep-tracker/progress.json",
            })
            return

        if not isinstance(parsed, dict):
            self._json(409, {
                "error": "not_an_object",
                "detail": f"{PROGRESS} holds {type(parsed).__name__}, not an object.",
            })
            return

        self._json(200, parsed, etag=revision())

    def do_POST(self):
        if self._route() != "/api/progress":
            self.send_error(404)
            return

        if not self._same_origin():
            self.send_error(403, "Cross-origin writes are not allowed")
            return

        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self.send_error(415, "Content-Type must be application/json")
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            self.send_error(413, "Body too large")
            return

        # Revision check. If-Match is required, so a client that has not been
        # taught the protocol cannot blind-write. "*" is the documented escape
        # hatch for a deliberate force (scripts, recovery).
        want = (self.headers.get("If-Match") or "").strip()
        have = revision()
        if not want:
            self.send_error(428, "If-Match required; GET /api/progress first")
            return
        if want != "*" and want != have:
            self._json(409, {
                "error": "stale_revision",
                "detail": "progress.json changed since this tab loaded it. Reload before "
                          "saving, or your older snapshot would revert newer work.",
                "expected": want,
                "actual": have,
            }, etag=have)
            return

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

        # Write to a temp file in the same directory, fsync it, then atomically
        # rename. Opening PROGRESS with "w" would truncate it first, so an
        # interrupt mid-dump would leave the source of truth truncated. The
        # fsync matters because os.replace only guarantees the RENAME is atomic;
        # without it a crash can publish a name that points at unwritten blocks.
        # Pretty-print + stable key order so git diffs stay readable.
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(PROGRESS) or ".", suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(parsed, f, indent=2, sort_keys=True)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, FILE_MODE)  # mkstemp is 0600; keep the repo file readable
            os.replace(tmp, PROGRESS)
        except Exception:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

        self.send_response(204)
        self.send_header("ETag", revision())
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # keep the console quiet


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Prep Tracker  ->  http://localhost:{port}/")
    print(f"Progress file ->  {PROGRESS}")
    print("Ctrl-C to stop.")
    try:
        ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
