### 爬取新浪新闻资讯

使用requests.get获取新闻页面信心，用BeautifulSoup解析页面

思路是需求导向，逆向思维

需要爬取什么: 新闻标题，新闻时间，新闻来源， 评论数， 新闻正文， 编辑， 以及
新闻评论
 
那就从某篇特定新闻开始，例如： url='http://news.sina.com.cn/c/nd/2017-10-17/doc-ifymvece2239312.shtml'
打开网络监控，观察Doc路由数据，查看搜索需要的数据，在里面，数据路径就对了。然后就就可以用requests 获取数据，
用BeautifulSoup解析数据，

爬取分页链接 


