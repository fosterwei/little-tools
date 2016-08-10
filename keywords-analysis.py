#coding:utf-8
import re
```正则提取字符串函数```
def search(req,line):
  data=re.search(req,line)
  if data:
    jieguo=data.group(1)
  else:
    jieguo='no'
  return jieguo
word_class={}
for line in open('keyword'):
  line=line.strip().split(' ')
  
  word=line[0]
  try:
    searchs=int(line[1])
    contend=int(line[2])
  except(ValueError,TypeError) as e:
    continue
  group=line[3]
  
  cixing=search('(招聘.*)',word)#提取含'招聘'的词，匹配
  
  if cixing=='招聘'：#如果词就是这个的话
    continue
  
  if word_class.has_key(cixing):
    word_class[cixing]['cishu']+=1
    word_class[cixing]['searvhes']+=searches
    word_class[cixing]['contend']+=contend
    word_class[cixing]['contend_average']=float(word_class[cixing]['contend'])/float(word_class[cixing]['cishu'])
  else:
    word_class[cixing]={'cishu':1,'searches':searches,'contend':contend,'contend_average':0}
    
```按值进行排序```
print '+'+'-'*30+'+'+'-'*12+'+'+'-'*12+'+'+'-'*12+'+'+'-'*20+'+'

    
