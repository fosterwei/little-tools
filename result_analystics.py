#coding:utf-8
import csv,re
rank_dict={}

def search(req,line):
  text=re.search(req,line)
  if text:
    data=text.group(1)
  else:
    data='no'
  return data
  
csvfile=file('serp_html.csv','rb')
reader=csv.reader(csvfile)

'''
site：要查询排名的网站
word_lsit：site这个站有哪些词排名首页
show：site这个网站在百度首页展现了多少次
rank：site这个网站有多少词排到百度首页
'''
def dict(site):
  if site in domain:# 如果site包含在domain中
    if rank_dict.has_key(site):
      rank_dict[site]['show']+=1
      if word not in rank_dict[site]['word_list']:
        rank_dict[site]['rank']+=1
        rank_dict[site]['word_list'].append(word)
    else:
      rank_dict[site]={'word_list':[word],'show':1,'rank':1}
  return rank_dict
  '''输出百度搜索结果数据：当前关键词，排名，排名网站，百度url（需转义后才是真实的url），标题'''
  for line in reader:
    word=line[0]
    html=line[2]
    count=line[1]
    
    number=search(r'id="(\d+)"',html)
    domain=search(r'<a class="c-showurl"[^>]*?>(.*?)</a>',html)
    bdurl=search(r'href="(http://www.baidu.com/link\?url=[^"]*?)"',html)
    title=search(r'"title":"([^"]*?)"',html)
    
    dict('www.ganji.com')
    dict('www.jobui.com')
    dict('58.com')
print rank_dict
