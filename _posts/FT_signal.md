---
title: 信号的傅里叶变换
tag: ['tag1','tag2']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

abstract

<!--more-->
## 能量信号与功率信号

对于信号$S(t)$，其能量$E$的定义为信号的平方在$(-\infty,+\infty)$上的积分：
$$
E=\lim_{T\rightarrow \infty}\int_{-T}^{T}|S(t)|^2\mathrm{d}t
$$
而功率$P$是单位时间内的能量大小：
$$
P=\lim_{T\rightarrow \infty}\frac{1}{2T}\int_{-T}^{T}|S(t)|^2\mathrm{d}t
$$
由上可知，若信号$S(t)$的能量$E$极限存在（$E\rightarrow C$），功率$P$为零，则该信号为**能量信号**如；若能量$E$极限不存在（$E\rightarrow\infty$），此时功率$P$可能存在极限，也可能不存在极限，当功率$P$的极限存在时（$P\rightarrow C$）时该信号为**功率信号**，而当功率$P$的极限不存（$E\rightarrow\infty$）在时该信号为**非功非能信号**。*所有有界周期信号都是功率信号，所有有限数量的脉冲信号都是能量信号。*

连续、离散信号

傅里叶变换类型FT、FS、DTFT、DFT、。。。

FT（Fourier Transformation）：傅里叶变换。就是我们理论上学的概念，但是对于连续的信号无法在计算机上使用。**其时域信号和频域信号都是连续的。**

DTFT（Discrete-time Fourier Transform）：离散时间傅里叶变换。这里的“离散时间”指的是时域上式离散的，也就是计算机进行了采样。不过傅里叶变换后的结果依然是连续的。

DFT（Discrete Fourier Transform）：离散傅里叶变换。在DTFT之后，将傅里叶变换的结果也进行离散化，就是DFT。

也就是说：**FT时域连续、频域连续；DTFT时域离散、频域连续；DFT时域离散、频域离散。**

FFT（Fast Fourier Transformation）：快速傅里叶变换。就是DFT的快速算法，一般工程应用时用的都是这种算法。

FS（Fourier Series）：傅里叶级数。是针对时域**连续周期**信号提出的，结果是离散的频域结果。

DFS（Discrete Fourier Series）：离散傅里叶级数。是针对时域**离散周期**信号提出的，DFS与DFT的本质是一样的。

另外补充几点相关知识：

- 在实际计算中通常使用**快速傅里叶变换（FFT）。**它是一种用来计算DFT（离散傅里叶变换）和IDFT（离散傅里叶反变换）的一种快速算法。
- 随机信号是无法做傅里叶变换的（*这里要再补充）

---

**参考**

1. [一幅图弄清DFT与DTFT,DFS的关系 - BitArt - 博客园](https://www.cnblogs.com/BitArt/archive/2012/11/24/2786390.html)
2. [能量信号和功率信号的分别 - 知乎](https://zhuanlan.zhihu.com/p/35363670)
3. [信号频域分析方法的理解（频谱、能量谱、功率谱、倒频谱、小波分析） - 知乎](https://zhuanlan.zhihu.com/p/34989414)
4. [傅里叶变换、自相关函数、频响函数与功率谱密度 - 逾之](https://blog.zhongyue.site/post/ft_frf_psd_af/)
5. [信号分析与处理技术基础](/assets/doc/信号分析与处理技术基础(FT).pdf)
