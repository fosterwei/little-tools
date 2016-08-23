#coding:utf-8
import urllib,re,threading,random,pycurl,StringIO,time,csv
form bs4 import BeautifulSoup as bs

csvfile=open('serp_html.csv','wb')# 新建一个存放百度数据的csv文件

daili_list=[]# 新建一个存放代理IP的列表
# 从daili.txt文件中随机提取出1个IP
def ip():
  for x in open('daili.txt'):
    x=x.strip()
    daili_list.append(x)\
  newip=random.choice(daili_list)
  return newip
# 随机提取一个cookie
def daili_cookie():
  cookie_list=[
    'BIDUPSID=4B0DC2F54860625BA83681F98C507951; BAIDUID=791ED7F86F43AF44A3808AB244404E1A:FG=1; PSTM=1441808712; BDUSS=RINjR4TVFBeHpKLTNIREJ4MkFUT0h3SFdFWlQwdHJIdlZORzc5aW00QWpnQ2hXQVFBQUFBJCQAAAAAAAAAAAEAAAAJkstJv7TXvMTj1NnM-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACPzAFYj8wBWd0; BDSFRCVID=tc4sJeC62wRkfgj40DCH-qjWNeMhJHrTH6aov8OLjxwzgCDAMXfsEG0Pt7lQpYD-MjrsogKK0mOTHUcP; H_BDCLCKID_SF=JJ4O_C-5tCv8fjrzhJbM-J3H-UnLq5btX57Z0lOnMp05jpjDjT823PFTKPKtaxTnW56uXRPyMn3zODO_e6-bDjQ3DaAs-460aK_X3bRVKbk_jR-k-PnVep8qQhbZKxJmMgkeoxJtJK-2SnbVKU5mytKXhq6qWnvN3mn2LIOFfDDbbDtxD5_32JLHqx5Ka43tHD7yWCvd-M75OR5JLn7nDUFdhpDJJpvm3Ibv3xQ73hbAVUnjqt8hXpjyyGCftj_JtnIeVb3HbTrMHJo1btQhq4tehHRJ553eWDTm_Do5LJvtenFmDMOTyKuLMRJwKxr3WebH-pPKKR7-bh7sMR7b24-dQ-QuXP5e3mkjbP-5aUj2oq-zXt6KKP4syP4j2xRnWNT2bIcJ-J8XhI86j5rP; BDRCVFR[ltbVPlNi2ac]=mk3SLVN4HKm; BD_HOME=1; BD_UPN=123253; sug=3; sugstore=1; ORIGIN=0; bdime=0; H_PS_645EC=5894fstaLnB%2Bx%2F1GkrMZWqKZiK7vVRh2YO9qL7vORnC1%2BY%2BbXOz%2BVwgRSuL80CXajur4; WWW_ST=1443000293566; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; BDSVRTM=146; H_PS_PSSID=17143_16716_1431_17100_12824_14430_12867_17245_17104_17182_17000_17003_17073_15864_17348_12413_13932_17351_14924_17050',
    'BAIDUID=1F63B9A436CE0DBA3C7D1849367F30CB:FG=1; BIDUPSID=1F63B9A436CE0DBA3C7D1849367F30CB; PSTM=1441517552; BD_UPN=13314452; ispeed_lsm=10; ispeed=1; sug=3; ORIGIN=0; bdime=0; BDUSS=m5TYjhuODBCWHpQcVNYV2FDeS1BLUFzV0t3WTQwcTctUkV2S2x6M1ZBcjZMU2RXQVFBQUFBJCQAAAAAAAAAAAEAAAChsHQiuqPAtjIyOQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPqg~1X6oP9Vc; H_PS_645EC=217efvXBesXqzUCKdQMslc2uc5TwenrsDDar8Tir0uHuQfpJAglN689%2BHSNYep8LeRTy; BD_HOME=1; H_PS_PSSID=16230_17326_1447_12657_12824_14432_12867_17246_17105_14952_17001_17004_17072_15713_17347_11798_13932_17352_14554_17051; __bsi=12190823682724921622_00_0_I_R_166_0303_C02F_N_I_I_0; sugstore=1',
    'Cookie: BAIDUID=1F63B9A436CE0DBA3C7D1849367F30CB:FG=1; BIDUPSID=1F63B9A436CE0DBA3C7D1849367F30CB; PSTM=1441517552; BDUSS=m5TYjhuODBCWHpQcVNYV2FDeS1BLUFzV0t3WTQwcTctUkV2S2x6M1ZBcjZMU2RXQVFBQUFBJCQAAAAAAAAAAAEAAAChsHQiuqPAtjIyOQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPqg~1X6oP9Vc; H_PS_PSSID=16230_17326_1447_12657_12824_14432_12867_17246_17105_14952_17001_17004_17072_15713_17347_11798_13932_17352_14554_17051; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0'
    ]
  cookie=random.choice(cookie_list)
  return cookie
