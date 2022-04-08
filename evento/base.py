import logging
from typing import Any, Callable, Generator, Iterable, Union

log = logging.getLogger(__name__)


class BaseEvent:
    @property
    def is_firing(self) -> bool:
        return self._currentFireCount > 0

    def __init__(self) -> None:
        self._subscribers: list[Callable[..., Any]] = []
        self._fireCount = 0
        self._currentFireCount = 0
        self._add_queue: list[Callable[..., Any]] = []
        self._remove_queue: list[Callable[..., Any]] = []

    def _fire(self, *args: Any, **kwargs: Any) -> Any:
        for subscriber in self._iter():
            subscriber(*args, **kwargs)

    def append(self, subscribers: Union[Callable[..., Any], Iterable[Callable[..., Any]]]) -> None:
        if callable(subscribers):
            subscribers = [subscribers]

        for subscriber in subscribers:
            if subscriber not in self._subscribers:
                if self.is_firing:
                    self._add_queue.append(subscriber)
                else:
                    self._subscribers.append(subscriber)

    def remove(self, subscriber: Callable[..., Any]) -> None:
        if self.is_firing:
            self._remove_queue.append(subscriber)
            return

        if subscriber not in self._subscribers:
            log.warning("Got unknown subscriber to remove from event")
            return

        self._subscribers.remove(subscriber)

    def add(self, subscriber: Callable[..., Any]) -> Callable[[], None]:
        """Same as `append` but returns a callable without arguments
        that can be used to unsubscribe the `subscriber`"""
        self.append(subscriber)

        def unsub() -> None:
            self.remove(subscriber)

        return unsub

    def _iter(self) -> Generator[Callable[..., Any], None, None]:
        # count the number of (recursive) fires currently happening
        self._currentFireCount += 1

        # execute all subscribers
        for subscriber in self._subscribers:
            # the handler might have got unsubscribed
            # inside one of the previous subscribers
            if subscriber not in self._remove_queue:
                # self._invoke(subscriber, value)
                yield subscriber

        # current fire cycle is done, uncount it
        self._currentFireCount -= 1

        # we're counting the number of fires (mostly for testing purposes)
        self._fireCount += 1

        # only if we're not still in a recursive fire situation
        if not self.is_firing:
            self._process_queues()

    def _process_queues(self) -> None:
        for subscriber in self._add_queue:
            self.append(subscriber)

        for subscriber in self._remove_queue:
            self.remove(subscriber)

        # reset processed queues
        self._add_queue = []
        self._remove_queue = []

    def __repr__(self) -> str:
        return f"Event(id={id(self)}, len={len(self)})"

    def __eq__(self, other: Any) -> bool:
        return id(self) == id(other)

    def __len__(self) -> int:
        return len(self._subscribers)

    def __contains__(self, subscriber: Callable[..., Any]) -> bool:
        return subscriber in self._subscribers
