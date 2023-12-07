import os


def _send_cmd(cmd: str) -> int:
    try:
        return os.system(cmd)
    except:
        return -1


def manage_systemctl_service(service_name: str, command: str) -> int:
    return _send_cmd("sudo systemctl {} {}".format(command, service_name))


def get_systemctl_service_state(service_name: str) -> int:
    return _send_cmd("systemctl is-active --quiet {}".format(service_name))
