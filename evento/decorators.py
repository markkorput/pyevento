from .event import Event

class BeforeEventMethodWrapper:
    def __init__(self, method):
        self.method = method
        self.beforeEvent = Event()

    def run(self, *args, **kwargs):
        self.beforeEvent(self.beforeEvent)
        self.method(*args, **kwargs)

    def subscribe(self, observer):
        self.beforeEvent += observer
        return self

    def unsubscribe(self, observer):
        self.beforeEvent -= observer
        return self

    __call__ = run
    __iadd__ = subscribe
    __isub__ = unsubscribe

def triggers_before_event(func):
    return BeforeEventMethodWrapper(func)

class AfterEventMethodWrapper:
    def __init__(self, method):
        self.method = method
        self.afterEvent = Event()

    def run(self, *args, **kwargs):
        self.method(*args, **kwargs)
        self.afterEvent(self.afterEvent)

    def subscribe(self, observer):
        self.afterEvent += observer
        return self

    def unsubscribe(self, observer):
        self.afterEvent -= observer
        return self

    __call__ = run
    __iadd__ = subscribe
    __isub__ = unsubscribe

def triggers_after_event(func):
    return AfterEventMethodWrapper(func)

class AroundEventMethodWrapper:
    def __init__(self, method):
        self.method = method
        self.beforeEvent = Event()
        self.afterEvent = Event()

    def __call__(self, *args, **kwargs):
        self.beforeEvent(self.beforeEvent)
        self.method(*args, **kwargs)
        self.afterEvent(self.afterEvent)

    def subscribe(self, before_callback, after_callback):
        self.beforeEvent += before_callback
        self.afterEvent += after_callback

def triggers_beforeafter_events(func):
    return AroundEventMethodWrapper(func)
