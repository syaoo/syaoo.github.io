---
title: Python数据处理(1) - Numpy数据类型
tag: Numpy Python
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover2.jpg
---

NumPy是Python中科学计算的基础包。它是一个Python库，提供多维数组对象，各种派生对象（如掩码数组和矩阵），以及用于数组快速操作的各种API，有包括数学、逻辑、形状操作、排序、选择、输入输出、离散傅立叶变换、基本线性代数，基本统计运算和随机模拟等等。本文主要从Numpy的数据类型，数据处理，数据运算三方面进行介绍。

<!--more-->

## 数据类型

NumPy包的核心是 ndarray 对象。它封装了Python原生的同数据类型的 n 维数组，在NumPy维度中称为 轴 。相较于原生的Python Array（数组），Numpy数组具有固定大小，其中元素须为相同类型，能够对对大量数据进行高级数学和其他类型的操作。  

### 创建数组
创建Numpy数组有多种方式，如`np.array`,`np.arange`等，
1. `np.array`：创建一个数组   

   ```python
   # array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
   # object: array_like, 公开数组接口的任何对象，其__array__方法返回数组的对象，或任何（嵌套的）序列。如list
   # dtype：数据类型
   # copy：bool, 如果是 True (default), 则复制object.

   obj1=[1,2,4] #list
   obj2=range(3) #range

   np.array(obj1)
   # array([1, 2, 4])
   np.array(obj2)
   # array([0, 1, 2])

   obj3 = np.arange(4) #ndarray
   # obj3 = array([0, 1, 2, 3])
   nd3 = np.array(obj3,copy=False)
   # nd3 = array([0, 1, 2, 3])
   # 由于nd3上面copy为False，相当于对nd3是对obj3的浅复制（同nd3=obj3），操作其中一个时另一个变量也会随之变化。
   # 不过对于list类型，copy=False 或 copy=True 效果都是深复制，对一个变量的操作不会影响另一个变量。
   nd3[0] = 11
   # obj3 = array([11,  1,  2,  3])
   # nd3 = array([11,  1,  2,  3])

   # 指定dtype为复数
   np.array([1, 2, 3], dtype=complex)
   # array([ 1.+0.j,  2.+0.j,  3.+0.j])
   # 包含多个元素的数据类型
   np.array([[(1,2)],[(3,4)],[(3,4)]],dtype=[('a','<i4'),('b','<i4')])
   # array([[(1, 2)],
   #        [(3, 4)],
   #        [(3, 4)]], dtype=[('a', '<i4'), ('b', '<i4')])
   ```

   另有`np.ndarray()`一种低阶方法，它会创建一个具有随机值`ndarray`对象，通常不推荐使用这组方式。  
   
2. 生成一定范围的数组  
   `np.arange([start,] stop[, step,], dtype=None)`: 返回给定范围的等间距数值 
   
   ```python
   np.arange(4) # 0-4 间隔为1的数组
   # array([0, 1, 2, 3])
   np.arange(3,9,2) # 3-9 间隔为2的数组
   # array([3, 5, 7])
   ```
   `np.linspace(start,stop,num=50,endpoint=True,retstep=False,dtype=None,axis=0,)`: 返回指定范围内的等距数字。`endpoint`是否包含`stop`,bool值；`retshtep`: bool值，如果True返回(`samples`, `step`), `step`是采样间隔；`axis`: 采样结果各存储方向，只有当`start`,`stop`为array_like类型是才有效，默认0。

   ```python
   np.linspace(2.0, 3.0, num=5)
   # array([2.  , 2.25, 2.5 , 2.75, 3.  ])
   np.linspace(2.0, 3.0, num=5, endpoint=False) # 不包含stop=3
   # array([2. , 2.2, 2.4, 2.6, 2.8])
   np.linspace(2.0, 3.0, num=5, retstep=True) # 返回采样间隔
   # (array([2.  , 2.25, 2.5 , 2.75, 3.  ]), 0.25)
   ```
   `np.logspace(start,stop,num=50,endpoint=True,base=10.0,dtype=None,axis=0,)`: 返回在对数尺度上均匀分布的数字。`base`对数空间的底，默认10；

   ```python
   np.logspace(2.0, 3.0, num=4, base=2.0)
   array([4.        ,  5.0396842 ,  6.34960421,  8.        ])
   ```
   `np.geomspace(start, stop, num=50, endpoint=True, dtype=None, axis=0)`: 返回在对数刻度上均匀分布的数字（几何级数）。
   
   ```python
   np.geomspace(1, 256, num=9)
   # array([   1.,    2.,    4.,    8.,   16.,   32.,   64.,  128.,  256.])
   ```
   
3. 生成指定大小的数组 
   `np.ones(shape, dtype=None, order='C')`: 返回给定形状和类型，由1填充的新数组; 
   `zeros(shape, dtype=float, order='C')`: 返回给定形状和类型，由0填充的新数组; 
   `empty(shape, dtype=float, order='C')`: 返回给定形状和类型的新数组，而不初始化；
   `np.full(shape, fill_value, dtype=None, order='C')`: 返回由给定值填充的给定形状和类型的新数组。

