#!/usr/bin/env python3
"""
EduAR — Local HTTPS Server
Run this on your laptop, then scan the QR code with your Android phone.
Both devices must be on the same Wi-Fi network.
"""

import http.server, ssl, socket, os, sys, subprocess, tempfile, threading, time, mimetypes

# ── Find local IP ─────────────────────────────────────────────────────────────
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

# ── Generate self-signed cert ─────────────────────────────────────────────────
def make_cert(ip):
    cert_file = os.path.join(tempfile.gettempdir(), "ar_cert.pem")
    key_file  = os.path.join(tempfile.gettempdir(), "ar_key.pem")
    if not os.path.exists(cert_file):
        print("Generating self-signed certificate...")
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", key_file, "-out", cert_file,
            "-days", "1", "-nodes", "-subj",
            f"/CN={ip}",
            "-addext", f"subjectAltName=IP:{ip}"
        ], check=True, capture_output=True)
    return cert_file, key_file

# ── Print QR code in terminal ─────────────────────────────────────────────────
def print_qr(url):
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        print("\n" + "─" * 50)
        print(f"  Scan this QR code with your Android phone:")
        print("─" * 50)
        qr.print_ascii(invert=True)
        print("─" * 50)
        print(f"  Or open manually: {url}")
        print("─" * 50 + "\n")
        print("  ⚠️  Your browser will show a security warning.")
        print("     Tap 'Advanced' → 'Proceed' to continue.\n")
    except Exception:
        print(f"\n  Open on your phone: {url}\n")

# ── HTTP handler — serves all files from the app directory ───────────────────
APP_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Normalise path — strip query string, decode %xx
        path = self.path.split('?')[0]
        try:
            from urllib.parse import unquote
            path = unquote(path)
        except Exception:
            pass

        # Map "/" to index.html
        if path == '/' or path == '':
            path = '/index.html'

        # Resolve to filesystem path (prevent directory traversal)
        rel = path.lstrip('/')
        full_path = os.path.normpath(os.path.join(APP_DIR, rel))
        if not full_path.startswith(APP_DIR):
            self.send_error(403, "Forbidden")
            return

        if not os.path.isfile(full_path):
            self.send_error(404, f"File not found: {rel}")
            return

        mime, _ = mimetypes.guess_type(full_path)
        mime = mime or 'application/octet-stream'

        with open(full_path, 'rb') as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        # Headers needed for WebXR / camera
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"  [{time.strftime('%H:%M:%S')}] {self.path}  →  {args[1]}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    PORT = 8443
    ip   = get_local_ip()
    url  = f"https://{ip}:{PORT}"

    index_path = os.path.join(APP_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"ERROR: index.html not found in {APP_DIR}")
        sys.exit(1)

    cert, key = make_cert(ip)

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)

    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    print_qr(url)
    print(f"  Serving {APP_DIR}")
    print(f"  on {url}  (Ctrl+C to stop)\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")

