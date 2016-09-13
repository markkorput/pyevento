# pyevento
Python evento package, making the Observer pattern estúpida sencillo.

## Install

```shell
pip install omxsync
```

## Usage

```python
from evento import Event

# observers are simply methods
def observer(param1, param2):
	print ', '.join([param1, param2])

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
		action_performer.runEvent += self._onActionRun

	def _onActionRun(self, action_performer):
		self.count += 1
		print "'{0}' ran {1} times".format(action_performer.name, self.count)

performer = Action('Foo action')
observer = ActionCounter(performer)
performer.run() # => "'Foo action' ran 1 times"
performer.run() # => "'Foo action' ran 2 times"
```