4. 生成与给定数组相同形状的数组   
   `np.ones_like(a, dtype=None, order='K', subok=True, shape=None)`: 返回与给定数组具有相同形状和类型的由1填充的数组。
   `np.zeros_like(a, dtype=None, order='K', subok=True, shape=None)`: 返回与给定数组具有相同形状和类型的由0填充的数组。
   `empty_like(prototype, dtype=None, order='K', subok=True, shape=None)`: 返回与给定数组具有相同形状和类型的新数组。
   `np.full_like(a, fill_value, dtype=None, order='K', subok=True, shape=None)`: 返回与给定数组具有相同形状和类型的由给定数值填充的数组。
   
5. 其他创建数组方式    
   `np.frombuffer(buffer, dtype=float, count=-1, offset=0)`: 将缓冲区解释为一维数组。
   `np.fromfile(file, dtype=float, count=-1, sep='', offset=0)`: 从文本或二进制文件中的数据构造数组。
   `np.fromiter(iterable, dtype, count=-1)`: 从iterable对象创建新的一维数组。
   `np.fromregex(file, regexp, dtype, encoding=None)`: 使用正则表达式解析从文本文件构造数组。
   `np.fromstring(string, dtype=float, count=-1, sep='')`: 从字符串中的文本数据初始化的新一维数组。

6. 坐标网格
   `np.meshgrid(*xi, **kwargs)`
   `np.ogrid`: Arrays of evenly spaced numbers in N-dimensions.
   `np.mgrid`: Grid-shaped arrays of evenly spaced numbers in N-dimensions.
   `np.fromfunction(function, shape, **kwargs)`: 通过在每个坐标上执行函数来构造数组。

### dtype
Numpy内置许多基本数据类型，对python的基本数据类型进行扩充已满足科学计算的需要，这里标量类型可以可以作为参数传递给`np.dtype()`构造函数产生一个dtype对象，如`np.dtype(np.int32)`。在NumPy中所有需要dtype作为参数的函数都可以使用scalar types代替，会自动转化为对应的dtype类型。下表列出了24中内置数据类型，更多详细介绍[Built-in scalar types](https://docs.scipy.org/doc/numpy/reference/arrays.scalars.html#arrays-scalars-built-in)

| 类型      | 注释                      |
| :-------- | :------------------------ |
| `bool_`   | 兼容Python内置的bool类型  |
| `bool8`   | 8位布尔                   |
| `int_`    | 兼容Python内置的int类型   |
| `int8`    | 8位整数                   |
| `int16`   | 16位整数                  |
| `int32`   | 32位整数                  |
| `int64`   | 64位整数                  |
| `uint8`   | 无符号8位整数             |
| `uint16`  | 无符号16位整数            |
| `uint32`  | 无符号32位整数            |
| `uint64`  | 无符号64位整数            |
| `float_`  | 兼容Python内置的float类型 |
| `float16` | 16位浮点数                |
| `float32` | 32位浮点数                |
| `float64` | 64位浮点数                |
| `str_`    | 兼容Python内置的str类型   |

### Structured Array

### ndarray属性

| 名称       | 返回                    | 说明                                                         |
| :--------- | :---------------------- | ------------------------------------------------------------ |
| `T`        | `ndarray`               | 转置数组                                                     |
| `data`     | `buffer`                | 返回数组的内存查看对象(Momory view)。|
| `dtype`    | `dtype object`          | 描述数组元素数据类型           |
| `flags`    | `dict`                  | 包含与内存使用相关信息的字典,如，'C_CONTIGUOUS', 'OWNDATA', 'WRITEABLE'等|
| `flat`     | `numpy.flatiter object` | 以迭代器的形式展开数组，可以对其复值。(See `ndarray.flat`). |
| `imag`     | `ndarray`               | 数组的复数部分                                 |
| `real`     | `ndarray`               | 数组的实部                                      |
| `size`     | `int`                   | 数组元素数量                             |
| `itemsize` | `int`                   | 每个数组元素的内存使用（字节）。               |
| `nbytes`   | `int`                   | 存储数组数据所需的字节总数=``itemsize * size``. |
| `ndim`     | `int`                   | 数组的维数                            |
| `shape`    | `tuple` of ints         | 数组形状.                                          |
| `strides`  | `tuple` of ints         | 在内存中从一个元素移动到下一个元素所需的步长。  |
| `ctypes`   | `ctypes object`         | Class containing properties of the array needed for interaction with ctypes. |
| `base`     | `ndarray`               | If the array is a view into another array, that array is its `base` (unless that array is also a view).  The `base` array is where the array data is actually stored. |



**参考:**  

1. [快速入门教程](https://www.numpy.org.cn/user/quickstart.html#%E5%85%88%E5%86%B3%E6%9D%A1%E4%BB%B6)
2. [numpy ndarray详解](https://danzhuibing.github.io/py_numpy_ndarray.html)
3. [Data type objects (dtype) — NumPy v1.17 Manual](https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html)

