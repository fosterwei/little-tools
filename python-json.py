#定义一个类person
class Person(object):
  def __init__(self,name,age):
    self.name=name
    self.age=age
  def __repr__(self):
    return 'Person Object name : %s, age: %d' % (self.name,self.age)
  if __name__ == '__main__':
    p=Person('Peter',22)
    print p
#如果直接通过json.dumps方法对Person的实例进行处理的话，会报错，因为json无法支持这样的自动转化。通过上面所提到的json和python的类型转化对照表，可以发现，object类型是和dict相关联的，所以我们需要把我们自定义的类型转化为dict，然后再进行处理。这里，有两种方法可以使用。
#新文件
import Person
import json

p=Person.Person('Peter',22)

class MyEncoder(json,JSONEncoder):
  def default(self,obj)
    #convert object to a dict
    d={}
    d['__class__']=obj.__class__.__name__
    d['__module__']=obj.__module__
    d.updata(obj.__dict__)
    return d
    
class MyDecoder(json.JSONDecoder):
  def __init__(self):
    json.JSONDecoder.__init__(self,object_hook=self.dic2object)
  def dict2object(self,d):
    #convert dict to object
    if '__class__' in d:
      class_name = d.pop('__class__')
      module_name= d.pop('__module__')
      module = __import__(module_name)
      class_ = getattr(module,class_name)
      args = dict((key.encode('ascii'),value) for key, value in d.items()) #get args
      inst=class_(**args) #create new instance
    else:
      inst = d
    return inst
    
d = MyEncoder().encode(p)
o = MyDecoder().decode(d)

print d
print type(o),o
