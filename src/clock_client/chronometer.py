import logging
import time
from threading import Timer, Lock
from typing import ByteString

from .instant import Instant

logger = logging.getLogger(__name__)


class Chronometer:
    """ A chronometer that can be set using a network date and time source and which 
        subsequently keeps time using a Timer and a monotonic tick counter.
    
        After an instance has been created you may start the chronometer by calling
        the `start` method. Before exiting a program that uses a chronometer, you must
        call `stop` in order to cancel the chronometer's timer thread.
        
        Before a chronometer will keep time, you must provide date and time from a 
        network time source. After obtaining the date and time from a network server,
        call the `set` method to set the time.
        
        At any point while the chronometer is running you may call `set` again to update
        the date and time. 
    """
    
    def __init__(self, refresh_interval: float = 0.125):
        """ Initializes a chronometer instance.

        Args:
            refresh_interval (float, optional): refresh timer interfaval. Defaults to 0.125 seconds.
        """
        self.refresh_interval = refresh_interval
        self._instant: Instant = None
        self._last_sys_clock = None
        self._refresh_timer: Timer = None
        self._lock = Lock()
    
    def _refresh(self):
        if self._instant:
            with self._lock:
                sys_clock = time.monotonic_ns()
                ticks = (sys_clock - self._last_sys_clock) // 1000
                self._instant = self._instant.incr(ticks)
                self._last_sys_clock = sys_clock

        self._refresh_timer = Timer(self.refresh_interval, self._refresh)
        self._refresh_timer.start()

    def is_set(self) -> bool:
        """ Gets the state of a flag indicating whether this chronometer has been set.

        Returns:
            bool: True if this chronometer has been set
        """
        return self._instant is not None

    def is_running(self) -> bool:
        """ Gets the state of a flag indicating whether the chronometer is running.

        Returns:
            bool: True if the chronometer is running; i.e. True if it is keeping time
        """
        return self._refresh_timer is not None

    def read(self) -> Instant:
        """ Gets an Instant that represents this chronometer's current date and time of day """
        with self._lock:
            return self._instant        

    def set(self, instant: Instant):
        """ Sets this chronometer to the given instant.
            If this chronometer isn't running before the call to `set` it is started.

        Args:
            instant (Instant): an instant representing the date and time to set
        """
        with self._lock:
            self._instant = instant
        if not self.is_running():
            self.start()
        
    def start(self):
        self._last_sys_clock = time.monotonic_ns()
        self._refresh_timer = Timer(self.refresh_interval, self._refresh)
        self._refresh_timer.start()
        logger.debug("chronometer started")
    
    def stop(self):
        if self._refresh_timer:
            self._refresh_timer.cancel()
            self._refresh_timer = None
            logger.debug("chronometer stopped")
    