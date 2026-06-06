#!/usr/bin/env python3
"""
Feedback server for Documental Infancia gallery.
Serves: gallery page, images, and accepts feedback submissions.
Run: python3 feedback_server.py
"""

import http.server
import json
import os
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8765

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
IMAGES_SRC = Path("/Users/pat/Desktop/CdtAI Assets")
FEEDBACK_FILE = SCRIPT_DIR / "feedback_data.json"
IMAGES_JSON = SCRIPT_DIR / "images.json"
HTML_FILE = SCRIPT_DIR / "index.html"

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}


class FeedbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Serve the main page
        if path == "/" or path == "/index.html":
            self.serve_file(HTML_FILE, "text/html; charset=utf-8")
            return

        # Serve images.json
        if path == "/images.json":
            self.serve_file(IMAGES_JSON, "application/json; charset=utf-8")
            return

        # Serve feedback data
        if path == "/api/feedback":
            self.send_json(self.load_feedback())
            return

        # Serve image files from CdtAI Assets
        if path.startswith("/images/"):
            rel = path[len("/images/"):]
            # Search in subdirectories
            for subdir in ["characterSheets", "Location", "Escenas", "Storyboards", "Ref/CDT.C1_JPG_Masters", "."]:
                src = IMAGES_SRC / subdir / rel
                if src.exists() and src.is_file():
                    ext = src.suffix.lower()
                    mime = MIME_TYPES.get(ext, "application/octet-stream")
                    self.serve_file(src, mime)
                    return
            self.send_error(404, f"Image not found: {rel}")
            return

        self.send_error(404, f"Not found: {path}")

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/feedback":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                self.send_json({"status": "error", "message": "Invalid JSON"}, 400)
                return

            # Save feedback
            feedback = self.load_feedback()
            feedback.append({
                "id": len(feedback) + 1,
                "timestamp": payload.get("timestamp", datetime.now().isoformat()),
                "items": payload.get("feedback", []),
            })
            self.save_feedback(feedback)

            print(f"\n📬 FEEDBACK RECIBIDO ({len(feedback[-1]['items'])} imágenes)")
            for item in feedback[-1]["items"]:
                icon = {"approve": "✅", "reject": "❌", "changes": "✏️"}.get(item["action"], "❓")
                print(f"  {icon} {item['title']} → {item['action'].upper()}")
                if item.get("text"):
                    print(f"     📝 {item['text']}")

            self.send_json({
                "status": "ok",
                "message": f"Feedback saved ({len(payload.get('feedback',[]))} images)",
                "id": feedback[-1]["id"],
            })
            return

        self.send_error(404)

    def serve_file(self, path, mime_type):
        try:
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def load_feedback(self):
        if FEEDBACK_FILE.exists():
            try:
                with open(FEEDBACK_FILE) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_feedback(self, data):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def log_message(self, format, *args):
        # Quieter logging
        msg = format % args
        if "File not found" in msg or len(args) > 0:
            sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")


def main():
    server = http.server.HTTPServer((HOST, PORT), FeedbackHandler)
    print(f"🎬 Documental Infancia — Feedback Server")
    print(f"📍 http://192.168.1.35:{PORT}")
    print(f"📁 Images from: {IMAGES_SRC}")
    print(f"💾 Feedback saved to: {FEEDBACK_FILE}")
    print(f"\nAbrí http://192.168.1.35:{PORT} desde tu celular en la misma WiFi")
    print("Presioná Ctrl+C para detener.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido.")
        server.server_close()


if __name__ == "__main__":
    main()
