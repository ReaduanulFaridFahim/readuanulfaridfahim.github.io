#!/usr/bin/env python3
"""
Local development server for Readuanul Farid Fahim Portfolio.
Features:
- Auto-detects available port (defaults to 8000)
- Auto-opens browser tab
- Disables aggressive caching so edits reflect immediately
- Explicit MIME type mapping for SVGs, WebP, JPEG, XML, etc.
- Safe console encoding for all Windows terminals
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import socket
import argparse
from pathlib import Path

# Ensure UTF-8 output if supported, safely handling legacy Windows code pages
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DIRECTORY = Path(__file__).parent.resolve()

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Prevent browser caching during local development
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def guess_type(self, path):
        # Ensure correct MIME types for modern web assets
        path_str = str(path).lower()
        if path_str.endswith(".svg"):
            return "image/svg+xml"
        if path_str.endswith(".jpg") or path_str.endswith(".jpeg"):
            return "image/jpeg"
        if path_str.endswith(".png"):
            return "image/png"
        if path_str.endswith(".xml"):
            return "application/xml"
        if path_str.endswith(".json"):
            return "application/json"
        return super().guess_type(path)

    def log_message(self, format, *args):
        # Clean terminal logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def find_available_port(start_port=8000, max_attempts=50):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port

def run_server(port=8000, open_browser=True):
    actual_port = find_available_port(port)
    handler = NoCacheHTTPRequestHandler
    
    # Allow socket reuse and multi-threaded request processing
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    
    with http.server.ThreadingHTTPServer(("127.0.0.1", actual_port), handler) as httpd:
        url = f"http://localhost:{actual_port}"
        print("=" * 64)
        print(">> Readuanul Farid Fahim Portfolio - Local Server is LIVE")
        print(f">> Local URL:   {url}")
        print(f">> Root Dir:    {DIRECTORY}")
        print("=" * 64)
        print("Press Ctrl+C to stop the server.\n")
        
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass
            
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down dev server. Goodbye!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start portfolio local server")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()
    
    run_server(port=args.port, open_browser=not args.no_browser)
