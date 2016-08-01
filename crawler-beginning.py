#coding:utf-8



'''
python爬虫常用到模块

抓取网页：urllib2	    pycurl    requests    httplib2    ......
元素提取：lxml    beautifulsoup    re
爬虫框架：scrapy


模块对比

1、网页抓取模块

	urllib2：python自带，属于标准库模块，无需单独安装。API略麻烦，但功能不多，且当抓取任务量大或使用多线程时经常莫名其妙的卡死。若有临时性且网页量不多的采集需求可以使用此模块，大范围的抓取不推荐。
	pycurl：性能强悍，功能多，所以配置较为复杂，非标准库模块，需要单独安装
	requests：没用过太多，API简单，已配置，性能好，用的人很多，适合懒人~~
	httplib2：没用过，不了解....

2、元素提取模块

	lxml(xpath)：通过xpath方法提取网页元素。提取速度快，需另行安装模块。xpath路径可以通过浏览器的工具来获取，但浏览器渲染的html跟能跟爬虫获取的html不一致，所以浏览器给的xpath路径可能是错误的。另外，多线程情况下xpath容易出现获取不到元素的情况。

	beautifulsoup(dom)：通过解析dom节点方式获取元素。方法简单，够脑残，但提取元素速度慢，还不到xpath速度的1/10，在抓取大量网页的情况下，效率会非常慢，另外本身也挺占用系统资源。模块需另行安装。

	re：通过正则方式获取元素。提取元素速度快，与xpath差不多，re模块本身也简单，但正则需要一定的学习成本。好像是自带的。

3、scrapy：相当完善的爬虫框架，初次接触，看起来配置挺复杂，但熟悉后很简单。支持python2.*，对python3.*支持度不高，主要不是scrapy本身不支持py3，而是为了运行scrapy所依附的一些模块不支持py3



文档：

- urllib2：https://docs.python.org/2/library/urllib2.html
- pycurl：http://pycurl.io/docs/latest/
- requests：
http://www.python-requests.org/en/master/
http://www.zhidaow.com/post/python-requests-install-and-brief-introduction


lxml：http://lxml.de/
beautifulsoup：http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

'''


# urllib2

# get & 拉勾

# 最简单
# import urllib2
# print urllib2.urlopen('http://www.lagou.com').read()

'''
urlopen(url, data, timeout)

第一个参数url即为URL，第二个参数data是访问URL时要传送的数据，第三个timeout是设置超时时间。
第二、三个参数是可以不传送的，data默认为空None，timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT
第一个参数URL是必须要传送的，在这个例子里面我们传送了百度的URL，执行urlopen方法之后，返回一个response对象，返回信息便保存在这里面。

'''


# 构造请求头

# import urllib2,zlib

# url = 'http://www.lagou.com'
# headers = {
# 	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
# 	"Accept-Encoding":"gzip, deflate, sdch",
# 	"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
# 	"Cache-Control":"no-cache",
# 	"Connection":"keep-alive",
# 	"Cookie":"user_trace_token=20150917181559-8043483503af406c9559efd38165a837; LGUID=20150917181602-19a0c47f-5d25-11e5-88b0-5254005c3644; utm_medium=sem; utm_campaign=SEM; fromsite=www.baidu.com; pgv_pvi=3864952832; tencentSig=5859762176; LGMOID=20160204162354-F3754C06E592596F01A0D2C1D8C113CA; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=537744A2341CA25379A23DA1235B8ED2; _gat=1; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D0fKL00c00fA-iwf07GVw0FNkUs0IBTwy00000aZ8ljY00000XLJrpK.THL0oUhY1x60UWdbuy7_pyqxuAT0T1dbPjTkuHnYP10snjIbuWFW0ZRqP1bkwRfLwW6vwWf1fRmYPDD1rj03fRczPjfYnjw7nRD0mHdL5iuVmv-b5HcYrHmdnHTkrjDhTZFEuA-b5HDvFhqzpHYkFMPdmhqzpHYhTZFG5Hc0uHdCIZwsrBtEILILQhk9uvqdQhPEUitOIgwVgLPEIgFWuHdVgvPhgvPsI7qBmy-bINqsmsKWThnqn1nkn16%26tpl%3Dtpl_10085_12986_1%26l%3D1038675489%26ie%3Dutf-8%26f%3D8%26tn%3Ddealio_dg%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; PRE_LAND=http%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1454597174,1455444482,1455506188,1455720742; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1455720750; _ga=GA1.2.438878965.1442484962; LGSID=20160217225222-0cf23236-d586-11e5-8aac-525400f775ce; LGRID=20160217225230-11b85494-d586-11e5-8aac-525400f775ce",
# 	"Host":"www.lagou.com",
# 	"Pragma":"no-cache",
# 	"Upgrade-Insecure-Requests":"1",
# 	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36",
#     }
# req = urllib2.Request(url = url, headers = headers)
# html = urllib2.urlopen(req).read()
# print zlib.decompress(html, 16+zlib.MAX_WBITS)




