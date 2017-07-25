#-*- coding:utf-8 -*-

filename='pes2016'

datas={}

keywordRoot='pes 2016'
for line in open(filename,'r'):
  keywords=line.split('\t',1)
  keywords=keywords[0]
  if keywordsRoot in keywords: #包含'pes 2016'的数据才是合法数据
    keywords=keywords.split() #将关键词字符串分成列表形式
    length=len(keywords) #计算出列表内元素的个数
    for i in range(3,length+1):# 'pes 2016'为词根，则词组最少有3个单词（pes 2016后面的词单独列出范围）
      for j in range(0,length-i+1):#i中的单词单独提取出来（去除pes 2016后的单词）
        key=' '.join(keywords[j:j+i])#以空格为分隔符，将单词列出重组，列表转换成字符串['pes','2016',pc]>>pes 2016 pc
        if keywordRoot in key:
          if key in datas:
            datas[key]+=1
          else:
            datas[key]=1
datas=sorted(datas.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
with open('result','w') as outfile:
  for key,value in datas:
    outfile.write(key + '\t' + str(value) + '\n')
    print key,value
