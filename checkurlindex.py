#coding:utf-8

import requests,csv,os,time
from bs4 import BeautifulSoup
from urllib.parse import urlencode

seconds=input('Enter number of seconds to wait between URL checks: ')
output=os.path.join(os.path.dirname(__file__),input('Enter a filename (minus file extension): ')+'.csv')
urlinput=os.path.join(os.path.dirname(__file__),input('Enter input text file: '))
urls=open(urlinput,"r")

proxies={
  'https':'http://localhost:8123',
  'https':'http://localhost:8123'
  }

user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
headers={'User-Agent':user_agent}

f=csv.writer(open(output,"w+", newline="\n",encoding="utf-8"))
f.writerow(["URL","Indexed"])

for line in iter(urls):
  query={'q':'info:'+line}
  google="https://www.google.com/search?" + urlencode(query)
  data=requests.get(google,headers=headers,proxies=proxies)
  data.encoding='ISO-8859-1'
  soup=BeautifulSoup(str(data.content),"html.parser")
  try:
    check=soup.find(id="rso").find("div").find("div").find("h3").find("a")
    href=check['href']
    f.writerow([line,"True"])
    print(line+ "is indexed!")
  except AttributeError:
    f.writerow([line,"False"])
    print(line+ "is NOT indexed!")
  print("Waiting" + str(seconds)+" second until checing next URL.\n")
  time.sleep(float(seconds))
urls.close()
