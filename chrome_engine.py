from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import signal
import sys

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        print("Received data")

def shutdown_server(signum, frame):
    print("Shutting down the server...")
    httpd.server_close()

def start_chrome_engine():
    port = 8080
    server_address = ('', port)

    with TCPServer(server_address, MyHandler) as httpd:
        print(f"Server listening on port {port}")
        httpd.serve_forever()
