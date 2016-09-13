from event import Event

class BeforeEventMethodWrapper:
    def __init__(self, method):
        self.method = method
        self.beforeEvent = Event()

    def __call__(self, *args, **kwargs):
        self.beforeEvent(self.beforeEvent)
        self.method(*args, **kwargs)

def trigger_before_event(func):
    return BeforeEventMethodWrapper(func)

class AfterEventMethodWrapper:
    def __init__(self, method):
        self.method = method
        self.afterEvent = Event()

    def __call__(self, *args, **kwargs):
        self.method(*args, **kwargs)
        self.afterEvent(self.afterEvent)

def trigger_after_event(func):
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

def trigger_beforeafter_events(func):
    return AroundEventMethodWrapper(func)
