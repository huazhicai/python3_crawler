import time

import requests
import asyncio


async def test1(i):
    r = await test2(i)
    print(i, r)


async def test2(i):
    r = requests.get(i)
    print(i)
    print(dir(r))
    await asyncio.sleep(3)
    print(time.time() - start)
    return r


url = ["https://segmentfault.com/p/1210000013564725",
       "https://www.jianshu.com/p/83badc8028bd",
       "https://www.baidu.com/"]

loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(test1(i)) for i in url]

start = time.time()
loop.run_until_complete(asyncio.wait(task))
endtime = time.time() - start
print(endtime)
loop.close()


loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(test2(i)) for i in url]
loop.run_until_complete(asyncio.wait(task))
loop.close()