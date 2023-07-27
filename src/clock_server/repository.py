import json
import logging
import os
import shutil

from typing import Iterable, Set

from .subscriber import ClockSubscriber

from threading import Thread, Event
from queue import Queue, Empty

logger = logging.getLogger(__name__)


class SubscriberRepository:
    """ A persistent repository of subscribers """

    def __init__(self, output_filename: str):
        """ Initializes a repository instance.

        Args:
            output_filename (str): output file path
        """
        self.output_filename = output_filename
        basename, suffix = os.path.splitext(output_filename)
        self.backup_filename = f"{basename}_backup{suffix}"
        self._thread = Thread(target=self._run)
        self._queue = Queue()
        self._shutdown = Event()
        self._subscribers = set()

    def _run(self):
        while not self._shutdown.is_set():
            try:
                action, subscriber = self._queue.get(timeout=0.250)
                action(subscriber)
            except Empty:
                pass

    def _load(self) -> Set[ClockSubscriber]:
        """ Loads a set of subscribers from a JSON file using the configured filename.

        Returns:
            Set[ClockSubscriber]: set of subscribers; empty set if the file does not exist
                or contains no subscribers
        """
        addresses = None
        if os.path.exists(self.output_filename):
            try:
                with open(self.output_filename, "r") as input_file:
                    addresses = json.load(input_file)
            except (OSError, json.JSONDecodeError) as err:
                logger.warning(f"failed to load subscribers from {self.output_filename}: {err}")
        
        return {ClockSubscriber(tuple(address)) for address in addresses} if addresses else set()

    def _save(self, subscribers: Iterable[ClockSubscriber]):
        """ Saves a set of subscribers as a JSON file using the configured filename.

        Args:
            subscribers (Iterable[ClockSubscriber]): an iterable of subscriber objects to be saved
        """
        if os.path.exists(self.output_filename):
            try:
                shutil.copyfile(self.output_filename, self.backup_filename)
                logger.debug(f"copied {self.output_filename} to {self.backup_filename}")
            except OSError as err:
                logger.warning(f"failed to copy {self.output_filename} to {self.backup_filename}: {err}")

        try:
            with open(self.output_filename, "w") as output_file:
                json.dump(sorted([list(subscriber.address) for subscriber in subscribers]), output_file, indent=2)
            logger.debug(f"stored subscribers in {self.output_filename}")
            logger.info(f"saved subscribers")
        except OSError as err:
            logger.warning(f"failed to save subscribers to {self.output_filename}: {err}")                
    
    def start(self) -> Iterable[ClockSubscriber]:
        """ Loads the persistent record of subscribers (if any) and starts the thread
            that services the queue of requests to add/discard subscribers.

        Returns:
            Iterable[ClockSubscriber]: an iterable of all subscribers that were loaded
                from persistent storage
        """
        subscribers = self._load()
        self._subscribers = subscribers
        self._thread.start()
        logger.debug("repository started")
        return set(subscribers)
        
    
    def stop(self):
        """ Stops the thread that services the queue of requests to add/discard subscribers
            in preparation for server shutdown. 
        """
        self._shutdown.set()
        self._thread.join()
        logger.debug("repository stopped")

    def _add(self, subscriber: ClockSubscriber):
        if subscriber not in self._subscribers:
            self._subscribers.add(subscriber)
            self._save(self._subscribers)
    
    def add(self, subscriber: ClockSubscriber):
        """ Adds a subscriber to the persistent record of all subscribers.
            This method accepts the request to add the subscriber and returns immediately
            (without blocking); the subscriber will be saved asynchronously.
        Args:
            subscriber (ClockSubscriber): the subscriber to add
        """
        self._queue.put((self._add, subscriber))

    def _discard(self, subscriber: ClockSubscriber):
        if subscriber in self._subscribers:
            self._subscribers.discard(subscriber)
            self._save(self._subscribers)
    
    def discard(self, subscriber: ClockSubscriber):
        """ Discards a subscriber from the persistent record of all subscribers.
            This method accepts the request to discards the subscriber and returns 
            immediately (without blocking); the subscriber will be saved asynchronously.
        Args:
            subscriber (ClockSubscriber): the subscriber to discard
        """
        self._queue.put((self._discard, subscriber))
