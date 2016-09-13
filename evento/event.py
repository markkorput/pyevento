import logging
logger = logging.getLogger(__name__)

class Event:
    def __init__(self):
        self._subscribers = set()
        self._fireCount = 0
        self._currentFireCount = 0
        self._subscribe_queue = []
        self._unsubscribe_queue = []

    def subscribe(self, subscriber):
        # only modify the _subscribers set if we're not currently firing
        # otherwise queue the subscription for processing after firing is done
        if self.isFiring():
            self._subscribe_queue.append(subscriber)
            return self

        self._subscribers.add(subscriber)
        return self

    def unsubscribe(self, subscriber):
        # only modify the _subscribers set if we're not currently firing
        # otherwise queue the unsubscription for processing after firing is done
        if self.isFiring():
            self._unsubscribe_queue.append(subscriber)
            return self

        try:
            self._subscribers.remove(subscriber)
        except KeyError as err:
            logger.warning('Event.unsubscribe got unknown handler: {}'.format(err))

        return self

    def hasSubscriber(self, subscriber):
        return subscriber in self._subscribers

    def fire(self, *args, **kargs):
        # count the number of (recursive) fires currently happening
        self._currentFireCount += 1

        # execute all subscribers
        for subscriber in self._subscribers:
            # the handler might have got unsubscribed
            # inside one of the previous subscribers
            if not subscriber in self._unsubscribe_queue:
                subscriber(*args, **kargs)

        # current fire cycle is done, uncount it
        self._currentFireCount -= 1

        # we're counting the number of fires (mostly for testing purposes)
        self._fireCount += 1

        # only if we're not still in a recursive fire situation
        if not self.isFiring():
            self._processQueues()

    def _processQueues(self):
        for subscriber in self._subscribe_queue:
            self.subscribe(subscriber)

        for subscriber in self._unsubscribe_queue:
            self.unsubscribe(subscriber)

        # reset processed queues
        self._subscribe_queue = []
        self._unsubscribe_queue = []

    def getSubscriberCount(self):
        return len(self._subscribers)

    def isFiring(self):
        return self._currentFireCount > 0

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = fire
    __len__  = getSubscriberCount
    __contains__ = hasSubscriber
