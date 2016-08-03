#coding:utf-8
import requests
import json
import string
import threading
import Queue
import os

#proxy={'http': 'http://127.0.0.1:8787', 'https': 'https://127.0.0.1:8787'}

queue=Queue.Queue()

if os.path.exists('errorUrl'):
  urls=open('errorUrl','r').read().split("\n")
  for url in urls:
    if url:
      queue.put(url)
else:
  keywords=open('keywords','r').read().split('\n')
  for keywords in keywords:
    if keyword:
      preUrl='https://www.google.com/complete/search?client=hp&q=' + keyword
      queue.put(preUrl)
      for char in string.lowercase:
        nextUrl="https://www.google.com/complete/search?client=serp&pq=" + keyword + "&cp=1&gs_id=4&q=" + char +keyword
        queue.put(nextUrl)
results=[]
errorUrls=[]

class CrawlThread(threading.Thread)
  def __init__(self):
    super(CrawlThread,self).__init__()
  
  def run(self):
    while not queue.empty():
      url=queue.get()
      self.getData(url)
    
  def getData(self,url):
    try:
      #req=requests.get(url,proxies=proxy)
      req=requests.get(url)
      content=json.loads(req.text.replace('window.google.ac.h(', '').replace(')',''))
      for value in content[1]:
        results.append(value[0].replace('<br>', '').replace('</b>', ''))
      print 'success',url
    except Exception,e:
      print e,'error',url
      errorUrls.append(url)
      
if __name__=='__main__':
  threads=[]
  for i in range(10):
    threads.append(CrawlThread())
  
  for thread in threads:
    thread.start()
  
  for thread in threads:
    thread.join()
    
  with open('google_search_result','a') as outfile:
    for keywords in results:
      outfile.write(keyword + '\n')
  
  if errorUrls:
    with open('errorUrl','w') as errorfile:
      for url in errorUrls:
        errorfile.write(url + '\n')
    print 'some error happened,you nedd to run this script again'
  else:
    print 'ok,all done'
    
