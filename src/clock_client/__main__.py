import argparse
import logging
import sys

from .chronometer import Chronometer
from .client import ClockClient
from .ui.clock import ClockUI
from .ui.led import COLORS

TITLE = "NetClock"
LOCAL_IP = "0.0.0.0"
LOCAL_PORT = 0
SERVER_PORT = 10010
DEFAULT_COLOR = "amber"
DEFAULT_SIZE = 8
BASE_SIZE = 4

def color(value):
    """ Validates a color argument """
    if value not in COLORS:
        raise argparse.ArgumentTypeError(f"color '{value}' is not available; choose from {', '.join(sorted(COLORS.keys()))}")
    return value

def size(value):
    """ Validates a size argument """
    try:
        value = int(value)  # raises value error if can't convert to int
        if value < 1 or value > 20:
            raise ValueError()
        return BASE_SIZE + value - 1
    except ValueError:
        raise argparse.ArgumentTypeError(f"size must be in the range 1..20")
    

def parse_cli():
    """ Parses and validates command line arguments """
    parser = argparse.ArgumentParser()
    parser.prog = TITLE
    parser.add_argument("-c", "--color", type=color, default=DEFAULT_COLOR, help=f"LED display color; {', '.join(sorted(COLORS.keys()))}")
    parser.add_argument("-s", "--size", type=size, default=DEFAULT_SIZE, help=f"LED display size [1..20]")
    parser.add_argument("-p", "--port", type=int, default=SERVER_PORT, help="server port")
    parser.add_argument("-D", "--debug", action="store_true", help="enable debug logging")
    parser.add_argument("host", type=str, help="server hostname or IP address")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_cli()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO)

    chronometer = Chronometer()
    client = ClockClient(LOCAL_IP, LOCAL_PORT, args.host, args.port, chronometer)
    client.start()
     
    ui = ClockUI(chronometer.read, args.color, args.size, TITLE)
    try:
        ui.run()
    except KeyboardInterrupt:
        pass
    
    client.stop()
    if chronometer.is_running():
        chronometer.stop()
