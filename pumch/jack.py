import time

import requests
import asyncio


async def a(i):
    r = await b(i)
    print(i, r)


async def b(i):
    r = requests.get(i)
    print(i)
    print(dir(r.text))
    await asyncio.sleep(3)
    print(time.time() - start)
    return r


url = ["https://segmentfault.com/p/1210000013564725",
       "https://www.jianshu.com/p/83badc8028bd",
       "https://www.baidu.com/"]

loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(a(i)) for i in url]

start = time.time()
loop.run_until_complete(asyncio.wait(task))
endtime = time.time() - start
print(endtime)
loop.close()


loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(b(i)) for i in url]
loop.run_until_complete(asyncio.wait(task))
loop.close()