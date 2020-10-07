---
title: Shell学习记录
tag: ['Shell']
article_header:
mathjax: false
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

Shell字符串与数字的一些使用方法，将字符串转换为数组的方法。

<!--more-->
注意：文中使用的是bash环境，对于其他shell（如csh、csh）会有所区别。

## Shell变量-字符串、数组

和所有程序语言一样，Shell也有变量，支持数值，字符串，数组类型，Shell是弱类型语言，默认为字符类串，参与运算是会自动进行隐式类型转换。根据作用范围Shell变量可以分为环境变量、特殊变量、局部变量等类型；环境变量和特殊变量通常用于Shell等其他程序的正常运行，局部变量通常实在Shell脚本中定义使用的变量。

### 变量的定义与使用

Shell脚本中有许多方式用于定义变量,如：

```shell
var1=var1
var1='var1'
var="var1"
files=$(ls ./)
files=`ls ./`
```

当变量字符串不包含空格、转义字符、变量引用时，使用（单、双）引号与不使用定义变量效果是相同的，单引号不对变量引用、转义字符做处理，直接原样输出。`readonly `，`unset `命令可以用于设置只读变量和删除变量。

### 字符串

字符串是Shell脚本最常用的变量类型，通常定义的变量都是默认为字符类型。字符串定义时，如果包含空格则必须使用单（双）引号，在含有对其他变量的引用时不能使用单引号，若使用单引号，则需要对变量引用部分加单引号以使变量引用可正常表达。

```shell
name="Tim"
echo 'my name is ${name}'
# 输出：my name is ${name}
echo 'my name is '${name}''
# 输出：my name is Tim
```

**字符串长度** `${#var}`可以获取字符串长度，输出`name`的长度：
```shell
# 下面方法都可以
echo ${#name}
echo `expr "${name}" : ".*"` 
echo `expr length ''${name}''`
```

**字符串切片1** 从指定位置提取一定长度的字符串：

```shell
# var=my name is tim
# 提取出var中的name
echo ${var:3:4} # 从0开始计数
echo `expr substr "${var}" 4 4` # 从1开始计数
```

**字符串切片2** 截取匹配的子字符串前后的子字符串,`#`截去前面的字符串，`%`截去后面的字符串：

```shell
foo="Able was I ere I saw Elba"
# 最小匹配，截去第一次匹配到*I前面的字符
echo ${foo#*I} # 输出 ere I saw Elba
# 最大匹，截去最后一次匹配到*I前面的字符
echo ${foo##*I} # 输出 saw Elba
# 最小匹配，截去最后一次匹配到*I后面的字符
echo ${foo%I*} # 输出 Able was I ere
# 最大匹，截去第一次匹配到*I后面的字符
echo ${foo%%I*} # 输出 Able was
```

**子字符串查找** 查找子字符串`name`中的字符在`my name is tim`最先出现位置:

```shell
echo `expr index "$var" name` # 返回1，m第一次出现的位置
echo `expr index "$var" na` #返回4，n第一次出现的位置
```

**字符串替换** 
`${str/源模式/目标模式} ` - 将字符串`str`首次出现的匹配`源模式`的子字符串替换为`目标模式`字符串；
`${str//源模式/目标模式}` - 将字符串`str`所有匹配`源模式`的子字符串替换为`目标模式`字符串。

```shell
str="ONE,TWO,THREE,FOUR"
# 替换全部,为空格
nstr=${str//,/ }
echo $nstr
# 输出 ONE TWO THREE FOUR
# 替换第一个匹配, 为空格
nstr=${str/,/ }
echo $nstr
# 输出 ONE TWO,THREE,FOUR
```



### 数组

Shell可以使用一维数组，数组元素的下标由 0 开始编号。获取数组中的元素要利用下标，下标可以是大于或等于 0所整数或算术表达式。

**数组定义**

数组使用`()`定义，空格或回车分割元素：

```shell
arr1=(var1 var2 var2)
arr1=(var1
var2
var2
)
```

**数组使用** `${数组名[下标]}`使用单个元素，下标为`@`或`*`获取数组的所有元素；类似字符串，变量名前加`#`可以获取数字长度。

```shell
var=(1 2 3)
echo ${var[2]} # 返回 3
echo ${var[@]} # 返回 1 2 3
echo ${var[*]} # 返回 1 2 3
# for循环变量数组
for i in ${var[@]};do echo $i; done
# 输出：
# 1
# 2
# 3
# 获取数字长度
echo ${#var[@]}
echo ${#var[*]}
```

### 字符串与数组转换

对于空格分割的字符串，可以直接加括号转换为数组，如：

```shell
a="ab cd ef"
b=($a)
echo $b # 返回 ab
echo ${b[*]} # 返回 ab cd ef
```

如果分隔符不是空格则需要吧分隔符替换为空格，加括号转换：

```shell
str="ONE,TWO,THREE,FOUR"
# 将str转为数组，需要先替换, 分隔符为空格
# 1. ${str//源模式/目标模式}方式替换
arr=(${str//,/ }) #数组
# 2. 使用tr命令
arr=(`echo $str | tr ',' ' '`)
# 3. 使用awk命令
arr=($(echo $str | awk 'BEGIN{FS=",";OFS=" "} {print $1,$2,$3,$4}'))
# 4. 使用IFS修改内部分隔符
IFS=","
arr=($str)
```

---

**参考**

1. Stenphen G. Kochan, Patrick Wood. Shell Programing in Unix, Linux and OS X[M]. Pearson, 2017.
2. [Shell 变量, 菜鸟教程](https://www.runoob.com/linux/linux-shell-variable.html)
3. [Shell中将分隔符的字符串转为数组的几种方法_杰瑞的专栏-CSDN博客](https://blog.csdn.net/Jerry_1126/article/details/83930956)
4. [BASH 字符串拆分_tanxs001的专栏-CSDN博客](https://blog.csdn.net/tanxs001/article/details/7666709?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.add_param_isCf&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.add_param_isCf)
