# pyevento

[![Build Status](https://travis-ci.org/markkorput/pyevento.svg)](https://travis-ci.org/markkorput/pyevento)
[![PyPI wheel](https://img.shields.io/pypi/wheel/evento?style=flat)](https://pypi.org/project/evento/ "View this project on npm")
[![Github Tag](https://img.shields.io/github/tag/markkorput/pyevento.svg?label=version)](https://github.com/markkorput/pyevento/releases/latest)

Python evento package, making the Observer pattern estúpida sencillo.

## Install

```shell
pip install evento
```

## Basic Usage

```python
from evento import Event

# observers are simply methods
def observer(value: str):
	print("Received: " + value)

# we need to create an instance for every event we want to fire
demo_event: Event[str] = Event()

# subscribe observer to the event
demo_event += observer

# trigger notifications for the event (run all observers)
demo_event('Hello') # => "Received: Hello"
demo_event('World') # => "Received: World"
```

## Typical usage

This is how Events are typically used to decouple code into separate classes;

```python
from evento import Event

class Action:
	def __init__(self, name) -> None:
		self.name = name
		self.run_event = Event[Action]()

	def run(self) -> None:
		self.run_event(self)

class ActionCounter:
	def __init__(self, action: Action) -> None:
		self.count = 0
		# Event.add returns an unsubscribe method
		self._disconnect = action.run_event.add(self._on_action)

	def __del__(self) -> None:
		# observers should make sure to unsubscribe from events when they are done
		self._disconnect()

	def _on_action(self, action: Action) -> None:
		self.count += 1
		print(f"'{action.name}' ran {self.count} times")

action = Action('Foo action')
counter = ActionCounter(action)
action.run() # => "'Foo action' ran 1 times"
action.run() # => "'Foo action' ran 2 times"
```

## Unsubscribe

```python

# setup
event = Event()

def handler(value) -> None:
	print(value)

def setup() -> Callable[[], None]:
	unsubscribe = event.add(handler)
	return unsubscribe

cleanup = setup()

# ... do stuff ...

# cleanup; all the following lines do the same
event -= handler
event.remove(handler)
cleanup()
```

## Async Event

Works the same as `Event` but takes async subscribers and has to be awaited;

```python
from evento import AsyncEvent
event = AsyncEvent[float]()

async def echo_double(value: float) -> None:
	print(f"double: {value * 2}")

event.append(echo_double)
# ...
await event(5.0) # using __call__
await event.fire(10.0) # using fire (same as __call__)
# ...
event.remove(echo_double)
```

## Signature Event

Since version 2.0.0 `evento` is typed and `Event` and `SyncEvent` are generic classes with a single type; they are 'fired' using a single argument, and all subscribers are expected to take one argument of that type.

To support more complex method signatures, the `event` and `async_event` decorator can be used to turn a method into an event;

### Sync

```python
from evento import event
@event
def multi_arg_event(id: int, message: str, price: float, **opts: Any) -> None:
    ...

def observer(id: int, message: str, price: float, **opts: Any) -> None:
    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")

multi_arg_event += observer
multi_arg_event(0, "Hello World!", 9.99, demo=True)
```

### Async

```python
from evento import async_event

async def observer(id: int, message: str, price: float, **opts: Any) -> Any:
    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")

@async_event
async def multi_arg_event(id: int, message: str, price: float, **opts: Any) -> str:
	return "Done"

# the original method is still invoked after all event subscribers have executed
result = await multi_arg_event(1, "Test-12", 9.99, feature=True)
print(f"Result: {result}") # => Done
```
