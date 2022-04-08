import asyncio
from typing import Any

from evento import async_event


async def observer(id: int, message: str, price: float, **opts: Any) -> Any:
    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")


async def observer_with_return_value(id: int, message: str, price: float, **opts: Any) -> int:
    print(f"observer_with_return_value: {id}")
    return id


async def main() -> None:
    @async_event
    async def multi_arg_event(id: int, message: str, price: float, **opts: Any) -> str:
        return "Done"

    multi_arg_event.append(observer)
    multi_arg_event += observer_with_return_value

    result = await multi_arg_event(1, "Test-12", 9.99, feature=True)
    print(f"Result: {result}")


asyncio.run(main())
