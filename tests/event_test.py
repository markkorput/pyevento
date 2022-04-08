import pytest

from evento import Event


class TestEvent:
    def test_fire(self):
        e = Event[list[str]]()

        def observer(val: list[str]):
            self.value = ",".join(val)

        e += observer

        e.fire(["p1", "p2"])
        assert self.value == "p1,p2"

    def test_append(self):

        e = Event()

        def observer(par1):
            self.counter = par1 * 2

        e.append(observer)

        e.fire(5)
        assert self.counter == 10
        e.fire(4)
        assert self.counter == 8

    def test_remove(self):

        e = Event()

        def observer(param):
            self.counter = param + 2

        e += observer

        e.fire(3)
        assert self.counter == 5
        e.remove(observer)
        e.fire(6)
        assert self.counter == 5

    def test_callback_order(self):
        e = Event()
        log = []
        e += lambda _: log.append(1)
        e += lambda _: log.append(2)
        e(0)
        assert log == [1, 2]

    def test_remove_during_fire(self):
        e = Event()
        self.e = e

        record = []

        def observer1(v: int):
            record.append((1, v))

        def observer2(v: int):
            record.append((2, v))
            self.e -= observer1

        e += observer1
        e += observer2

        assert len(e) == 2
        e(1)
        assert record == [(1, 1), (2, 1)]
        assert len(e) == 1
        e(2)
        assert record == [(1, 1), (2, 1), (2, 2)]

    def test_append_during_fire(self):
        e = Event()

        record = []

        def observer1(v: int):
            record.append((1, v))

        def observer2(v: int):
            nonlocal e
            record.append((2, v))
            e += observer1

        e.append(observer2)
        assert len(e) == 1
        e(1)
        assert record == [(2, 1)]
        assert len(e) == 2
        e(2)
        assert record == [(2, 1), (2, 2), (1, 2)]
        assert len(e) == 2

    def test_len(self):

        e = Event()

        def observer1():
            pass

        def observer2():
            pass

        def observer3():
            pass

        assert len(e) == 0
        e += observer1
        assert len(e) == 1
        e += observer2
        assert len(e) == 2
        e += observer3
        assert len(e) == 3

    def test_len_with_duplicates(self):
        e = Event()

        def observer1():
            pass

        e += observer1
        assert len(e) == 1
        e += observer1
        assert len(e) == 1

    def test_add(self):
        e = Event()

        def foo():
            pass

        # add method does the same as subscribe, but returns an unsubscribe function
        unsub = e.add(foo)
        assert len(e) == 1
        unsub()
        assert len(e) == 0

    def test_invoke_with_invalid_signature(self):
        e = Event()
        e(1)
        # these don't give runtime issues, but should trigger mypy
        e("1")
        e(False)

        with pytest.raises(TypeError):
            e()

        with pytest.raises(TypeError):
            e(1, 2)

        with pytest.raises(TypeError):
            e(1, foo="bar")

    class TestEventModifyingSubscribers:
        def remover_callback(self, v):
            self.e -= self.remover_callback

        def test_recursion_with_removing_callback(self):
            self.e = Event()
            self.e += self.remover_callback

            try:
                self.e(1)
            except RuntimeError:
                self.fail("Event failed to deal with a subscriber that unsubscribed itself")

        def appender_callback(self, v):
            self.e += self.remover_callback

        def test_recursion_with_appending_callback(self):
            self.e = Event()
            self.e += self.appender_callback

            try:
                self.e(1)
            except RuntimeError:
                self.fail("Event failed to deal with a subscriber that appended another observer")

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
