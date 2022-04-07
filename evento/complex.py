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

    def __iadd__(self, observer: Callable[P, Any]) -> "ComplexEvent[P, T]":
        self._event += Proxy(observer)
        return self

    def __isub__(self, observer: Callable[P, Any]) -> "ComplexEvent[P, T]":
        proxy = self._find_proxy(observer)
        if proxy:
            self._event -= proxy
        return self

    def __contains__(self, subscriber: Callable[P, Any]) -> bool:
        return self._find_proxy(subscriber) is not None

    def _find_proxy(self, subscriber: Callable[P, Any]) -> Optional[Proxy[P]]:
        return next(
            (
                cast(Proxy[P], p)
                for p in self._event._subscribers
                if isinstance(p, Proxy) and p.observer == subscriber
            ),
            None,
        )

    def append(self, observer: Callable[P, Any]) -> None:
        self.add(observer)

    def remove(self, observer: Callable[P, Any]) -> None:
        self.__isub__(observer)

    def add(self, observer: Callable[P, Any]) -> Callable[[], Any]:
        self += observer
        return lambda: self.remove(observer)

    @property
    def is_firing(self) -> bool:
        return self._event.is_firing

    def __len__(self) -> int:
        return len(self._event)

    __call__ = fire
