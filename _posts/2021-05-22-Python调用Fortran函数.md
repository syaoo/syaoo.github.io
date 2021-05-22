---
title: 在Python中调用Fortran函数
tag: ['Python',"Fortran"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---
Fortran作为一个有着历史悠久的用于科学计算的编程语言，有着许多优秀的库函数，而Python是一个比较容易上手的脚本语言，同时拥有丰富的工具库，将二者结合能大大提升程序开发及运行效率。f2py是Python库Numpy提供的一个用于连接Fortran和Python的工具，它能够将Fortran代码编译为可供Python使用的动态库。

<!---more-->
C04序列作为一个相对权威的EOP产品，它提供了极移X、Y、UT1、日长等参数。通常为了检核EOP解算结果的准确性，要与C04进行比较，而C04中提供的EOP的时标都是在UTC 0时的，而解算的时标可能回在其他时刻，因此需要对C04进行插值后在进行比较。

刚好手上有一个Fortran编写的C04插值程序，它可以根据输入的EOP序列（mjd、X、Y、UT1）进行任意时刻的插值。但是懒得去写一个Fortran程序来调用这个函数，于是想到如果用Python直接调用这个函数，那么可以大大减少工作量。这时就需要请出F2PY这个工具了。

F2PY(Fortran to Python)是Numpy的一部分，安装Numpy的即可使用该工具。通过它可以实现在Python中调用Fortran 77/90/95的外部子程序、Fortran 90/95模块中的子程序以及C函数。下面以两个例子说明在Python中调用Fortran的程序的方法。

首先，编写一个Fortran程序，其中有一个子过程dot()和一个函数add()，前者计算向量的点乘，后者计算两个数的和，程序如下：
```fortran
subroutine dot(a,b,c,n)
integer, intent(in) :: n
real*8,intent(in) :: a(n), b(n)
real*8, intent(out) :: c

c=0
do i = 1,n;
  c = c+a(i)*b(i)
end do
return
end subroutine

function add(a,b)
real :: a,b
real :: add
add = a+b
return
end function

```
然后可以使用f2py构建名为`test`的扩展模块，如在Linux x86上则会生成一个名为`test.cpython-38-x86_64-linux-gnu.so`的动态库，将该库方法系统路径如`/usr/lib`或当前目录下，便可在python中使用`teest`模块。
```bash
f2py -c -m test test.f90
```
下面是一段测试用Python程序：
```python
import test
import numpy as np
print(Fortran.__doc__)
a=np.array([1,2,3])
b=np.array([2,2,3])
c=test.dot(a,b)
print(f"a dot b in {c}")
print(f"3+4={test.add(3,4)}")
```
输出结果：
```
This module 'test' is auto-generated with f2py (version:2).
Functions:
  c = dot(a,b,n=len(a))
  add = add(a,b)
.
a dot b in 15.0
3+4=7.0
```
由于Fortran的子过程中采用的是传址调用的方式，而非C/C++中的值传递方式，子过程的输入参数可以被改变。所以在子过程的定义中要声明输入输出的变量，使f2py正确识别各参数。如果不声明输入、输出f2py会都认为是输入。例如下面是没有声明输入输出是`test.__doc__`的输出结果，`dot()`被认为有三个输入参数，没有返回值：
```
This module 'test' is auto-generated with f2py (version:2).
Functions:
  dot(a,b,c,n=len(a))
  add = add(a,b)
.
```
当声明输入输出时，`dot()`有两种参数`c`被正确转换为返回值。
```
This module 'test' is auto-generated with f2py (version:2).
Functions:
  c = dot(a,b,n=len(a))
  add = add(a,b)
.
```
在Fortran程序中显式的声明输入输出，或者以注释的形式（需要`f2py`标识）都可以。
```fortran
integer, intent(in) :: n
real*8,intent(in) :: a(n), b(n)
real*8, intent(out) :: c
```
或者：
```python
integer:: n
real*8:: a(n),b(n),c
!f2py intent(in)  a,b,n
!f2py intent(out) c
```

**参考:**  
[完全用Python工作——F2PY简明使用指南 - Tech Notes of Code Monkey](https://blog.finaltheory.me/research/Introduction-to-F2PY.html)
[Python调用C/C++的两种方法 - 知乎](https://zhuanlan.zhihu.com/p/39098612)
[使用 F2PY | NumPy 中文](https://www.numpy.org.cn/f2py/usage.html)
