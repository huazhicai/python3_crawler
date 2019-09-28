### 爬取信息

[起始链接](http://chinackd.medidata.cn/login.jsp#/blgl/bllb0/30042)


1/ 单线程
2/ 登录
3/ 多线程
4/ 异步

网站分析：
第一步需要登录才能看到信息，所以可以直接复制cookie
或者模拟登录

索引页：病例列表，需要提取每条记录编号，然后构成详情页url,
索引页病例列表信息是ajax异步加载，数据类型是xml
所以需要找到ajax数据api接口，

ajax接口：http://chinackd.medidata.cn/doAction?Action=runCaseCustQry&CCQId=30042&start=0&limit=70000&ExtTerm_0=&tranid=0
limit返回的数据条数，当limit>实际数条数，返回的是实际数据条数


登录有加密，需要执行js加密
