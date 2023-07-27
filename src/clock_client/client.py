from datetime import date
import logging
import selectors
import socket
from threading import Thread, Event
import time
from typing import ByteString
from .chronometer import Chronometer
from .instant import Instant


logger = logging.getLogger(__name__)

SELECT_TIMEOUT = 0.250
BUFFER_SIZE = 512

TAG_HELLO = 0
TAG_DATE = 1
TAG_TIME = 2

LENGTH_HELLO = 2
LENGTH_DATE = 4
LENGTH_TIME = 4

class ClockClient:
    """ The client communication module. 
        A single instance of this type is created in the main entry point of the client program.
    """
    
    def __init__(self, local_ip: str, local_port: int, server_ip: str, server_port: int, chronometer: Chronometer):
        """ Initializes a clock client instance.

        Args:
            local_ip (str): local IP address for the client's UDP socket
            local_port (int): local port for the client client's UDP socket
            server_ip (str): IP address for the server's UDP socket
            server_port (int): port for the server's UDP socket
            chronometer (Chronometer): the chronometer instance to be updated using
                network date and time
        """
        self.local_address = (local_ip, local_port)
        self.server_address = (server_ip, server_port)
        self.chronometer = chronometer
        self._thread = Thread(target=self._run)
        self._shutdown = Event()
        self._hello_interval = 0
        self._last_hello_time = 0


    def start(self):
        """ Starts the service thread for the client communication module.
            This method is called from the main thread of the client program. It
            must start a new thread and return to the caller.
            
            The entry point method for the new thread will subscribe to the server,
            receive and process date and time updates, and periodically renew the 
            subscription with the server.
        """
        self._thread.start()
        logger.debug("communication module started")
        
    def stop(self):
        """ Stops the service thread for the client communication module in preparation
            for client program shutdown. This method must signal to the service thread
            that it should exit and then it must `join` the service thread to await the
            thread's termination before returning.
        """
        self._shutdown.set()
        self._thread.join()


    def _to_int(byte: bytes) -> int:
        return int.from_bytes(byte, 'big')
    
    # def _decode_date(self, date: ByteString):
    #     try:
    #         if len(date) != 4:
    #             raise ValueError("Date field should not have a value of length more than 4 octets")
    #         flag = date[0] << 7
    #         week_day = self._to_int(date[0] & 0b111)
    #         year = self._to_int(date[1] + 2000)
    #         if flag:
    #             year += 100
    #         month = self._to_int(date[2])
    #         month_day = self._to_int(date[3])
    #         return week_day, year, month, month_day
    #     except ValueError:
    #         logger.error(ValueError)
    #         return None

    # def _decode_time(self, time: ByteString):
    #     try:
    #         if len(time) != 4:
    #             raise ValueError("Time field should not have a value of length more than 4 octets")
    #         hour = self._to_int(time[0])
    #         minute = self._to_int(time[1])
    #         second = self._to_int(time[2])
    #         centi_second = self._to_int(time[3])
    #         return hour, minute, second, centi_second
    #     except ValueError:
    #         logger.error(ValueError)
    #         return None

    def _handle_input(self, data: ByteString):
        date, time = None, None
        logger.info("handling input")
        for tag, value in self._tlv_reader(data):
            logger.info(f"Tag: {tag}, \t Value: {value}")
            if tag == TAG_HELLO:
                print(value)
                self._hello_interval = value
            elif tag == TAG_DATE:
                date = value
            elif tag == TAG_TIME:
                time = value
            else:
                # Invalid tag, skip this iteration and get the next tag and value
                continue
        if date and time:
            logger.info("Received datetime")
            print("Recieved date and time")
            instant = self._decode_instant(date, time)
            self.chronometer.set(instant)


    def _decode_instant(self, date, time):
        week  = int(date / 16777216) % 16
        year  = int(date / 65536) % 256
        year  = int(year / 16) * 10 + year % 16
        month = int(date / 256) % 256
        month = int(month / 16) * 10 + month % 16
        day   = date % 256
        day   = int(day / 16) * 10 + day % 16
        hours = int(time / 16777216) % 256
        hours = int(hours / 16) * 10 + hours % 16
        minutes = int(time / 65536) % 256
        minutes = int(minutes / 16) * 10 + minutes % 16
        seconds = int(time / 256) % 256
        seconds = int(seconds / 16) * 10 + seconds % 16
        centi = time % 256
        centi = int(centi / 16) * 10 + centi % 16
        #year = int.from_bytes(date[0:2], "big")
        #month = date[2]
        #day = date[3]
        #hours = time[0]
        #minutes = time[1]
        #seconds = time[2]
        logger.info(f"Year:   \t{year}")
        logger.info(f"Month:  \t{month}")
        logger.info(f"Day:    \t{day}")
        logger.info(f"Week:   \t{week}")
        logger.info(f"Hour:   \t{hours}")
        logger.info(f"Minute: \t{minutes}")
        logger.info(f"Second: \t{seconds}")
        logger.info(f"Centi:  \t{centi}")
        return Instant(year, month, day, week, hours, minutes, seconds, centi)


    def _create_hello(self):
        message = bytearray()
        tag = int(TAG_HELLO)
        length = int(0)
        tag_length = self._tag_length(tag, length)
        print("Entered create hello")
        print(tag_length)
        message.append(tag_length)
        return message  

    def _tag_length(self, tag, length):
        return (tag << 8) | length

    def _tlv_reader(self, data):
        logger.info(f"Received Data: {data}")
        for i in data: print(hex(i))
        index = 0
        while index < len(data):
            if index + 2 > len(data):
                # Not enough elements to decode TLV, break loop
                break
            tag = data[index]
            length = tag % 16
            tag = int(tag / 16)
            #logger.info(f"Tag: {tag}, \t Length: {length}")
            #index += 1
            #length = data[index]
            index += 1
            if index + length > len(data):
                # Not enough elements to decode TLV value, break loop
                break
            value = int.from_bytes(data[index : index + length], "big")
            index += length
            # create a generator that can be iterated over
            # tuple of (tlv_type, tlv_value)
            yield tag, value

        
    def _send_hello(self, max_attempts=5):
        attempt = 0
        while attempt < max_attempts:
            hello_delta = time.monotonic() - self._last_hello_time
            print("hello_delta: ", hello_delta)
            print("_hello_interval: ", self._hello_interval)
            if hello_delta >= self._hello_interval:
                try:
                    message = self._create_hello()
                    print("Message to send: ", message)
                    self._socket.sendto(message, self.server_address)
                    print("Message sent: ", message)
                    self._last_hello_time = time.monotonic()
                    if self._hello_interval == 0:
                        self._hello_interval = 10
                    return
                except Exception as e:
                    attempt += 1
                    logger.error(f"Error occurred while sending hello: {e}")
                    time.sleep(self._hello_interval)
            else:
                time.sleep(self._hello_interval - hello_delta)
        raise Exception("Failed to send hello after multiple attempts")




    def _open_socket(self):
        """ Open a UDP socket and bind it to a local address.

        Returns:
            The new socket object.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.local_address)
        return sock
    
    def _run(self):
        logger.info("running")
        self._socket = self._open_socket()
        selector = selectors.DefaultSelector()
        selector.register(self._socket, selectors.EVENT_READ)
        while not self._shutdown.is_set():
            self._send_hello()
            print("Successfully sent hello")
            try:
                if selector.select(SELECT_TIMEOUT):
                    data = self._socket.recv(BUFFER_SIZE)
                    self._handle_input(data)
            except OSError as err:
                logger.error(f"receive error: {err}")

        self._socket.close()