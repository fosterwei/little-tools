import multiprocessing as mp
#import threading as td

def job(a,d):
  print 'aaaa'

if __name__=='__main__'
#t1=td.Thread(target=job,args=(1,2))
  p1=mp.Process(target=job,args=(1,2))
#t1.start()
  p1.start()
#t1.join()
  p1.join()
  
#多进程queue
def job(a,d):
  res=0
  for i in range(1000):
    res+=i+i**2+i**3
  q.put(res)#queue

if __name__=='__main__'
  q=mp.Queeu()#定义一个多进程的值
  p1=mp.Process(target=job,args=(q,))#把值放到process的值当中
  p2=mp.Process(target=job,args=(q,))
  p1.start()
  p2.start()
  p1.join()
  p2.join()
  res1=q.get()
  res2=q.get()
  print res1+res2
  
#效率对比
#进程池
import multiprocessing as mp

def job(x):
  return x*x
  
def muticore():
  pool=mp.Pool(processes=2)
  res=pool.map(job,range(10))
  print res
  res=pool.apply_async(job,(2,))
  print res.get()
  multi_res=[pool.apply_async(job,(i,)) for i in range(10)]
  print [res.get() for res in multi_res]
  
if __name__=='__main__'
  multicore()

#共享内存
import multiprocessing as mp

value=mp.Value('i',1)
array=mp.Array('i',[1,2,3])

#锁lock
import mutiprocessing as mp
import time

def job(v,num,l):
  l.acquire()#创建锁
  for _ in range(10):
    time.sleep(0.1)
    v.value+=num
    print v.value
  l.release() #释放锁

def multicore():
  l=mp.Lock()
  v=mp.Value('i',0)
  p1=mp.Process(target=job,args=(v,1,l))
  p2=mp.Process(target=job,args=(v,3,l))
  p1.start()
  p2.start()
  p1.join()
  p2.join()
  
  
  
  
