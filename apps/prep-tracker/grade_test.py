"""Tests for grade.py -- run with: .venv/bin/python -m pytest apps/prep-tracker

Never touches the real progress.json: every run points PREP_PROGRESS at a temp
file and PORT at a port this test owns, so a tracker running on :8000 is never
reached either.
"""
import datetime
import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

import grade

HERE = os.path.dirname(os.path.abspath(__file__))
GRADE = os.path.join(HERE, "grade.py")
SERVER = os.path.join(HERE, "server.py")
TODAY = datetime.date(2026, 10, 12)

FAILED, SLOW, CLEAN, FAST = 1, 2, 3, 4


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    assert port != 8000, "8000 is the real tracker"
    return port


@pytest.fixture(autouse=True)
def never_the_real_tracker(monkeypatch, tmp_path):
    """grade.py defaults to :8000 and the real progress.json. Every test starts
    pointed at a closed port and a temp file, so a test that forgets cannot
    reach either."""
    monkeypatch.setenv("PORT", str(free_port()))
    monkeypatch.setenv("PREP_PROGRESS", str(tmp_path / "never-written.json"))


def entry(**kw):
    base = {"box": 3, "due": "2026-10-01", "last": "2026-09-24", "attempts": 2, "trigger": "note"}
    base.update(kw)
    return base


# ---------- the next-box rule: same cases as selection.test.js ----------

@pytest.mark.parametrize("cur,want", [(0, 4), (1, 4), (2, 4), (3, 4), (4, 5), (5, 6), (6, 6)])
def test_fast_climbs_one_box_from_4_and_holds_at_6(cur, want):
    assert grade.next_box(cur, FAST, "full") == want


@pytest.mark.parametrize("cur", range(7))
def test_failed_slow_clean_set_their_box(cur):
    assert grade.next_box(cur, FAILED, "full") == 1
    assert grade.next_box(cur, SLOW, "full") == 2
    assert grade.next_box(cur, CLEAN, "quick") == 3


def test_missing_box_counts_as_0():
    assert grade.next_box(None, FAST, "new") == 4


def test_quick_rep_cannot_promote_to_box_6():
    assert grade.next_box(5, FAST, "quick") == 5
    assert grade.next_box(4, FAST, "quick") == 5
    assert grade.next_box(6, FAST, "quick") == 6
    assert grade.next_box(6, FAILED, "quick") == 1


def test_interval_matches_selection_js():
    assert grade.INTERVAL == {1: 1, 2: 3, 3: 7, 4: 21, 5: 45, 6: 120}


# ---------- quick-rep result -> grade ----------

def test_fail_is_failed_from_any_box():
    for box in range(7):
        assert grade.quick_grade(entry(box=box), "fail") == FAILED


def test_pass_on_triage_is_clean():
    triage = {"box": 2, "due": "2026-09-01", "last": None, "attempts": 0, "trigger": ""}
    assert grade.quick_grade(triage, "pass") == CLEAN


@pytest.mark.parametrize("box", [4, 5, 6])
def test_pass_on_box_4_and_up_is_fast(box):
    assert grade.quick_grade(entry(box=box), "pass") == FAST


@pytest.mark.parametrize("box", [0, 1, 2, 3])
def test_pass_on_any_other_box_is_clean(box):
    assert grade.quick_grade(entry(box=box), "pass") == CLEAN


def test_box_2_with_a_grade_is_not_triage():
    assert grade.quick_grade(entry(box=2, attempts=1), "pass") == CLEAN
    assert not grade.is_triage(entry(box=2, attempts=1))


# ---------- applying a grade ----------

@pytest.mark.parametrize("old,new", [(4, 5), (5, 5), (6, 6)])
def test_quick_pass_on_high_boxes_respects_the_box_6_cap(old, new):
    _, got = grade.apply_grade({"k#1": entry(box=old)}, "k#1", "pass", TODAY)
    assert got["box"] == new


def test_apply_writes_kind_last_due_and_increments_attempts():
    old_box, got = grade.apply_grade({"k#1": entry(box=4, attempts=2)}, "k#1", "pass", TODAY)
    assert old_box == 4
    assert got["box"] == 5
    assert got["kind"] == "quick"
    assert got["last"] == "2026-10-12"
    assert got["due"] == "2026-11-26"  # +45 days
    assert got["attempts"] == 3
    assert got["trigger"] == "note"


TRIAGE = {"box": 2, "due": "2026-09-01", "last": None, "attempts": 0, "trigger": ""}
LEGACY = {"box": 4, "due": "2026-10-01", "last": "2026-09-10", "attempts": 2, "trigger": ""}


@pytest.mark.parametrize("name,before", [("triage", TRIAGE), ("legacy", LEGACY)])
@pytest.mark.parametrize("result", ["pass", "fail"])
def test_apply_never_writes_started(name, before, result):
    _, got = grade.apply_grade({"k#1": dict(before)}, "k#1", result, TODAY)
    assert "started" not in got, f"{name} {result} must stay a rep, not a new problem"


def test_apply_keeps_an_existing_started():
    _, kept = grade.apply_grade({"k#1": entry(started="2026-01-05")}, "k#1", "fail", TODAY)
    assert kept["started"] == "2026-01-05"


def test_apply_does_not_mutate_the_input():
    state = {"k#1": entry()}
    grade.apply_grade(state, "k#1", "pass", TODAY)
    assert state == {"k#1": entry()}


def test_apply_unknown_key_is_exit_code_2():
    with pytest.raises(grade.GradeError) as e:
        grade.apply_grade({"k#1": entry()}, "nope#9", "pass", TODAY)
    assert e.value.code == 2


# ---------- the CLI, file path (no server listening) ----------