# 处理经过gizp压缩的网页
'''
方法1：去掉请求头中的“"Accept-Encoding":"gzip, deflate, sdch"
方法2：本地解压
import zlib
print zlib.decompress(html, 16+zlib.MAX_WBITS)
'''
	

# 构造post请求

# import urllib2,urllib

# url = 'http://qy.m.58.com/m_entlist/ajax_listinfo/2'
# headers = {
# 	"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
#     }
# post_data = {
# 	'cityListName':'',
# 	'trade':'',
# 	}
# data = urllib.urlencode(post_data)
# req = urllib2.Request(url=url, headers=headers,data=data)
# html = urllib2.urlopen(req).read()
# print html




# Pycurl通用模板 

# import pycurl,StringIO,json

# url = 'http://qy.m.58.com/m_entlist/ajax_listinfo/2'

# headers = [
# 	"User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
# ]

# data = json.dumps({
# 	"cityListName":"",
# 	"trade": ""
# 	})

# c = pycurl.Curl()	#通过curl方法构造一个对象
# #c.setopt(pycurl.REFERER, 'http://qy.m.58.com/')	#设置referer
# c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
# c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
# c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
# c.setopt(pycurl.TIMEOUT,120)			#下载超时
# c.setopt(pycurl.ENCODING, 'gzip,deflate')	#处理gzip内容，有些傻逼网站，就算你给的请求没有gzip，它还是会返回一个gzip压缩后的网页
# # c.setopt(c.PROXY,ip)	# 代理
# c.fp = StringIO.StringIO()	
# c.setopt(pycurl.URL, url)	#设置要访问的URL
# c.setopt(pycurl.HTTPHEADER,headers)		#传入请求头
# c.setopt(pycurl.POST, 1)
# c.setopt(pycurl.POSTFIELDS, data)		#传入POST数据
# c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
# c.perform()		

# code = c.getinfo(c.HTTP_CODE)	#返回状态码
# html = c.fp.getvalue()	#返回源代码

# print c.getinfo(c.TOTAL_TIME)


'''
pycurl的部分API：

pycurl.Curl() #创建一个pycurl对象的方法
pycurl.Curl(pycurl.URL, http://www.google.com.hk) #设置要访问的URL
pycurl.Curl().setopt(pycurl.MAXREDIRS, 5) #设置最大重定向次数
pycurl.Curl().setopt(pycurl.CONNECTTIMEOUT, 60)
pycurl.Curl().setopt(pycurl.TIMEOUT, 300) #连接超时设置
pycurl.Curl().setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)") #模拟浏览器
pycurl.Curl().perform() #服务器端返回的信息
pycurl.Curl().getinfo(pycurl.HTTP_CODE) #查看HTTP的状态 类似urllib中status属性


pycurl.NAMELOOKUP_TIME 域名解析时间
pycurl.CONNECT_TIME 远程服务器连接时间
pycurl.PRETRANSFER_TIME 连接上后到开始传输时的时间
pycurl.STARTTRANSFER_TIME 接收到第一个字节的时间
pycurl.TOTAL_TIME 上一请求总的时间
pycurl.REDIRECT_TIME 如果存在转向的话，花费的时间
pycurl.HTTP_CODE HTTP 响应代码
pycurl.REDIRECT_COUNT 重定向的次数
pycurl.SIZE_UPLOAD 上传的数据大小
pycurl.SIZE_DOWNLOAD 下载的数据大小
pycurl.SPEED_UPLOAD 上传速度
pycurl.HEADER_SIZE 头部大小
pycurl.REQUEST_SIZE 请求大小
pycurl.CONTENT_LENGTH_DOWNLOAD 下载内容长度
pycurl.CONTENT_LENGTH_UPLOAD 上传内容长度
pycurl.CONTENT_TYPE 内容的类型
pycurl.RESPONSE_CODE 响应代码
pycurl.SPEED_DOWNLOAD 下载速度
pycurl.INFO_FILETIME 文件的时间信息
pycurl.HTTP_CONNECTCODE HTTP 连接代码
'''




