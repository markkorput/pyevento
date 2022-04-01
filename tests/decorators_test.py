from evento import (
    triggers_after_event,
    triggers_before_event,
    triggers_beforeafter_events,
)


class TestDecorators:
    def test_triggers_before_event(self):
        # add before events to a method with this decorator
        @triggers_before_event
        def some_action():
            self.value += "a"

        def observer(param):
            self.observed_param = param
            self.value += "b"

        some_action.beforeEvent += observer
        self.value = ""
        some_action()
        assert self.value == "ba"
        assert self.observed_param == some_action.beforeEvent

    def test_triggers_after_event(self):
        # add before events to a method with this decorator
        @triggers_after_event
        def some_action():
            self.value += "a"

        def observer(param):
            self.observed_param = param
            self.value += "b"

        some_action.afterEvent += observer
        self.value = ""
        some_action()
        assert self.value == "ab"
        assert self.observed_param == some_action.afterEvent

    def test_triggers_beforeafter_events(self):
        # add before events to a method with this decorator
        @triggers_beforeafter_events
        def some_action():
            self.value += "a"

        def observer(param):
            if param == some_action.beforeEvent:
                self.value += "before-"

            if param == some_action.afterEvent:
                self.value += "-after"

        some_action.beforeEvent += observer
        some_action.afterEvent += observer
        self.value = ""
        some_action()
        assert self.value == "before-a-after"

    def test_before_subscribtion(self):
        @triggers_before_event
        def some_action():
            self.value += "a"

        def before(event):
            pass

        assert not some_action.beforeEvent.hasSubscriber(before)
        # some_action.subscribe(before)
        some_action += before
        assert some_action.beforeEvent.hasSubscriber(before)
        some_action -= before
        assert not some_action.beforeEvent.hasSubscriber(before)

        # magic methods explained
        # this lets you do some_action += before
        assert some_action.__iadd__ == some_action.subscribe
        # this lets you do some_action -= before
        assert some_action.__isub__ == some_action.unsubscribe

    def test_after_subscribtion(self):
        @triggers_after_event
        def some_action():
            self.value += "a"

        def after(event):
            pass

        assert not some_action.afterEvent.hasSubscriber(after)
        # some_action.subscribe(before)
        some_action += after
        assert some_action.afterEvent.hasSubscriber(after)
        some_action -= after
        assert not some_action.afterEvent.hasSubscriber(after)

        # magic methods explained
        # this lets you do some_action += before
        assert some_action.__iadd__ == some_action.subscribe
        # this lets you do some_action -= before
        assert some_action.__isub__ == some_action.unsubscribe

    def test_beforeafter_subscribe(self):
        @triggers_beforeafter_events
        def some_action():
            self.value += "a"

        def before(event):
            pass

        def after(event):
            pass

        assert not some_action.beforeEvent.hasSubscriber(before)
        assert not some_action.afterEvent.hasSubscriber(after)

        some_action.subscribe(before, after)

        assert some_action.beforeEvent.hasSubscriber(before)
        assert some_action.afterEvent.hasSubscriber(after)

    def test_beforeafter_subscribe(self):
        @triggers_beforeafter_events
        def some_action():
            self.value += "a"

        def before(event):
            pass

        def after(event):
            pass

        assert not some_action.beforeEvent.hasSubscriber(before)
        assert not some_action.afterEvent.hasSubscriber(after)

        some_action.subscribe(before, after)

        assert some_action.beforeEvent.hasSubscriber(before)
        assert some_action.afterEvent.hasSubscriber(after)
