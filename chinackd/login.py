import asyncio
from pyppeteer import launch


async def login():
    # browser = await launch({'headless': False, 'slowMo': 10})
    browser = await launch()   # 无头无lang=zh_CN
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('http://chinackd.medidata.cn/login.jsp?FocusDomain=dn')
    await page.type("#LoginId", "demo3")
    await page.type("#Password", "tpqr6844", )
    # await page.waitFor(1000)
    await page.click("#btn_signin")
    await page.waitFor(500)
    # global Cookie
    Cookie = await get_cookies(page)
    await browser.close()
    return Cookie


async def get_cookies(page):
    """
    获取cookie
    :param page: page对象
    :return: 处理后的cookies
    """
    cookie_list = await page.cookies()
    cookies = ''
    print(cookie_list)
    for cookie in cookie_list:
        coo = f'{cookie.get("name")}={cookie.get("value")};'
        cookies += coo
    print(cookies)
    if 'lang=zh_CN' not in cookies:
        cookies = cookies + 'lang=zh_CN;'
    return cookies


# task = [asyncio.ensure_future(mains())]
# cook = asyncio.get_event_loop().run_until_complete(asyncio.wait(task))
result = asyncio.get_event_loop().run_until_complete(login())
print(result)

# JSESSIONID=73AF5AE044C9A887E017104F10055A14;lang=zh_CN;