from unittest import TestCase
from src.SystemctlHelper import manage_systemctl_service, get_systemctl_service_state, _send_cmd


class Test(TestCase):
    def setUp(self):
        self.servicename = "counter_test"

    def test_manage_systemctl_service(self):
        res = manage_systemctl_service(self.servicename, "status")

        assert type(res) is int

    def test_get_systemctl_service_state(self):
        res = get_systemctl_service_state(self.servicename)

        assert type(res) is int

    def test__send_cmd(self):
        assert _send_cmd(None) == -1
