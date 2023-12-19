import time
from threading import Thread
from unittest import TestCase
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.SystemctlRequestsHandler import SystemctlRequestsHandler, build_server

import requests


class TestBuildServer(TestCase):
    def test_build_server(self):
        cvr = build_server(['a.service'], 'localhost', 1968)
        assert cvr is not None

    def test_build_server_noservice(self):
        cvr = build_server(None, 'localhost', 1968)
        assert cvr is None

    def test_build_server_wrong_service(self):
        cvr = build_server(["a.service", 1, 4.4], 'localhost', 1968)
        assert cvr is None

class TestSystemctlRequestsHandler(TestCase):
    def setUp(self):
        self.port = 1313
        self.host = "127.0.0.1"
        server_address = (self.host, self.port)
        self.services = ['a.service', 'b.service']
        handler_cls = lambda *args, **kwargs: SystemctlRequestsHandler(*args, services=self.services, **kwargs)
        self.server = HTTPServer(server_address, handler_cls)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()
        time.sleep(1)  # Give some time for the server to start

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
        print("Server stopped.")

    def test_GET_OK(self):
        response = requests.get(f'http://{self.host}:{self.port}/api/service/state', params={"servicename": self.services[0]})

        self.assertEqual(response.status_code, 200)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertIn('result', answer)
        self.assertEqual('ok', answer['state'])
        self.assertEqual('Correctly checked', answer['message'])
        assert type(answer['result']) is int

    def test_GET_service_notallowed(self):
        response = requests.get(f'http://{self.host}:{self.port}/api/service/state', params={"servicename": "328947rh3q8947gf"})

        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertEqual('Service not allowed', answer['message'])

    def test_GET_noparam(self):
        response = requests.get(f'http://{self.host}:{self.port}/api/service/state')

        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertEqual('Missing required params in GET request', answer['message'])

    def test_POST_OK(self):
        params = {'servicename': self.services[0], 'mode': 'start'}
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 200)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertIn('result', answer)
        self.assertEqual('ok', answer['state'])
        self.assertEqual(f'{"start"} {self.services[0]} done', answer['message'])
        assert type(answer['result']) is int

    def test_POST_wrong_mode(self):
        params = {'servicename': self.services[0], 'mode': 'modeaaaaaaaaaaa'}
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertIn("Unknown parameter", answer['message'])

    def test_POST_service_notallowed(self):
        params = {'servicename': "ierubgibgweriop789grbiubiouby8o07b", 'mode': 'start'}
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertIn("not allowed", answer['message'])

    def test_POST_noparam_servicename(self):
        params = {'servicename': self.services[0]}
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertIn("Missing", answer['message'])

    def test_POST_noparam_mode(self):
        params = {'mode': 'start'}
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertIn("Missing", answer['message'])

    def test_POST_noparam_all(self):
        params = None
        response = requests.post(f'http://{self.host}:{self.port}/api/service/manage', params=params)
        self.assertEqual(response.status_code, 400)
        answer = response.json()
        self.assertIn('state', answer)
        self.assertIn('message', answer)
        self.assertEqual('error', answer['state'])
        self.assertIn("Missing", answer['message'])
