#!/usr/bin/env python3
"""Record a quick-rep grade in the prep tracker.

    python3 apps/prep-tracker/grade.py <key> pass|fail [--date YYYY-MM-DD]

<key> is a progress.json key such as "two_pointers#3". The mapping from a
quick-rep result to a tracker grade is PRACTICE.md "Quick rep -> tracker grade".

Write path: through the running server when it answers on
http://localhost:${PORT:-8000}/api/progress, so the revision check that guards
the file still applies. Only when nothing listens there is the file at
$PREP_PROGRESS (default: progress.json next to this script) written directly.

Exit codes: 0 graded, 1 could not read or write progress, 2 bad key or usage.
"""

import argparse
import datetime
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

FAILED, CLEAN, FAST = 1, 3, 4

# Copy of INTERVAL in selection.js. Change both.
INTERVAL = {1: 1, 2: 3, 3: 7, 4: 21, 5: 45, 6: 120}

FILE_MODE = 0o644  # match server.py: mkstemp makes 0600 and the rename keeps it
TIMEOUT = 5         # seconds; a server that stays silent this long is stuck, not absent


class GradeError(Exception):
    """A failure the user must see. `code` is the exit code."""

    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def next_box(current, grade, kind):
    """Twin of nextBox() in selection.js. Change both."""
    cur = current or 0
    box = grade
    if grade == FAST:
        box = FAST if cur < 4 else min(cur + 1, 6)
    if kind == "quick" and box == 6 and cur != 6:
        box = 5
    return box


def is_triage(entry):
    """Seeded at box 2 and never graded: PRACTICE.md "The triage set"."""
    return entry.get("box") == 2 and not entry.get("attempts") and not entry.get("last")


def quick_grade(entry, result):
    if result == "fail":
        return FAILED
    if is_triage(entry):
        return CLEAN
    if (entry.get("box") or 0) >= 4:
        return FAST
    return CLEAN


# Twin of PREV_FIELDS in selection.js. Change both.
PREV_FIELDS = ("box", "due", "last", "attempts", "kind")


def prev_of(entry):
    """Twin of prevOf(). A field the entry never had stays out."""
    return {f: entry[f] for f in PREV_FIELDS if f in entry}


def regrade_base(entry, today_iso):
    """Twin of regradeBase(): a second grade on the same day starts from the
    entry as it was before the first, so the app's re-grade and this CLI agree."""
    if entry.get("last") != today_iso or not isinstance(entry.get("prev"), dict):
        return entry
    base = {k: v for k, v in entry.items() if k not in PREV_FIELDS}
    base.update(entry["prev"])
    return base


def apply_grade(state, key, result, today):
    """Return (old_box, new_entry). Does not mutate `state`.

    Never writes `started`: a quick rep is never a first attempt, and a
    started date would count the problem as new this week (PRACTICE.md).
    The first grade of a day stores `prev`; a same-day grade keeps it.
    """
    entry = state.get(key)
    if not isinstance(entry, dict):
        raise GradeError(f"unknown key {key!r}: not in progress.json", code=2)
    today_iso = today.isoformat()
    base = regrade_base(entry, today_iso)
    box = next_box(base.get("box") or 0, quick_grade(base, result), "quick")
    new = dict(base)
    new.update(
        box=box,
        due=(today + datetime.timedelta(days=INTERVAL[box])).isoformat(),
        last=today_iso,
        attempts=(base.get("attempts") or 0) + 1,
        kind="quick",
    )
    if entry.get("last") != today_iso:
        new["prev"] = prev_of(entry)
    return entry.get("box") or 0, new


# ---------- server path ----------

def _server_url():
    return f"http://localhost:{os.environ.get('PORT') or '8000'}/api/progress"


def _server_get(url):
    """(state, etag), or None when no tracker server answers at `url`."""
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return json.loads(r.read()), r.headers.get("ETag")
    except urllib.error.HTTPError as e:
        # 404: something else serves this port (the app treats it as offline too).
        if e.code == 404:
            return None
        # Reachable but refusing, e.g. an empty or corrupt file. Writing the
        # file behind the server's back is exactly what it is refusing.
        raise GradeError(f"server answered {e.code}: {e.read().decode(errors='replace')}")
    except urllib.error.URLError as e:
        # Only a refused connection proves nothing is listening. A timeout means
        # a server is there but stuck, and the file must be left to it.
        if isinstance(e.reason, ConnectionRefusedError):
            return None
        raise GradeError(f"could not reach {url}: {e.reason}")
    except ConnectionRefusedError:
        return None
    except (TimeoutError, OSError) as e:
        raise GradeError(f"could not reach {url}: {e}")


def _server_post(url, state, etag):
    """True on success, False on a stale revision (409)."""
    body = json.dumps(state).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "If-Match": etag or "0",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT):
            return True
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return False
        raise GradeError(f"server refused the write ({e.code})")
    except (urllib.error.URLError, OSError) as e:
        raise GradeError(f"write to {url} failed, check the tracker before retrying: {e}")


def grade_via_server(key, result, today):
    """(old_box, new_entry), or None when no server is running."""
    url = _server_url()
    for _ in range(2):  # one retry: the tab may have saved between GET and POST
        got = _server_get(url)
        if got is None:
            return None
        state, etag = got
        old_box, new = apply_grade(state, key, result, today)
        if _server_post(url, {**state, key: new}, etag):
            return old_box, new
    raise GradeError("progress changed twice while grading; run it again")


# ---------- file path ----------

def _progress_path():
    return os.environ.get("PREP_PROGRESS") or os.path.join(HERE, "progress.json")


def read_file(path):
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        raise GradeError(f"{path} does not exist")
    # Same rule as server.py: an empty or broken file is an error, never {}.
    try:
        state = json.loads(raw)
    except json.JSONDecodeError as e:
        raise GradeError(f"{path} is not valid JSON ({e})")
    if not isinstance(state, dict):
        raise GradeError(f"{path} holds {type(state).__name__}, not an object")
    return state


def write_file(path, state):
    """Temp file, fsync, rename: the same atomic write as server.py."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(state, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, FILE_MODE)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def grade_via_file(key, result, today):
    path = _progress_path()
    state = read_file(path)
    old_box, new = apply_grade(state, key, result, today)
    state[key] = new
    write_file(path, state)
    return old_box, new


# ---------- CLI ----------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Record a quick-rep grade.")
    parser.add_argument("key", help='progress.json key, e.g. "two_pointers#3"')
    parser.add_argument("result", choices=["pass", "fail"])
    parser.add_argument("--date", type=datetime.date.fromisoformat,
                        default=datetime.date.today(), help="YYYY-MM-DD, default today")
    args = parser.parse_args(argv)

    try:
        graded = grade_via_server(args.key, args.result, args.date)
        if graded is None:
            graded = grade_via_file(args.key, args.result, args.date)
    except GradeError as e:
        print(f"grade.py: {e}", file=sys.stderr)
        return e.code

    old_box, new = graded
    print(f"{args.key}: box {old_box} → {new['box']}, next due {new['due']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