#随机提取一个UA
def getUA():
  uaList= [
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+TencentTraveler)',
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.4506.2152;+.NET+CLR+3.5.30729)',
        'Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.89+Safari/537.1',
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1)',
        'Mozilla/5.0+(Windows+NT+6.1;+rv:11.0)+Gecko/20100101+Firefox/11.0',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+SV1)',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+KB974489)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
  headers=random.choice(uaList)
  return headers
  
#请求网页源代码，需要传入url，headers两个变量
def getHtml(url,headers):
  while 1:
    try:
      newip=ip()
      c=pycurl.Curl()
      c.setopt(pycurl.MAXREDIRS,2)
      c.setopt(pycurl.REFERER,url)
      #c.setopt(pycurl.FOLLOWLOCATION,True)
      c.setopt(pycurl.CONNECTTIMEOUT,10)
      c.setopt(pycurl.TIMEOUT,15)
      c.setopt(pycurl.ENCODING,'gzip,deflate')
      c.setopt(c.PROY,newip)
      c.fp=StringIO.StringIO()
      c.setopt(pycurl.URL,url)
      c.setopt(Pycurl.HTTPHEADER,headers)
      c.setopt(c.WRITEFUNCTION,c.fp.write)
      c.perform()
      code=c.getinfo(c.HTTP_CODE)
      html=c.fp.getvalue()
      if '="http://verify.baidu.com' in html:
        print '出验证码，重试'
        continue
      elif '302 Found' in html or code !=200:
        print '代理失效，重试'
      else:
        return html
    except EXCEPTION,e:
      #print e
      continue
#通过正则提取元素
def search(req,line):
  text=re.search(req,line)
  if text:
    data=text.group(1)
  else:
    data='no'
  return data

#线程要执行的内容
def getInfo(word):
  url='http://www.baidu.com/s?wd=%s' % urllib.quote_plue(word)   #构造getHTML()要请求的url
  
  #构造请求头信息
  headers=[
        "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding:gzip, deflate, sdch",
        "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control:max-age=0",
        "Connection:keep-alive",
        "Cookie:%s" % daili_cookie(),
        "Host:www.baidu.com",
        "RA-Sid:7739A016-20140918-030243-3adabf-48f828",
        "RA-Ver:2.10.4",
        "User-Agent:%s" % getUA()
    ]
    
    html=getHtml(url,headers)
    mutex.acquire()   #创建锁
    count=search(r'百度为您找到相关结果约(.*?)个',html).replace(',','')
    '''beautiful方法'''
    soup=bs(html)
    '''提取百度1-10名的块级元素'''
    b_tags=soup.find_all('div',{'class':'result c-container'})
    '''将百度1-10名块级元素的代码下载至serp_html.csv，之后在计算首页词数、展现次数、排名质量分等数据需求'''
    
    for line in b_tags:
      newline=str(line)
      number=search(r'di="(\d+)"',newline)
      
      data=[]
      data.append(word)
      data.append(count)
      data.append(newline)
      writer=csv.writer(csvfile,dialect='excel')
      writer.writerow(data)
    
    print '>>已抓取：%s,返回%s条搜索结果' % (word,count)
    
    mutex.release()   #释放锁
    
#每个线程处理一个区间
def getRange(1,r):
  for i in url_list[1:r]:
    getInfo(i)
    
url_list=[]
for line in open('word'):
  word=line.strip()
  url_list.append(word)
totalThread=100 #新建100个线程
gap=(len(url_list)=1)/totalThread #获取每个线程要住区的网页数

mutex=threading.Lock()#threading.Lock()方法添加互斥锁

for i in range(1,len(url_list),gap):
  t=threading.Thread(target=getRange,args=(i,i+gap,))
  t.start()
  
      
  
