import asyncio
from pyppeteer import launch
import time
#
# # exepath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
# # exepath = "C:\\Windows\\SystemApps\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\MicrosoftEdge.exe"
# exepath = "D:\software\\firefox.exe"


async def main():
    browser = await launch({'headless': False, 'slowMo': 20})
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('http://chinackd.medidata.cn/login.jsp?FocusDomain=dn')
    await page.type("#LoginId", "demo3")
    await page.type("#Password", "tpqr6844", )
    # await page.waitFor(1000)
    await page.click("#btn_signin")
    await page.waitFor(10000)
    # await browser.close()


asyncio.get_event_loop().run_until_complete(main())


# import asyncio
# from pyppeteer import launch
#
#
# async def main():
#     browser = await launch({'headless': False})
#     page = await browser.newPage()
#     await page.goto('https://www.baidu.com/')
#     await page.screenshot({'path': 'D:\example.png'})
#     await page.waitFor(3000)
#     await browser.close()
#
#
# asyncio.get_event_loop().run_until_complete(main())

