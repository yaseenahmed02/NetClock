import logging
import socket
import threading
import datetime

from .repository import SubscriberRepository
from .message import MessageBuilder
from .subscriber import ClockSubscriber
from typing import ByteString

logger = logging.getLogger(__name__)

MAX_DATAGRAM_SIZE = 65536

TAG_HELLO = 0
TAG_DATE = 1
TAG_TIME = 2

LENGTH_HELLO = 2
LENGTH_DATE = 4
LENGTH_TIME = 4

class ClockServer:
    """ The clock server.
        A single instance of this type is created in the main entry point of the server
        program.
    """
    
    def __init__(self, local_ip: str, local_port: int, dead_interval: float, refresh_interval: float,
                 subscriber_repository: SubscriberRepository):
        """ Initializes a server instance.

        Args:
            local_ip (str): local IP address to bind to the server's UDP socket
            local_port (int): local port address to bind to the server's UDP socket
            dead_interval (float): the time interval (in seconds) after which the
                server will assume a client is dead when no HELLO is received from
                the client
            refresh_interval (float): the time interval (in secones) between
                date and time broadcasts to all subscribed clients
            subscriber_repository (ClockSubscriberRepository): a repository that
                will be used to make client subscription's peristent across server
                restarts
        """
        self.dead_interval = dead_interval
        self.refresh_interval = refresh_interval
        self.local_address = (local_ip, local_port)
        self.subscriber_repository = subscriber_repository
        self._lock = threading.Lock()
        self._timer = threading.Timer(self.refresh_interval, self.refresh)
        self._subscribers = set()


    def refresh(self):
        subs_new = set()
        logger.info("refreshing")
        with self._lock:
            now = datetime.datetime.now()
            subs = set(self._subscribers)
            for sub in subs:
                if sub.last_hello is not None and sub.last_hello + datetime.timedelta(seconds=self.dead_interval) < now:
                    self._subscribers.discard(sub)
                    self.subscriber_repository.discard(sub)
                    subs_new = set(self._subscribers)
        message = MessageBuilder()
        message.append_date(now.date())
        message.append_time(now.time())
        message = message.to_bytes()
        logger.info(f"Sending time: " + str(message))
        for sub_new in subs_new:
            sub_new.send(self.serv_sock, message)
        if subs_new:
            self.schedule()
            
    def schedule(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(self.refresh_interval, self.refresh)
        self._timer.start()


    def initialize(self):
        builder = MessageBuilder()
        builder.append_hello(self.dead_interval)
        now = datetime.datetime.now()
        builder.append_date(now.date())
        builder.append_time(now.time())
        bytes = builder.to_bytes()
        for sub in self._subscribers:
            sub.send(self.serv_sock, bytes)
        if self._subscribers:
            self.schedule()

    def update(self, address: tuple):
        new_sub = ClockSubscriber(address)
        subToBe = False
        with self._lock:
            if new_sub not in self._subscribers:
                subToBe = True
                self._subscribers.add(new_sub)
                self.subscriber_repository.add(new_sub)
                new_sub.last_hello = datetime.datetime.now()
        return subToBe, new_sub

    
    def tlv_reader(self, message: ByteString):
        i = 0
        while i + 1 <= len(message):
            tag = message[i] << 4
            length = message[i] & 0xf
            if i + 1 + length > len(message):
                raise ValueError(f"tag {tag} length {length} has short value {value}")
            value = message[i + 1:i + 1 + length]
            yield tag, value
            #yield int.from_bytes(tag, 'big'), value
            i += 1 + len(value)

    def handle_field(self, tag: int, value: bytes, address: tuple):
        print(f"Handling field with tag {tag} and value {value}")
        try:
            if tag != TAG_HELLO:
                raise ValueError(f"Recieved tag from client other than HELLO: {tag}")
            added, sub = self.update(address)
            builder = MessageBuilder()
            builder.append_hello(self.dead_interval)
            if added:
                now = datetime.datetime.now()
                builder.append_date(now.date())
                builder.append_time(now.time())
            message = builder.to_bytes()
            logger.info(f"message: {message}")
            sub.send(self.serv_sock, builder.to_bytes())
            if added:
                self.schedule()
        except ValueError:
            logger.error(ValueError) 

    def handle_input(self, data: ByteString, address):
        for tag, value in self.tlv_reader(data):
            self.handle_field(tag, value, address)

    def run(self):
        """ Run the server.
            This method will be called from the main thread of the server program.
            It will use a loop to receive client messages and a Timer object to
            periodically send date and time broadcasts and age the set of subscribers.
        """
        
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv_sock.bind(self.local_address)
        # self.serv_sock.listen()
        #self.serv_sock.setblocking(False)

        self._subscribers = self.subscriber_repository.start()
        self.initialize()
        print(f"Address is: {self.local_address}")
        try:
            while True:
                print("waiting")
                data, addr = self.serv_sock.recvfrom(MAX_DATAGRAM_SIZE)
                print("received " + str(data))
                self.handle_input(data, addr)
        except KeyboardInterrupt:
            pass
        
        self._timer.cancel()
        self.subscriber_repository.stop()


        
