import logging
from typing import Any, Callable, List, Set

log = logging.getLogger(__name__)

Observer = Any


class Event:
    def __init__(self) -> None:
        self._subscribers: Set[Observer] = set()
        self._fireCount = 0
        self._currentFireCount = 0
        self._subscribe_queue: List[Observer] = []
        self._unsubscribe_queue: List[Observer] = []

    def subscribe(self, subscriber: Observer) -> "Event":
        # only modify the _subscribers set if we're not currently firing
        # otherwise queue the subscription for processing after firing is done
        if self.isFiring():
            self._subscribe_queue.append(subscriber)
            return self

        self._subscribers.add(subscriber)
        return self

    def unsubscribe(self, subscriber: Observer) -> "Event":
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

    def hasSubscriber(self, subscriber: Observer) -> bool:
        return subscriber in self._subscribers

    def fire(self, *args: Any, **kargs: Any) -> None:
        # count the number of (recursive) fires currently happening
        self._currentFireCount += 1

        # execute all subscribers
        for subscriber in self._subscribers:
            # the handler might have got unsubscribed
            # inside one of the previous subscribers
            if subscriber not in self._unsubscribe_queue:
                subscriber(*args, **kargs)

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

    def add(self, subscriber: Observer) -> Callable[[], None]:
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
