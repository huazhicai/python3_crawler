#!/usr/bin/env python
import requests
from pandas import json

res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
print(type(res))
print(res.text)

from bs4 import BeautifulSoup

html_sample = '\
<html>\
<body>\
<h1 id="title">Hello World</h1>\
<a href="#" class="link">This is link1</a>\
</body>\
</html>'
soup = BeautifulSoup(html_sample, 'html.parser')
print(type(soup))
print(soup.text)

soup = BeautifulSoup(html_sample, 'html.parser')
header = soup.select('h1')
print(header)

# 使用select找出所有id为title的元素（id前面加#）
alink = soup.select('#title')
print(alink)
for link in soup.select('.link'):
    print(link)

alinks = soup.select('a')
for link in alinks:
    print(link['href'])

for news in soup.select('.news-item'):
    if len(news.select('h2')) > 0:
        h2 = news.select('h2')[0].text
        time = news.select('.time')[0].text
        a = news.select('a')[0]['href']
        print(time, h2, a)

# 取得新闻内文
res = requests.get('http://news.sina.com.cn/o/2017-09-26/doc-ifymenmt7129299.shtml')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

# 抓取标题
soup.select('#artibodyTitle')[0].text
# 取得时间
timesource = soup.selct('.time-source span a')[0].contents[0].strip()
timesource
# 取得来源
medianame = soup.select('.time-source span a')[0].text
medianame

# 时间字符串转换
from datetime import datetime

# 字符串转时间 - strptime
dt = datetime.strptime(timesource, '%Y年%m月%d日%H:%M')
dt
# 时间转字符串 - strftime
dt.strftime('%Y-%m-%d')

# 将每一段落加到list中
article = []
for p in soup.select('#artibody p')[:-1]:
    article.append(p.text.strip())
' '.join(article)
' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])

# 取得编辑名称
editor = soup.select('.article-editor')[0].text.lstrip('责任编辑:')
# 取得评论数
soup.select('#commentCountl')
jd = json.loads(comments.text.strip('var data='))
jd['result']['count']['total']

# 如何取得新闻编号
newsurl = 'http://news.sina.com.cn/o/2017-09-26/doc-ifymenmt7129299.shtml'
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
newsid
import re

m = re.search(r'doc-i(.*).shtml', newsurl)
print(m.group(1))

# 将抓取评论数的方法整理成一函式
commentURL = ''


def getCommentCounts(newsurl):
    m = re.search('doc-i(.+).shtml', newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


# 将抓取的内文信息方法整理成函数式
import requests
from bs4 import BeautifulSoup


def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    result['newssource'] = soup.select('.time-source span a')[0].text
    timesource = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.strptime(timesource, '%Y年%m月%d日%H:%M')
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].strip('责任编辑：')
    result['comments'] = getCommentCounts(newsurl)
    return result


# 找到分页连结
# 选择network 点选js 点到下面连接

# 剖析分页信息
res = requests.get('')
jd = json.loads(res.text.lstrip('newsloadercallback(').rstrip(');'))
jd
for ent in jd['result']['data']:
    print(ent['url'])


# 建立剖析清单链接韩式
def parseLisLinks(url):
    newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('newsloaddrcallback(').strip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent))
    return newsdetails


# 使用for 循环产生多页连结
url = ''
for i in range(1, 10):
    newsurl = url.format(i)
    print(nesurl)

# 批次抓取每页新闻内文
url = ''
news_total = []
for i in range(1, 3):
    newsurl = url.format(i)
    newsary = parseLisLinks(newsurl)
    news_total.extend(newsary)

# 使用pandas整理资料
import pandas

df = pandas.DataFrame(news_total)
df.head()
df.head(10)

# 保存数据到数据库
# 将资料保存至excel
df.to_excel('news.xlsx')

# 将资料保存至资料库
import sqlite3

with sqlite3.connect('news.sqlite') as db:
    db.to_sql('news', con=db)


