#!/usr/bin/env python3
"""Minimal HTTP API exposing Manglish -> Malayalam conversion.

Endpoints:
    GET  /health
    GET  /convert?text=...&num=5&itc=ml-t-i0-und
    POST /convert   body: {"text": "...", "num": 5, "itc": "ml-t-i0-und"}

Returns JSON: {"input": ..., "candidates": [...], "top": ...}
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import inputtools as manglish

HOST = "0.0.0.0"
PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send(200, {"status": "ok"})
            return
        if parsed.path == "/convert":
            q = parse_qs(parsed.query)
            text = (q.get("text") or [""])[0]
            if not text:
                self._send(400, {"error": "missing 'text'"})
                return
            num = int((q.get("num") or ["5"])[0])
            lang = (q.get("lang") or ["malayalam"])[0]
            itc = (q.get("itc") or [manglish.itc_for(lang)])[0]
            conv = manglish.convert(text, itc=itc, num=num)
            self._send(200, {"input": conv.input, "candidates": conv.candidates, "top": conv.top})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.split("?")[0] != "/convert":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send(400, {"error": "invalid json"})
            return
        text = data.get("text", "")
        if not text:
            self._send(400, {"error": "missing 'text'"})
            return
        num = int(data.get("num", 5))
        itc = data.get("itc") or manglish.itc_for(data.get("lang", "malayalam"))
        conv = manglish.convert(text, itc=itc, num=num)
        self._send(200, {"input": conv.input, "candidates": conv.candidates, "top": conv.top})

    def log_message(self, *args):
        pass


def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"manglish typing api listening on http://{HOST}:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
