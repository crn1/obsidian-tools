from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import signal
import sys

import global_variables

def update_global_variables(data):
    try:
        if "<<SEPARATOR>>" in data:
            # More than one line
            global_variables.current_url, global_variables.current_html = data.split("<<SEPARATOR>>", 1)
            # print('HTML: ' + current_html)
        else:
            # One-line string
            global_variables.current_url = data
            global_variables.current_html = ''

    except Exception as e:
        print(e)

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        update_global_variables(data)

def start_chrome_engine():
    port = 8080
    server_address = ('', port)

    with TCPServer(server_address, MyHandler) as httpd:
        print(f"Server listening on port {port}")
        httpd.serve_forever()
