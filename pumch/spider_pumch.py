import re, time
import asyncio
from datetime import datetime
from fake_useragent import UserAgent
import aiohttp
from pyquery import PyQuery as pq
from asyncio import Queue

sleep_interval = 0.1


def get_departments_url(base_url):
    try:
        doc = pq(base_url)
        url_iter = doc('div.box.clearfix > div > div > div.h2 > a').items()
        return url_iter
    except Exception as e:
        print('get_departments_url: {}'.format(e))


def is_first_level_url(url):
    if re.search(r'department', url, re.S):
        return True
    return False


class Crawler:
    def __init__(self, departments_url, max_tries=4, max_tasks=10, _loop=None):
        self.loop = _loop or asyncio.get_event_loop()
        self.headers = {}
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.urls_queue = Queue(loop=self.loop)
        self.seen_urls = set()
        self.session = aiohttp.ClientSession(loop=self.loop)

        for item in departments_url:
            url = 'https://www.pumch.cn' + item.attr('href')
            self.urls_queue.put_nowait(url)

    @staticmethod
    async def fetch(response):
        if response.status == 200:
            text = await response.text()
            doc = pq(text)
            return doc

    def parse_first_etree(self, doc):
        doctors_url = doc('#datalist > div.list.clearfix a').items()
        for url in doctors_url:
            second_level_url = 'https://www.pumch.cn' + url.attr('href')
            self.urls_queue.put_nowait(second_level_url)

    def parse_second_etree(self, doc):
        name = doc('div.text-box > div.dorname > div.title1').text()
        print(name)

    async def handle(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                self.headers['User-Agent'] = UserAgent(verify_ssl=False).random
                response = await self.session.get(url, headers=self.headers, allow_redirects=False)
                break
            except aiohttp.ClientError as e:
                print("handle: {}".format(e))
                tries += 1
                print('try {}: {}'.format(tries, url))
        try:
            doc = await self.fetch(response)
            if is_first_level_url(url):
                print("first_level: {}".format(url))
                self.parse_first_etree(doc)
            else:
                print("second level: {}".format(url))
                self.parse_second_etree(doc)
        finally:
            await response.release()

    async def work(self):
        try:
            while True:
                url = await self.urls_queue.get()
                await self.handle(url)
                time.sleep(sleep_interval)
                self.urls_queue.task_done()
        except asyncio.CancelledError as e:
            print(repr(e))

    async def run(self):
        workers = [asyncio.ensure_future(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        await self.urls_queue.join()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    start = datetime.now()
    base_url = 'https://www.pumch.cn/doctors.html'
    departments_link = get_departments_url(base_url)
    # 创建异步事件循环
    loop = asyncio.get_event_loop()
    crawler = Crawler(departments_link, max_tasks=100)
    # 用loop.run_until_complete(asyncio.wait(task))来监测task
    # 的运行情况并返回结果， 比如什么时候挂起来，什么时候回来执行原方法等。
    loop.run_until_complete(crawler.run())
    # crawler.close()
    print(datetime.now() - start)
    loop.close()
