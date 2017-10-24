import json
import re
from multiprocessing.dummy import Pool
from json.decoder import JSONDecodeError
import pandas
import requests
from requests import RequestException
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36'}


# 获取索引页的html代码
def get_index(page):
    url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'.format(
        page)
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


# 获取索引页的数据，并提取文章标题和详情页的url
def get_urls(html):
    try:
        jd = json.loads(html)
        if jd['result']['data']:
            for ent in jd['result']['data']:
                yield ent['url']
    except JSONDecodeError:
        print('解析json失败')


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
def parser_news_detail(url, html):
    print('爬取{}'.format(url))
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('#artibodyTitle')[0].text
    timesource = soup.select('#navtimeSource')[0].next.strip()
    # timesource3 = soup.select('#navtimeSource')[0].contents[0].strip()
    medianame = soup.select('#navtimeSource > span > span > a')[0].text
    article = []
    for p in soup.select('#artibody p')[:-1]:
        article.append(p.text.strip())
    editor = soup.select('#artibody > p.article-editor')[0].text.lstrip('责任编辑：')
    soup.select('#commentCountl')
    commentCounts = getCommentCounts(url)
    # comments数据没取到, 那么猜想数据可能是异步加载，或是js形式加载的， 打印一下soup,搜索一下
    # 果真没有，那就
    result = {
        'title': title,
        'timesource': timesource,
        'medianame': medianame,
        'article': article,
        'editor': editor,
        'commentCounts': commentCounts,
        'url': url
    }
    return result


# 获取评论数
def getCommentCounts(newsurl):
    commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=0&compress=0&ie=gbk&oe=gbk&page=1'
    m = re.search('doc-i(.+?).shtml', newsurl)
    newsid = m.group(1)
    # http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fymvece2239312&group=0&compress=0&ie=utf-8&oe=gbk&page=1
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


def main(page):
    html = get_index(page)
    for url in get_urls(html):
        html = get_news_detail(url)
        news_total = parser_news_detail(url, html)
        df = pandas.DataFrame(news_total)
        df.to_excel('news.xlsx')
        print('存储成功{}'.format(news_total))
        # df.head()
        # df.head(10)


if __name__ == '__main__':
    group = range(10)
    pool = Pool()
    pool.map(main, group)
    pool.close()
    pool.join()

