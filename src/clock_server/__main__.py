import argparse
import logging
import sys

from .repository import SubscriberRepository
from .server import ClockServer

LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 10010
DEAD_INTERVAL_SECONDS = 120
REFRESH_INTERVAL_SECONDS = 30


def parse_cli():
    """ Parses and validates command line arguments """
    parser = argparse.ArgumentParser()
    parser.prog = "netclock"
    parser.add_argument("-i", "--interface", type=str, default=LOCAL_IP, help="address of network interface on which to listen")
    parser.add_argument("-p", "--port", type=int, default=LOCAL_PORT, help="UDP port on which to communicate")
    parser.add_argument("-d", "--dead-interval", type=int, default=DEAD_INTERVAL_SECONDS, 
                        help="interval at which subscribers are required to send HELLO messages")
    parser.add_argument("-r", "--refresh-interval", type=float, default=REFRESH_INTERVAL_SECONDS, 
                        help="interval at which date/time updates will be sent to all subscribers")
    parser.add_argument("-D", "--debug", action="store_true", help="enable debug logging")
    parser.add_argument("--ref", action="store_true", help="enable reference implementation")
    parser.add_argument("output_file", type=str, help="directory path for subscriber database")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_cli()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s %(threadName)s %(message)s")
    
    subscriber_repository = SubscriberRepository(args.output_file)
    
    server = ClockServer(args.interface, args.port, args.dead_interval, args.refresh_interval, 
                         subscriber_repository)
    
    server.run()