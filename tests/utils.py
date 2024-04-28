from asyncio import sleep


async def a_moment() -> None:
    """
    Messages are handled in a thread. This is to wait for them to be handled.
    "moment" is a relative term and will reflect whatever time is needed here.
    """
    await sleep(0.01)
