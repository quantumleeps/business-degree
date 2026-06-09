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

import record_attempt  # same directory; uv runs from repo via path below

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8753


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

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
            body = json.dumps(out).encode()
            self.send_response(200)
        except Exception as e:  # noqa: BLE001
            body = json.dumps({"error": str(e)}).encode()
            self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT}")
    print(f"Lessons index: http://127.0.0.1:{PORT}/lessons/index.html")
    print(f"Results:       http://127.0.0.1:{PORT}/harness/results.html")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
