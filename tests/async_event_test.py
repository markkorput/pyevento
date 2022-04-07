import pytest
from mock import AsyncMock

from evento import AsyncEvent


class TestAsyncEvent:
    pytestmark = [pytest.mark.asyncio, pytest.mark.focus]

    async def test_fire(self):
        e = AsyncEvent[list[str]]()
        mock = AsyncMock()
        e += mock
        await e.fire(["p1", "p2"])
        mock.assert_awaited_once_with(["p1", "p2"])

    async def test_subscribe(self):
        e = AsyncEvent()
        mock = AsyncMock()

        e.append(mock)

        await e.fire(5)
        mock.assert_awaited_with(5)
        assert mock.await_count == 1
        await e.fire(4)
        mock.assert_awaited_with(4)
        assert mock.await_count == 2

    async def test_unsubscribe(self):
        e = AsyncEvent()
        mock = AsyncMock()
        e += mock
        await e.fire(3)
        mock.assert_awaited_once_with(3)
        e.remove(mock)
        await e.fire(6)
        mock.assert_awaited_once_with(3)

    async def test_callback_un(self):
        e = AsyncEvent()
        log = []

        async def f1(_):
            log.append(1)

        async def f2(_):
            log.append(2)

        e += f1
        e += f2
        await e(0)
        assert log == [1, 2]

    async def test_unsubscribe_during_fire(self):
        e = AsyncEvent()
        self.e = e

        record = []

        async def observer1(v: int):
            record.append((1, v))

        async def observer2(v: int):
            record.append((2, v))
            self.e -= observer1

        e += observer1
        e += observer2

        assert len(e) == 2
        await e(1)
        assert record == [(1, 1), (2, 1)]
        assert len(e) == 1
        await e(2)
        assert record == [(1, 1), (2, 1), (2, 2)]

    async def test_subscribe_during_fire(self):
        e = AsyncEvent()

        record = []

        async def observer1(v: int):
            record.append((1, v))

        async def observer2(v: int):
            nonlocal e
            record.append((2, v))
            e += observer1

        e.append(observer2)
        assert len(e) == 1
        await e(1)
        assert record == [(2, 1)]
        assert len(e) == 2
        await e(2)
        assert record == [(2, 1), (2, 2), (1, 2)]
        assert len(e) == 2

    async def test_len(self):
        e = AsyncEvent()

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

    async def test_len_with_duplicates(self):
        e = AsyncEvent()

        def observer1():
            pass

        e += observer1
        assert len(e) == 1
        e += observer1
        assert len(e) == 1

    async def test_add(self):
        e = AsyncEvent()

        def foo():
            pass

        # add method does the same as subscribe, but returns an unsubscribe function
        unsub = e.add(foo)
        assert len(e) == 1
        unsub()
        assert len(e) == 0

    async def test_invoke_with_invalid_signature(self):
        e = AsyncEvent()
        await e(1)
        # these don't give runtime issues, but should trigger mypy
        await e("1")
        await e(False)

        with pytest.raises(TypeError):
            await e()

        with pytest.raises(TypeError):
            await e(1, 2)

        with pytest.raises(TypeError):
            await e(1, foo="bar")

    class TestEventModifyingSubscribers:
        async def remover_callback(self, v):
            self.e -= self.remover_callback

        async def test_recursion_with_unsubscribing_callback(self):
            self.e = AsyncEvent()
            self.e += self.remover_callback

            try:
                await self.e(1)
            except RuntimeError:
                self.fail("AsyncEvent failed to deal with a subscriber that unsubscribed itself")

        async def subscriber_callback(self, v):
            self.e += self.remover_callback

        async def test_recursion_with_subscribing_callback(self):
            self.e = AsyncEvent()
            self.e += self.subscriber_callback

            try:
                await self.e(1)
            except RuntimeError:
                self.fail(
                    "AsyncEvent failed to deal with a subscriber that subscribed another observer"
                )

        async def test_recursion_without_complications(self):
            self.e = AsyncEvent()

            async def callback(val):
                self.value += val
                if len(self.value) < 3:
                    await self.e(self.value)

            self.e += callback
            self.value = ""
            await self.e("a")
            assert self.value, "aaaa"
