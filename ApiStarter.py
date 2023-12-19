import argparse
from src.SystemctlRequestsHandler import run_server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", type=str, default="127.0.0.1", help="Exposed host, e.g. 127.0.0.1 or 0.0.0.0")
    parser.add_argument("-port", type=int, default=1200, help="Exposed Port, e.g. 1200")
    parser.add_argument("-services", type=lambda s: s, nargs='+', help="Allowed services")
    args = parser.parse_args()
    services = args.services
    run_server(services, args.host, args.port)
