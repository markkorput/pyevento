from evento import Event


class TestEventMethods:
    def test_fire(self):
        e = Event[list[str]]()

        def observer(val: list[str]):
            self.value = ",".join(val)

        e += observer

        e.fire(["p1", "p2"])
        assert self.value == "p1,p2"

    def test_subscribe(self):

        e = Event()

        def observer(par1):
            self.counter = par1 * 2

        e.subscribe(observer)

        e.fire(5)
        assert self.counter == 10
        e.fire(4)
        assert self.counter == 8

    def test_unsubscribe(self):

        e = Event()

        def observer(param):
            self.counter = param + 2

        e += observer

        e.fire(3)
        assert self.counter == 5
        e.unsubscribe(observer)
        e.fire(6)
        assert self.counter == 5

    def test_getSubscriberCount(self):

        e = Event()

        def observer1():
            pass

        def observer2():
            pass

        def observer3():
            pass

        assert e.getSubscriberCount() == 0
        e += observer1
        assert e.getSubscriberCount() == 1
        e += observer2
        assert e.getSubscriberCount() == 2
        e += observer3
        assert e.getSubscriberCount() == 3

    def test_getSubscriberCount_with_duplicates(self):
        e = Event()

        def observer1():
            pass

        e += observer1
        assert e.getSubscriberCount() == 1
        e += observer1
        assert e.getSubscriberCount() == 1

    def test_hasSubscriber(self):
        e = Event()

        def observer():
            pass

        assert not e.hasSubscriber(observer)
        e += observer
        assert e.hasSubscriber(observer)
        e -= observer
        assert not e.hasSubscriber(observer)

    def test_magic_methods(self):
        e = Event()
        # this lets you trigger the event like this:
        # e('param1', 'param2')
        assert e.__call__ == e.fire
        # this lets you add subscribers like this:
        # e += observer_method
        assert e.__iadd__ == e.subscribe
        # this lets you remove subscribers like this:
        # e -= observer_method
        assert e.__isub__ == e.unsubscribe
        # this lets you request the number of observers like this:
        # len(e)
        assert e.__len__ == e.getSubscriberCount
        # this lets you check if a method is already subscribed to the event like this:
        # observer_method in e
        assert e.__contains__ == e.hasSubscriber

    def test_add(self):
        e = Event()

        def foo():
            pass

        # add method does the same as subscribe, but returns an unsubscribe function
        unsub = e.add(foo)
        assert e.getSubscriberCount() == 1
        unsub()
        assert e.getSubscriberCount() == 0

    def test_unsubscribe_during_fire(self):
        e = Event()
        self.e = e

        record = []

        def observer2(v: int):
            record.append((2, v))
            self.e -= observer1

        def observer1(v: int):
            record.append((1, v))

        e += observer1
        e += observer2

        assert len(e) == 2
        e(1)
        assert record == [(1, 1), (2, 1)]
        assert len(e) == 1
        e(2)
        assert record == [(1, 1), (2, 1), (2, 2)]

    def test_subscribe_during_fire(self):
        e = Event()

        record = []

        def observer2(v: int):
            nonlocal e
            record.append((2, v))
            e += observer1

        def observer1(v: int):
            record.append((1, v))

        e.subscribe(observer2)
        assert len(e) == 1
        e(1)
        assert record == [(2, 1)]
        assert len(e) == 2
        e(2)
        assert record == [(2, 1), (1, 2), (2, 2)]
        assert len(e) == 2


class TestEventModifierSubscribers:
    def remover_callback(self, v):
        self.e -= self.remover_callback

    def test_recursion_with_unsubscribing_callback(self):
        self.e = Event()
        self.e += self.remover_callback

        try:
            self.e(1)
        except RuntimeError:
            self.fail("Event failed to deal with a subscriber that unsubscribed itself")

    def subscriber_callback(self, v):
        self.e += self.remover_callback

    def test_recursion_with_subscribing_callback(self):
        self.e = Event()
        self.e += self.subscriber_callback

        try:
            self.e(1)
        except RuntimeError:
            self.fail("Event failed to deal with a subscriber that subscribed another observer")

    def test_recursion_without_complications(self):
        self.e = Event()

        def callback(val):
            self.value += val
            if len(self.value) < 3:
                self.e(self.value)

        self.e += callback
        self.value = ""
        self.e("a")
        assert self.value, "aaaa"
