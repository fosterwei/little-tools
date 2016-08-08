#coding:utf-8
import pycrul,StringIo,json,time,re,sys
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

headers=["User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",]

data=json.dumps({"cityListName":"",
                "trade":""})

def getHtml(url,headers,pagetype):
  
  if pagetype=='list':
    c=pycurl.Curl()#通过curl方法构造一个对象
    #c.setopt(pycurl.REFERER,'http://qy.m.58.com/') #设置referer
    c.setopt(pycurl.FOLLOWLOCATION,True) #自动进行跳转抓取
    c.setopt(pycurl.MAXREDIRS,5)   #设置最多跳转多少次
    c.setopt(pycurl.CONNECTTIMEOUT,60)#设置连接超时
    c.setopt(pycurl.TIMEOUT,120) #下载超时
    c.setopt(pycurl.ENCODING,'gzip,deflate')#处理gzip内容
    #c.setopt(c.PROXY,ip)#代理
    c.fp=StringIO.StringIO()
    c.setopt(pycurl.HTTPHEADER,headers)#传入请求头
    c.setopt(pycurl.POST,1)
    c.setopt(pycurl.POSTFIELDS,data)#传入post数据
    c.setopt(c.WRITEFUNCTION,c.fp.write)#回调写入字符串缓存
    c.perform()
    
    code=c.getinfo(c.HTTP_CODE)#返回状态码
    html=c.fp.getvalue()#返回源代码
    
    return html
    
  elif pagetype=='datail':
    c=pycurl.Curl()#通过curl方法构造一个对象
    #c.setopt(pycurl.REFERER,'http://qy.m.58.com/') #设置referer
    c.setopt(pycurl.FOLLOWLOCATION,True) #自动进行跳转抓取
    c.setopt(pycurl.MAXREDIRS,5)   #设置最多跳转多少次
    c.setopt(pycurl.CONNECTTIMEOUT,60)#设置连接超时
    c.setopt(pycurl.TIMEOUT,120) #下载超时
    c.setopt(pycurl.ENCODING,'gzip,deflate')#处理gzip内容
    #c.setopt(c.PROXY,ip)#代理
    c.fp=StringIO.StringIO()
    c.setopt(pycurl.HTTPHEADER,headers)#传入请求头
    c.setopt(pycurl.POST,1)
    c.setopt(pycurl.POSTFIELDS,data)#传入post数据
    c.setopt(c.WRITEFUNCTION,c.fp.write)#回调写入字符串缓存
    c.perform()
    
    code=c.getinfo(c.HTTP_CODE)#返回状态码
    html=c.fp.getvalue()#返回源代码
    
    return html
  
  else:
    return '参数错误'
    
for page in range(1,1000):
  url='http://qy.m.58/m_entlist/ajax_listinfo/%s' % page
  
  for url_datai in ['http://qy.m.58.com/m_detail/%s/' % id for in re.findall(r'"i":(\d+),',getHtml(url,headers,'list'))]:
    html_detail=getHtml(url_datail,headers,'detail').decode('utf-8','ignore')
    
    content=etree.HTML(html_detail)
    
    company_name=content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[1]/h2')[0].text.replace('公司全称：','')
    company_nature = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[1]')[0].text.strip()
		company_num = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[2]')[0].text
		company_indutry = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[3]/a')[0].text
		company_adress = content.xpath('/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/dl/dd[4]')[0].text
		
		print company_name,company_nature,company_num,company_indutry
		
		time.sleep(5)
    
    
    
    
    
