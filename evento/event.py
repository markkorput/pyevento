import logging
from typing import Callable, Generic, TypeVar

log = logging.getLogger(__name__)


T = TypeVar("T")


class Event(Generic[T]):
    def __init__(self) -> None:
        self._subscribers: set[Callable[[T], None]] = set()
        self._fireCount = 0
        self._currentFireCount = 0
        self._subscribe_queue: list[Callable[[T], None]] = []
        self._unsubscribe_queue: list[Callable[[T], None]] = []

    def subscribe(self, subscriber: Callable[[T], None]) -> "Event[T]":
        """Adds given `subscriber` and returns this Event"""
        # only modify the _subscribers set if we're not currently firing
        # otherwise queue the subscription for processing after firing is done
        if self.isFiring():
            self._subscribe_queue.append(subscriber)
            return self

        self._subscribers.add(subscriber)
        return self

    def unsubscribe(self, subscriber: Callable[[T], None]) -> "Event[T]":
        """Removes given `subscriber` and returns this Event"""
        # only modify the _subscribers set if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        if self.isFiring():
            self._unsubscribe_queue.append(subscriber)
            return self

        try:
            self._subscribers.remove(subscriber)
        except KeyError as err:
            log.warning("Event.unsubscribe got unknown handler: {}".format(err))

        return self

    def hasSubscriber(self, subscriber: Callable[[T], None]) -> bool:
        return subscriber in self._subscribers

    def fire(self, value: T) -> None:
        # count the number of (recursive) fires currently happening
        self._currentFireCount += 1

        # execute all subscribers
        for subscriber in self._subscribers:
            # the handler might have got unsubscribed
            # inside one of the previous subscribers
            if subscriber not in self._unsubscribe_queue:
                subscriber(value)

        # current fire cycle is done, uncount it
        self._currentFireCount -= 1

        # we're counting the number of fires (mostly for testing purposes)
        self._fireCount += 1

        # only if we're not still in a recursive fire situation
        if not self.isFiring():
            self._processQueues()

    def _processQueues(self) -> None:
        for subscriber in self._subscribe_queue:
            self.subscribe(subscriber)

        for subscriber in self._unsubscribe_queue:
            self.unsubscribe(subscriber)

        # reset processed queues
        self._subscribe_queue = []
        self._unsubscribe_queue = []

    def getSubscriberCount(self) -> int:
        return len(self._subscribers)

    def isFiring(self) -> bool:
        return self._currentFireCount > 0

    def add(self, subscriber: Callable[[T], None]) -> Callable[[], None]:
        """Same as `subscribe` but returns a callable without arguments
        that can be used to unsubscribe the `subscriber`"""
        self.subscribe(subscriber)

        def unsub() -> None:
            self.unsubscribe(subscriber)

        return unsub

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = fire
    __len__ = getSubscriberCount
    __contains__ = hasSubscriber
