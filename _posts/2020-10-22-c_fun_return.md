---
title: C语言-从函数返回数组
date: 2020-10-22 15:08
tag: ['C/C++']
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

从函数返回数组分两种方法：返回静态变量地址、以指针参数的形式获得数组。

<!--more-->

C程序中，函数是不能直接返回一个完整的数组的，我们指定数组名本质是一个指针常量，那么能不能通过返回指针的方式间接返回数组呐？答案是不完全可以，函数内变量是局部变量，返回局部变量的地址是不可以的，但是由于静态变量的作用域为全局所有可以返回静态变量。所以这里有两种方式从函数中活动数组：返回静态变量地址、以指针参数的形式获得数组。

下面两个函数的定义，`fun1`在函数内定义一个静态数组变量，然后返回该静态变量地址（数组名）得到返回数组；`fun2`中使用两个指针作为参数，其中`in_arg`为入参用于传入数组，`out_arg`为出参，用于活动数组结果，第三个参数指定数组长度避免索引数组时下标越界。

```c
// 以静态变量的形式返回数组地址
int *fun1(int *arr,int len){
    int static out[20];
    for ( int i = 0; i < len; i++)
    {
        out[i]=2*arr[i];
    }
    return out;
}
// 用指针参数带回数组
void fun2(int *in_arg, int *out_arg,int len){
    for (int i = 0; i < len; i++)
    {
        out_arg[i]=3*in_arg[i];
    }
    
}
```

两种方式中，由于静态数组定义必须由固定的大小，这限制了函数使用的自由性，所有用指针参数带回数组的方式更好一些。




---

**参考**

1. [C 从函数返回数组](https://www.runoob.com/cprogramming/c-return-arrays-from-function.html)
