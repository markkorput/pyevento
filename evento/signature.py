from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterable,
    ParamSpec,
    TypeVar,
    Union,
)

from .base import BaseEvent

P = ParamSpec("P")
R = TypeVar("R")


class SignatureEvent(Generic[P, R], BaseEvent):
    def __init__(self, method: Callable[P, R]) -> None:
        super().__init__()
        self._method = method

    def fire(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self._fire(*args, **kwargs)
        return self._method(*args, **kwargs)

    __call__ = fire

    def __iadd__(
        self, subscribers: Union[Callable[P, Any], Iterable[Callable[P, Any]]]
    ) -> "SignatureEvent[P, R]":
        """Adds given `subscriber` and returns this Event"""
        self.append(subscribers)
        return self

    def __isub__(self, subscriber: Callable[P, Any]) -> "SignatureEvent[P, R]":
        """Removes given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        self.remove(subscriber)
        return self

    def append(self, subscribers: Union[Callable[P, Any], Iterable[Callable[P, Any]]]) -> None:
        super().append(subscribers)

    def remove(self, subscriber: Callable[P, Any]) -> None:
        super().remove(subscriber)

    def add(self, subscriber: Callable[P, Any]) -> Callable[[], Any]:
        return super().add(subscriber)


class AsyncSignatureEvent(Generic[P, R], BaseEvent):
    def __init__(self, method: Callable[P, Awaitable[R]]) -> None:
        super().__init__()
        self._method = method

    async def fire(self, *args: P.args, **kwargs: P.kwargs) -> R:
        for subscriber in self._iter():
            await subscriber(*args, **kwargs)

        return await self._method(*args, **kwargs)

    __call__ = fire

    def __iadd__(
        self, subscribers: Union[Callable[P, Awaitable[Any]], Iterable[Callable[P, Awaitable[Any]]]]
    ) -> "AsyncSignatureEvent[P, R]":
        """Adds given `subscriber` and returns this Event"""
        self.append(subscribers)
        return self

    def __isub__(self, subscriber: Callable[P, Awaitable[Any]]) -> "AsyncSignatureEvent[P, R]":
        """Removes given `subscriber` and returns this Event"""
        # only modify self if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        self.remove(subscriber)
        return self

    def append(
        self, subscribers: Union[Callable[P, Awaitable[Any]], Iterable[Callable[P, Awaitable[Any]]]]
    ) -> None:
        super().append(subscribers)

    def remove(self, subscriber: Callable[P, Awaitable[Any]]) -> None:
        super().remove(subscriber)

    def add(self, subscriber: Callable[P, Awaitable[Any]]) -> Callable[[], Any]:
        return super().add(subscriber)
