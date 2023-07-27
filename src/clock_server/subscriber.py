import logging
from datetime import datetime
from socket import socket as Socket
from typing import ByteString


logger = logging.getLogger(__name__)

class ClockSubscriber:
    """ A client that has subscribed for date and time updates """

    def __init__(self, address: tuple):
        """ Initializes a subscriber instance.

        Args:
            address (tuple): a 2-tuple consisting of an IP adddress (str) and port (int)
        """
        self.address = address
        self.last_hello: datetime = None
        
    def send(self, socket: Socket, message: ByteString):
        """ Sends a message to this subscriber

        Args:
            socket (Socket): the UDP socket on which to send the message
            message (ByteString): the message to send
        """
        try:
            socket.sendto(message, self.address)
            logger.debug(f"sent message to subscriber {self.address}: {message.hex()}")
        except OSError as err:
            logger.error(f"error sending message to subscriber {self.address}: {err}")

    def __str__(self) -> str:
        """ Produces a string representation of a subscriber """
        return str(self.address)
    
    def __repr__(self) -> str:
        """ Produces a debugging representation of a subscriber """
        return f"{__class__.__name__}(address={self.address}, last_hello={self.last_hello.isoformat() if self.last_hello else None})"

    def __eq__(self, other):
        """ Compares this subscriber to another for logical equality.
            Two different subscriber objects are considered logically equal if they have the same address.
        """
        return self is other or (other, ClockSubscriber) and self.address == other.address
    
    def __hash__(self):
        """ Produces a hash code for this subscriber.
            Since logically equal objects must have equal hashes, the hash is based solely on the address attribute.
        """
        return hash(self.address)