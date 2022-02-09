---
title: 标准差
date: 2022-02-09 15:51
tag: ['概率统计','标准差','均方根误差']
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

关于标准差、方差、均方根和均方根误差的计算方法。

<!--more-->
**标准差**(Standard Deviation, SD)，又称标准偏差、均方差，在概率统计中最常用于衡量一组样本的离散程度，通常用$\sigma$表示。

对于一个总体的标准差采用下面方法计算：

$$
\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2}
$$

其中，$N$为总体数，$x_i$为第$i$个元素的值，$\mu$为各个元素的平均值。

而样本的标准差，则是采用总体的部分样本对总体标准差的无偏估计：

$$
\sigma = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\mu)^2}
$$

其中，$n(n<N)$为样本数，$x_i$为第$i$个样本的值，$\mu$为样本的平均值。

在`numpy.std()`函数中提供`ddof`参数可用于指示计算总体标准差（`ddof=0`）或样本标准差（`ddof=1`），默认计算总体标准差；而在`pandas.DataFrame.std()`中`ddof`默认为`1`，即计算样本标准差。

**方差**（Variance）在概率论和统计学中，一个随机变量的方差描述的是它的离散程度，也就是该变量离其期望值的距离。一个实随机变量的方差也称为它的二阶矩或二阶中心矩。

$$
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2
$$

**均方根**（root mean square, RMS）也称平方平均数（quadratic mean），在物理上也称作为有效值

$$
RMS = \sqrt{\frac{\sum_{i=1}^{N}(x_i)^2}{N}}
$$

**均方根误差**（root-mean-square error, RMSE）或均方根偏移（root-mean-square deviation, RMSD）表示预测的值和测量值之差（残差或预测误差）的样本标准差（sample standard deviation）,它能够很好地反映出测量的准确程度。

$$
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i-\hat{x}_i)^2}
$$

---

**参考**
1. [方差 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/%E6%96%B9%E5%B7%AE)
2. [标准差 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/%E6%A8%99%E6%BA%96%E5%B7%AE)
