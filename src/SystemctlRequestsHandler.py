import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SystemctlRequestsHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))

    def do_GET(self):
        return self._send_response(500, {'result': 'err'})

    def do_POST(self):
        return self._send_response(500, {'result': 'err'})


def run_server(host='127.0.0.1', port=6500):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SystemctlRequestsHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
