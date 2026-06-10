#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Tiny local server so lesson quizzes can record results.

- Serves the repo statically (open http://127.0.0.1:8753/lessons/index.html).
- Accepts POST /record  with {address, answers, ts}, grades via
  record_attempt.record(), stores to the DB, and returns the score JSON
  (including per-question explanations) back to the page.

Run:
    uv run scripts/serve.py
"""
import json
import pathlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import build_index     # same directory; rebuild results.json after each attempt
import record_attempt  # same directory; uv runs from repo via path below

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8753
HOST = "0.0.0.0"  # all interfaces, so other devices on the LAN (iPad) can study


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        # Never cache: lessons and results.json change as you study, and a
        # stale cached results.json is the classic "no data yet" gotcha.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def _blocked(self) -> bool:
        # Never serve answer keys or the DB over HTTP; grading reads them
        # from disk server-side. Matters once we listen beyond loopback.
        return ".answers.json" in self.path or self.path.startswith("/db/")

    def do_GET(self):
        if self._blocked():
            self.send_error(403, "Not served")
            return
        super().do_GET()

    def do_HEAD(self):
        if self._blocked():
            self.send_error(403, "Not served")
            return
        super().do_HEAD()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path.rstrip("/") != "/record":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        try:
            out = record_attempt.record(payload["address"], payload.get("answers", {}))
            build_index.main()  # refresh results.json so the page is live on reload
            body = json.dumps(out).encode()
            self.send_response(200)
        except Exception as e:  # noqa: BLE001
            body = json.dumps({"error": str(e)}).encode()
            self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(body)


def _lan_ip() -> str | None:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))  # never sends traffic; just picks the route
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def main() -> None:
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT}")
    print(f"Lessons index: http://127.0.0.1:{PORT}/lessons/index.html")
    print(f"Results:       http://127.0.0.1:{PORT}/harness/results.html")
    ip = _lan_ip()
    if ip:
        print(f"On your LAN (iPad etc.): http://{ip}:{PORT}/lessons/index.html")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
