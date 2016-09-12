#!/usr/bin/env python
import unittest
import helper
from evento import Event

class TestEventMethods(unittest.TestCase):
    def test_fire(self):
        # setup
        e = Event()
        def observer(p1, p2):
            self.value = ','.join([p1, p2])
        e += observer
        # assert
        e.fire('p1', 'p2')
        self.assertEqual(self.value, 'p1,p2')

    def test_subscribe(self):
        # setup
        e = Event()
        def observer(par1):
            self.counter = par1 * 2
        e.subscribe(observer)
        # assert
        e.fire(5)
        self.assertEqual(self.counter, 10)
        e.fire(4)
        self.assertEqual(self.counter, 8)

    def test_unsubscribe(self):
        # setup
        e = Event()
        def observer(param):
            self.counter = param + 2
        e += observer
        # assert
        e.fire(3)
        self.assertEqual(self.counter, 5)
        e.unsubscribe(observer)
        e.fire(6)
        self.assertEqual(self.counter, 5) # still

    def test_getSubscriberCount(self):
        # setup
        e = Event()
        def observer1():
            pass
        def observer2():
            pass
        def observer3():
            pass
        # assert
        self.assertEqual(e.getSubscriberCount(), 0)
        e += observer1
        self.assertEqual(e.getSubscriberCount(), 1)
        e += observer2
        self.assertEqual(e.getSubscriberCount(), 2)
        e += observer3
        self.assertEqual(e.getSubscriberCount(), 3)

    def test_getSubscriberCount_with_duplicates(self):
        # setup
        e = Event()
        def observer1():
            pass
        # asset
        e += observer1
        self.assertEqual(e.getSubscriberCount(), 1)
        e += observer1
        self.assertEqual(e.getSubscriberCount(), 1)

    def test_isSubscribed(self):
        # setup
        e = Event()
        def observer():
            pass
        # assert
        self.assertEqual(e.isSubscribed(observer), False)
        e += observer
        self.assertEqual(e.isSubscribed(observer), True)
        e -= observer
        self.assertEqual(e.isSubscribed(observer), False)

    def test_magic_methods(self):
        e = Event()
        # this lets you trigger the event like this:
        # e('param1', 'param2')
        self.assertEqual(e.__call__, e.fire)
        # this lets you add subscribers like this:
        # e += observer_method
        self.assertEqual(e.__iadd__, e.subscribe)
        # this lets you remove subscribers like this:
        # e -= observer_method
        self.assertEqual(e.__isub__, e.unsubscribe)
        # this lets you request the number of observers like this:
        # len(e)
        self.assertEqual(e.__len__, e.getSubscriberCount)
        # this lets you check if a method is already subscribed to the event like this:
        # observer_method in e
        self.assertEqual(e.__contains__, e.isSubscribed)

# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
