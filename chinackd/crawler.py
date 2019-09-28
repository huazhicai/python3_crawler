import requests
from lxml.html import etree
import time
from retrying import retry
from pprint import pprint


@retry
def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Cookie': 'JSESSIONID=AB10F1041194961F54457AE0A74D4140; lang=zh_CN'
    }
    try:
        response = requests.get(url, headers=headers, timeout=1)
        if response.status_code == 200 and response:
            return response  # 不可用text, 必须content, 有编码
    except requests.RequestException as e:
        print('get_response: {}'.format(e))
        get_response(url)


def parse_index(html):
    # fromstring Parses an XML document or fragment from a string.
    doc = etree.fromstring(html)
    pid = doc.xpath('//ROW/@PTID')
    return pid


def parse_detail(html):
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


def main(base_url):
    resp = get_response(base_url)
    for pid in parse_index(resp.content):
        detail_url = 'http://chinackd.medidata.cn/jsp/para/pm2/pdm.jsp?PtId={}'.format(pid)
        print('detail', detail_url)
        response = get_response(detail_url)
        parse_detail(response.text)


if __name__ == '__main__':
    base_url = 'http://chinackd.medidata.cn/doAction?Action=runCaseCustQry&CCQId=30042&start=0&limit=30&ExtTerm_0=&tranid=0'
    start = time.time()
    main(base_url)
    end = time.time()
    print((end - start)/60)
