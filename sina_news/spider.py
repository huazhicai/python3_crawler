import requests
from requests import RequestException
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36'}


# 获取新闻内文html数据
def get_news_detail(url):
    try:
        response = requests.get(url, headers=headers, timeout=6)
        # 获取的内容编码不为utf-8需要转换为utf-8
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求页面失败: {}'.format(url))
        return None


# 解析新闻内文数据， 提取标题，日期，来源，正文，评论数，责任编辑
def parser_news_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup.text)
    title = soup.select('#artibodyTitle')[0].text
    timesource = soup.select('#navtimeSource')[0].next.strip()
    # timesource3 = soup.select('#navtimeSource')[0].contents[0].strip()
    medianame = soup.select('#navtimeSource > span > span > a')[0].text
    article = []
    for p in soup.select('#artibody p')[:-1]:
        article.append(p.text.strip())
    editor = soup.select('#artibody > p.article-editor')[0].text.lstrip('责任编辑：')
    # result['comments'] = getCommentCounts(newsurl)


def main():
    url = 'http://news.sina.com.cn/c/nd/2017-10-17/doc-ifymvece2239312.shtml'
    html = get_news_detail(url)
    parser_news_detail(html)


if __name__ == '__main__':
    main()
