import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from modules.get_selector import GetSelector
from modules.post_selector import PostSelector
from modules.delete_selector import DeleteSelector


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        result = GetSelector.get_data(self.path)
        if not result:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('404'.encode(encoding='utf-8'))
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        post_data = self.rfile.read(content_length)
        PostSelector.do_method(self.path, post_data)

        self.send_response(200)
        self.end_headers()

    def do_DELETE(self):
        DeleteSelector.delete_row(self.path)
        self.send_response(200)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=Server, port=5000):
    server_address = ('', port)
    http_daemon = server_class(server_address, handler_class)

    print(f'Сервер запущен на порте {port}')
    http_daemon.serve_forever()
