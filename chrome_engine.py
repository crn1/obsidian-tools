from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import signal
import sys

def update_global_variables(data):
    global current_url
    global current_html
    try:
        if "<<SEPARATOR>>" not in data:
            # One-line string
            current_url = data
            current_html = ''
            print('URL: ' + current_url)
        else:
            # More than one line
            current_url, current_html = text.split("<<SEPARATOR>>", 1)
            print('URL: ' + current_url)
            print('HTML: ' + current_html)
    except:
        pass

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        update_global_variables(data)

def shutdown_server(signum, frame):
    print("Shutting down the server...")
    httpd.server_close()

def start_chrome_engine():
    port = 8080
    server_address = ('', port)

    with TCPServer(server_address, MyHandler) as httpd:
        print(f"Server listening on port {port}")
        httpd.serve_forever()
