#!/usr/bin/env python
import unittest
import helper
from evento import triggers_before_event, triggers_after_event, triggers_beforeafter_events

class TestDecorators(unittest.TestCase):
    def test_trigger_before_event(self):
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

    def test_trigger_after_event(self):
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

    def test_trigger_beforeafter_events(self):
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

# run just the tests in this file
if __name__ == '__main__':
    unittest.main()
