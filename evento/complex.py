from typing import Any, Callable, Generic, Optional, ParamSpec, TypeVar, cast

from .event import Event

T = TypeVar("T")
P = ParamSpec("P")


class Proxy(Generic[P]):
    def __init__(self, observer: Callable[P, Any]) -> None:
        self.observer = observer

    def __call__(self, value: tuple[tuple[Any, ...], dict[str, Any]]) -> None:
        args, kwargs = value
        self.observer(*args, **kwargs)


class ComplexEvent(Generic[P, T]):
    @property
    def _fireCount(self) -> int:
        return self._event._fireCount

    def __init__(self, method: Callable[P, T]) -> None:
        self._event: Event[Any] = Event()
        self._method = method

    def fire(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self._event((args, kwargs))
        return self._method(*args, **kwargs)

    def subscribe(self, observer: Callable[P, Any]) -> "ComplexEvent[P, T]":
        self._event += Proxy(observer)
        return self

    def unsubscribe(self, observer: Callable[P, Any]) -> "ComplexEvent[P, T]":
        proxy = self._findProxy(observer)
        if proxy:
            self._event -= proxy
        return self

    def hasSubscriber(self, subscriber: Callable[P, Any]) -> bool:
        return self._findProxy(subscriber) is not None

    def _findProxy(self, subscriber: Callable[P, Any]) -> Optional[Proxy[P]]:
        return next(
            (
                cast(Proxy[P], p)
                for p in self._event._subscribers
                if isinstance(p, Proxy) and p.observer == subscriber
            ),
            None,
        )

    def add(self, observer: Callable[P, Any]) -> Callable[[], "ComplexEvent[P, T]"]:
        self.subscribe(observer)
        return lambda: self.unsubscribe(observer)

    def isFiring(self) -> bool:
        return self._event.isFiring()

    def getSubscriberCount(self) -> int:
        return len(self._event)

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = fire
    __len__ = getSubscriberCount
    __contains__ = hasSubscriber
