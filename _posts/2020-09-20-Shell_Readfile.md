---
title: Shell文件读取
tag: ['Shell']
mathjax: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

Shell脚本文件读取的方法，在循环中不能同时使用`read`读取文件与接收键盘输入。

<!--more-->
Shell中有多种方式实现文件的读取，如使用`cat`或重定向符读取全文，在循环语句中分行读取。有这样一个文件：

```
drwxr-xr-x  1 root root 4.0K Jan 14  2020 bin
drwxr-xr-x 1 root root 4.0K Jan 14 2020 bin
drwxr-xr-x  1 root root 4.0K Sep 20 10:21 dev
drwxr-xr-x  1 root root 4.0K Sep 20 10:21 etc
```

要直接读取全文：

```shell
txt=$(cat filename)
# 或者
txt=$(< filename)
```

按行读取，并输出：

```bash
while read line; do echo $line; done < filename
# 或者
cat filename | while read line; do echo $line; done
############# 输出 ##############
# drwxr-xr-x 1 root root 4.0K Jan 14 2020 bin
# drwxr-xr-x 1 root root 4.0K May 21 2019 boot
# ...
```

按列读取，输出需要的列：

```shell
while read l1 l2 l3 l4 l5 l6 l7 l8 l9; do echo $l5 $l9;done < filename
# or
cat filename | while read l1 l2 l3 l4 l5 l6 l7 l8 l9; do echo $l5 $l9;done
############# 输出 ##############
# drwxr-xr-x bin
# drwxr-xr-x boot
# ...
```

分别读取、输出以空格分隔的每个元素（如果修改了内置分隔符`IFS`效果可能有所不同）：

```shell
for line in $(cat filename); do echo $line; done
############# 输出 ##############
# drwxr-xr-x
# 1
# root
# root
# 4.0K
# ...
```

**如果在循环中需要使用`read`接收键盘输入时，不能使用`read`读取文件****,如下面的示例中，循环中相要使用`read`接收一些键盘的输入，如果按下面的写法使用`read`读取文件行，那么想要接收键盘输入的`read`实际上也是直接从文件读取行。

```shell
while read line; do echo $line; read -p "input something" tmp;done < filename
```

此时需要使用其他方式读取文件行，如前面示例，使用`for`循环读取文件并不是按行读取，这里需要`IFS`修改为换行，使用`for`循环可以按行来读取：

```shell
local IFS=$'\n' # 使用local变量IFS来保存临时设置, 如在函数中使用可避免对其他部分脚本造成不良影响
for line in $(cat filename); do echo $line;read -p "input something" tmp;done
```

---

**参考**
1. [shell:读取文件的每一行内容并输出 - cbwcwy - 博客园](https://www.cnblogs.com/iloveyoucc/archive/2012/07/10/2585529.html)
2. [详细解析Shell中的IFS变量_洛奇看世界-CSDN博客](https://blog.csdn.net/guyongqiangx/article/details/80220434)
