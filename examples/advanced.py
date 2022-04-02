from typing import Any

from evento import decorators


@decorators.event
def multi_arg_event(id: int, message: str, price: float, **opts: Any) -> Any:
    ...


def observer(id: int, message: str, price: float, **opts: Any) -> Any:
    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")


def observer_with_return_value(id: int, message: str, price: float, **opts: Any) -> Any:
    result = (id, message, price, opts)
    print(f"observer_with_return_value: {result}")
    return result


multi_arg_event.subscribe(observer)
multi_arg_event += observer_with_return_value


multi_arg_event(1, "Test-12", 9.99, feature=True)
