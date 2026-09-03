from __future__ import annotations

import argparse
import socket
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"



class PSNOVAThreadingHTTPServer(ThreadingHTTPServer):
    request_queue_size = socket.SOMAXCONN
    allow_reuse_address = True
    daemon_threads = True


class PSNOVARequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def translate_path(self, path: str) -> str:
        request_path = urlsplit(path).path
        if request_path == "/PSNOVA":
            request_path = "/PSNOVA/"
        if request_path.startswith("/PSNOVA/"):
            request_path = request_path[len("/PSNOVA"):]
        return super().translate_path(request_path)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()

    handler = partial(PSNOVARequestHandler, directory=str(DOCS))
    server = PSNOVAThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
