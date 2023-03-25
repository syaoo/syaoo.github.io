---
title: Python异常处理
date: 2022-05-08 23:54
tag: ['python', 'try', 'except']
mathjax: false
mathjax_autoNumber: true
# Mermaid
mermaid: false
# Chart
chart: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

# Python异常处理

## try/except
python中的try/except语句可以方便的处理程序运行过程中发生的错误（异常），使程序更加稳定健壮。try/except语句中，try子句中执行需要检测异常的代码，如果没有出现异常则完成try/except的执行，如果出现异常，则执行except子句来处理异常。except子句可以有多个，分别用于匹配不同的错误类型，同一个except中也可以匹配处理多种类型的错误。此外还有可选子句else和finally搭配使用，else子句语言处理前面except没有匹配到的错误类型，而finally子句是在try语句结束前执行的最后一项任务，无论是否发生异常都会执行该子句，可以用于执行如释放资源等清理操作。

```python
    try:
        # 任务代码
    except 异常类型1:
        # 错误处理代码
    except (异常类型2, 异常类型3):
        # 错误处理代码
    except 异常类型4 as err:
        # 错误处理代码
        #通过异常类型4的实例err可以方法错误信息
    else:
        # 其他错误处理
    finally:
        # 错误有没有发生是都需要执行的代码

```

## raise和assert

raise语句可以主动抛出一个异常，某些情况下捕获异常后，完成所需操作如日志记录等操作，可以使用raise重新抛出捕获的异常。raise两种常见的用法：
1. 单独一个 raise。该语句引发当前上下文中捕获的异常（比如在 except 块中），或默认引发 RuntimeError 异常。
2. raise 后带一个异常类名称，表示引发执行类型的异常，异常类参数中也可以增加描述信息。

```python
# raise [exceptionName [(reason)]]

raise
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# RuntimeError: No active exception to reraise

raise ValueError
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ValueError

raise ValueError("参数值错误")
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ValueError: 参数值错误
```

assert用于判断一个表达式是否成立，不成立时则触发AssertionError类型的异常。assert后面可以指跟表达式用于判断该表达式是否成立，也可加一个参数用于描述具体错误情况。

```python
# assert expression [, arguments]

assert 1==3
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AssertionError

assert 1==3, "1 不等于3"
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AssertionError: "1 不等于3"
```

## 常见异常类型

Python中有许多[内置异常](https://docs.python.org/zh-cn/3.10/library/exceptions.html#concrete-exceptions)类型，下面列出几种比较常见的异常类型：
 - `AssertionError`  当 assert 关键字后的条件为假时，程序运行会停止并抛出 AssertionError 异常
 - `AttributeError`  当试图访问的对象属性不存在时抛出的异常
 - `IndexError`  索引超出序列范围会引发的异常
 - `KeyError`  字典中查找一个不存在的关键字时引发的异常
 - `NameError` 尝试访问一个未声明的变量时引发的异常
 - `TypeError`  不同类型数据之间的无效操作
 - `ZeroDivisionError`  除法运算中除数为0引发的异常

上述异常类型都有共同的基类`Exception`，用于自定义的异常类型也应该从`Exception`派生。下图展示了Python异常类的继承结构，`BaseException`是所有异常类的基类， 是为系统退出异常而保留的，比如`KeyboardInterrupt`或 `SystemExit`以及其他那些会给应用发送信号而退出的异常。

except捕获异常时应将子类放在前面，如将父类放在前面则会优先检测的父类异常，造成难以准确判断错误类型。

![](/assets/post_pic/python-error-type-relation.gif)

下面代码中会处理Exception错误，而不会处理NameError

```python
try:
    raise NameError
except Exception:
    # 处理Exception
except NameError:
    # 处理NameError
```

下面代码能够正确处理到NameError

```python
try:
    raise NameError
except NameError:
    # 处理NameError
except Exception:
    # 处理Exception
```

所有的异常对象都包含`args`属性和`with_traceback()`方法：
- args：该属性返回异常的错误编号和描述字符串。
- with_traceback()：通过该方法可处理异常的传播轨迹信息。

此外`OSError`或基于该类的子类对象还有`errno`和`strerror`属性
- errno：该属性返回异常的错误编号。
- strerror：该属性返回异常的描述宇符串。

## 用户自定义异常类型

用户可以通过继承`Exception`类或其子类来创建适应自己项目需要的异常类型。
异常类可以被定义成能做其他类所能做的任何事，但通常应当保持简单，它往往只提供一些属性，允许相应的异常处理程序提取有关错误的信息。异常命名通常以 “Error” 结尾。下面是一下自定义异常类型示例

```python
# 定义两个异常类型，MyError0派生自Exception，MyError1派生自MyError0
class MyError0(Exception):
    pass
class MyError1(MyError0):
    pass
```

`Exception`的`__init__`是接受所有传递的参数并将它们以元组形式存储在`.args`属性中，定义新的异常类时可以重写`__init__`方法，以适应特殊需求

```python
# 定义MyError0异常类型，并重写__init__方法
class MyError0(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status

# 产生MyError0异常，并输出信息
try:
    raise MyError0("Some error","1")
except MyError0 as err:
    print(err.message,err.status)
```

## 异常连接

使用`raise from`语句可以连接两个异常信息，下面展示了几个使用示例。

1. 捕获异常，处理后直接抛出该异常

```python
# 捕获异常，并输出异常信息
try:
    raise ValueError("N/A is Not Nub.")
except ValueError as e:
    print("Exception args is:",e.args)
    raise
```

输出了print打印内容以及raise抛出的ValueError信息

```
Exception args is: ('N/A is Not Nub.',)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ValueError: N/A is Not Nub.
```

2. 捕获异常进行处理并抛出另一个异常，示例中捕获处理了ValueError并抛出RuntimeError错误

```python
try:
    raise ValueError("N/A is Not Nub.")
except ValueError as e:
    raise RuntimeError("Somethin Error in Runtime...")
```

此时隐式的输出了两个异常的关系，在处理ValueError时发生了另一个异常RuntimeError

```
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ValueError: N/A is Not Nub.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
RuntimeError: Somethin Error in Runtime...
```

3. 捕获异常进行处理并抛出另一个异常，同时显示的表明两个异常的关系

```python
try:
    raise ValueError("N/A is Not Nub.")
except ValueError as e:
    raise RuntimeError("Somethin Error in Runtime...") from ValueError
```

这种情况下输出的是，ValueError导致了RuntimeError的发生
```
ValueError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
RuntimeError: Somethin Error in Runtime...
```

3. 捕获异常进行处理并抛出另一个异常，但仅显示最后一个异常

```python
try:
    raise ValueError("N/A is Not Nub.")
except ValueError as e:
    raise RuntimeError("Somethin Error in Runtime...") from None
```

此时，只输出RuntimeError

```
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
RuntimeError: Somethin Error in Runtime...
```

---

**参考**

1. [Python try except else（异常处理）用法详解](http://c.biancheng.net/view/2315.html)
2. [8. 错误和异常 — Python 3.10.4 文档](https://docs.python.org/zh-cn/3/tutorial/errors.html)
3. [第十四章：测试、调试和异常 — python3-cookbook 3.0.0 文档](https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p14_test_debug_and_exceptions.html)
4. [Python3 错误和异常 | 菜鸟教程](https://www.runoob.com/python3/python3-errors-execptions.html)
5. [Python 异常处理 | 菜鸟教程](https://www.runoob.com/python/python-exceptions.html)
6. [内置异常 — Python 3.10.10 文档](https://docs.python.org/zh-cn/3.10/library/exceptions.html#bltin-exceptions)