# 案例：抓取 qy.m.58.com 所有公司信息

import pycurl,StringIO,json,time,re,sys
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

headers = [
	"User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
]

data = json.dumps({
	"cityListName":"",
	"trade": ""
	})


def getHtml(url,headers,pagetype):

	if pagetype == 'list':
		c = pycurl.Curl()	#通过curl方法构造一个对象
		#c.setopt(pycurl.REFERER, 'http://qy.m.58.com/')	#设置referer
		c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
		c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
		c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
		c.setopt(pycurl.TIMEOUT,120)			#下载超时
		c.setopt(pycurl.ENCODING, 'gzip,deflate')	#处理gzip内容，有些傻逼网站，就算你给的请求没有gzip，它还是会返回一个gzip压缩后的网页
		# c.setopt(c.PROXY,ip)	# 代理
		c.fp = StringIO.StringIO()	
		c.setopt(pycurl.URL, url)	#设置要访问的URL
		c.setopt(pycurl.HTTPHEADER,headers)		#传入请求头
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, data)		#传入POST数据
		c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
		c.perform()		

		code = c.getinfo(c.HTTP_CODE)	#返回状态码
		html = c.fp.getvalue()	#返回源代码

		return html

	elif pagetype == 'detail':

		c = pycurl.Curl()	#通过curl方法构造一个对象
		#c.setopt(pycurl.REFERER, 'http://qy.m.58.com/')	#设置referer
		c.setopt(pycurl.FOLLOWLOCATION, True)	#自动进行跳转抓取
		c.setopt(pycurl.MAXREDIRS,5)			#设置最多跳转多少次
		c.setopt(pycurl.CONNECTTIMEOUT, 60)		#设置链接超时
		c.setopt(pycurl.TIMEOUT,120)			#下载超时
		c.setopt(pycurl.ENCODING, 'gzip,deflate')	#处理gzip内容，有些傻逼网站，就算你给的请求没有gzip，它还是会返回一个gzip压缩后的网页
		# c.setopt(c.PROXY,ip)	# 代理
		c.fp = StringIO.StringIO()	
		c.setopt(pycurl.URL, url)	#设置要访问的URL
		c.setopt(pycurl.HTTPHEADER,headers)		#传入请求头
		c.setopt(c.WRITEFUNCTION, c.fp.write)	#回调写入字符串缓存
		c.perform()		

		code = c.getinfo(c.HTTP_CODE)	#返回状态码
		html = c.fp.getvalue()	#返回源代码

		return html	

	else:
		return '参数写错了亲~~'


for page in range(1,1000):
	
	url = 'http://qy.m.58.com/m_entlist/ajax_listinfo/%s' % page
	
	for url_datail in ['http://qy.m.58.com/m_detail/%s/' % id for id in  re.findall(r'"i":(\d+),',getHtml(url,headers,'list'))]:
		html_detai =  getHtml(url_datail, headers, 'detail').decode('utf-8','ignore')

		content = etree.HTML(html_detai)

		company_name = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[1]/h2')[0].text.replace('公司全称：','')
		company_nature = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[1]')[0].text.strip()
		company_num = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[2]')[0].text
		company_indutry = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[3]/a')[0].text
		company_adress = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[4]')[0].text

		print company_name,company_nature,company_num,company_indutry


		time.sleep(5)



