from unittest import TestCase
from src.SystemctlHelper import manage_systemctl_service, get_systemctl_service_state

class Test(TestCase):
    def setUp(self):
        self.servicename = "dmesg"

    def test_manage_systemctl_service(self):
        res = manage_systemctl_service(self.servicename, "status")

        assert res is int

    def test_get_systemctl_service_state(self):
        res = get_systemctl_service_state(self.servicename)

        assert res is int
