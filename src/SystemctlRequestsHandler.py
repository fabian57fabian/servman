import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from src.SystemctlHelper import manage_systemctl_service, get_systemctl_service_state


class SystemctlRequestsHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))

    def _build_answer(self, state: bool, message: str) -> dict:
        s = 'ok' if state else 'error'
        return {'state': s, 'message': message}

    def _read_json_data(self) -> Optional[dict]:
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data) if post_data else {}
            return data
        except Exception as e:
            return None

    def _parse_query_params(self) -> Optional[dict]:
        # Parse the query parameters manually
        try:
            query_params = {}
            if '?' in self.path:
                query_string = self.path.split('?', 1)[1]
                for param in query_string.split('&'):
                    key, value = param.split('=')
                    query_params[key] = value
            return query_params
        except Exception as e:
            return None

    def do_GET(self):
        try:
            api = self.path.split('?', 1)[0]
            if api == '/api/service/state':
                return self.do_GET_safe()
            else:
                return self._send_response(400, "Bad request")
        except Exception as e:
            print("Unable to process GET: " + str(e))
            error_message = self._build_answer(False, 'Unable to process request')
            return self._send_response(500, error_message)

    def do_GET_safe(self):
        # Handle GET request with "servicename" parameter
        query_params = self._parse_query_params()
        if query_params is None or "servicename" not in query_params:
            error_message = self._build_answer(False, 'Missing required params in GET request')
            return self._send_response(400, error_message)
        service_name = query_params["servicename"]
        res = get_systemctl_service_state(service_name)
        response = self._build_answer(True, 'Correctly checked')
        response['result'] = res
        self._send_response(200, response)

    def do_POST(self):
        try:
            api = self.path.split('?', 1)[0]
            if api == '/api/service/manage':
                return self.do_POST_safe()
            else:
                return self._send_response(400, "Bad request")
        except Exception as e:
            print("Unable to process POST: " + str(e))
            error_message = self._build_answer(False, 'Unable to process request')
            return self._send_response(500, error_message)

    def do_POST_safe(self):
        # Handle POST request
        query_params = self._parse_query_params()
        if query_params is None or "servicename" not in query_params or "mode" not in query_params:
            error_message = self._build_answer(False, 'Missing required params in POST request')
            return self._send_response(400, error_message)

        state_mode = str(query_params["mode"]).lower()
        if state_mode not in ["stop", "start", "restart"]:
            error_message = self._build_answer(False, "Unknown parameter for 'mode'")
            return self._send_response(400, error_message)

        service_name = query_params["servicename"]

        res = manage_systemctl_service(state_mode, service_name)
        response = self._build_answer(True, '{} {} done'.format(state_mode, service_name))
        response['result'] = res
        self._send_response(200, response)


def run_server(host='127.0.0.1', port=1200):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SystemctlRequestsHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
