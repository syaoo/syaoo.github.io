---
title: Python类中的方法-实例方法、类对象、静态对象以及__str__和__repr__
tag: ['Python']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

在类定义时，定义函数方法时除了普通的实例函数、还有通过装饰器来定义的类函数和静态函数，可以根据不同的需求来定义不同的方法，为了可以更好的输出对象，还有可以定义`__str__`、`__rper__`函数。

<!--more-->

[toc]

**类(class)**是对一类事物的抽象描述，是创建实例的模板，如“人”类，它具有姓名、年龄、性别等属性，它可以跑、可以说话；而“小明”是一个**对象(object)**，是“人”类的一个**实例(instance)**，“小明”的姓名叫小明、19岁、男，“小明”会跑、会说话。用代码来表示：

```python
class human():
    def __init__(self,name,age,gender):
        # 人类的属性：姓名、年龄、性别
        self.name=name
        self.age=age
        self.gender=gender
    def run(self):
        # 定义跑方法（函数）
        pass
    def say(self):
        # 定义说话方法（函数）
        pass

if __name__ == "__main__":
    xiaoming = human("小明",19,"男")
    # 小明跑
    xiaoming.run()
    # 小明说话
    xiaoming.say()
```
## 方法类型
在上面例子中“人”类有两个方法，它需要实例化后才可通过实例来调用如：`xiaoming.run()`，而`human.run()`是不可以的，这类方法成为“实例方法”，在python中类内的方法（成员函数）有三种：实例方法、类方法、静态方法。
从使用方法来看，实例可以使用任意种方法，而类只可以使用类方法和静态方法，即类方法、静态方法在实例化前可以通过类调用。
从定义的方法上来看，实例方法就是一个普通的python函数的定义，只不过需要传入代表当前实例的`self`参数，而类方法和静态方法则分别需要使用`@staticmethod`和`@classmethod`装饰器来装饰，并且类方法需要传入一个代表当前类的`cls`参数。
### 类方法
下面展示类两个类方法的定义，`getsize()`可以获取当前人口数量、`newperson`用于产生一个新的“人”类对象，类似构造函数`__init()`。
```python
    @classmethod
    def getpsize(cls):
        print("this is CLASSMETHOD:{}".format(sys._getframe().f_code.co_name))
        print("population size：{}".format(cls.num))
        return cls.num
    @classmethod
    def newperson(cls,name,age,gender):
        print("this is CLASSMETHOD:{}".format(sys._getframe().f_code.co_name))
        return cls(name,age,gender)
```
使用上面定义的类方法：
```pythn=on
    wl = human.newperson('wl',22,'nan')
    human.getpsize()
    wl.getpsize()
    # 输出
    # this is CLASSMETHOD:newperson
    # this is CLASSMETHOD:getpsize
    # population size：3
    # this is CLASSMETHOD:getpsize
    # population size：3
```

### 静态方法
定义一个静态方法`birthday()`，根据年龄计算出生年份，然后在实例方法`getbirth()`中调用它
```python
    def getbirth(self):
        return self.birthday(self.age)
    @staticmethod
    def birthday(age):
        print("this is STATICMETHOD:{}".format(sys._getframe().f_code.co_name))
        return 2020-age
```
可以通过类或者实例来调用静态方法：
```python
    print(ll.getbirth()) # 获取ll的出生年份
    print(human.birthday(10)) # 计算一个10岁人的出生年份
    # 输出结果
    # this is STATICMETHOD:birthday
    # 2008
    # this is STATICMETHOD:birthday
    # 2010
```
### 类方法与静态方法的应用
类方法可以在实例化前调用，可以定义一些需要在实例化前进行，或者不需要实例化类的操作。如为类定义多个构造器。
静态方法不需要传入`self`和`cls`参数，通常不能获得类中的其他属性，也不能操作类中的其他方法，静态方法可以看作附属于类对象的“工具”。


## `__str__` 和`__repr__`
python中`__str__`与`__repr__`都是用于更好的字符串表示自定义数据类型，不过二者有些不同。当仅定义`__repr__`时，`str()`,`print()`使用`__repr__`定义的形式。

| `__str__` `str()` | `__repr__` `repr()` |
| ----------------- | ------------------- |
|使对象易读  | 展示生成对象所需的代码|
|为用户生成输出  |为开发者生产输出|

实例代码:
```python
    def __repr__(self):
        return "human({},{},{})".format(self.name,self.age,self.gender)
    def __str__(self):
        return "Name:{},Age:{},gender:{}".format(self.name,self.age,self.gender)
```
测试效果：
```python
    print(ll)
    print(str(ll))
    print(repr(ll))
    now = datetime.datetime.now()
    print(str(now))
    print(repr(now))
    
    # 输出结果
    # Name:li,Age:12,gender:nv
    # Name:li,Age:12,gender:nv
    # human(li,12,nv)
    # 2020-07-16 23:13:54.634582
    # datetime.datetime(2020, 7, 16, 23, 13, 54, 634582)
    
```



#### 示例代码
```python
import sys
import datetime

class human():
    num = 0
    ancestors='fish'
    def __init__(self,name,age,gender):
        self.name=name
        self.age=age
        self.gender=gender
        human.num+=1
        self.id=human.num
    def run(self):
        # 定义跑方法（函数）
        pass
    def say(self):
        # 定义说话方法（函数）
        pass
    @classmethod
    def getpsize(cls):
        print("this is CLASSMETHOD:{}".format(sys._getframe().f_code.co_name))
        print("population size：{}".format(cls.num))
        return cls.num
    @classmethod
    def newperson(cls,name,age,gender):
        print("this is CLASSMETHOD:{}".format(sys._getframe().f_code.co_name))
        return cls(name,age,gender)

    def getbirth(self):
        return self.birthday(self.age)
    @staticmethod
    def birthday(age):
        print("this is STATICMETHOD:{}".format(sys._getframe().f_code.co_name))
        return 2020-age
    def __repr__(self):
        return "human({},{},{})".format(self.name,self.age,self.gender)
    def __str__(self):
        return "Name:{},Age:{},gender:{}".format(self.name,self.age,self.gender)

if __name__ == "__main__":
    xiaoming = human("小明",19,"男")
    # 小明跑
    ll = human('li',12,'nv')
    xiaoming.run()
    # 小明说话
    xiaoming.say()
    wl = human.newperson('wl',22,'nan')
    human.getpsize()
    wl.getpsize()
    mm=wl.newperson('mm',22,'nv')
    mm.getpsize()
    print(ll.getbirth())
    print(human.birthday(10))
    print(ll)
    print(str(ll))
    print(repr(ll))
    now = datetime.datetime.now()
    print(str(now))
    print(repr(now))
```



---

**参考**

1. [Python实例方法、类方法、静态方法](https://zhuanlan.zhihu.com/p/40162669)
2. [Class method vs static method in Python](https://www.tutorialspoint.com/class-method-vs-static-method-in-python)
2. [str() vs repr() in Python?](https://www.tutorialspoint.com/str-vs-repr-in-python)
