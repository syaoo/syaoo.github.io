---
title: C语言-动态内存分配
date: 2020-10-21 20:06
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
    src: /assets/images/cover0.jpg
---

动态内存是相对静态内存而言的，其是在堆上分配内存。动态内存分配可以更自由的为数据存储分配内存空间，但是容易引起内存泄露，因此在使用时要极力避免因造成内存泄露。动态内存分配和释放常用到的四个函数为：malloc()、calloc()、realloc() 和 free()。

<!--more-->

C程序中内存分配有系统自动分配和动态内存分配两种。如全局变量、静态变量在编译时即由系统自动在静态存储区（static）分配；函数内局部变量在程序运行过程中由系统自动在栈（heap）中进行分配；而动态内存的分配则根据程序设计在需要时调用malloc()等函数在堆（stack）中动态分配、调整。
C程序中数组长度是固定的，即其所占内存在定义时就要确定，然而在许多场景中会遇到不能实现确定数组大小，如果使用一个很大的值来定义数组长度会造成很大的内存浪费，所以动态内存分配的方法可以有效的解决这一问题。

## 动态内存分配相关函数
在动态内存分配常用的`stdlib`中的`malloc()`、`calloc()`、`realloc()`和`free()`，前两个用于分配新的的空间，`realloc()`可以调整已分配的内存大小，`free()`则用于释放已分配的空间。
### 内存分配
`malloc()`和`calloc()`均可用于内存分配，其函数原型：
```c
void* malloc (size_t size);
void *calloc (size_t nitems, size_t size);
````
两函数的都是用于分配内存，并返回指向该内存首地址的void类型指针，如果内存申请失败则返回NULL。从其原型可以看出二者所需参数不同，除此之外`malloc()`仅分配size字节大小的空间不初始化其中的值，而`calloc()`会将分配`nitems*size`大小的内存空间并初始化为0。
由于二者返回的都是void类型指针，在使用时根据需要强制转换为相应类型。不同系统中同一类型数据的长度可能不同，因此在指定内存大小时最好根据数据类型计算而不是直接指定数值。

```c
// 分配5个int大小的内存，即5*4 bit
int *p1 = (int*)malloc(5*sizeof(int));
// 内存分配后检测是否分配成功
if (p1 == NULL){
    printf("%s","内存分配错误");
}
// memset(p1, 0, 5*sizeof(int)); // malloc+memset == calloc
int *p2 = (int*)calloc(5,sizeof(int));
if (p2 == NULL){
    printf("%s","内存分配错误");
}
```
### 内存调整

`realloc()`可以修改`malloc()`、`calloc()`分配的内存空间大小，当已分配的内存空间不够使用时，可以使用该函数动态调整大小，其函数原型：

```c
void* realloc(void *ptr, size_t size);
```

该函数重新调整`ptr`指针所指内存大小为size字节，关于其返回值有void类型指针和NULL两种结果，具体存在以下几种种情况：

- 如果`ptr`所指向的内存块有足够的空间，会重新调整分配内存为size字节，然后返回指向该内存块首地址的void指针，并保持原数内存块中数据不变；
- 如果`ptr`所指的内存块后面没有做够的空间，会在其他区域重新开辟一个大小为size字节的内存块，并复制原内存块中的数据到新的内存块，然后返回该内存块的首地址；

- 当没有足够的内存空间或其他原因造成空间调整失败，会返回`NULL`，原内存空间维持不变。 
- 如果 `ptr = NULL`，那么相当于调用 `malloc(size)`；
- 如果 `size = 0`，那么相当于调用 `free(ptr)`，`ptr`所指内存空间被释放，返回`NULL`。

注意`realloc()`重新分配内存成功后，原指针`ptr`将被释放，此时其地址不具有实际意义，不应继续使用，也不需要对其使用`free()`。

下面是一个示例程序：

```c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
    int num = 4;
    int new_num;
    int *p1 = (int*)malloc(num*sizeof(int));
    int *p2 = NULL;
    // 内存申请成功后执行操作
    if (p1!=NULL){
        printf("%s","data of p1 is:");
        for (int i = 0; i < num; i++)
        {
            p1[i] = 2*(i+1);
            printf("%3d",p1[i]);
        }
        new_num = 8;
        printf("%s","Increase space...\n");
        p2 = realloc(p1,(new_num)*sizeof(int));
        if (p2 != NULL)
        {
            printf("addr of p1 is：%p\n",p1);
            printf("addr of p2 is：%p\n",p2);
            printf("%s","New data of p2 is:");
            for (int i = 0; i < new_num; i++)
            {
                printf("%3d",p2[i]);
            }
            printf("%s","\n");
            free(p2);
            p2 = NULL;
        }
    } else
    {
        printf("%s","memory allocation errors");
    }
    return 0;
}
```

编译运行程序得到如下输出：

```shell
$ ./a.out 
data of p1 is:  2  4  6  8
Increase space...
addr of p1 is：0x7fffe1b6c260
addr of p2 is：0x7fffe1b6c690
New data of p2 is:  2  4  6  8  0  0  0  0
```

从上面程序输出结果可以看出，由于p1后面的连续空间不足，`realloc()`在其他位置开辟了一块新的空间，`p1`和`p2`所指向的内存地址不同，但新内存空间中前面的数据与原空间的相同。

### 内存释放

动态分配的内存只有调用`free()`释放或在程序结束后释放，如果动态分配内存后使用完毕比手动释放，有可能会造成内存泄露。

```c
void free(void* ptr);
```

`free()`函数调用十分简单，但是在使用时要注意一些问题：

- 每个`malloc()`或`calloc`都要有一个`free()`与之对应，确保分配的空间都要在合适的时机被释放；
- `free(p)`释放`p`所指向的空间后，只是告诉系统这可空间可以自由使用，并不会主动清除其中的数据，而且指针`p`依然会执行那块空间，对该指针操作依然可以读写数据，但不建议这么做。
- 在调用`free(p)`是否空间后，应将`p`指向`NULL`（`p = NULL;`）避免误操作；
- 释放空间时必须完整释放，如对移动指针`p`后需要将`p`复位再使用`free(p)`，否则会出错；
- 同一块动态分配的内存只能释放一次，否则在运行时会出现”double free“问题；（不过在测试中，同样代码，释放两次内存，在wsl Ubuntu18环境中没有出现这个问题，Centos8中出现了这一问题，后者是符合预想的）
- 使用`realloc()`重新分配内存空间后，原指针已经被自动释放，当前空间不需要使用时，需要释放`realloc()`新返回的指针。



## 动态内存分配常见问题

动态内存分配中常常遇到内存泄露、野指针、非法释放内存等错误，在使用时需要注意：

1. 内存泄露是指程序已申请所内存在不使用时未得到释放，致使可用内存不断较少，影响程序运行甚至系统崩溃。

2. 野指针是由于一个内存指针已经被释放`free()`或者重新分配内存`realloc()`后没有置为`NULL`。当指向动态分配内存的指针被释放或成功重新分配内存后，该指针所指地址已无实际意义，其中所存储数据可能为一些”垃圾值“，将该指针置为`NULL`能有效避免此问题。

3. 非法释放内存指释放非`malloc()`、`calloc()`、`realloc()`返回的指针所指向的内存空间，如下面两个内存释放示例都是错误的，会在运行时出现`free(): invalid pointer`错误。
    ```c
    int arr[10];int *p1 = arr();
    free(p1); // p1指向系统在栈中分配的空间
    int *p2 = (int*)malloc(4);p2++;
    free(p2) // p2发生移动，此时p2不再指向动态分配的内存空间的首地址
    ```


---

**参考**

1. [C语言为指针动态分配内存_C语言中文网](http://c.biancheng.net/cpp/html/2752.html)
2. [C语言中手把手教你动态内存分配](https://blog.csdn.net/qq_29924041/article/details/54897204)
3. [安全起见，小心使用C语言realloc()函数_C语言中文网](http://c.biancheng.net/cpp/html/2536.html)
4. [C语言realloc()函数：重新分配内存空间_C语言中文网](http://c.biancheng.net/cpp/html/2859.html)
5. [c - How free memory after of realloc - Stack Overflow](https://stackoverflow.com/questions/37013251/how-free-memory-after-of-realloc)
