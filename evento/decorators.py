from typing import Any, Callable

from .complex import ComplexEvent, P, T
from .event import Event

Method = Callable[..., Any]
Observer = Callable[..., Any]


def event(method: Callable[P, T]) -> ComplexEvent[P, T]:
    return ComplexEvent(method)  # type: ignore


class BeforeEventMethodWrapper:
    def __init__(self, method: Method) -> None:
        self.method = method
        self.beforeEvent: Event[Any] = Event()

    def run(self, *args: Any, **kwargs: Any) -> None:
        self.beforeEvent(self.beforeEvent)
        self.method(*args, **kwargs)

    def subscribe(self, observer: Observer) -> "BeforeEventMethodWrapper":
        self.beforeEvent += observer
        return self

    def unsubscribe(self, observer: Observer) -> "BeforeEventMethodWrapper":
        self.beforeEvent -= observer
        return self

    __call__ = run
    __iadd__ = subscribe
    __isub__ = unsubscribe


def triggers_before_event(method: Method) -> BeforeEventMethodWrapper:
    return BeforeEventMethodWrapper(method)


class AfterEventMethodWrapper:
    def __init__(self, method: Method) -> None:
        self.method = method
        self.afterEvent: Event[Any] = Event()

    def run(self, *args: Any, **kwargs: Any) -> None:
        self.method(*args, **kwargs)
        self.afterEvent(self.afterEvent)

    def subscribe(self, observer: Observer) -> "AfterEventMethodWrapper":
        self.afterEvent += observer
        return self

    def unsubscribe(self, observer: Observer) -> "AfterEventMethodWrapper":
        self.afterEvent -= observer
        return self

    __call__ = run
    __iadd__ = subscribe
    __isub__ = unsubscribe


def triggers_after_event(method: Method) -> AfterEventMethodWrapper:
    return AfterEventMethodWrapper(method)


class AroundEventMethodWrapper:
    def __init__(self, method: Method) -> None:
        self.method = method
        self.beforeEvent: Event[Event[Any]] = Event()
        self.afterEvent: Event[Event[Any]] = Event()

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.beforeEvent(self.beforeEvent)
        self.method(*args, **kwargs)
        self.afterEvent(self.afterEvent)

    def subscribe(self, before: Observer, after: Observer) -> None:
        self.beforeEvent += before
        self.afterEvent += after


def triggers_beforeafter_events(method: Method) -> AroundEventMethodWrapper:
    return AroundEventMethodWrapper(method)
