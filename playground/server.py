"""Локальный Python-плейграунд: страница в браузере + настоящий Python на этом ПК.

Запуск:
    python server.py            # сервер на http://127.0.0.1:8765
    python server.py --open     # то же + сразу открыть страницу в браузере
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import tempfile
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE_DIR = HERE.parent.parent / "site"
HOST = "127.0.0.1"
PORT = 8765
TIMEOUT_SECONDS = 15


def run_code(code: str, stdin_text: str) -> dict:
    """Выполняет код в отдельном процессе и возвращает результат."""
    with tempfile.TemporaryDirectory(prefix="pyplay_") as tmp:
        script = Path(tmp) / "main.py"
        script.write_text(code, encoding="utf-8")

        started = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-u", str(script)],
                input=stdin_text,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_SECONDS,
                cwd=tmp,
            )
            duration = time.perf_counter() - started
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
                "duration": round(duration, 3),
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Превышено время выполнения ({TIMEOUT_SECONDS} с). Возможно, бесконечный цикл.",
                "exit_code": -1,
                "duration": TIMEOUT_SECONDS,
            }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:  # тише в консоли
        pass

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            html = (HERE / "index.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
        elif self.path in ("/game", "/game/", "/game/index.html"):
            page = SITE_DIR / "index.html"
            if page.exists():
                self._send(200, page.read_bytes(), "text/html; charset=utf-8")
            else:
                self._send(404, b"Game page not found", "text/plain; charset=utf-8")
        else:
            self._send(404, b"Not found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        if self.path != "/api/run":
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"

        try:
            payload = json.loads(raw.decode("utf-8"))
            code = payload.get("code", "")
            stdin_text = payload.get("stdin", "")
        except (ValueError, UnicodeDecodeError):
            self._send(400, b'{"error":"bad json"}', "application/json")
            return

        result = run_code(code, stdin_text)
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self._send(200, body, "application/json; charset=utf-8")


def port_is_busy() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex((HOST, PORT)) == 0


def main() -> None:
    url = f"http://{HOST}:{PORT}/"
    open_browser = "--open" in sys.argv

    if port_is_busy():
        print(f"Сервер уже запущен: {url}")
        if open_browser:
            webbrowser.open(url)
        return

    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Плейграунд запущен: {url}")
    print("Остановить: Ctrl+C")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановлено.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
