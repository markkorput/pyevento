import logging
from typing import Any, Callable, Generic, Iterable, TypeVar, Union

log = logging.getLogger(__name__)


T = TypeVar("T")


class Event(Generic[T], list[Callable[[T], Any]]):
    @property
    def is_firing(self) -> bool:
        return self._currentFireCount > 0

    def __init__(self) -> None:
        super().__init__(())
        self._fireCount = 0
        self._currentFireCount = 0
        self._subscribe_queue: list[Callable[[T], None]] = []
        self._unsubscribe_queue: list[Callable[[T], None]] = []

    def subscribe(
        self, subscribers: Union[Callable[[T], None], Iterable[Callable[[T], None]]]
    ) -> "Event[T]":
        """Adds given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the subscription for processing after firing is done
        if callable(subscribers):
            subscribers = [subscribers]

        for s in subscribers:
            self.append(s)

        return self

    def unsubscribe(self, subscriber: Callable[[T], None]) -> "Event[T]":
        """Removes given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        try:
            self.remove(subscriber)
        except KeyError as err:
            log.warning("Event.unsubscribe got unknown handler: {}".format(err))

        return self

    def fire(self, value: T) -> None:
        # count the number of (recursive) fires currently happening
        self._currentFireCount += 1

        # execute all subscribers
        for subscriber in self:
            # the handler might have got unsubscribed
            # inside one of the previous subscribers
            if subscriber not in self._unsubscribe_queue:
                subscriber(value)

        # current fire cycle is done, uncount it
        self._currentFireCount -= 1

        # we're counting the number of fires (mostly for testing purposes)
        self._fireCount += 1

        # only if we're not spropertytill in a recursive fire situation
        if not self.is_firing:
            self._process_queues()

    def _process_queues(self) -> None:
        for subscriber in self._subscribe_queue:
            self.append(subscriber)

        for subscriber in self._unsubscribe_queue:
            self.remove(subscriber)

        # reset processed queues
        self._subscribe_queue = []
        self._unsubscribe_queue = []

    def add(self, subscriber: Callable[[T], None]) -> Callable[[], None]:
        """Same as `subscribe` but returns a callable without arguments
        that can be used to unsubscribe the `subscriber`"""
        if subscriber not in self:
            if self.is_firing:
                self._subscribe_queue.append(subscriber)
            else:
                super().append(subscriber)

        def unsub() -> None:
            self.unsubscribe(subscriber)

        return unsub

    def append(self, subscriber: Callable[[T], None]) -> None:
        self.add(subscriber)

    def remove(self, subscriber: Callable[[T], None]) -> None:
        if self.is_firing:
            self._unsubscribe_queue.append(subscriber)
            return

        if subscriber in self:
            super().remove(subscriber)

    def _equals(self, other: Any) -> bool:
        return id(self) == id(other)

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = fire
    __eq__ = _equals