@pytest.fixture
def fixture_file(tmp_path):
    path = tmp_path / "progress.json"
    state = {
        "two_pointers#3": entry(box=4, attempts=1),
        "stacks#1": {"box": 2, "due": "2026-09-01", "last": None, "attempts": 0, "trigger": "t"},
        "sprint#x": {"status": "done", "trigger": ""},
    }
    path.write_text(json.dumps(state, indent=2))
    return path, state


def run_cli(args, progress, port):
    env = dict(os.environ, PREP_PROGRESS=str(progress), PORT=str(port))
    return subprocess.run([sys.executable, GRADE, *args], env=env,
                          capture_output=True, text=True, timeout=30)


def test_cli_file_path_writes_atomically(fixture_file):
    path, before = fixture_file
    r = run_cli(["two_pointers#3", "pass", "--date", "2026-10-12"], path, free_port())
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "two_pointers#3: box 4 → 5, next due 2026-11-26"

    after = json.loads(path.read_text())
    assert after["two_pointers#3"]["box"] == 5
    assert after["two_pointers#3"]["kind"] == "quick"
    assert "started" not in after["two_pointers#3"], "a legacy entry stays a rep"
    assert after["stacks#1"] == before["stacks#1"]
    assert after["sprint#x"] == before["sprint#x"]
    assert oct(path.stat().st_mode)[-3:] == "644"
    assert sorted(os.listdir(path.parent)) == ["progress.json"], "no temp file left behind"


def test_cli_triage_pass_lands_in_box_3(fixture_file):
    path, _ = fixture_file
    r = run_cli(["stacks#1", "pass", "--date", "2026-10-12"], path, free_port())
    assert r.returncode == 0, r.stderr
    got = json.loads(path.read_text())["stacks#1"]
    assert (got["box"], got["attempts"], got["trigger"]) == (3, 1, "t")
    assert "started" not in got


def test_cli_unknown_key_exits_2_and_leaves_the_file(fixture_file):
    path, _ = fixture_file
    raw = path.read_text()
    r = run_cli(["nope#1", "pass"], path, free_port())
    assert r.returncode == 2
    assert "unknown key" in r.stderr
    assert path.read_text() == raw


def test_cli_refuses_an_empty_file(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("")
    r = run_cli(["stacks#1", "pass"], path, free_port())
    assert r.returncode == 1
    assert "not valid JSON" in r.stderr
    assert path.read_text() == ""


# ---------- the CLI, server path ----------

@pytest.fixture
def live_server(tmp_path, fixture_file):
    """The real server.py on a fixture, so the test proves the real If-Match protocol."""
    path, _ = fixture_file
    port = free_port()
    env = dict(os.environ, PREP_PROGRESS=str(path), PORT=str(port))
    proc = subprocess.Popen([sys.executable, SERVER], cwd=HERE, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                with socket.create_connection(("127.0.0.1", port), 0.2):
                    break
            except OSError:
                time.sleep(0.05)
        else:
            pytest.fail("server.py never came up")
        yield path, port
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_cli_server_path_writes_through_the_server(live_server, tmp_path):
    served, port = live_server
    # Point the file fallback somewhere that does not exist: success can then
    # only have come through the server.
    nowhere = tmp_path / "missing" / "progress.json"
    r = run_cli(["two_pointers#3", "fail", "--date", "2026-10-12"], nowhere, port)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "two_pointers#3: box 4 → 1, next due 2026-10-13"
    got = json.loads(served.read_text())["two_pointers#3"]
    assert (got["box"], got["kind"], got["attempts"]) == (1, "quick", 2)
    assert not nowhere.exists()


class StubState:
    def __init__(self, get_status=200):
        self.get_status = get_status
        self.revision = 1
        self.gets = 0
        self.posts = []  # (If-Match, body)
        self.state = {"heaps#1": entry(box=5)}


def stub_server(stub):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            stub.gets += 1
            body = json.dumps(stub.state if stub.get_status == 200 else {"error": "x"}).encode()
            self.send_response(stub.get_status)
            self.send_header("ETag", str(stub.revision))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            # Another writer lands between this GET and the first POST.
            if stub.gets == 1:
                stub.revision = 2

        def do_POST(self):
            want = self.headers.get("If-Match")
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            stub.posts.append((want, body))
            self.send_response(204 if want == str(stub.revision) else 409)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *a):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def test_server_path_retries_once_on_409_with_a_fresh_revision(monkeypatch, capsys):
    """A stub, not server.py: forcing a 409 between GET and POST needs a second
    writer at an exact moment, which a stub can script and a real server cannot."""
    stub = StubState()
    server = stub_server(stub)
    try:
        monkeypatch.setenv("PORT", str(server.server_address[1]))
        assert grade.main(["heaps#1", "pass", "--date", "2026-10-12"]) == 0
    finally:
        server.shutdown()
    assert stub.gets == 2
    assert [want for want, _ in stub.posts] == ["1", "2"]
    assert stub.posts[1][1]["heaps#1"]["box"] == 5, "quick Fast from box 5 stays 5"
    assert "heaps#1: box 5 → 5" in capsys.readouterr().out


def test_server_that_refuses_the_read_is_an_error_not_a_file_write(monkeypatch, tmp_path):
    stub = StubState(get_status=409)
    server = stub_server(stub)
    try:
        monkeypatch.setenv("PORT", str(server.server_address[1]))
        assert grade.main(["heaps#1", "pass"]) == 1
    finally:
        server.shutdown()
    assert stub.posts == []
    assert not (tmp_path / "never-written.json").exists()


# ---------- server_test.py ----------

def test_server_safety_script_passes():
    """server_test.py is a script that runs on import and calls sys.exit, so
    conftest.py keeps pytest from importing it; this runs it the way it expects."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "server_test.py")],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
