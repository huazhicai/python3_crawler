from asyncio import Queue
import aiohttp
import time
from crawler import parse_detail, get_response, parse_index
import asyncio

sleep_interval = 0.1


class Crawler:
    def __init__(self, urls, max_tries=4, max_tasks=10):
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.urls_queue = Queue()
        self.seen_urls = set()
        self.session = aiohttp.ClientSession()

        for url in urls:
            self.urls_queue.put_nowait(url)

    async def close(self):
        await self.session.close()

    @staticmethod
    async def fetch(response):
        if response.status == 200:
            return await response.text()

    async def handle(self, url):
        tries = 0
        response = None
        while tries < self.max_tries:
            try:
                response = await self.session.get(url, allow_redirects=False)
                break
            except aiohttp.ClientError as e:
                print("handle: {}".format(e))
                tries += 1

        if response:
            html = await self.fetch(response)
            parse_detail(html)
            response.release()

    async def work(self):
        try:
            while True:
                url = await self.urls_queue.get()
                await self.handle(url)
                time.sleep(sleep_interval)
                self.urls_queue.task_done()
        except asyncio.CancelledError as e:
            print("work: {}".format(e))

    async def run(self):
        workers = [asyncio.ensure_future(self.work()) for _ in range(self.max_tasks)]
        await self.urls_queue.join()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    base_url = 'http://chinackd.medidata.cn/doAction?Action=runCaseCustQry&CCQId=30042&start=0&limit=30&ExtTerm_0=&tranid=0'
    start = time.time()

    resp = get_response(base_url)
    detail_urls = ['http://chinackd.medidata.cn/jsp/para/pm2/pdm.jsp?PtId={}'.format(pid)
                   for pid in parse_index(resp.content)]
    crawler = Crawler(detail_urls, max_tasks=26)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.run())
    crawler.close()
    loop.close()
    print(time.time() - start)
