from typing import Any, Awaitable, Callable, Generic, Iterable, TypeVar, Union

from .base import BaseEvent

T = TypeVar("T")


class AsyncEvent(Generic[T], BaseEvent):
    async def fire(self, value: T) -> None:
        for subscriber in self._iter():
            await subscriber(value)

    __call__ = fire

    def __iadd__(
        self,
        subscribers: Union[Callable[[T], Awaitable[Any]], Iterable[Callable[[T], Awaitable[Any]]]],
    ) -> "AsyncEvent[T]":
        """Adds given `subscriber` and returns this Event"""
        self.append(subscribers)
        return self

    def __isub__(self, subscriber: Callable[[T], Awaitable[Any]]) -> "AsyncEvent[T]":
        """Removes given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        self.remove(subscriber)
        return self

    def append(
        self,
        subscribers: Union[Callable[[T], Awaitable[Any]], Iterable[Callable[[T], Awaitable[Any]]]],
    ) -> None:
        super().append(subscribers)

    def remove(self, subscriber: Callable[[T], Awaitable[Any]]) -> None:
        super().remove(subscriber)

    def add(self, subscriber: Callable[[T], Awaitable[Any]]) -> Callable[[], Any]:
        return super().add(subscriber)
