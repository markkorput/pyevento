#!/usr/bin/env python
import unittest
import helper
from evento import triggers_before_event, triggers_after_event, triggers_beforeafter_events

class TestDecorators(unittest.TestCase):
    def test_triggers_before_event(self):
        # add before events to a method with this decorator
        @triggers_before_event
        def some_action():
            self.value += 'a'

        def observer(param):
            self.observed_param = param
            self.value += 'b'

        some_action.beforeEvent += observer
        self.value = ''
        some_action()
        self.assertEqual(self.value, 'ba')
        self.assertEqual(self.observed_param, some_action.beforeEvent)

    def test_triggers_after_event(self):
        # add before events to a method with this decorator
        @triggers_after_event
        def some_action():
            self.value += 'a'

        def observer(param):
            self.observed_param = param
            self.value += 'b'

        some_action.afterEvent += observer
        self.value = ''
        some_action()
        self.assertEqual(self.value, 'ab')
        self.assertEqual(self.observed_param, some_action.afterEvent)

    def test_triggers_beforeafter_events(self):
        # add before events to a method with this decorator
        @triggers_beforeafter_events
        def some_action():
            self.value += 'a'

        def observer(param):
            if param == some_action.beforeEvent:
                self.value += 'before-'

            if param == some_action.afterEvent:
                self.value += '-after'

        some_action.beforeEvent += observer
        some_action.afterEvent += observer
        self.value = ''
        some_action()
        self.assertEqual(self.value, 'before-a-after')

    def test_before_subscribtion(self):
        @triggers_before_event
        def some_action():
            self.value += 'a'

        def before(event):
            pass

        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), False)
        # some_action.subscribe(before)
        some_action += before
        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), True)
        some_action -= before
        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), False)

        # magic methods explained
        # this lets you do some_action += before
        self.assertEqual(some_action.__iadd__, some_action.subscribe)
        # this lets you do some_action -= before
        self.assertEqual(some_action.__isub__, some_action.unsubscribe)

    def test_after_subscribtion(self):
        @triggers_after_event
        def some_action():
            self.value += 'a'

        def after(event):
            pass

        self.assertEqual(some_action.afterEvent.hasSubscriber(after), False)
        # some_action.subscribe(before)
        some_action += after
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), True)
        some_action -= after
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), False)

        # magic methods explained
        # this lets you do some_action += before
        self.assertEqual(some_action.__iadd__, some_action.subscribe)
        # this lets you do some_action -= before
        self.assertEqual(some_action.__isub__, some_action.unsubscribe)

    def test_beforeafter_subscribe(self):
        @triggers_beforeafter_events
        def some_action():
            self.value += 'a'

        def before(event):
            pass
        def after(event):
            pass

        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), False)
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), False)

        some_action.subscribe(before, after)

        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), True)
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), True)

    def test_beforeafter_subscribe(self):
        @triggers_beforeafter_events
        def some_action():
            self.value += 'a'

        def before(event):
            pass
        def after(event):
            pass

        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), False)
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), False)

        some_action.subscribe(before, after)

        self.assertEqual(some_action.beforeEvent.hasSubscriber(before), True)
        self.assertEqual(some_action.afterEvent.hasSubscriber(after), True)

# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
