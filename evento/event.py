from typing import Any, Callable, Generic, Iterable, TypeVar, Union

from .base import BaseEvent

T = TypeVar("T")


class Event(Generic[T], BaseEvent):
    def fire(self, value: T) -> None:
        self._fire(value)

    __call__ = fire

    def __iadd__(
        self, subscribers: Union[Callable[[T], Any], Iterable[Callable[[T], Any]]]
    ) -> "Event[T]":
        """Adds given `subscriber` and returns this Event"""
        self.append(subscribers)
        return self

    def __isub__(self, subscriber: Callable[[T], Any]) -> "Event[T]":
        """Removes given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        self.remove(subscriber)
        return self

    def append(self, subscribers: Union[Callable[[T], Any], Iterable[Callable[[T], Any]]]) -> None:
        super().append(subscribers)

    def remove(self, subscriber: Callable[[T], Any]) -> None:
        super().remove(subscriber)

    def add(self, subscriber: Callable[[T], Any]) -> Callable[[], Any]:
        return super().add(subscriber)
