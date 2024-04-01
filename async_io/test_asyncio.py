# https://testdriven.io/blog/flask-async/
import asyncio

queue = asyncio.Queue()


async def sub():

    while True:
        d = await queue.get()
        print(d)

        yield d
        # yield await queue.get()


async def pub():

    while True:
        await asyncio.sleep(2)
        await queue.put(1)

async def tt():
    print("HI")


async def main():

    asyncio.create_task(pub())

    async for data in sub():
        print(f"hi: {data}")

    await tt()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
