# pyevento
[![Build Status](https://travis-ci.org/markkorput/pyevento.svg)](https://travis-ci.org/markkorput/pyevento)


Python evento package, making the Observer pattern estúpida sencillo.

## Install

```shell
pip install evento
```

## Usage

```python
from evento import Event

# observers are simply methods
def observer(param1, param2):
	print(', '.join([param1, param2]))

# we need to create an instance for every event we want to fire
demo_event = Event()

# subscribe observer to the event
demo_event += observer

# trigger notifications for the event (run all observers)
demo_event('Hello', 'World') # => "Hello, World"
```

## Usage within classes

This is how Events are typically used to decouple code into separate classes;

```python
from evento import Event

class Action:
	def __init__(self, name):
		self.name = name
		self.runEvent = Event()

	def run(self):
		# do action-specific stuff
		self.runEvent(self)

class ActionCounter:
	def __init__(self, action_performer):
		self.count = 0
		self.actionEvent = action_performer.runEvent
		self.actionEvent += self._onActionRun

	def __del__(self):
		# observers should always make sure to _unsubscribe_ from events when they are done
		self.actionEvent -= self._onActionRun

	def _onActionRun(self, action_performer):
		self.count += 1
		print("'{0}' ran {1} times".format(action_performer.name, self.count))

performer = Action('Foo action')
observer = ActionCounter(performer)
performer.run() # => "'Foo action' ran 1 times"
performer.run() # => "'Foo action' ran 2 times"
```

### Unsubscribe function returned by .add
```python

# setup
event = Event()

def setup():
	def handler(value):
		print(value)

	unsubscribe = event.add(handler)
	return unsubscribe

cleanup = setup()

# do stuff
# ...

# cleanup
cleanup()
```
		


## Decorators

The evento package provides the following decorators to easily add before and/or after events to any method:

```python
@triggers_before_event
@triggers_after_event
@triggers_beforeafter_events
```

They can be used as followed:

```python
from evento import triggers_before_event, triggers_after_event, triggers_beforeafter_events

def before(event):
    print('before')

def after(event):
    print('after')

@triggers_before_event
def before_action(param1):
    print(param1)

@triggers_after_event
def after_action(param1, param2, param3):
    print(' '.join([param1, param2, param3]))

@triggers_beforeafter_events
def both_action():
    print('during')


before_action('first before') # => "first before"
after_action('first after:', '1', '2') # => "first after: 1 2"
both_action() # => "during"

# subscribe callbacks to the decorated methods
before_action.subscribe(before)
after_action.subscribe(after)
both_action.subscribe(before, after)

before_action('second before') # => "before\nsecond before"
after_action('second after:', '3', '4') # => second after: 3 4\nafter"
both_action() # before\nduring\nafter

```

Note that these decorators simply wrap the function in a class that also holds a beforeEvent and/or afterEvent, which is/are triggered before/after the function is invoked. To clarify; within the context of the above example, the following two lines do exactly the same:

```python
before_action.subscribe(before)
before_action.beforeEvent += before
```
