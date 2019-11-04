import requests
from lxml import etree
import time
from retrying import retry
from pprint import pprint
import aiohttp
import asyncio
from login import login

cookie = asyncio.get_event_loop().run_until_complete(login())

# Cookie = 'lang=zh_CN; JSESSIONID=B04B4D95D9C54DC43DBCE4B80E020A45'

cookie = cookie.update({'lang': 'zh_CN'})
print(cookie)


@retry
def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        # 'Cookie': Cookie
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookie)
        if response.status_code == 200 and response:
            return response  # 不可用text, 必须content, 有编码
    except requests.RequestException as e:
        print(f'get_response: {e}')
        get_response(url)


def parse_index(html):
    # fromstring Parses an XML document or fragment from a string.
    doc = etree.fromstring(html)
    pid = doc.xpath('//ROW/@PTID')
    return pid


@retry
async def get_resp(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        # 'Cookie': Cookie
    }
    session = aiohttp.ClientSession()
    try:
        response = await session.get(url, headers=headers, cookies=cookie)
        if response.status == 200 and response:
            result = await response.text()
            return result
    except aiohttp.ClientError as e:
        print(f'get_resp: {e}')
    finally:
        await session.close()


async def parse_detail(url):
    html = await get_resp(url)
    if html:
        doc = etree.HTML(html)
        name = doc.xpath("//*[@id='P101']/@value")
        sex = doc.xpath("//*[@id='tr_102']/span[2]/input[@checked=checked]/@value")
        patient_num = doc.xpath("//*[@id='P103']/@value")
        career = doc.xpath("//*[@id='P104']/@value")
        national = doc.xpath("//*[@id='tr_105']//option[@selected=selected]/text()")
        education = doc.xpath("//*[@id='tr_107']/span[2]/input[@checked=checked]/@value")
        id_num = doc.xpath("//*[@id='P108']/@value")
        birthplace = doc.xpath("//*[@id='tr_1110']/span[2]/select/option[@selected=selected]/@value")
        medical_ins_num = doc.xpath("//*[@id='P110']/@value")
        birth_date = doc.xpath("//*[@id='P111']/@value")
        pprint(
            {
                'name': name,
                'sex': sex,
                'patient_num': patient_num,
                'career': career,
                'national': national,
                'education': education,
                'id_num': id_num,
                'birthplace': birthplace,
                'medical_ins_num': medical_ins_num,
                'birth_date': birth_date
            }
        )
    else:
        print(f'html: {html}')


if __name__ == '__main__':
    base_url = 'http://chinackd.medidata.cn/doAction?Action=runCaseCustQry&CCQId=30042&start=0&limit=30&ExtTerm_0=&tranid=0'
    start = time.time()

    resp = get_response(base_url)
    detail_urls = ['http://chinackd.medidata.cn/jsp/para/pm2/pdm.jsp?PtId={}'.format(pid)
                   for pid in parse_index(resp.content)]

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(parse_detail(i)) for i in detail_urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.time()
    print((end - start) / 60)
