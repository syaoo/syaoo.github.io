---
title: C语言-主函数参数
date: 2020-10-21 16:43
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

C/C++程序中必须有一个main()函数，称为程序的主函数是程序的入口。main()函数参数不是必须的，其参数可以用于接收程序运行所需的外部参数。通常会定义两个参数argc和argv，分别用于传递参加数量和参数字符串数组。

<!--more-->
在C语言标准中给出了main()函数的两种形式，第一种没有参数，程序执行时不能输入参数；第二种有参数，可以在程序执行时输入参数：
```c
// 无参数
int main(void) { /* ... */ } 
// 有参数
int main(int argc, char *argv[]) { /* ... */ }
````
形参`argc`是argument counter的缩写，指程序传入参数的个数；`argv`是argument vector的缩写，是一个指针数组用于传递程序的输入参数。
下面一个示例会输出参数的个数，以及每个参数：

```c
#include <stdio.h>
int main(int argc, char *argv[]){
    printf("Number of args:%d\n",argc);
    for (int i=0; i < argc; i++){
        printf("argv[%d] is: %s\n",i,argv[i]);
    }
    return 0;
}
```
编译上面的代码，执行程序：
```shell
# 不指定参数
$ ./a.out
Number of args:1
argv[0] is: ./a.out
# 指定两个参数
$./a.out a b
Number of args:3
argv[0] is: ./a.out
argv[1] is: a
argv[2] is: b
```

由上面的测试可以看出，`argc`所表示的参数数量是包含程序本身的，及`argv[0]`存储程序的执行命令（`./a.out`），后面依次是程序输入参数，因此`argc`的值为输入的参数数量加1。

```c
int main(int argc,char *argv[]){
	int num_arg = argc;
	// printf("Number of args = %d\n",num_arg);
	int num_n=0,num_p=0;
	for (int i=1; i<num_arg; i++){
		char *tmp = argv[i];
		if (tmp[0] == '-'){
			num_n++;
		} else {
			num_p++;
		}
	}
	printf("%d,%d\n",num_p,num_n);
	return 0;
}
```

形参`argv`可以理解为是一个字符串数组，使用参数时需要从这个数组中提取每个字符串并根据需要做转换。如下面的示例计算输入参数的平均值，由于输入参数以字符串的形式存储，需要使用`atof()`转换为浮点数：

```c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
    if ( argc > 1)
    {
        double sum = 0,avg;
        for (int i = 1; i < argc; i++)
        {
            sum += atof(argv[i]);
        }
        avg = sum / (argc-1);
        printf("Sum is:%f\n",avg);
    } else
    {
        printf("Please give some numbers.\n");
    }
    return 0;
}
```

以上就是关于主函数参数的简单介绍及使用方法，在ANSI-C的标准中只给出了前面的两种形式，不过在一些平台上还可以使用在main()函数中使用第三个形参来获取环境变量：

```c
int main(int argc,char *argv[],char *envp[])
```

这里的`envp`与`argv`类似也是指针数组，以字符串数组的形成存储各个系统环境变量，当然也可以使用`stdlib`中的`getenv()`函数来或者指定环境变量。本文就不作讨论了。

---

**参考**
1. [C 命令行参数-菜鸟教程](https://www.runoob.com/cprogramming/c-command-line-arguments.html)
