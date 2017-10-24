import re

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

commentURL = ''


# 将抓取的内文信息方法整理成函数式
def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    # 获取的内容编码不为utf-8需要转换为utf-8
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


# 获取评论数
def getCommentCounts(newsurl):
    m = re.search('doc-i(.+).shtml', newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['resul']['count']['total']

#http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=5&callback=newsloadercallback&_=1508856676182
#http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=6
# 建立剖析清单链接函数
def parseListLinks(url):
    newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('newsloaddrcallback(').strip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent))
    return newsdetails