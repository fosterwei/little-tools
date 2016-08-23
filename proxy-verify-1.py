#coding:utf-8

import urllib2,zlib,json,time,re,threading

ISOTIMEFORMAT='%Y-%m-%d %X'

rawProxyList=[] #所有代理ip
checkedProxyList=[]#验证通过的代理

print "开始获取http代理》》》》"

#正则提取模块
def search(req,line):
  text=re.search(req,line)
  if text:
    data=text.group(1)
  else:
    data='no'
  return data
  
url='...........此处为代理ip获取链接（付费）(http://multiproxy.org/txt_all/proxy.txt)'

request=urllib2.Request(url)
opener=urllib2.build_open(request)
resonse=opener.open(request)
html=response.read()

for ip in html.split('\n')
  ip.strip()
  rawProxyList.append(ip)
  
#print '已获得%s个代理' % len(html.split('\n'))

class ProxyCheck(threading.Thread):
  def __init__(self,proxyList):
    threading.Thread.__init__(self)
    self.proxyList=proxyList
    self.timeout=10 #设置超时时间
    self.testUrl="http://www.google.com" #设置一个访问的网站
    
  def checkProxy(self):
    for proxy in self.proxyList:
      proxyHandler=urllib2.ProxyHandler({"http":r'http://%s' % proxy})
      opener=urllib2.build_opener(proxyHandler)
      opener.addheaders=[('User-agetn','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')]
      t1=time.time() #获取请求网页的开始时间
      
      try:
        req=opener.open(self.testUrl,timeout=self.timeout)
        result=req.read()
        timeused=time.time() - t1   #实际访问网页的耗时
        
        title=re.search(r'<title>(.*?)</title>',result)
        if title:
          title=title.group(1)
        else:
          title='不能打开网页'
        
        print timeused,title,proxy
        
        if (timeused < 5) and title =='Google': #如果，当前的ip访问网页耗时< 5s,且返回的源代码的title等于‘Google’,则这个Ip通过验证
          checkedProxyList.append((proxy,timeused))
        else:
          continue
        
        except Exception,e:
          print e
          continue
  
  def sort(self):
    sorted(checkedProxyList,cmp=lambda x,y:cmp(x[1],y[1]))
    
  def run(self):
    self.checkProxy()
    self.sort()

if __name__=="__main__":
  getThreads=[]
  checkThreads=[]
  
  n=50 #设置线程数
  for i in range(n):
    t=ProxyCheck(rawProxyList[((len(rawProxyList)+(n-1))/n]) * i:((len(rawProxyList)+(n-1))/n) * (i+1)])
    checkThreads.append(t)
    
  for i in range(len(checkThreads)):
    checkThreads[i].start()
  for i in range(len(checkThreads)):
    checkThreads[i].join()
  #print   "........总共%s 个代理，共有%s个通过校验....." % (len(rawProxylist),len(checkedProxyList))
  
  f=open("daili.txt",'W+')
  
  currtent_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  
  f.write("代理更新于：%s,共计通过验正\n\n" % (current_time,len(checkedProxyList)))
  
  for proxy in checkedProxyList:
    #print "qualified:%s\t%s" % (proxy[0],proxy[1])
    f.write(proxy[0]+"\n")
  f.close
