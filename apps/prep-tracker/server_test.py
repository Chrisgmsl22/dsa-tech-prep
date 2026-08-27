"""Safety tests for server.py -- run with: python3 apps/prep-tracker/server_test.py

Every case here corresponds to a path that was verified, on 2026-08-21, to
destroy practice history. They are regression guards, not hypotheticals.
Stdlib only, no dependencies. Never touches the real progress.json: the server
under test is pointed at a tempfile via PREP_PROGRESS.
"""
import http.client, json, os, socket, subprocess, sys, tempfile, threading, time

# Layout-independent on purpose: this used to derive the repo root by walking
# up two directories, which broke the moment the app moved into apps/.
# The server is simply the sibling file.
HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(HERE, "server.py")

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

PORT = free_port()
TMP = tempfile.mkdtemp()
PROGRESS = os.path.join(TMP, "progress.json")

env = dict(os.environ, PREP_PROGRESS=PROGRESS, PORT=str(PORT))
proc = subprocess.Popen([sys.executable, SERVER], cwd=HERE, env=env,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wait_up():
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", PORT), 0.2):
                return True
        except OSError:
            time.sleep(0.05)
    return False

results = []
def check(label, cond, got=""):
    results.append(bool(cond))
    print(f"  {'PASS' if cond else 'FAIL'}  {label}" + (f"   [{got}]" if got and not cond else ""))

def req(method, path="/api/progress", body=None, headers=None):
    c = http.client.HTTPConnection("127.0.0.1", PORT, timeout=5)
    c.request(method, path, body=body, headers=headers or {})
    r = c.getresponse()
    data = r.read()
    out = (r.status, dict(r.getheaders()), data)
    c.close()
    return out

JSON = {"Content-Type": "application/json"}

try:
    if not wait_up():
        print("server never came up"); sys.exit(1)

    print("=== GET with no file at all (a genuine first run) ===")
    st, h, b = req("GET")
    check("200", st == 200, st)
    check("body is {}", json.loads(b) == {}, b[:60])
    check('ETag is "0"', h.get("ETag") == "0", h.get("ETag"))

    print("=== POST creates the file ===")
    st, h, b = req("POST", body=json.dumps({"a#1": {"box": 3, "last": "2026-08-21"}}),
                   headers={**JSON, "If-Match": "0"})
    check("204", st == 204, st)
    check("file exists", os.path.exists(PROGRESS))
    check("mode is 0644", oct(os.stat(PROGRESS).st_mode)[-3:] == "644",
          oct(os.stat(PROGRESS).st_mode)[-3:])
    rev1 = h.get("ETag")
    check("returned a new ETag", rev1 and rev1 != "0", rev1)

    print("=== a stale tab cannot revert newer work ===")
    st, h, b = req("POST", body=json.dumps({"wiped": True}),
                   headers={**JSON, "If-Match": "0"})
    check("409 on stale If-Match", st == 409, st)
    check("file untouched", json.load(open(PROGRESS)) == {"a#1": {"box": 3, "last": "2026-08-21"}})

    print("=== a current tab can write ===")
    st, h, b = req("GET")
    rev = h.get("ETag")
    st, h, b = req("POST", body=json.dumps({"a#1": {"box": 4}}), headers={**JSON, "If-Match": rev})
    check("204 with the current ETag", st == 204, st)

    print("=== a client that skips the protocol is refused ===")
    st, _, _ = req("POST", body="{}", headers=JSON)
    check("428 without If-Match", st == 428, st)

    print("=== the CSRF path is closed ===")
    st, _, _ = req("POST", body="{}", headers={**JSON, "If-Match": "*",
                                              "Origin": "https://evil.example.com"})
    check("403 for a foreign Origin", st == 403, st)
    st, _, _ = req("POST", body="{}", headers={"Content-Type": "text/plain", "If-Match": "*"})
    check("415 for text/plain", st == 415, st)
    st, _, _ = req("POST", body="{}", headers={**JSON, "If-Match": "*",
                                              "Origin": f"http://localhost:{PORT}"})
    check("204 for our own Origin", st == 204, st)

    print("=== oversized bodies are refused before being read ===")
    c = http.client.HTTPConnection("127.0.0.1", PORT, timeout=5)
    c.putrequest("POST", "/api/progress")
    c.putheader("Content-Type", "application/json")
    c.putheader("If-Match", "*")
    c.putheader("Content-Length", str(9 * 1024 * 1024))
    c.endheaders()
    try:
        st = c.getresponse().status
    except Exception as e:
        st = f"err {e}"
    check("413 for a 9 MB Content-Length", st == 413, st)
    c.close()

    print("=== an empty or corrupt file is an ERROR, never an empty object ===")
    good = open(PROGRESS).read()
    open(PROGRESS, "w").close()                       # zero bytes
    st, _, b = req("GET")
    check("409 for a zero-byte file", st == 409, st)
    check("the message names the recovery command", b"git checkout" in b)

    open(PROGRESS, "w").write("<<<<<<< HEAD\n{}\n")   # conflict markers
    st, _, b = req("GET")
    check("409 for conflict markers", st == 409, st)

    open(PROGRESS, "w").write("5")                    # a JSON scalar
    st, _, b = req("GET")
    check("409 for a JSON scalar", st == 409, st)

    open(PROGRESS, "w").write(good)                   # restore
    st, _, _ = req("GET")
    check("200 once restored", st == 200, st)

    print("=== a half-open request no longer stalls every other one ===")
    s = socket.create_connection(("127.0.0.1", PORT), 5)
    s.sendall(b"POST /api/progress HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\n"
              b"If-Match: *\r\nContent-Length: 500000\r\n\r\n" + b'{"partial"')
    t0 = time.time()
    try:
        st, _, _ = req("GET")
    except Exception as e:
        st = f"err {e}"
    check("a concurrent GET is still served", st == 200, st)
    print(f"       (served in {time.time() - t0:.2f}s while a POST hung)")
    s.close()

    print("=== path traversal ===")
    st, _, _ = req("GET", "/../CLAUDE.md")
    check("traversal 404s", st in (404, 400), st)

finally:
    proc.terminate()
    proc.wait(timeout=5)

print(f"\nTOTAL: {sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
