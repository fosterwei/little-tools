#-*- coding:utf-8 -*-
import request,multiprocessing
import re,sys

reload(sys)
sys.setdefaultencoding('utf-8')

DBUG=0

reBODY = re.compile(r'<body.*?>([\s\S]*?)<\/body>', re.I)
reBODY2=re.compile(r'<scrip.*?>([\s\S]*?)<\/script>', re.I)
reCOMM=r'<!--.*?-->'

def search(req,html):
  text=re.search(req,html)
  if text:
    data=text.group(1)
  else:
    data='no'
  return data

class Extractor():
  def __init__(self, url="",blockSize=3,timeout=5,image=False):
    self.url=url
    self.blockSize=blockSize
    self.timeout=timeout
    self.saveImage=image
    self.rawPage=""
    self.ctexts=[]
    self.cblocks=[]
    
    def getRawPage(self):
      host=search('^([^/]*?)/',re.sub(r'(https|http)://','',self.url))
      
      headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            #"Cookie":"__cfduid=df26a7c536a0301ccf36481a14f53b4a81469608715; BIDUPSID=E9B0B6A35D4ABC6ED4891FCC0FD085BD; PSTM=1474352745; lsv=globalTjs_97273d6-wwwTcss_8eba1c3-routejs_6ede3cf-activityControllerjs_b6f8c66-wwwBcss_eabc62a-framejs_902a6d8-globalBjs_2d41ef9-sugjs_97bfd68-wwwjs_8d1160b; MSA_WH=1433_772; BAIDUID=E9B0B6A35D4ABC6ED4891FCC0FD085BD:FG=1; plus_cv=1::m:2a9fb36a; H_WISE_SIDS=107504_106305_100040_100100_109550_104341_107937_108437_109700_109794_107961_108453_109737_109558_109506_110022_107895_107917_109683_109588_110072_107318_107300_107242_100457; BDUSS=XNNMTJlWEdDdzFPdU1nSzVEZ1REYn4tNWNwZk94NVducXpaaThjWjE4bU1TQXRZQVFBQUFBJCQAAAAAAAAAAAEAAADLTBsKYTYzMTM4MTcwMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIy741eMu-NXQ; BDRCVFR[ltbVPlNi2ac]=mk3SLVN4HKm; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; BDRCVFR[uLXjBGr0i56]=mbxnW11j9Dfmh7GuZR8mvqV; rsv_jmp_slow=1474644236473; sug=3; sugstore=1; ORIGIN=0; bdime=21110; H_PS_645EC=60efFRJ1dM8ial205oBcDuRmtLgH3Q6NaRzxDuIkbMkGVXNSHmXBfW0GZL4l5pnj; BD_UPN=123253; BD_CK_SAM=1; BDSVRTM=110; H_PS_PSSID=17947",
            "Host":host,
            "Pragma":"no-cache",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        }
      
      proxyHost="proxy.abuyun.com"
      proxyPort="9010"
      
      #代理隧道验证信息
      proxyUser = "天王盖地虎"
      proxyPass = "裤衩遮不住"
      proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
          "host" : proxyHost,
          "port" : proxyPort,
          "user" : proxyUser,
          "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }

        try:
            f = requests.get(self.url,headers=headers,timeout=30)
        except Exception as e:
            raise e

        code = f.status_code
        content = f.content

        '''修改python2这个王八蛋使用request对网页编码误识别为iso-8859-1的BUG'''
        if f.encoding.lower() != 'utf-8':
            charset = re.compile(r'content="text/html;.?charset=(.*?)"').findall(content)
            coding = f.encoding.lower()
            print coding, f.headers['content-type']
            try:
                if len(charset)>0 and charset[0].lower()!=coding:
                    content = content.decode('gbk').encode('utf-8')
                elif coding == 'gbk' or coding == 'gb2312':
                    content = content.decode('gbk').encode('utf-8')
            except:
                pass

        return code,content

    def processTags(self):
        self.body = re.sub(reBODY, "", self.body)
        self.body = re.sub(reBODY2, "", self.body)
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(r'<(?!p|/p)[^<>]*?>|下一篇.*','',self.body)
        self.body = re.sub(r'<p[^>]*?>','<p>',self.body)
        #self.body = re.sub(reTAG, "", self.body)
        self.body = re.sub(r'[\t\r\f\v]','',self.body)

        '''抽取图片'''
        self.img = search(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>',self.body)
        if 'http' not in self.img:
            self.img = '<img src="%s%s" >' % (search('^([^/]*?)/',re.sub(r'(https|http)://','',self.url)),self.img)

    def processBlocks(self):
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))

        maxTextLen = max(self.cblocks)

        if DBUG: print(maxTextLen)

        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1

        content = "".join(self.ctexts[self.start:self.end])
        return content

    def getContext(self):
        code, self.rawPage = self.getRawPage()
        self.body = re.findall(reBODY, self.rawPage)[0]

        if DBUG: print(code, self.rawPage)

        self.processTags()
        return self.processBlocks()

url = 'http://news.xiancity.cn/readnews.php?id=337002'

def getIndex(url):
    if __name__ == '__main__':
        ext = Extractor(url=url,blockSize=1, image=False)
        text = ext.getContext() 
        print '@@@@@@@@@@> %s <@@@@@@@@@@' % url  
        print text
        print '\n\n\n\n'




url_list  = [
    "http://www.sdpc.gov.cn/fzgggz/flfg/dfdtn/201701/t20170117_835391.html",
    "http://zgsc.china.com.cn/difang/2017-01-17/575919.html",
    "http://sports.sohu.com/20170117/n478969110.shtml",
    "http://news.medlive.cn/all/info-news/show-123334_97.html",
    "http://www.yangzhou.gov.cn/canlian/jjccldt/201701/b20bd6a73b61490f85557cf0a6153942.shtml",
    "http://www.yznews.com.cn/xsqpd/yizheng/2017-01/17/content_5879719.htm",
    "http://www.jiaxing.gov.cn/swhj/gzdt_6157/qtywxx_6161/201701/t20170117_663181.html",
    "http://www.cqn.com.cn/pp/content/2017-01/17/content_3849688.htm",
    "http://news.ifeng.com/a/20170117/50589300_0.shtml",
    "http://www.shyouth.net/html/defaultsite/root_qcsh/2017-01-17/Detail_2157200.htm",
    "http://zgsc.china.com.cn/zxun/zhzx/2017-01-17/575706.html",
    "http://gps.zol.com.cn/624/6243851.html",
    "http://www.gx211.com/news/2017117/n9886428743.html",
    "http://aft.ts.cn/content/2017-01/17/content_12482674.htm",
    "http://news.xiancity.cn/readnews.php?id=337002",
    "http://news.sjtu.edu.cn/info/1010/1281952.htm",
    "http://hangzhou.zjol.com.cn/system/2017/01/17/021423613.shtml",
    "http://info.cloth.hc360.com/2017/01/162137861109.shtml",
    "http://www.yangzhou.gov.cn/canlian/sqcdt/201701/868937e1cc9e4805b2ea5358c84e2e3a.shtml",
    "http://house.ifeng.com/detail/2017_01_16/50984839_0.shtml",
]

pool = multiprocessing.Pool(processes=3)
for url in url_list:
    pool.apply_async(getIndex, (url, ))
pool.close()
pool.join()


      
    
