from src.core.runners.console.console_runner import ConsoleRunner
import asyncio


async def __main__():
    await asyncio.gather(ConsoleRunner().run())

asyncio.run(__main__())
