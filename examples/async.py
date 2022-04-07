import asyncio

from evento import AsyncEvent


async def observer(value: str) -> None:
    print(value)


async def main():
    event = AsyncEvent[str]()
    await event("This does nothing.")
    event += observer
    await event("This is printed.")


asyncio.run(main())
